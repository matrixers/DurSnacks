"""
Deep Rooted Guidance: backend.

The frontend (or anything else) calls plain functions and gets dicts back:

    wheel()                            -> the feelings tree (tree.json: labels and tags only)
    questions(path)                    -> the 3 questions to ask after the tree
    refine(path, answers)              -> the user's card: their answers + an LLM rewrite of the
                                          problem in general first-person terms (if a key is set)
    find(path, answers=None, card=None, k=3)
                                       -> passages from people who faced the same problem

`path` is what the user picked on the tree, outermost first: the app's tree gives
("Sad", "Lonely", "Isolated") (tree.json, labels copied from Frontend/Main.py FEELINGS);
Harry's older wheel gives ("Heavy", "lonely") (wheel.json) and still works.
The emotion tags of the chosen feeling steer the search. This module never
imports the frontend.

Try it in the terminal:

    python -m Backend.Backend chat            # tree -> guiding questions -> a passage; loops
    python -m Backend.Backend demo            # five fixed cases
    options: --method raw|profile|blend   --wheel other_wheel.json
             --no-llm  (no rewrite, no judge: plain search on the answers)
             --judge   (search makes a short list; the LLM judge picks the match, or none)
    The LLM steps need ANTHROPIC_API_KEY set (see Backend/llm.py); without it, plain search.
"""
import sys

import os

import numpy as np

from Backend import cards, fame
from Backend.library import WHEEL_PATH, load_wheel

METHODS = {"raw": 0.0, "profile": 1.0, "blend": 0.6}   # w in w*profile + (1-w)*raw
MIX = (1, 2)         # chat/showcase: one well-known writer, then two everyday people (Backend/fame.py)
SHOW_SENTENCES = 4   # sentences of the letter shown either side of a final result (the judge reads the same)

_LIB = None
TREE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tree.json")
_WHEEL = {"path": TREE_PATH, "cores": None}
_OLD_WHEEL = []      # Harry's wheel.json, so ("Heavy", "lonely") paths keep their tags


def library():
    """Load the passage library once (it loads the embedding model, which is slow)."""
    global _LIB
    if _LIB is None:
        from Backend.library import Library
        _LIB = Library()
    return _LIB


def wheel():
    """The feelings tree: [{id, label, plain, specifics: [{label, tags}]}] (labels and tags only)."""
    if _WHEEL["cores"] is None:
        _WHEEL["cores"] = load_wheel(_WHEEL["path"])
    return _WHEEL["cores"]


def _all_cores():
    if not _OLD_WHEEL:
        _OLD_WHEEL.extend(load_wheel(WHEEL_PATH))
    return wheel() + _OLD_WHEEL


def _core(path):
    return next((c for c in _all_cores() if path and c["label"].lower() == str(path[0]).lower()), None)


def tags_for(path):
    """Emotion tags of the chosen feeling, e.g. ("Sad", "Lonely", "Isolated") -> ["loneliness", "not_belonging"],
    ("Heavy", "lonely") -> ["loneliness"]."""
    core = _core(path)
    if not core or len(path) < 2:
        return []
    picked = {str(p).lower() for p in path[1:]}
    return next((s["tags"] for s in core["specifics"]
                 if s["label"].lower() in picked or (s.get("deeper") or "").lower() in picked), [])


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------
def questions(path):
    """The questions asked after the tree, as [{"key", "text", "optional"}]."""
    path = [p for p in path if p]
    feeling = path[-1].lower() if path else "this way"
    return [
        {"key": "event", "optional": False, "text": "What's happened?"},
        {"key": "cause", "optional": False, "text": f"Why do you think you feel {feeling}?"},
        {"key": "extra", "optional": True, "text": "Anything else?"},
    ]


