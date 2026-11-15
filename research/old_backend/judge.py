"""
The judge: reads the user's problem and a short list of candidate passages and
decides which one (if any) shows someone facing the SAME problem.

Search (numbers) is good at finding the right area; it is bad at picking the
right passage. EmpathicStories (Shen et al. 2023) found prompted LLMs strongest
at picking the top match, but too costly to run on a whole library. So: search
gives ~20 candidates, the judge picks one or says "none".

    python -m Backend.judge export [--label NAME] [--n 20] [--rephrase]  (--rephrase: LLM rewrite first, paid but cheap)
        writes results/judge_input_NAME.json (+ a readable .md) for the review cases
    python -m Backend.judge run [--label NAME]
        PAID: sends each exported case to call_llm, writes judge_output_NAME.json, then scores it
    python -m Backend.judge score results/judge_output_NAME.json [--label NAME]
        reads verdicts, prints the numbers, writes a blind review sheet

call_llm(prompt) sends the prompt to Claude via Backend/llm.py (needs ANTHROPIC_API_KEY). Without a key the judge is not used
by find() (it falls back to plain search), and verdicts can be produced by hand
or by anyone/anything reading judge_input_*.json and writing judge_output_*.json
in the format of OUTPUT_FORMAT.
"""
import json
import os
import random
import sys

from Backend import cards

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")

INSTRUCTIONS = """You are matching a person's problem to passages from real historical letters and diaries.

Goal: find a passage where the WRITER is facing the same underlying problem as the person:
the same emotion, the same kind of situation, felt for the same kind of reason, with the same fear.
A passage is more useful when it also shows how the writer deals with it: still struggling but
coping (writing to someone, keeping going, finding a way to see it) helps a reader more than pure
despair or an effortless triumph.
Sharing a topic or words is NOT enough (a passage about letters is not a match for "nobody replies to me"
unless the writer is the one waiting and hurt). A writer describing someone else's problem, giving advice,
or saying they are NOT troubled is not a match.

Each PASSAGE comes with the sentences just before and after it in the same letter or diary. Read them:
they show who is writing, to whom, about whom, and what is really going on (a line that sounds like grief
may be about a pet, a novel, or someone else's loss). Judge the writer's situation from the passage AND
its context together, but the passage itself must carry the feeling; a match found only in the context
is "partly" at most.
Judge only from the text given. Do not guess what the writer felt if the text does not show it.
"none" is a correct answer when no passage is a real match.

For each candidate give:
  emotion:   yes | partly | no      (the writer feels the same emotion)
  situation: yes | partly | no      (same kind of thing happening to the writer)
  cause:     yes | partly | no | not stated   (same kind of reason for the feeling)
  fear:      yes | partly | no | not stated   (same fear about what it means)
  coping:    none | despair | struggling | coping | resolved   (how the writer is dealing with it)
  overall:   yes | partly | no      (yes needs emotion and situation yes, and cause or fear yes/partly)
  why:       one short sentence, including how the writer deals with it if shown
  quote:     only when overall is yes or partly: the one or two sentences of the PASSAGE that show the
             writer's feeling most clearly, at most 30 words, copied EXACTLY word for word from the PASSAGE
             (no changes, no "...", nothing from the context). This is what the person will read.
Then give "best": the number of the single best candidate whose overall is yes or partly (when two
are equally close, prefer the one whose writer is struggling but coping), or "none".
Reply with JSON only, in exactly this format:"""

OUTPUT_FORMAT = {
    "verdicts": [{"n": 1, "emotion": "yes", "situation": "yes", "cause": "partly", "fear": "not stated",
                  "coping": "struggling", "overall": "partly", "why": "...", "quote": "..."}],
    "best": 1,
}


def build_prompt(card, candidates):
    """card: Card or dict; candidates: list of result dicts from Backend.shortlist()."""
    c = card if isinstance(card, cards.Card) else cards.Card(**card)
    lines = [INSTRUCTIONS, json.dumps(OUTPUT_FORMAT), "", "THE PERSON'S PROBLEM (their own words)",
             f"  feeling (picked on a feelings wheel): {c.feeling}", f"  what's happened: {c.event}",
             f"  why they think they feel it: {c.cause}"]
    for label, field in (("anything else", "extra"), ("afraid", "meaning"), ("coping so far", "coping")):
        if c.stated(field):
            lines.append(f"  {label}: {getattr(c, field)}")
    if c.stated("statement"):
        lines.append(f"  in general terms (a rewrite, used for the search): {c.statement}")
    lines += ["", "CANDIDATE PASSAGES"]
    for n, r in enumerate(candidates, 1):
        tr = f", translated by {r['translator']}" if r.get("translator") else ""
        lines += [f"[{n}] {r['author']}, {r['title']} ({r['when']}){tr}",
                  f"  context before: {r['context_before'] or '-'}",
                  f"  PASSAGE: {r['text']}",
                  f"  context after: {r['context_after'] or '-'}", ""]
    return "\n".join(lines)


