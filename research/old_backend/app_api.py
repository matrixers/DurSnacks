"""
The bridge the app (Frontend/Main.py) calls. No Kivy in here: it runs the slow work on a
background thread and hands the answer to `on_done`, so the window never freezes.
(In Kivy, decorate on_done with @mainthread before it touches any widget.)

    app_api.warm_up()                                   # at app start: loads the library (~1 min)
    app_api.search(path, who, what, why, on_done)       # after "Let's dig deeper..."

on_done receives a dict:
    {"ok": True, "text": "...ready for a Label...", "poem": "3 lines", "no_match": False,
     "results": [{"quote", "author", "title", "when", "famous", "url", "passage",
                  "context_before", "context_after"}, ...]}
    or {"ok": False, "text": "...friendly message...", "error": "..."}
"""
import threading

from Backend import llm
from Backend.Backend import MIX, find, library, refine

_READY = threading.Event()


def warm_up():
    """Start loading the library (embedding model + passages) in the background."""
    def load():
        library()
        _READY.set()
    threading.Thread(target=load, daemon=True).start()


def _label(r):
    kind = {True: "well known", False: "lesser known"}.get(r.get("famous"))
    who = f"{r['author']}, {r['title']} ({r['when']})"
    return who + (f"  ({kind})" if kind else "")


def _text(poem, res):
    if res["no_match"]:
        return "Nobody in the library faced quite this yet. Try saying a little more about what happened."
    parts = []
    for r in res["results"]:
        parts.append(f"“{r.get('quote') or r['text']}”\n    — {_label(r)}")
    return "\n\n".join(parts)


def search(path, who="", what="", why="", on_done=print, use_judge=None):
    """path: the tree path, e.g. ["Sad", "Lonely", "Isolated"]; who/what/why: the three text boxes.
    use_judge: None = use the judge when an API key is set."""
    if use_judge is None:
        use_judge = llm.available()

    def work():
        try:
            answers = {"event": what.strip(), "cause": why.strip(),
                       "extra": f"People involved: {who.strip()}" if who.strip() else ""}
            r = refine(list(path), answers)
            res = find(list(path), card=r["card"], use_judge=use_judge, mix=MIX)
            out = {"ok": True, "poem": r["card"].get("poem", ""), "no_match": res["no_match"],
                   "text": _text(r["card"].get("poem", ""), res),
                   "results": [{"quote": x.get("quote") or x["text"], "author": x["author"],
                                "title": x["title"], "when": x["when"], "famous": x.get("famous"),
                                "url": x["url"], "passage": x["text"],
                                "context_before": x["context_before"], "context_after": x["context_after"]}
                               for x in res["results"]]}
        except Exception as e:      # never crash the app: show a message instead
            out = {"ok": False, "error": f"{type(e).__name__}: {e}",
                   "text": "Sorry, the search did not work this time. Please try again."}
        on_done(out)

    threading.Thread(target=work, daemon=True).start()
