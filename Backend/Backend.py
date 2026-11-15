"""
Deep Rooted Guidance backend: finds passages from real old letters and diaries where
the writer went through the same thing as you.

What the app calls:
    questions(path)                            the questions to ask after the tree
    find(path, answers)                        one well-known writer + two lesser-known ones
    sentiment(path), picture(sentiment)        the picked feeling (keyed like the picture JSON) and its painting
    find_in_background(path, answers, on_done) the same, without freezing the app window
    as_text(result)                            the results as text, ready to put on screen

`path` is what was picked on the tree, e.g. ["Sad", "Lonely", "Isolated"] (labels in Backend/tree.json).
`answers` is {"event": ..., "cause": ..., "extra": ...}, the person's answers to the questions.

How a match is found:
    1. rewrite   the answers become one short, general sentence (and a 3-line poem to show back)
    2. search    every passage is scored against that sentence; the best 10 from well-known writers
                 and the best 10 from lesser-known ones are kept, one per writer
    3. judge     Claude reads those 20 with the sentences around them and keeps only the real matches
Without an API key, steps 1 and 3 are skipped and the person's own words are searched.
"""
import json
import os
import re
import threading

import numpy as np

from Backend import fame, llm
from Backend.library import ROOT, Library

TREE = json.load(open(os.path.join(os.path.dirname(__file__), "tree.json"), encoding="utf-8"))["cores"]
CONTEXT_SENTENCES = 4      # sentences shown (and read by the judge) either side of a passage
ALWAYS_THREE = True        # True = always fill the 3 quote boxes: if the judge keeps fewer, the closest
                           # other search results fill the rest. False = show only what the judge kept.
_library = None
_loading = threading.Lock()


def library():
    """The passage library, loaded once (about a minute the first time).
    Safe to call from several threads: the app can start loading it while the person uses the tree."""
    global _library
    with _loading:
        if _library is None:
            _library = Library()
    return _library


def emotions_for(path):
    """The emotions a tree choice points the search at, e.g. Sad > Lonely > Isolated -> loneliness, not_belonging."""
    picked = {p.lower() for p in path[1:]}
    for core in TREE:
        if path and core["label"].lower() == path[0].lower():
            for feeling in core["specifics"]:
                if feeling["label"].lower() in picked or feeling["deeper"].lower() in picked:
                    return feeling["tags"]
    return []


def sentiment(path):
    """The feeling picked on the tree, in the tree's own labels and with the same keys as the
    picture JSON (Backend/backend_JSON.JSON): emotion = core, name = secondary.
    ["sad", "lonely", "isolated"] -> {"emotion": "Sad", "name": "Lonely", "deeper": "Isolated"}"""
    found = {"emotion": None, "name": None, "deeper": None}
    picked = {p.lower() for p in path[1:]}
    for core in TREE:
        if path and core["label"].lower() == path[0].lower():
            found["emotion"] = core["label"]
            for feeling in core["specifics"]:
                if feeling["label"].lower() in picked or feeling["deeper"].lower() in picked:
                    found.update(name=feeling["label"], deeper=feeling["deeper"])
                    break
    return found


def picture(feeling):
    """The painting for a sentiment (from data/manifest.json), or None if there isn't one on disk."""
    manifest = os.path.join(ROOT, "data", "manifest.json")
    if not feeling["name"] or not os.path.exists(manifest):
        return None
    pair = f"{feeling['name']} / {feeling['deeper']}"
    for p in json.load(open(manifest, encoding="utf-8")):
        if p["core"] == feeling["emotion"] and p["pair"] == pair:
            if not os.path.exists(os.path.join(ROOT, "data", p["file"])):
                return None
            return {"imageURL": f"data/{p['file']}", "title": p["title"], "artist": p["artist"],
                    "year": p["year"], "link": p["page"]}
    return None


def questions(path):
    feeling = path[-1].lower() if path else "this way"
    return [{"key": "event", "text": "What's happened?", "optional": False},
            {"key": "cause", "text": f"Why do you think you feel {feeling}?", "optional": False},
            {"key": "extra", "text": "Anything else?", "optional": True}]


def rewrite(path, answers):
    """{"sentence", "poem", "error"}. If Claude can't be used, the sentence is just their own words."""
    try:
        return {**llm.rewrite(path, answers), "error": None}
    except Exception as e:
        own_words = [f"I feel {path[-1].lower()}." if path else ""]
        own_words += [answers.get(k, "").strip().rstrip(".") + "." for k in ("event", "cause", "extra")
                      if answers.get(k, "").strip()]
        return {"sentence": " ".join(w for w in own_words if w), "poem": "", "error": str(e)}


