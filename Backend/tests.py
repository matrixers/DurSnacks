"""
Quick checks. Free: Claude is replaced by fake replies, so nothing is paid.

    python -m Backend.tests
"""
import json
import os
import re
import sys

from Backend import Backend, fame, llm
from Backend.library import EMOTIONS

failed = []


def check(name, ok):
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}")
    if not ok:
        failed.append(name)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    path = ["Sad", "Lonely", "Isolated"]
    answers = {"event": "My best friend moved away and stopped replying.", "cause": "I think I did something wrong"}

    print("the tree")
    check("6 core feelings with 6 feelings each",
          [c["label"] for c in Backend.TREE] == ["Mad", "Scared", "Joyful", "Sad", "Peaceful", "Powerful"]
          and all(len(c["specifics"]) == 6 for c in Backend.TREE))
    check("every emotion in tree.json exists in the library",
          all(t in EMOTIONS for c in Backend.TREE for f in c["specifics"] for t in f["tags"]))
    check("Sad > Lonely > Isolated points at loneliness",
          Backend.emotions_for(path) == ["loneliness", "not_belonging"])
    check("questions use the feeling", Backend.questions(path)[1]["text"] == "Why do you think you feel isolated?")

    print("the library")
    lib = Backend.library()
    check("every passage is word for word from its book", all(lib.verify(r) for r in lib.rows))

    print("search without Claude")
    key = os.environ.pop("ANTHROPIC_API_KEY", None)
    try:
        r = Backend.rewrite(path, answers)
        check("no key: the search uses their own words", "stopped replying" in r["sentence"] and r["error"])
        result = Backend.find(path, answers)
        check("3 results from 3 different writers",
              len(result["results"]) == 3 and len({x["author"] for x in result["results"]}) == 3)
        if fame.ready():
            check("one well-known writer, then two lesser-known",
                  [x["famous"] for x in result["results"]] == [True, False, False])
        check("results can be sent as JSON", bool(json.dumps(result)))
    finally:
        if key:
            os.environ["ANTHROPIC_API_KEY"] = key

    print("Claude, with fake replies")
    real_call, real_available = llm.call, llm.available
    llm.available = lambda: True
    try:
        llm.call = lambda prompt, model, **kw: "SENTENCE: My closest friend has gone quiet.\nPOEM:\na\nb\nc"
        r = Backend.rewrite(path, answers)
        check("rewrite gives a sentence and a 3-line poem",
              r["sentence"] == "My closest friend has gone quiet." and r["poem"] == "a\nb\nc")
        shortlist = Backend.search(path, r["sentence"], 4)
        quote = " ".join(shortlist[1]["text"].split()[:8])
        llm.call = lambda prompt, model, **kw: json.dumps(
            {"matches": [{"n": 2, "match": "yes", "quote": quote, "why": "same"},
                         {"n": 3, "match": "partly", "quote": "words that are not in it", "why": "close"}],
             "best": 2})
        matches, best = llm.judge(path, answers, r["sentence"], shortlist)
        check("the judge's reply is read", best == 2 and set(matches) == {2, 3})
        check("a quote copied exactly is kept", matches[2]["quote"] == quote)
        check("a quote that is not in the passage is dropped", matches[3]["quote"] is None)

        def fake_judge(prompt, model, **kw):      # quotes the first 8 words of passage [2]
            if "PASSAGES" not in prompt:
                return "SENTENCE: My closest friend has gone quiet.\nPOEM:\na\nb\nc"
            second = re.search(r"\[2\] .*?\n  PASSAGE: (.*?)\n", prompt, re.S).group(1)
            return json.dumps({"matches": [{"n": 2, "match": "yes", "quote": " ".join(second.split()[:8]),
                                            "why": "same"}], "best": 2})
        llm.call = fake_judge
        result = Backend.find(path, answers)
        check("find() uses the judge's quote", result["judged"] and any(x["quote"] for x in result["results"]))
        llm.call = lambda prompt, model, **kw: '{"matches": [], "best": "none"}'
        check("the judge can say nothing matches", Backend.find(path, answers)["no_match"])

        if Backend.guidance_library() is not None:
            def fake_guide(prompt, model, **kw):      # picks [3] (first 6 words) and [1] (a made-up quote)
                third = re.search(r"\n\[3\] [^:]*: (.*)", prompt).group(1)
                return json.dumps({"picks": [{"n": 3, "quote": " ".join(third.split()[:6])},
                                             {"n": 1, "quote": "not in the passage"}]})
            llm.call = fake_guide
            advice = Backend.find_guidance(path, answers, "My closest friend has gone quiet.")
            check("2 guidance quotes from 2 different writers",
                  len(advice) == 2 and advice[0]["name"] != advice[1]["name"])
            g = Backend.guidance_library().search("My closest friend has gone quiet. How should I bear "
                                                  "feeling isolated?", Backend.GUIDANCE_POOL)
            check("the AI's guidance pick and exact quote are used",
                  advice[0]["name"] == g[2]["author"] and advice[0]["quote"].split() == g[2]["text"].split()[:6])
            check("a guidance quote not in the passage falls back to the whole passage",
                  advice[1]["quote"].split() == g[0]["text"].split())
    finally:
        llm.call, llm.available = real_call, real_available

    print("separate from the app")
    folder = os.path.dirname(os.path.abspath(__file__))
    code = "".join(open(os.path.join(folder, f), encoding="utf-8").read() for f in os.listdir(folder)
                   if f.endswith(".py") and f != "tests.py")
    check("the backend never imports kivy or the frontend", "import kivy" not in code and "Frontend" not in code)

    print("\nALL OK" if not failed else f"\n{len(failed)} FAILED")


if __name__ == "__main__":
    main()