def call_llm(prompt):
    """Send `prompt` to the judge model (Backend/llm.py, JUDGE_MODEL) and return its text reply.
    Raises llm.NoLLM (a NotImplementedError) when ANTHROPIC_API_KEY is not set."""
    from Backend import llm
    return llm.call(prompt, llm.JUDGE_MODEL, effort=llm.EFFORT)


LEVELS = {"yes", "partly", "no", "not stated"}
COPING = {"none", "despair", "struggling", "coping", "resolved", "not stated"}


def parse(text, n_candidates):
    """Validate a judge reply. Returns {"verdicts": [...], "best": int|None} or raises ValueError."""
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`").split("\n", 1)[1] if "\n" in t else t
    data = json.loads(t[t.find("{"): t.rfind("}") + 1])
    verdicts = data.get("verdicts", [])
    for v in verdicts:
        if not (1 <= int(v["n"]) <= n_candidates):
            raise ValueError(f"verdict for unknown candidate {v['n']}")
        for k in ("situation", "cause", "fear", "overall"):
            if str(v.get(k, "")).lower() not in LEVELS:
                raise ValueError(f"bad value {k}={v.get(k)!r}")
        if "emotion" in v and str(v["emotion"]).lower() not in LEVELS:
            raise ValueError(f"bad value emotion={v['emotion']!r}")
        if "coping" in v and str(v["coping"]).lower() not in COPING:
            raise ValueError(f"bad value coping={v['coping']!r}")
    best = data.get("best")
    if best in (None, "none", "None", ""):
        best = None
    else:
        best = int(best)
        if not 1 <= best <= n_candidates:
            raise ValueError(f"best={best} out of range")
        if next((v["overall"] for v in verdicts if int(v["n"]) == best), "no") == "no":
            raise ValueError("best candidate was judged 'no'")
    return {"verdicts": verdicts, "best": best}


def checked_quote(quote, passage, max_words=40):
    """The judge's short quote, only if it is word for word inside the passage (so still verbatim
    from the source); otherwise None and the whole passage is shown."""
    q = " ".join(str(quote or "").split()).strip('"“”\'')
    if not q or "..." in q or "…" in q or len(q.split()) > max_words:
        return None
    return q if q in " ".join(passage.split()) else None


def judge(card, candidates, call=None):
    """Ask the judge. Returns parsed verdicts, or None if no judge is available."""
    call = call or call_llm
    try:
        return parse(call(build_prompt(card, candidates)), len(candidates))
    except NotImplementedError:
        return None


# --------------------------------------------------------------------------
# Offline: export the review cases, score verdicts written by any judge
# --------------------------------------------------------------------------
def review_cases():
    from Backend.Backend import DEMO
    from Backend.eval import REVIEW_EXTRA
    return DEMO + REVIEW_EXTRA


def export(label, n=20, rephrase=False):
    """rephrase=True: each case first gets the LLM rewrite (cheap model, one call per case), as in chat."""
    from Backend.Backend import shortlist
    cases = []
    md = [f"# Judge input ({label})", "", INSTRUCTIONS, "", "```json", json.dumps(OUTPUT_FORMAT, indent=1),
          "```", ""]
    for i, (path, answers) in enumerate(review_cases(), 1):
        card = cards.from_answers(path, answers)
        if rephrase:
            from Backend import llm
            card.statement = llm.rephrase(path, answers)
        cands = shortlist(path, card=card.to_dict(), n=n)
        cases.append({"case": i, "path": list(path), "card": card.to_dict(),
                      "candidates": cands, "prompt": build_prompt(card, cands)})
        md += [f"## Case {i}: {' > '.join(path)}", "", "```", build_prompt(card, cands).split(
            "THE PERSON'S PROBLEM", 1)[1].strip(), "```", ""]
    os.makedirs(RESULTS, exist_ok=True)
    out = os.path.join(RESULTS, f"judge_input_{label}.json")
    json.dump({"label": label, "n": n, "cases": cases}, open(out, "w", encoding="utf-8"), indent=1)
    open(out[:-5] + ".md", "w", encoding="utf-8").write("\n".join(md))
    print(f"wrote {out} and {out[:-5]}.md ({len(cases)} cases x {n} candidates)")


