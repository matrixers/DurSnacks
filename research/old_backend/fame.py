"""
Famous or everyday? Each author in the library gets a fame score, worked out automatically
(no hand-labelling): the number of Wikipedia language editions with an article about them
(Wikidata "sitelinks"). Pepys or Darwin are in 100+ languages; a Wyoming homesteader or a
Boston schoolgirl of 1771 in a handful or none.

    python -m Backend.fame build     looks every author up on Wikidata (free, a few minutes, cached)
    python -m Backend.fame show      prints the list, most famous first

Saved to data/fame.json: {author: {"qid", "label", "sitelinks", "how"}}.
famous(author) is True when sitelinks >= FAMOUS_AT. Authors not found on Wikidata count as everyday.
"""
import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "library.db")
OUT = os.path.join(ROOT, "data", "fame.json")
API = "https://www.wikidata.org/w/api.php"
WIKIPEDIA = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "DeepRootedGuidance-research/0.1 (student project)"}
FAMOUS_AT = 20      # Wikipedia languages; set once from the spread printed by `show`, not per author

_CACHE = None


def _get(params, api=API):
    url = api + "?" + urllib.parse.urlencode({**params, "format": "json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise RuntimeError(f"Wikidata error {e.code}") from e
            time.sleep(int(e.headers.get("Retry-After") or 30) + 1)     # rate limited: wait as asked
        except OSError:
            time.sleep(3 + 3 * attempt)
    raise RuntimeError("Wikidata did not answer")


def person_name(author):
    """'John Adams and Abigail Adams' -> 'John Adams'; 'Acton, John Emerich Edward Dalberg Acton' -> reordered."""
    first = re.split(r"\s+and\s+|\s*;\s*", author)[0].strip()
    if "," in first:
        last, rest = first.split(",", 1)
        first = f"{rest.strip()} {last.strip()}"
    return re.sub(r"\s*\(.*?\)", "", first).strip()


def _birth_year(entity):
    for c in entity.get("claims", {}).get("P569", []):
        t = c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time", "")
        m = re.match(r"([+-]\d+)-", t)
        if m:
            return int(m.group(1))
    return None


def _is_human(entity):
    return any(c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q5"
               for c in entity.get("claims", {}).get("P31", []))


def _born(dates):
    m = re.match(r"\s*(\d+)", dates or "")
    return int(m.group(1)) if m else None


def _choose(entities, born):
    """A human with the same birth year (+-1), or the first human when no birth year is known."""
    humans = [e for e in entities if _is_human(e)]
    if born is not None:
        same = [e for e in humans if _birth_year(e) is not None and abs(_birth_year(e) - born) <= 1]
        return (same[0], "name + birth year") if same else (None, "")
    return (humans[0], "name only (no birth year to check)") if humans else (None, "")


def _result(e, how):
    if e is None:
        return {"qid": None, "label": None, "sitelinks": 0, "how": how}
    return {"qid": e["id"], "label": e.get("labels", {}).get("en", {}).get("value"),
            "sitelinks": len(e.get("sitelinks", {})), "how": how}


def _entities(qids):
    out = {}
    for i in range(0, len(qids), 50):
        out.update(_get({"action": "wbgetentities", "ids": "|".join(qids[i:i + 50]),
                         "props": "claims|sitelinks|labels", "languages": "en"}).get("entities", {}))
    return out


def name_variants(author):
    """'of Siena Catherine' -> 'Catherine of Siena'; 'Sauk chief Black Hawk' -> also 'Black Hawk'."""
    name = person_name(author)
    out = [name]
    m = re.match(r"(of \S+(?: \S+)?) (\S+)$", name)
    if m:
        out.append(f"{m.group(2)} {m.group(1)}")
    words = name.split()
    if len(words) > 2:
        out.append(" ".join(words[-2:]))
    return list(dict.fromkeys(out))


def lookup(author, dates):
    """Best Wikidata match for one author (one search per name variant)."""
    born = _born(dates)
    for name in name_variants(author):
        hits = _get({"action": "wbsearchentities", "search": name, "language": "en", "limit": 7,
                     "type": "item"}).get("search", [])
        if hits:
            ents = _entities([h["id"] for h in hits])
            e, how = _choose([ents[h["id"]] for h in hits if h["id"] in ents], born)
            if e is not None:
                return _result(e, how + ("" if name == person_name(author) else f" (as '{name}')"))
        time.sleep(1)
    return _result(None, "not found")


def _by_wikipedia_title(todo, authors):
    """Fast first pass: English Wikipedia titles in batches of 50 -> Wikidata ids -> check birth year."""
    found = {}
    for i in range(0, len(todo), 50):
        chunk = todo[i:i + 50]
        names = {a: person_name(a) for a in chunk}
        q = _get({"action": "query", "titles": "|".join(set(names.values())), "prop": "pageprops",
                  "ppprop": "wikibase_item", "redirects": 1}, api=WIKIPEDIA)["query"]
        alias = {}
        for kind in ("normalized", "redirects"):
            for x in q.get(kind, []):
                alias[x["from"]] = x["to"]
        title_qid = {p["title"]: p.get("pageprops", {}).get("wikibase_item")
                     for p in q.get("pages", {}).values()}

        def qid_of(n):
            while n in alias:
                n = alias[n]
            return title_qid.get(n)

        qids = {a: qid_of(n) for a, n in names.items()}
        ents = _entities(sorted({x for x in qids.values() if x}))
        for a, qid in qids.items():
            if qid and qid in ents:
                e, how = _choose([ents[qid]], _born(authors[a]))
                if e is not None:
                    found[a] = _result(e, how + " (Wikipedia title)")
        time.sleep(1)
    return found


def build():
    db = sqlite3.connect(DB)
    authors = {}
    for author, dates in db.execute("SELECT author, dates FROM sources"):
        authors.setdefault(author, dates)
    done = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    todo = [a for a in authors if a not in done or done[a]["qid"] is None]
    print(f"{len(authors)} authors, {len(todo)} to look up")
    done.update(_by_wikipedia_title(todo, authors))
    json.dump(done, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    rest = [a for a in todo if a not in done or done[a]["qid"] is None]
    print(f"  found by Wikipedia title: {len(todo) - len(rest)}; searching the other {len(rest)} one by one")
    for n, a in enumerate(rest, 1):
        try:
            done[a] = lookup(a, authors[a])
        except RuntimeError as e:
            print(f"  {a}: {e} (skipped, run again later)")
            continue
        if n % 10 == 0:
            json.dump(done, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            print(f"  {n}/{len(rest)}", flush=True)
        time.sleep(1)
    json.dump(done, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"wrote {OUT}")


def table():
    global _CACHE
    if _CACHE is None:
        _CACHE = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    return _CACHE


def famous(author):
    """True / False, or None when the fame list has not been built yet."""
    t = table()
    if not t:
        return None
    return t.get(author, {}).get("sitelinks", 0) >= FAMOUS_AT


def show():
    t = sorted(table().items(), key=lambda kv: -kv[1]["sitelinks"])
    for a, v in t:
        print(f"{v['sitelinks']:>4}  {'FAMOUS ' if v['sitelinks'] >= FAMOUS_AT else 'everyday'}  {a}"
              f"   [{v['label'] or '-'}; {v['how']}]")
    n_f = sum(v["sitelinks"] >= FAMOUS_AT for _, v in t)
    print(f"\n{len(t)} authors: {n_f} famous (>= {FAMOUS_AT} Wikipedia languages), {len(t) - n_f} everyday")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    {"build": build, "show": show}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
