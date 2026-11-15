"""
Everything that talks to Claude (the Anthropic API).

    rewrite(path, answers)               -> {"sentence", "poem"}       cheap model (Haiku)
    judge(path, answers, sentence, passages) -> which passages really match   stronger model (Opus)

The key goes in the .env file in the project folder:  ANTHROPIC_API_KEY=sk-ant-...
Optional .env settings: JUDGE_MODEL, JUDGE_EFFORT (low/medium/high), JUDGE_POOL (passages the judge reads).
"""
import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_env():
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8-sig"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


_load_env()

REWRITE_MODEL = os.environ.get("REWRITE_MODEL", "claude-haiku-5-5")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-opus-5-5")
JUDGE_EFFORT = os.environ.get("JUDGE_EFFORT")             # lower effort = less thinking = cheaper
JUDGE_POOL = int(os.environ.get("JUDGE_POOL", "20"))

# dollars per million tokens (input, output)
PRICES = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.0, 10.0),
          "claude-opus-5-5": (4.0, 20.0), "claude-fable-5-2": (8.0, 40.0)}
spent = {"usd": 0.0, "calls": 0}
_client = None


def available():
    return bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())


def call(prompt, model, max_tokens=16000, effort=None):
    """Send one message to Claude and return the text of the reply."""
    global _client
    if not available():
        raise RuntimeError("no API key (put ANTHROPIC_API_KEY=... in the .env file)")
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic()
    extra = {"output_config": {"effort": effort}} if effort else {}
    reply = _client.messages.create(model=model, max_tokens=max_tokens,
                                    messages=[{"role": "user", "content": prompt}], **extra)
    _count_cost(model, reply.usage)
    if reply.stop_reason == "refusal":
        raise RuntimeError("the model declined to answer")
    text = "".join(block.text for block in reply.content if block.type == "text").strip()
    if not text:
        raise RuntimeError(f"empty reply ({reply.stop_reason})")
    return text


def _count_cost(model, usage):
    price_in, price_out = PRICES.get(model, (0, 0))
    usd = (usage.input_tokens * price_in + usage.output_tokens * price_out) / 1e6
    spent["usd"] += usd
    spent["calls"] += 1
    try:
        with open(os.path.join(ROOT, "data", "usage.log"), "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{model}\tin {usage.input_tokens}\t"
                    f"out {usage.output_tokens}\t${usd:.4f}\n")
    except OSError:
        pass


# --- 1. rewrite: the person's answers -> a short sentence (for the search) and a 3-line poem ---
REWRITE_PROMPT = """Below is what a person wrote about how they feel. Write two things.

1. SENTENCE: one short first-person sentence (at most 15 words), the way someone in any century might put it
   in a private letter or diary: what is happening to them and why. Plain words. It is used for a search.
2. POEM: their answers joined into a short, gentle poem of exactly three lines (one line for what
   happened, one for why they feel it, one for anything else, or for the feeling if nothing else was said).
   At most 6 words a line, first person, plain words that sound good read aloud. No rhyme needed.

Rules for both:
- Keep the situation and the reason exactly, but make modern details general (no phones, apps, social media,
  course or brand names, or people's names: "my best friend stopped replying to my messages" becomes
  "the friend I was closest to has gone silent").
- Use only what they said. Do NOT add feelings, causes, fears, secrets or images they did not mention.
  No advice or comfort.

Reply in exactly this format and nothing else:
SENTENCE: ...
POEM:
...
...
...

THE PERSON
  feeling (picked on a feelings tree): {feeling}
  what's happened: {event}
  why they think they feel {deepest}: {cause}
  anything else: {extra}"""


def rewrite(path, answers):
    """{"sentence": short general sentence (what we search for), "poem": 3 lines (shown to the person)}."""
    words = [p for p in path if p]
    prompt = REWRITE_PROMPT.format(feeling=" > ".join(words) or "not given",
                                   deepest=words[-1].lower() if words else "this way",
                                   event=answers.get("event") or "-", cause=answers.get("cause") or "-",
                                   extra=answers.get("extra") or "-")
    reply = call(prompt, REWRITE_MODEL, max_tokens=4000)
    sentence, _, poem = reply.partition("POEM:")
    sentence = " ".join(sentence.replace("SENTENCE:", "").split()).strip('"')
    poem = "\n".join(line.strip() for line in poem.strip().splitlines() if line.strip())
    if not sentence or len(sentence.split()) > 60:
        raise RuntimeError("the rewrite came back empty or too long")
    return {"sentence": sentence, "poem": poem}


