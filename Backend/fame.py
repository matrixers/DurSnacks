"""
Is a writer well known or lesser known? We count how many languages Wikipedia has an
article about them in (from Wikidata): Darwin or Pepys are in 100+, a Wyoming homesteader
in a handful or none. 20 or more counts as well known.

    python -m Backend.fame build    looks every writer up once (free, takes a while), saves data/fame.json
    python -m Backend.fame show     prints the list, most famous first
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

from Backend.library import DB_PATH, ROOT

FAME_FILE = os.path.join(ROOT, "data", "fame.json")
WELL_KNOWN_AT = 20
WIKIDATA = "https://www.wikidata.org/w/api.php"
WIKIPEDIA = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "DeepRootedGuidance-research/0.1 (student project)"}
_fame = None


def ready():
    return bool(_table())


def famous(author):
    return _table().get(author, {}).get("sitelinks", 0) >= WELL_KNOWN_AT


def _table():
    global _fame
    if _fame is None:
        _fame = json.load(open(FAME_FILE, encoding="utf-8")) if os.path.exists(FAME_FILE) else {}
    return _fame


# --- looking writers up -------------------------------------------------------------------------
def _get(api, params):
    url = api + "?" + urllib.parse.urlencode({**params, "format": "json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise RuntimeError(f"Wikidata error {e.code}") from e
            time.sleep(int(e.headers.get("Retry-After") or 30) + 1)      # asked to slow down: wait
        except OSError:
            time.sleep(3 + 3 * attempt)
    raise RuntimeError("Wikidata did not answer")


def _names(author):
    """Names to search for: 'John Adams and Abigail Adams' -> 'John Adams';
    'of Siena Catherine' -> also 'Catherine of Siena'; 'Sauk chief Black Hawk' -> also 'Black Hawk'."""
    name = re.sub(r"\s*\(.*?\)", "", re.split(r"\s+and\s+|\s*;\s*", author)[0]).strip()
    names = []
    if "," in name:                                   # 'Sévigné, Marie de Rabutin-Chantal'
        last, first = [x.strip() for x in name.split(",", 1)]
        name = f"{first} {last}"
        names.append(first)
    words = name.split()
    if len(words) > 2 and words[-1] == words[-2]:     # 'Horatio Nelson Nelson'
        words = words[:-1]
    name = " ".join(words)
    names.insert(0, name)
    m = re.match(r"((?:of|de|von|van|du) \S+(?: \S+)?) (\S+)$", name)    # 'de Lisieux Thérèse'
    if m:
        names.append(f"{m.group(2)} {m.group(1)}")
    if len(words) > 2:
        names.append(" ".join(words[-2:]))
    return list(dict.fromkeys(names))


def _birth_year(entity):
    for claim in entity.get("claims", {}).get("P569", []):
        t = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time", "")
        m = re.match(r"([+-]\d+)-", t)
        if m:
            return int(m.group(1))
    return None


def _is_person(entity):
    return any(c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q5"
               for c in entity.get("claims", {}).get("P31", []))


def _pick(entities, born):
    """A person born in the same year (give or take one), or any person if we don't know the year."""
    people = [e for e in entities if _is_person(e)]
    if born is None:
        return people[0] if people else None
    return next((e for e in people if _birth_year(e) is not None and abs(_birth_year(e) - born) <= 1), None)


def _entities(ids):
    found = {}
    for i in range(0, len(ids), 50):
        found.update(_get(WIKIDATA, {"action": "wbgetentities", "ids": "|".join(ids[i:i + 50]),
                                     "props": "claims|sitelinks|labels", "languages": "en"}).get("entities", {}))
    return found


def _entry(entity):
    if entity is None:
        return {"qid": None, "label": None, "sitelinks": 0}
    return {"qid": entity["id"], "label": entity.get("labels", {}).get("en", {}).get("value"),
            "sitelinks": len(entity.get("sitelinks", {}))}


def _born(dates):
    m = re.match(r"\s*(\d+)( BC)?", dates or "")      # '107 BC-44 BC' -> -107
    return None if not m else -int(m.group(1)) if m.group(2) else int(m.group(1))


def _by_wikipedia_title(authors):
    """Quick first pass: look up 50 names at a time as English Wikipedia page titles."""
    found = {}
    names = list(authors)
    for i in range(0, len(names), 50):
        chunk = {a: _names(a)[0] for a in names[i:i + 50]}
        q = _get(WIKIPEDIA, {"action": "query", "titles": "|".join(set(chunk.values())), "prop": "pageprops",
                             "ppprop": "wikibase_item", "redirects": 1})["query"]
        renamed = {x["from"]: x["to"] for kind in ("normalized", "redirects") for x in q.get(kind, [])}
        page_id = {p["title"]: p.get("pageprops", {}).get("wikibase_item") for p in q.get("pages", {}).values()}

        def wikidata_id(title):
            while title in renamed:
                title = renamed[title]
            return page_id.get(title)

        ids = {a: wikidata_id(t) for a, t in chunk.items()}
        entities = _entities(sorted({x for x in ids.values() if x}))
        for a, qid in ids.items():
            if qid in entities and _pick([entities[qid]], _born(authors[a])) is not None:
                found[a] = _entry(entities[qid])
        time.sleep(1)
    return found


def _by_search(author, dates):
    """Slower second pass: search Wikidata for the name."""
    for name in _names(author):
        hits = _get(WIKIDATA, {"action": "wbsearchentities", "search": name, "language": "en", "limit": 7,
                               "type": "item"}).get("search", [])
        if hits:
            entities = _entities([h["id"] for h in hits])
            entity = _pick([entities[h["id"]] for h in hits if h["id"] in entities], _born(dates))
            if entity is not None:
                return _entry(entity)
        time.sleep(1)
    return _entry(None)


def build():
    authors = {}
    for author, dates in sqlite3.connect(DB_PATH).execute("SELECT author, dates FROM sources"):
        authors.setdefault(author, dates)
    table = dict(_table())
    todo = {a: d for a, d in authors.items() if not table.get(a, {}).get("qid")}
    print(f"{len(authors)} writers, {len(todo)} to look up")
    table.update(_by_wikipedia_title(todo))
    rest = [a for a in todo if not table.get(a, {}).get("qid")]
    print(f"  {len(todo) - len(rest)} found by page title; searching for the other {len(rest)}")
    for n, a in enumerate(rest, 1):
        try:
            table[a] = _by_search(a, authors[a])
        except RuntimeError as e:
            print(f"  {a}: {e} (run again later)")
        if n % 10 == 0:
            json.dump(table, open(FAME_FILE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            print(f"  {n}/{len(rest)}", flush=True)
        time.sleep(1)
    json.dump(table, open(FAME_FILE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"saved {FAME_FILE}")


def show():
    table = sorted(_table().items(), key=lambda kv: -kv[1]["sitelinks"])
    for author, v in table:
        print(f"{v['sitelinks']:>4}  {'well known  ' if v['sitelinks'] >= WELL_KNOWN_AT else 'lesser known'}  "
              f"{author}   [{v['label'] or 'not found'}]")
    n = sum(v["sitelinks"] >= WELL_KNOWN_AT for _, v in table)
    print(f"\n{len(table)} writers: {n} well known, {len(table) - n} lesser known")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    {"build": build, "show": show}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