def run(label):
    """Send every exported case to call_llm (PAID: one call per case) and write
    results/judge_output_LABEL.json (+ the raw replies) for score()."""
    inp = json.load(open(os.path.join(RESULTS, f"judge_input_{label}.json"), encoding="utf-8"))
    out, raw = [], []
    for case in inp["cases"]:
        reply = call_llm(case["prompt"])
        raw.append({"case": case["case"], "reply": reply})
        try:
            p = parse(reply, len(case["candidates"]))
            out.append({"case": case["case"], "verdicts": p["verdicts"], "best": p["best"]})
            print(f"  case {case['case']}: best {p['best']}")
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            print(f"  case {case['case']}: reply could not be parsed ({e}); see the raw file")
    json.dump(raw, open(os.path.join(RESULTS, f"judge_raw_{label}.json"), "w", encoding="utf-8"), indent=1)
    path = os.path.join(RESULTS, f"judge_output_{label}.json")
    json.dump({"cases": out}, open(path, "w", encoding="utf-8"), indent=1)
    print(f"wrote {path}")
    return path


def score(output_path, label):
    """Verdicts file: {"cases": [{"case": i, "verdicts": [...], "best": n|null}]} (or a list of those)."""
    inp = json.load(open(os.path.join(RESULTS, f"judge_input_{label}.json"), encoding="utf-8"))
    out = json.load(open(output_path, encoding="utf-8"))
    out = {c["case"]: c for c in (out["cases"] if isinstance(out, dict) else out)}
    rows, sheet, key = [], [f"# Blind review: plain search vs judge ({label})", "",
                            "For each case, does the passage show someone facing the SAME problem?",
                            "Which version produced which passage is hidden; see the _key.json file.", ""], {}
    rng = random.Random(0)
    for case in inp["cases"]:
        i, cands = case["case"], case["candidates"]
        o = out.get(i)
        if o is None:
            continue
        p = parse(json.dumps({"verdicts": o["verdicts"], "best": o["best"]}), len(cands))
        overall = {int(v["n"]): v["overall"] for v in p["verdicts"]}
        first_yes = next((n for n in range(1, len(cands) + 1) if overall.get(n) == "yes"), None)
        rows.append({"case": i, "search_top1": overall.get(1, "?"), "judge_best": p["best"],
                     "judge_best_overall": overall.get(p["best"]) if p["best"] else "none",
                     "yes_in_list": sum(v == "yes" for v in overall.values()),
                     "first_yes_rank": first_yes})
        picks = {"search": cands[0]}
        if p["best"]:
            picks["judge"] = cands[p["best"] - 1]
        distinct = {}
        for who, r in picks.items():
            distinct.setdefault(r["passage_id"], (r, []))[1].append(who)
        items = list(distinct.values())
        rng.shuffle(items)
        c = case["card"]
        sheet += [f"## Case {i}: {' > '.join(case['path'])}", "", f"- what happened: {c['event']}",
                  f"- because: {c['cause']}", f"- afraid it means: {c['meaning']}", ""]
        if not p["best"]:
            sheet += ["(one version found no good match)", ""]
        for j, (r, who) in enumerate(items, 1):
            sheet += [f"**{i}.{j}** {r['author']}, *{r['title']}* ({r['when']})", "", f"> {r['text']}", "",
                      "same problem? [ ] yes  [ ] partly  [ ] no", ""]
            key[f"{i}.{j}"] = who
    n = len(rows)
    print(f"cases judged: {n}")
    print(f"  plain search top-1 judged yes / partly: {sum(r['search_top1'] == 'yes' for r in rows)} / "
          f"{sum(r['search_top1'] == 'partly' for r in rows)}")
    print(f"  judge pick judged yes / partly / none:  {sum(r['judge_best_overall'] == 'yes' for r in rows)} / "
          f"{sum(r['judge_best_overall'] == 'partly' for r in rows)} / "
          f"{sum(r['judge_best'] is None for r in rows)}")
    print(f"  cases with at least one 'yes' in the top {inp['n']}: {sum(r['yes_in_list'] > 0 for r in rows)}")
    for r in rows:
        print(f"    case {r['case']}: search top-1 {r['search_top1']:<7} judge best {str(r['judge_best']):<5}"
              f" ({r['judge_best_overall']}), yes in list {r['yes_in_list']}, first yes at rank "
              f"{r['first_yes_rank']}")
    base = os.path.join(RESULTS, f"review_judge_{label}")
    open(base + ".md", "w", encoding="utf-8").write("\n".join(sheet))
    json.dump(key, open(base + "_key.json", "w", encoding="utf-8"), indent=1)
    json.dump(rows, open(base + "_scores.json", "w", encoding="utf-8"), indent=1)
    print(f"review sheet: {base}.md")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = sys.argv
    label = argv[argv.index("--label") + 1] if "--label" in argv else "run"
    if len(argv) > 1 and argv[1] == "export":
        export(label, int(argv[argv.index("--n") + 1]) if "--n" in argv else 20, rephrase="--rephrase" in argv)
    elif len(argv) > 1 and argv[1] == "run":
        score(run(label), label)
    elif len(argv) > 2 and argv[1] == "score":
        score(argv[2], label)
    else:
        print(__doc__)
