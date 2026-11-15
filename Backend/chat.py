"""
Try the backend in the terminal.

    python -m Backend.chat             pick a feeling, answer the questions, read the passages
    python -m Backend.chat showcase    two ready-made examples (for a demo)
"""
import sys
import textwrap

from Backend import llm
from Backend.Backend import TREE, find, library, questions, rewrite, short_title

SHOWCASE = [
    (["Sad", "Guilty", "Remorseful"], {"event": "My grandad died last month", "cause": "I never got to say goodbye"}),
    (["Sad", "Lonely", "Isolated"], {"event": "My best friend stopped replying to my messages",
                                     "cause": "I think I did something wrong"}),
]


def wrap(text, indent="    "):
    return textwrap.fill(text, 76, initial_indent=indent, subsequent_indent=indent)


def choose(prompt, options):
    """Pick by number or by typing (the start of) a word. Returns the index."""
    for n, option in enumerate(options, 1):
        print(f"  {n:>2}. {option}")
    while True:
        typed = input(f"{prompt} ").strip().lower()
        if typed.isdigit() and 1 <= int(typed) <= len(options):
            return int(typed) - 1
        hits = [i for i, o in enumerate(options) if len(typed) >= 3 and typed in o.lower()]
        if len(hits) == 1:
            return hits[0]
        print("  Please type a number from the list.")


def pick_feeling():
    core = TREE[choose("How does today feel?", [c["label"] for c in TREE])]
    options = [f"{f['label']} / {f['deeper']}" for f in core["specifics"]]
    feeling = core["specifics"][choose("Which is closest?", options)]
    return [core["label"], feeling["label"], feeling["deeper"]]


def show(result, ask=True):
    if result["error"]:
        print(f"\n({result['error']})")
    if not result["results"]:
        print("\nNobody in the library has written about quite this yet.")
    for r in result["results"]:
        label = {True: "  (well known)", False: "  (lesser known)"}.get(r["famous"], "")
        print(f"\n{wrap('“' + (r['quote'] or r['text']) + '”')}\n        - {r['author']}, {short_title(r['title'])} "
              f"({r['when']}){label}")
        if ask and input("\n  Read the letter around it? [y/N] ").strip().lower() == "y":
            print(f"\n  {r['url']}\n")
            for part in (r["context_before"], r["text"], r["context_after"]):
                if part:
                    print(wrap(part) + "\n")
            if r["why"]:
                print(f"  Why it matches: {r['why']}")


def chat():
    print("Loading the library (about a minute)...", flush=True)
    library()
    if not llm.available():
        print("(No API key in .env, so no rewrite and no judge: searching your own words.)")
    while True:
        path = pick_feeling()
        answers = {}
        for q in questions(path):
            hint = "  (optional, press Enter to skip)" if q["optional"] else ""
            answers[q["key"]] = input(f"\n{q['text']}{hint}\n  > ").strip()
        rewritten = rewrite(path, answers)
        if rewritten["poem"]:
            print("\nSo what you're saying is:\n\n" + "\n".join("    " + l for l in rewritten["poem"].splitlines()))
        print("\nSearching old letters and diaries (about 30 seconds)...", flush=True)
        show(find(path, answers, sentence=rewritten["sentence"]))
        if llm.spent["calls"]:
            print(f"\n(API cost so far: ${llm.spent['usd']:.3f})")
        if input("\nAgain? [y/N] ").strip().lower() != "y":
            return


def showcase():
    print("Loading the library (about a minute)...", flush=True)
    library()
    for path, answers in SHOWCASE:
        print("\n" + "=" * 78 + f"\n{' > '.join(path)}")
        for q in questions(path):
            if answers.get(q["key"]):
                print(f"  {q['text']}  {answers[q['key']]}")
        print("\nSearching (about 30 seconds)...", flush=True)
        result = find(path, answers)
        print(f"Searched for: {result['sentence']}")
        show(result, ask=False)
    print(f"\n(API cost of this run: ${llm.spent['usd']:.3f})")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        showcase() if "showcase" in sys.argv else chat()
    except (KeyboardInterrupt, EOFError):
        print()
