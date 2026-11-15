"""
Set-up checks. Run after every build or code change:

    python -m Backend.check

Checks the library is sound (every passage verbatim at its offsets, no
duplicates), the API contract, and the LLM wiring (rewrite and judge) with fake
replies, so it never makes a paid call even when ANTHROPIC_API_KEY is set.
Prints PASS/FAIL per check.
"""
import json
import os
import sys

from Backend import cards, judge, llm
from Backend.Backend import find, library, questions, refine, shortlist

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def ok(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}{('  ' + detail) if detail else ''}")
    if not cond:
        FAILS.append(name)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("library")
    lib = library()
    n = len(lib.rows)
    bad = [r["id"] for r in lib.rows if not lib.verify(r)]
    ok("every passage is verbatim at its stored offsets", not bad, f"{n} passages, {len(bad)} mismatches")
    texts = [r["text"] for r in lib.rows]
    ok("no duplicate passages", len(set(texts)) == len(texts), f"{len(texts) - len(set(texts))} duplicates")
    n_src = lib.db.execute("SELECT COUNT(*) FROM sources WHERE clean_text != ''").fetchone()[0]
    n_empty = lib.db.execute("SELECT COUNT(*) FROM sources WHERE clean_text = ''").fetchone()[0]
    ok("sources with passages", n_src > 0, f"{n_src} books used, {n_empty} skipped (no new passages)")
    short = [r for r in lib.rows if len(r["text"].split()) < 15]
    ok("passages are 15+ words (short units)", not short, f"{len(short)} shorter")

    print("API contract")
    path = ("Heavy", "lonely")
    ans = {"event": "My best friend moved away and stopped replying.",
           "cause": "I think I did something wrong", "extra": "evenings are the worst"}
    qs = questions(path)
    ok("questions() gives event/cause/extra",
       [q["key"] for q in qs] == ["event", "cause", "extra"]
       and qs[1]["text"] == "Why do you think you feel lonely?")
    from Backend.Backend import tags_for, wheel
    from Backend.library import wheel_tags
    ok("wheel.json loads (labels and tags)", len(wheel()) >= 5 and tags_for(path) == ["loneliness"])
    ok("the emotion scores use exactly the wheel's tags", lib.engine.names == wheel_tags())
    rf = refine(path, ans, use_llm=False)
    ok("refine() gives a card and a reflect-back", rf["card"] and rf["reflect_back"] and not rf["used_llm"])
    res = find(path, card=rf["card"], k=3)
    ok("find() gives 3 results, one per author",
       len(res["results"]) == 3 and len({x["author"] for x in res["results"]}) == 3)
    ok("results are JSON-serialisable", bool(json.dumps(res)))
    sl = shortlist(path, card=rf["card"], n=20)
    ok("shortlist() gives 20 verified candidates", len(sl) == 20 and all(
        lib.verify(lib.rows[[x["id"] for x in lib.rows].index(c["passage_id"])]) for c in sl[:3]))

    print("LLM rewrite wiring (fake replies, no API)")
    real_llm_call = llm.call
    statement = "The friend I was closest to has gone silent, and I fear it was my fault."
    llm.call = lambda prompt, model, max_tokens=16000: statement
    rf2 = refine(path, ans)
    ok("refine() puts the rewrite in card.statement",
       rf2["used_llm"] and rf2["card"]["statement"] == statement and rf2["card"]["event"] == ans["event"])
    ok("the search compares the rewrite", cards.Card(**rf2["card"]).as_query() == statement)

    def broken(prompt, model, max_tokens=16000):
        raise RuntimeError("fake API error")

    llm.call = broken
    rf3 = refine(path, ans)
    ok("a failed rewrite falls back to the person's words", not rf3["used_llm"] and rf3["llm_error"]
       and rf3["card"]["statement"] == cards.NOT_STATED)
    llm.call = real_llm_call
    prompt2 = judge.build_prompt(cards.Card(**rf2["card"]), sl[:2])
    ok("judge prompt has the person's own answers and the rewrite",
       all(v in prompt2 for v in ans.values()) and statement in prompt2)

    print("judge wiring (fake judge, no API)")
    real_call = judge.call_llm

    def no_llm(prompt):
        raise NotImplementedError("check.py never calls the real LLM")

    judge.call_llm = no_llm  # the checks stay free even after call_llm is implemented
    ok("judge returns None when no LLM is available",
       judge.judge(cards.Card(**rf["card"]), sl, call=no_llm) is None)
    res = find(path, card=rf["card"], k=3, use_judge=True)
    ok("find(use_judge=True) falls back to plain search", not res["judged"] and len(res["results"]) == 3)
    judge.call_llm = real_call
    fake = json.dumps({"verdicts": [{"n": 5, "emotion": "yes", "situation": "yes", "cause": "partly",
                                     "fear": "not stated", "coping": "struggling", "overall": "yes",
                                     "why": "test"}], "best": 5})
    v = judge.judge(cards.Card(**rf["card"]), sl, call=lambda p: fake)
    ok("a valid judge reply is parsed", v and v["best"] == 5)
    none = json.dumps({"verdicts": [], "best": "none"})
    ok("'none' is accepted", judge.judge(cards.Card(**rf["card"]), sl, call=lambda p: none)["best"] is None)
    try:
        judge.parse(json.dumps({"verdicts": [{"n": 2, "situation": "no", "cause": "no", "fear": "no",
                                               "overall": "no", "why": ""}], "best": 2}), 20)
        ok("a 'best' judged 'no' is rejected", False)
    except ValueError:
        ok("a 'best' judged 'no' is rejected", True)
    prompt = judge.build_prompt(cards.Card(**rf["card"]), sl)
    ok("judge prompt contains every candidate verbatim", all(c["text"] in prompt for c in sl))
    words = sl[0]["text"].split()
    part = " ".join(words[2:12])
    ok("a short quote copied from the passage is kept", judge.checked_quote(part, sl[0]["text"]) == part)
    ok("a quote not word for word in the passage is dropped",
       judge.checked_quote(part + " and more", sl[0]["text"]) is None
       and judge.checked_quote(words[0] + " ... " + words[-1], sl[0]["text"]) is None)
    fake_q = json.dumps({"verdicts": [{"n": 1, "emotion": "yes", "situation": "yes", "cause": "yes",
                                       "fear": "not stated", "overall": "yes", "why": "x", "quote": part}],
                         "best": 1})
    real_judge = judge.call_llm
    judge.call_llm = lambda prompt: fake_q
    rq = find(("Heavy", "lonely"), answers=ans, use_judge=True, pool=5)["results"][0]
    judge.call_llm = real_judge
    ok("find() returns the judge's quote", rq.get("quote") == " ".join(part.split()))

    print("the app's tree (tree.json) and the famous / everyday mix")
    from Backend.Backend import tags_for, wheel, MIX
    ok("app tree paths get tags", tags_for(("Sad", "Lonely", "Isolated")) == ["loneliness", "not_belonging"]
       and tags_for(("Scared", "Anxious", "Overwhelmed")) == ["anxiety", "overwhelm"])
    ok("old wheel paths still get tags", tags_for(("Heavy", "lonely")) == ["loneliness"])
    ok("tree has the app's 6 cores x 6 feelings",
       [c["label"] for c in wheel()] == ["Mad", "Scared", "Joyful", "Sad", "Peaceful", "Powerful"]
       and all(len(c["specifics"]) == 6 and all(s["deeper"] for s in c["specifics"]) for c in wheel()))
    from Backend import fame
    if fame.famous("") is None:
        print("  (skip) data/fame.json not built: python -m Backend.fame build")
    else:
        mres = find(("Sad", "Lonely", "Isolated"), answers=ans, mix=MIX)["results"]
        ok("mix gives one well-known writer then two everyday ones",
           [r["famous"] for r in mres] == [True, False, False])
        ok("who='everyday' gives only everyday writers", all(r["famous"] is False for r in
           shortlist(("Sad", "Lonely", "Isolated"), answers=ans, n=4, who="everyday")))

    print("separation from the frontend")
    src = "".join(open(os.path.join(ROOT, "Backend", f), encoding="utf-8").read()
                  for f in os.listdir(os.path.join(ROOT, "Backend")) if f.endswith(".py") and f != "check.py")
    ok("no Backend file imports kivy or Frontend",
       "import kivy" not in src and "from kivy" not in src and "Frontend" not in src.replace("frontend", ""))

    print(f"\n{'ALL PASS' if not FAILS else str(len(FAILS)) + ' FAILED: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