def search(path, sentence, n, famous=None):
    """The n passages closest to the sentence, one per writer, each with the sentences around it.
    famous=True / False keeps only well-known / lesser-known writers."""
    lib = library()
    scores = lib.scores(sentence, emotions_for(path))
    found, writers = [], set()
    for i in np.argsort(scores)[::-1]:
        row = lib.rows[i]
        if row["author"] in writers or (famous is not None and fame.famous(row["author"]) != famous):
            continue
        assert lib.verify(row), "a passage does not match its book"
        before, after = lib.context(row, CONTEXT_SENTENCES)
        found.append({"text": row["text"], "quote": None, "why": None, "match": None,
                      "context_before": before, "context_after": after,
                      "author": row["author"], "title": row["title"], "when": lib.when(row),
                      "translator": row["translator"], "url": row["url"],
                      "famous": fame.famous(row["author"]) if fame.ready() else None})
        writers.add(row["author"])
        if len(found) == n:
            break
    return found


def one_famous_two_others(passages):
    if not fame.ready():
        return passages[:3]
    return [p for p in passages if p["famous"]][:1] + [p for p in passages if not p["famous"]][:2]


def find(path, answers, sentence=None, use_judge=True):
    """Returns {"sentence", "results", "no_match", "judged", "error"}.
    Each result has the passage `text`, a shorter `quote` picked by the judge (or None),
    the author, title, dates, link and the sentences around it."""
    error = None
    if sentence is None:
        rewritten = rewrite(path, answers)
        sentence, error = rewritten["sentence"], rewritten["error"]
    use_judge = use_judge and llm.available()
    each = llm.JUDGE_POOL // 2 if use_judge else 3
    if fame.ready():
        well_known, others = search(path, sentence, each, True), search(path, sentence, each, False)
        shortlist = [p for pair in zip(others, well_known) for p in pair]    # take turns
    else:
        shortlist = search(path, sentence, 2 * each)
    result = {"sentence": sentence, "results": one_famous_two_others(shortlist), "no_match": False,
              "judged": False, "error": error}
    if not use_judge:
        return result
    try:
        matches, best = llm.judge(path, answers, sentence, shortlist)
    except Exception as e:
        result["error"] = f"judge failed, showing the plain search: {e}"
        return result
    order = sorted(matches, key=lambda n: (n != best, matches[n]["match"] != "yes", n))
    for n in order:
        shortlist[n - 1]["quote"], shortlist[n - 1]["why"] = matches[n]["quote"], matches[n]["why"]
        shortlist[n - 1]["match"] = matches[n]["match"]
    judged = [shortlist[n - 1] for n in order]
    result["no_match"], result["judged"] = not judged, True
    if ALWAYS_THREE:
        # the judge's matches first, then the closest of the rest of the search to fill the 3 boxes
        judged += [p for p in shortlist if all(p is not j for j in judged)]
    result["results"] = one_famous_two_others(judged)
    return result


def find_in_background(path, answers, on_done):
    """Runs find() on another thread and calls on_done(result) when it is finished.
    (In Kivy, put @mainthread on on_done so it can update the screen.)"""
    def work():
        try:
            result = find(path, answers)
        except Exception as e:
            result = {"sentence": "", "results": [], "no_match": True, "judged": False, "error": str(e)}
        on_done(result)
    threading.Thread(target=work, daemon=True).start()


def short_title(title, limit=60):
    """Long book titles cut to a readable length."""
    return title if len(title) <= limit else title[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def display_name(author):
    """The main writer's name as people say it: 'Cécile Tormay and Northumberland, Alan Ian Percy'
    -> 'Cécile Tormay' (the second is the translator); 'Goethe, Johann Wolfgang von' -> 'Johann Wolfgang
    von Goethe'; 'Victoria, Queen of Great Britain' stays as it is."""
    name = "".join(ch for ch in author if ch.isprintable()).split(" and ")[0].strip()
    if ", " in name and " of " not in name:
        last, first = name.split(", ", 1)
        words = f"{first} {last}".split()
        if len(words) > 2 and words[-1] == words[-2]:      # 'Byron, George Gordon Byron'
            words = words[:-1]
        name = " ".join(words)
    return name


def simple(r):
    """One quote box: the words, who wrote them and when they lived."""
    return {"quote": r["quote"] or r["text"], "name": display_name(r["author"]), "years": r["when"]}


def as_text(result):
    if not result["results"]:
        return "Nobody in the library has written about quite this yet. Try saying a little more about what happened."
    boxes = [simple(r) for r in result["results"]]
    return "\n\n".join(f"“{b['quote']}”\n    — {b['name']} ({b['years']})" for b in boxes)