# --- 2. judge: read the shortlist and keep only real matches -----------------------------------
JUDGE_PROMPT = """You are matching a person's problem to passages from real old letters, diaries and memoirs.

Find the passages where the WRITER is going through the same thing as the person: the same feeling, the same
kind of situation, for the same kind of reason. Sharing a topic or some words is not enough (a passage about
letters is not a match for "nobody replies to me" unless the writer is the one waiting and hurt). A writer
describing someone else's trouble, giving advice, or saying they are fine is not a match. If two passages are
equally close, prefer the writer who is struggling but coping over pure despair.

Each passage comes with the sentences around it. Use them to understand who is writing and what is really
going on (a line that sounds like grief may be about a pet, a novel or someone else's loss), but the passage
itself must show the feeling. Judge only from the text. Saying no passage matches is a fine answer.

THE PERSON
{person}

PASSAGES
{passages}
Reply with JSON only, in this format:
{{"matches": [{{"n": 3, "match": "yes", "quote": "...", "why": "..."}}], "best": 3}}
- matches: only the passages that match, with "match" set to "yes" or "partly".
- quote: the one or two sentences of the PASSAGE that show the feeling best, at most 30 words, copied
  exactly word for word from the PASSAGE (no changes, no "...", nothing from the surrounding sentences).
- why: one short sentence.
- best: the number of the single best match, or "none"."""


def judge(path, answers, sentence, passages):
    """Ask the judge which passages match. Returns ({n: {"match", "quote", "why"}}, best n or None),
    numbering the passages from 1."""
    person = [f"  feeling: {' > '.join(p for p in path if p)}",
              f"  what's happened: {answers.get('event') or '-'}",
              f"  why they think they feel it: {answers.get('cause') or '-'}"]
    if answers.get("extra"):
        person.append(f"  anything else: {answers['extra']}")
    person.append(f"  in general terms: {sentence}")
    listing = ""
    for n, p in enumerate(passages, 1):
        listing += (f"[{n}] {p['author']}, {p['title']} ({p['when']})\n"
                    f"  before: {p['context_before'] or '-'}\n"
                    f"  PASSAGE: {p['text']}\n"
                    f"  after: {p['context_after'] or '-'}\n\n")
    reply = call(JUDGE_PROMPT.format(person="\n".join(person), passages=listing), JUDGE_MODEL,
                 effort=JUDGE_EFFORT)
    data = json.loads(reply[reply.find("{"): reply.rfind("}") + 1])
    matches = {}
    for m in data.get("matches", []):
        n = int(m.get("n", 0))
        if 1 <= n <= len(passages) and m.get("match") in ("yes", "partly"):
            matches[n] = {"match": m["match"], "quote": exact_quote(m.get("quote"), passages[n - 1]["text"]),
                          "why": m.get("why", "")}
    best = data.get("best")
    best = int(best) if str(best).isdigit() and int(best) in matches else None
    return matches, best


# --- 3. guidance: pick the advice from the philosophy books ---------------------------------------
GUIDANCE_PROMPT = """A person is struggling. Below are short passages from philosophy and wisdom books.
Pick the {n} that would give this person the most helpful, kind and wise guidance for what they are going
through right now: advice they could actually use, not just a passage that shares a word with their problem.
Leave out anything harsh, preachy, cold or off-topic. Each pick must be from a different writer.

THE PERSON
{person}

PASSAGES
{passages}
Then write 3 journalling questions to help them reflect on their own situation in writing:
open questions (not yes/no), gentle, in plain words, at most 20 words each, about what they actually said.
At least one should build on the idea in one of your picks. No advice, no diagnosis, and do not add
feelings or facts they did not mention.

Reply with JSON only, in this format:
{{"picks": [{{"n": 3, "quote": "..."}}], "prompts": ["...", "...", "..."]}}
- picks: the best first, at most {n}.
- quote: the part of the PASSAGE that gives the guidance, at most 35 words, copied exactly word for word
  (no changes, no "..."). Use the whole passage if it is all needed.
- prompts: the 3 journalling questions."""


def choose_guidance(path, answers, sentence, passages, n=2):
    """Ask the AI which passages give the best guidance, and for 3 journalling questions.
    Returns {"picks": [(passage number from 1, exact quote or None)], "prompts": [question, ...]}."""
    person = [f"  feeling: {' > '.join(p for p in path if p)}",
              f"  what's happened: {answers.get('event') or '-'}",
              f"  why they think they feel it: {answers.get('cause') or '-'}",
              f"  in general terms: {sentence}"]
    listing = "".join(f"[{i}] {p['author']}: {p['text']}\n" for i, p in enumerate(passages, 1))
    reply = call(GUIDANCE_PROMPT.format(n=n, person="\n".join(person), passages=listing), JUDGE_MODEL,
                 max_tokens=4000, effort=JUDGE_EFFORT)
    data = json.loads(reply[reply.find("{"): reply.rfind("}") + 1])
    picks, writers = [], set()
    for m in data.get("picks", []):
        i = int(m.get("n", 0))
        if 1 <= i <= len(passages) and passages[i - 1]["author"] not in writers:
            picks.append((i, exact_quote(m.get("quote"), passages[i - 1]["text"])))
            writers.add(passages[i - 1]["author"])
    prompts = [" ".join(str(p).split()) for p in data.get("prompts", []) if isinstance(p, str)]
    return {"picks": picks[:n], "prompts": [p for p in prompts if 0 < len(p.split()) <= 30][:3]}


def exact_quote(quote, passage):
    """The judge's short quote, but only if it really is word for word in the passage."""
    quote = " ".join(str(quote or "").split()).strip("\"“”'")
    if not quote or "..." in quote or "…" in quote or len(quote.split()) > 40:
        return None
    return quote if quote in " ".join(passage.split()) else None