def refine(path, answers, use_llm=True):
    """Turn the wheel path + answers into a card and a reflect-back sentence.

    The card keeps the person's own answers (the judge reads them) and, when the
    LLM is available, adds `statement`: their problem rewritten in general
    first-person terms, which is what the search compares. Without the LLM (no
    key, error, or use_llm=False) the answers are joined by a template instead.
    Returns {"card", "reflect_back", "used_llm", "llm_error"}."""
    answers = answers or {}
    card = cards.from_answers(path, answers)
    used_llm, err = False, None
    if use_llm:
        from Backend import llm
        try:
            rw = llm.rewrite(path, answers)
            card.statement, card.poem = rw["statement"], rw["poem"]
            used_llm = True
        except llm.NoLLM as e:
            err = str(e)
        except Exception as e:  # API error, bad reply: fall back, but say why
            err = f"{type(e).__name__}: {e}"
    return {"card": card.to_dict(), "reflect_back": cards.reflect_back(path, card),
            "used_llm": used_llm, "llm_error": err}


def shortlist(path, answers=None, card=None, n=20, per_author=1, method="blend", with_heard=False,
              context=2, who=None):
    """Plain search: the n closest passages (at most `per_author` from one author),
    each verified word for word and given its surrounding sentences.
    who="famous" / "everyday": only writers of that kind (needs data/fame.json)."""
    c = cards.Card(**card) if card else cards.from_answers(path, answers or {})
    lib = library()
    scores, prof = lib.engine.scores(c.as_query(), METHODS[method], tags=tags_for(path))
    out, count = [], {}
    for i in np.argsort(scores)[::-1]:
        row = lib.rows[i]
        if count.get(row["author"], 0) >= per_author:
            continue
        if who is not None and fame.famous(row["author"]) != (who == "famous"):
            continue
        assert lib.verify(row), "passage does not match its source"
        before, after = lib.context(row, n=context)
        out.append({
            "passage_id": row["id"], "text": row["text"],
            "context_before": before, "context_after": after,
            "author": row["author"], "title": row["title"], "when": lib.when(row),
            "translator": row.get("translator"), "kind": row.get("kind"),
            "year": row["year"], "url": row["url"], "score": round(float(scores[i]), 3),
            "famous": fame.famous(row["author"]),
        })
        count[row["author"]] = count.get(row["author"], 0) + 1
        if len(out) == n:
            break
    if with_heard:
        return out, [name for name, _ in lib.engine.concerns(prof)]
    return out


