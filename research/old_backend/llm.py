"""
The only file that talks to an LLM (Claude, Anthropic Python SDK).

    rewrite(path, answers)  -> {statement: short general sentence (searched), poem: 3 lines (shown)}
    rephrase(path, answers) -> just the statement
    call(prompt, model)     -> the text reply (used by judge.call_llm)

Key: set the environment variable ANTHROPIC_API_KEY (never put it in code).
Without a key every function here raises NoLLM and the backend falls back to
plain search, so nothing breaks.

Models (override with the env vars REPHRASE_MODEL / JUDGE_MODEL):
    rephrase: claude-haiku-5-5  (short rewrite, cheap: $0.10 / $0.50 per million tokens in / out)
    judge:    claude-opus-5-5   (reads 20 passages and decides: $4 / $20 per million tokens)
"""
import os
import re


def _load_dotenv():
    """Read KEY=value lines from the project's .env file (git-ignored) into the environment.
    A key already set in the environment wins. Values are never printed."""
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8-sig"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv()

REPHRASE_MODEL = os.environ.get("REPHRASE_MODEL", "claude-haiku-5-5")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-opus-5-5")

_CLIENT = None


class NoLLM(NotImplementedError):
    """No API key (or the SDK is missing): callers fall back to plain search."""


def available():
    return bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())


def _client():
    global _CLIENT
    if not available():
        raise NoLLM("ANTHROPIC_API_KEY is not set")
    if _CLIENT is None:
        try:
            import anthropic
        except ImportError as e:
            raise NoLLM("pip install anthropic") from e
        _CLIENT = anthropic.Anthropic()      # reads ANTHROPIC_API_KEY from the environment
    return _CLIENT


# $ per million tokens (input, output), from Anthropic's model docs, Nov 2026. Thinking counts as output.
PRICES = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.0, 10.0),
          "claude-opus-5-5": (4.0, 20.0), "claude-fable-5-2": (8.0, 40.0)}
SPENT = {"usd": 0.0, "calls": 0}
EFFORT = os.environ.get("JUDGE_EFFORT")      # optional: low | medium | high (lower = fewer thinking tokens)
JUDGE_POOL = int(os.environ.get("JUDGE_POOL", "20"))   # passages the judge reads per search (fewer = cheaper)


def _record(model, usage):
    pin, pout = PRICES.get(model, (0.0, 0.0))
    usd = (usage.input_tokens * pin + usage.output_tokens * pout) / 1e6
    SPENT["usd"] += usd
    SPENT["calls"] += 1
    try:
        import time
        log = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "usage.log")
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{model}\tin {usage.input_tokens}\t"
                    f"out {usage.output_tokens}\t${usd:.4f}\n")
    except OSError:
        pass
    return usd


def call(prompt, model, max_tokens=16000, effort=None):
    """Send one user message, return the reply text. Raises on refusal or empty reply.
    Every call's tokens and cost are added to SPENT and results/usage.log."""
    kwargs = {"output_config": {"effort": effort}} if effort else {}
    response = _client().messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        **kwargs,
    )
    _record(model, response.usage)
    if response.stop_reason == "refusal":
        raise RuntimeError("the model declined to answer")
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    if not text:
        raise RuntimeError(f"empty reply (stop_reason={response.stop_reason})")
    return text


REPHRASE_PROMPT = """Below is what a person wrote about how they feel. Write two things.

1. SENTENCE: one short first-person sentence (at most 15 words), the way someone in any century might put it
   in a private letter or diary: what is happening to them and why. Plain words. It is used for a search.
2. POEM: their three answers joined into a short, gentle poem of exactly three lines (one line for what
   happened, one for why they feel it, one for anything else, or for the feeling if nothing else was said).
   At most 6 words a line, first person, plain words that sound good read aloud. No rhyme needed.

Rules for both:
- Keep the underlying situation and the reason exactly; generalise the surface details
  (no phones, apps, social media, course names, brand names or people's names: "my best friend stopped
  replying to my messages" becomes "the friend I was closest to has gone silent").
- Every part must come from their words. Do NOT add feelings, causes, fears, secrets, images or details
  they did not say (no "I am afraid...", "a weight I cannot put down" unless they said so).
  Do not give advice or comfort.

Reply in exactly this format and nothing else:
SENTENCE: ...
POEM:
...
...
...

THE PERSON
  feeling (picked on a feelings wheel): {feeling}
  what's happened: {event}
  why they think they feel {deepest}: {cause}
  anything else: {extra}"""


def _parse_rewrite(text):
    """'SENTENCE: ... / POEM: three lines' -> (sentence, poem). A reply without the labels is the sentence."""
    t = text.strip()
    sentence, poem = t, ""
    m = re.search(r"SENTENCE:\s*(.+?)\s*(?:POEM:|$)", t, re.S)
    if m:
        sentence = m.group(1)
        if "POEM:" in t:
            lines = [l.strip() for l in t.split("POEM:", 1)[1].strip().splitlines() if l.strip()]
            poem = "\n".join(lines[:4])
    return " ".join(sentence.split()).strip('"'), poem


def rewrite(path, answers):
    """One cheap call -> {"statement": short general sentence (searched), "poem": 3 lines (shown)}.
    Raises NoLLM without a key."""
    a = {k: (v or "").strip() for k, v in (answers or {}).items()}
    words = [p for p in path if p]
    deepest = words[-1].lower() if words else "this way"
    feeling = " > ".join(words) if words else "not given"
    extra = " ".join(x for x in (a.get("extra"), a.get("meaning"), a.get("coping")) if x) or "-"
    prompt = REPHRASE_PROMPT.format(feeling=feeling, deepest=deepest, event=a.get("event") or "-",
                                    cause=a.get("cause") or "-", extra=extra)
    sentence, poem = _parse_rewrite(call(prompt, REPHRASE_MODEL, max_tokens=4000))
    if not sentence or len(sentence.split()) > 60:
        raise RuntimeError("rewrite missing or too long")
    return {"statement": sentence, "poem": poem}


def rephrase(path, answers):
    """Just the short general sentence (what the search compares)."""
    return rewrite(path, answers)["statement"]