def find(path, answers=None, card=None, k=3, method="blend", use_judge=False, pool=None, mix=None):
    """Passages from people facing the same problem.

    Give either the diary `answers` or an already confirmed `card` (dict).
    use_judge: plain search makes a short list of `pool` passages and the judge
    (Backend/judge.py) picks the real matches, or none. If the judge is not
    implemented or fails, plain search order is returned and judged=False.
    mix=(1, 2): one well-known writer then two everyday people (k is ignored); the judge reads
    half its pool from each group. Without data/fame.json mix is ignored.
    Returns {"heard", "card", "judged", "judge_error", "no_match", "results"}."""
    answers = answers or {}
    if pool is None:   # how many passages the judge reads (fewer = cheaper); JUDGE_POOL in .env
        from Backend import llm
        pool = llm.JUDGE_POOL
    c = cards.Card(**card) if card else cards.from_answers(path, answers)
    if mix and fame.famous("") is None:
        mix = None                       # fame list not built yet: plain order
    # the judge reads each passage with the same surrounding sentences the person will see
    if mix:
        nf, ne = (pool // 2, pool - pool // 2) if use_judge else mix
        fam, heard = shortlist(path, card=c.to_dict(), n=nf, method=method, with_heard=True,
                               context=SHOW_SENTENCES, who="famous")
        eve = shortlist(path, card=c.to_dict(), n=ne, method=method, context=SHOW_SENTENCES, who="everyday")
        cands = [x for pair in zip(eve, fam) for x in pair] + eve[len(fam):] + fam[len(eve):]  # mixed
        first = fam[:mix[0]] + eve[:mix[1]]
    else:
        cands, heard = shortlist(path, card=c.to_dict(), n=pool if use_judge else k, method=method,
                                 with_heard=True, context=SHOW_SENTENCES)
        first = cands[:k]
    judged, no_match, results, err = False, False, first, None
    if use_judge:
        from Backend import judge
        try:
            v = judge.judge(c, cands)
            if v is None:
                err = "no LLM available (ANTHROPIC_API_KEY not set)"
        except Exception as e:
            v, err = None, f"{type(e).__name__}: {e}"
        if v is not None:
            judged = True
            overall = {int(x["n"]): x for x in v["verdicts"]}
            good = [n for n in range(1, len(cands) + 1)
                    if overall.get(n, {}).get("overall") in ("yes", "partly")]
            order = ([v["best"]] if v["best"] else []) + [n for n in good if n != v["best"]]
            if mix:   # the best famous match(es), then the best everyday ones
                order = ([n for n in order if cands[n - 1]["famous"]][:mix[0]]
                         + [n for n in order if not cands[n - 1]["famous"]][:mix[1]])
            results = []
            for n in (order if mix else order[:k]):
                r = dict(cands[n - 1])
                r["verdict"] = overall.get(n)
                # a shorter quote picked by the judge, kept only if it is word for word in the passage
                r["quote"] = judge.checked_quote((r["verdict"] or {}).get("quote"), r["text"])
                results.append(r)
            no_match = not results
    return {"card": c.to_dict(), "heard": heard, "judged": judged, "judge_error": err,
            "no_match": no_match, "results": results}


# --------------------------------------------------------------------------
# Terminal
# --------------------------------------------------------------------------
DEMO = [
    (("Heavy", "lonely"),
     {"event": "Nobody has replied to my messages in weeks.",
      "cause": "my friends seem to have forgotten me",
      "meaning": "that I am easy to forget",
      "coping": "I keep checking my phone"}),
    (("Small", "like a failure"),
     {"event": "I failed my exams and everyone on my course did better than me.",
      "cause": "I am not clever enough for this course",
      "meaning": "that I will never make anything of myself",
      "coping": "I have stopped going to lectures"}),
    (("Heavy", "grieving"),
     {"event": "My dad died this year.",
      "cause": "I miss him and I do not know how to carry on without him",
      "meaning": "that the best part of my life is over",
      "coping": "I keep busy so I don't have to think"}),
    (("Heavy", "homesick"),
     {"event": "I moved to a new city for university.",
      "cause": "I miss home and my family so much",
      "meaning": "that I do not belong here",
      "coping": "I call my mum every night"}),
    (("Drained", "stuck"),
     {"event": "I am doing everything I am supposed to do.",
      "cause": "none of it feels like it matters",
      "meaning": "that my life has no point",
      "coping": "I just keep going through the motions"}),
]


def _pick(prompt, options):
    """Choose by number or by typing a word (any word is accepted)."""
    for n, o in enumerate(options, 1):
        print(f"  {n:>2}. {o}")
    while True:
        a = input(f"{prompt} ").strip()
        if not a:
            continue
        if a.isdigit() and 1 <= int(a) <= len(options):
            return options[int(a) - 1]
        return a


def _wrap(text, prefix):
    import textwrap
    return "\n".join(textwrap.wrap(text, 76 - len(prefix), initial_indent=prefix,
                                   subsequent_indent=prefix)) if text else ""


def print_result(r, full=False):
    """Short by default: just the quote (the judge's key sentence(s), else the passage).
    full=True: the whole passage with the sentences around it."""
    who = f"{r['author']}, {r['title']} ({r['when']})"
    if r.get("translator"):
        who += f", translated by {r['translator']}"
    if r.get("famous") is not None:
        who += "  (well known)" if r["famous"] else "  (lesser known)"
    if not full:
        print(f"\n{_wrap('“' + (r.get('quote') or r['text']) + '”', '    ')}\n\n        - {who}")
        return
    print(f"\n  {who}    match {r['score']:.2f}")
    print(f"  {r['url']}\n")
    if r["context_before"]:
        print(_wrap(r["context_before"], "    "))
    print(_wrap(r["text"], "  > "))
    if r["context_after"]:
        print(_wrap(r["context_after"], "    "))
    if r.get("verdict"):
        v = r["verdict"]
        print(f"\n  judge: emotion {v.get('emotion', '?')}, situation {v['situation']}, cause {v['cause']}, "
              f"fear {v['fear']}; coping: {v.get('coping', '?')}. {v['why']}")


def _match(text, options):
    """Index of the option matching typed text (number, exact word, or start of a word), else None."""
    t = text.strip().lower()
    if t.isdigit():
        n = int(t)
        return n - 1 if 1 <= n <= len(options) else None
    for i, o in enumerate(options):
        if o.lower() == t or o.lower().split(" (")[0] == t:
            return i
    hits = [i for i, o in enumerate(options) if o.lower().startswith(t)] if len(t) >= 3 else []
    return hits[0] if len(hits) == 1 else None


def _spec_path(core, spec):
    return [core["label"], spec["label"]] + ([spec["deeper"]] if spec.get("deeper") else [])


def pick_path():
    """Walk the tree: core feeling, then the specific feeling (labels from tree.json).
    Accepts a number, a word, both at once ("4 lonely"), or a specific feeling straight away ("isolated").
    Returns the full path, e.g. ["Sad", "Lonely", "Isolated"]."""
    cores = wheel()
    labels = [f"{c['label']} ({c['plain']})" if c.get("plain") else c["label"] for c in cores]
    for n, o in enumerate(labels, 1):
        print(f"  {n:>2}. {o}")
    while True:
        a = input("How does today feel? (number or word) ").strip()
        if not a:
            continue
        first, _, rest = a.partition(" ")
        i = _match(first, labels) if rest else _match(a, labels)
        if i is not None:
            core, typed = cores[i], rest.strip()
            break
        # a specific feeling typed straight away: find its core
        found = [(c, s) for c in cores for s in c["specifics"]
                 if a.lower() in (s["label"].lower(), (s.get("deeper") or "").lower())]
        if found:
            return _spec_path(*found[0])
        print("  Please type a number from the list (or a feeling from the next list, e.g. lonely).")
    specs = core["specifics"]
    if not specs:
        return [core["label"]]
    names = [s["label"] for s in specs]
    deeper = [s.get("deeper") or s["label"] for s in specs]

    def pick(text):
        j = _match(text, names)
        return j if j is not None else _match(text, deeper)

    if typed and pick(typed) is not None:
        return _spec_path(core, specs[pick(typed)])
    for n, s in enumerate(specs, 1):
        print(f"  {n:>2}. {s['label']}" + (f" / {s['deeper']}" if s.get("deeper") else ""))
    while True:
        a = input("Which is closest? (number or word) ").strip()
        j = pick(a) if a else None
        if j is not None:
            return _spec_path(core, specs[j])
        if a:
            return [core["label"], a]      # their own word is accepted


def chat(method, use_llm, use_judge=False):
    from Backend import llm
    print("Deep Rooted Guidance (terminal). Ctrl+C to stop.")
    if use_llm and not llm.available():
        print("(ANTHROPIC_API_KEY is not set: no rewrite and no judge, plain search only)")
        use_llm = use_judge = False
    elif use_llm:
        print(f"(rewrite: {llm.REPHRASE_MODEL}" + (f", judge: {llm.JUDGE_MODEL})" if use_judge else ", no judge)"))
    print("\nLoading the library (about a minute the first time)...", flush=True)
    library()
    print()
    while True:
        path = pick_path()
        print(f"\npath: {' > '.join(path)}    emotion tags: {', '.join(tags_for(path)) or 'none'}\n")
        while True:
            answers = {}
            for q in questions(path):
                hint = "  (optional, Enter to skip)" if q["optional"] else ""
                answers[q["key"]] = input(f"{q['text']}{hint}\n  > ").strip()
            if use_llm:
                print("\n(rewriting...)", flush=True)
            out = refine(path, answers, use_llm=use_llm)
            if out["llm_error"]:
                print(f"\n(rewrite failed, using your words as they are: {out['llm_error']})")
            print(f"\n{out['reflect_back']}")
            if input("[Y/n] ").strip().lower() in ("", "y", "yes"):
                break
            print("Let's try again.\n")
        if use_judge:
            print(f"\n(searching, then the judge reads {llm.JUDGE_POOL} passages with their context: "
                  "about 20-40 seconds...)", flush=True)
        res = find(path, card=out["card"], k=3, method=method, use_judge=use_judge, mix=MIX)
        print(f"\nheard: {', '.join(res['heard'])}")
        if use_judge and not res["judged"]:
            print(f"(judge failed, showing plain search: {res['judge_error']})")
        if res["no_match"]:
            print("\nNo passage in the library is a real match for this yet.")
            if input("\nAgain? [y/N] ").strip().lower() not in ("y", "yes"):
                return
            continue
        for r in res["results"]:
            print_result(r)
            if input("\nRead the letter around it? [y/N] ").strip().lower() in ("y", "yes"):
                print_result(r, full=True)
        if use_llm:
            print(f"\n(API cost so far this session: ${llm.SPENT['usd']:.3f} over {llm.SPENT['calls']} calls)")
        if input("\nAgain? [y/N] ").strip().lower() not in ("y", "yes"):
            return


SHOWCASE = [
    # paths from the app's tree (tree.json); it has no "grieving", so the first case is guilty > remorseful
    (("Sad", "Guilty", "Remorseful"), {"event": "My grandad died last month",
                                       "cause": "I never got to say goodbye"}),
    (("Sad", "Lonely", "Isolated"), {"event": "My best friend stopped replying to my messages",
                                     "cause": "I think I did something wrong"}),
]


def demo(method, use_llm=False, use_judge=False, cases=None):
    from Backend import llm
    if use_llm and not llm.available():
        print("ANTHROPIC_API_KEY not found (put it in the .env file): running plain search only.")
        use_llm = use_judge = False
    print("Loading the library (about a minute the first time)...", flush=True)
    library()
    for n, (path, answers) in enumerate(cases or DEMO, 1):
        if use_llm:
            print(f"\nExample {n}: rewriting" + (", searching and judging (about 20-40 seconds)..." if use_judge
                                                  else " and searching..."), flush=True)
        out = refine(path, answers, use_llm=use_llm)
        res = find(path, card=out["card"], k=1, method=method, use_judge=use_judge,
                   mix=MIX if cases is SHOWCASE else None)
        print("\n" + "=" * 78)
        print("path:", " > ".join(path), "   tags:", ", ".join(tags_for(path)))
        for q in questions(path):
            if answers.get(q["key"]):
                print(f"{q['text']}  {answers[q['key']]}")
        if out["llm_error"]:
            print(f"(rewrite failed: {out['llm_error']})")
        print("searched for:", cards.Card(**out["card"]).as_query())
        if use_judge and not res["judged"]:
            print(f"(judge failed, plain search: {res['judge_error']})")
        if res["no_match"]:
            print("\nThe judge found no real match in the shortlist.")
        else:
            for r in (res["results"] if cases is SHOWCASE else res["results"][:1]):
                print_result(r)
    if use_llm:
        print(f"\nAPI cost of this run: ${llm.SPENT['usd']:.3f} over {llm.SPENT['calls']} calls "
              f"(logged in results/usage.log)")


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    method = argv[argv.index("--method") + 1] if "--method" in argv else "blend"
    if "--wheel" in argv:
        _WHEEL["path"], _WHEEL["cores"] = argv[argv.index("--wheel") + 1], None
    use_llm = "--no-llm" not in argv
    cmd = argv[1] if len(argv) > 1 and not argv[1].startswith("--") else "chat"
    try:
        if cmd == "demo":
            demo(method, use_llm="--llm" in argv or "--judge" in argv, use_judge="--judge" in argv)
        elif cmd == "showcase":   # the two friend-demo cases, with rewrite + judge
            demo(method, use_llm=True, use_judge=True, cases=SHOWCASE)
        else:
            chat(method, use_llm, use_judge="--judge" in argv and use_llm)
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main(sys.argv)
