"""
Builds data/library.db from Project Gutenberg. Only needed once (takes about 1.5 hours).

    python -m Backend.build_library fetch     download the books (cached in data/texts)
    python -m Backend.build_library build     cut them into passages and save them

Books are chosen by the Gutenberg catalogue's own subject headings (letters, diaries,
autobiographies), not by hand.
"""
import csv
import json
import os
import re
import sqlite3
import sys
import time
import urllib.request

from Backend.library import DB_PATH, MODEL, ROOT, SENTENCE_END, encode, load_model

TEXT_DIR = os.environ.get("HUG_TEXT_DIR", os.path.join(ROOT, "data", "texts"))
BOOK_LIST = os.path.join(TEXT_DIR, "archive.json")
MIRROR = "https://gutenberg.pglaf.org/cache/epub/{id}/pg{id}.txt"   # Gutenberg asks bulk downloads to use a mirror
CATALOG = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv"

# A few books added by hand: (gutenberg id, author, title, year, kind)
EXTRA_BOOKS = [
    (2811, "Pliny the Younger", "Letters", 105, "letters"),
    (3296, "Augustine", "Confessions", 400, "memoir"),
    (9863, "Robert Burns", "Letters", 1790, "letters"),
    (35698, "John Keats", "Letters to His Family and Friends", 1819, "letters"),
    (10378, "John Stuart Mill", "Autobiography", 1873, "memoir"),
    (6408, "Anton Chekhov", "Letters to His Family and Friends", 1890, "letters"),
    (921, "Oscar Wilde", "De Profundis", 1897, "letter"),
]

LETTERS = re.compile(r"\b(correspondence|diaries|letters)\b", re.I)
MEMOIR = re.compile(r"autobiograph|memoirs? of my|my life|recollections|reminiscences", re.I)
SKIP = re.compile(r"fiction|juvenile|poetry|drama|humor|stories|sermons|letter[- ]writing|"
                  r"business|commercial|form letters|etiquette|readers", re.I)
NOT_THE_WRITER = re.compile(r"\[(editor|translator|compiler|contributor|annotator|commentator|"
                            r"illustrator|other|transcriber|introduction)[^\]]*\]", re.I)

# A passage is kept only if the writer talks about themselves ("I", "my") and about a feeling.
FEELING_WORDS = set("""
alone lonely solitude solitary forsaken forgotten abandoned grief grieve sorrow sorrows mourn weep tears wept
sad sadness melancholy miserable misery wretched unhappy despair hopeless hope fear afraid dread anxious anxiety
trouble troubled ashamed shame guilt guilty fault regret remorse envy jealous heart love loved longing miss
absent absence death die dying dead grave ill illness sick pain suffer suffering weary tired poor poverty debt
fail failure failed useless worthless lost comfort console consolation friend friendless home exile
""".split())
FIRST_PERSON = {"i", "me", "my", "myself", "mine"}


# --- choosing and downloading books ---------------------------------------------------------
def download(book_id):
    """The raw text of a book, downloaded once and then read from data/texts."""
    os.makedirs(TEXT_DIR, exist_ok=True)
    path = os.path.join(TEXT_DIR, f"{book_id}.txt")
    if not os.path.exists(path):
        with urllib.request.urlopen(MIRROR.format(id=book_id), timeout=60) as r, open(path + ".part", "wb") as f:
            f.write(r.read())
        os.replace(path + ".part", path)
    return open(path, encoding="utf-8", errors="replace").read()


def person(entry):
    """'Keats, John, 1795-1821' -> ('John Keats', 1795, 1821)."""
    entry = re.sub(r"\s*\([^)]*\)", "", entry).strip()
    m = re.search(r",\s*(\d{1,4})?\??\s*(BCE)?\s*-\s*(\d{1,4})?\??\s*(BCE)?\s*$", entry)
    born = died = None
    if m:
        entry = entry[:m.start()]
        if m.group(1):
            born = -int(m.group(1)) if m.group(2) else int(m.group(1))
        if m.group(3):
            died = -int(m.group(3)) if m.group(4) else int(m.group(3))
    parts = [p.strip() for p in entry.split(",") if p.strip()]
    if len(parts) > 1 and len(parts[1].split()) >= 3:      # 'Victoria, Queen of Great Britain'
        return f"{parts[0]}, {parts[1]}", born, died
    name = " ".join(parts[1:2] + parts[:1]) if len(parts) > 1 else (parts[0] if parts else "Unknown")
    return name, born, died


def year_text(y):
    return "?" if y is None else (f"{-y} BC" if y < 0 else str(y))


def choose_books():
    """Every English letters / diaries / autobiography book in the Gutenberg catalogue."""
    os.makedirs(TEXT_DIR, exist_ok=True)
    catalog = os.path.join(TEXT_DIR, "pg_catalog.csv")
    if not os.path.exists(catalog):
        urllib.request.urlretrieve(CATALOG, catalog)
    extra = {b[0] for b in EXTRA_BOOKS}
    books = []
    for r in csv.DictReader(open(catalog, encoding="utf-8")):
        if r["Type"] != "Text" or r["Language"] != "en" or int(r["Text#"]) in extra:
            continue
        if SKIP.search(r["Subjects"] + " " + r["Bookshelves"]):
            continue
        writers = [a for a in r["Authors"].split(";") if a.strip() and not NOT_THE_WRITER.search(a)]
        if not writers:                    # only an editor listed: we could not say who wrote each passage
            continue
        surname = writers[0].split(",")[0].strip()
        letters = bool(LETTERS.search(r["Subjects"]))
        memoir = (not letters and bool(MEMOIR.search(r["Title"] + " " + r["Subjects"]))
                  and len(surname) > 2 and surname in r["Subjects"]      # the author is the book's own subject
                  and not re.search(r"personal narratives", r["Subjects"], re.I))
        if not (letters or memoir):
            continue
        people = [person(a) for a in writers[:2]]
        born, died = people[0][1], people[0][2]
        year = died if died is not None else (born + 40 if born is not None else None)
        if year is None:
            continue
        kind = "memoir" if memoir else "diary" if re.search(r"diaries", r["Subjects"], re.I) else "letters"
        books.append([int(r["Text#"]), " and ".join(p[0] for p in people), re.sub(r"\s+", " ", r["Title"]).strip(),
                      year, kind, f"{year_text(born)}-{year_text(died)}"])
    return books


def fetch():
    books = choose_books()
    print(f"{len(books)} books chosen from the Gutenberg catalogue")
    got = []
    for n, b in enumerate(books, 1):
        new = not os.path.exists(os.path.join(TEXT_DIR, f"{b[0]}.txt"))
        try:
            download(b[0])
            got.append(b)
        except Exception as e:
            print(f"  skipped {b[0]} ({type(e).__name__})")
        if new:
            time.sleep(1)                  # be polite to the mirror
        if n % 25 == 0:
            print(f"  {n}/{len(books)}", flush=True)
            json.dump(got, open(BOOK_LIST, "w", encoding="utf-8"))
    json.dump(got, open(BOOK_LIST, "w", encoding="utf-8"))
    print(f"{len(got)} books saved in {TEXT_DIR}")


# --- cutting books into passages ------------------------------------------------------------
def clean(raw):
    """Remove the Gutenberg header and footer; one paragraph per line."""
    start = re.search(r"\*\*\* ?START OF.*?\*\*\*", raw, flags=re.S)
    end = re.search(r"\*\*\* ?END OF", raw)
    body = raw[start.end() if start else 0: end.start() if end else len(raw)]
    body = body.replace("\r\n", "\n").replace("_", "")
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", body)]
    return "\n".join(p for p in paras if p)


def is_personal(chunk):
    """The writer's own words about how they feel (not a date, a quote or an editor's note)."""
    words = re.findall(r"[a-z']+", chunk.lower())
    if re.search(r"\d{3,}|\(\d+\)", chunk):         # dates, page numbers, footnote marks
        return False
    if chunk.lstrip()[:1] in "\"'“‘«":                # starts with a quote: maybe someone else's words
        return False
    if re.search(r"\([^)]{25,}\)", chunk):           # long brackets: usually an editor's note
        return False
    return any(w in FIRST_PERSON for w in words) and any(w in FEELING_WORDS for w in words)


def passages(text, min_words=15, max_words=60):
    """(start, end) of short passages: one or a few sentences from one paragraph, 15-60 words."""
    pos = 0
    for para in text.split("\n"):
        p_start = text.index(para, pos)
        pos = p_start + len(para)
        if len(para.split()) < 8 or "[" in para or para.isupper():
            continue
        cuts = [0] + [m.end() for m in SENTENCE_END.finditer(para)] + [len(para)]
        start, words = None, 0
        for a, b in zip(cuts, cuts[1:]):
            if not para[a:b].strip():
                continue
            if start is None:
                start, words = a, 0
            words += len(para[a:b].split())
            if words >= min_words:
                chunk = para[start:b].strip()
                if words <= max_words and is_personal(chunk):
                    s = p_start + para.index(chunk, start)
                    yield s, s + len(chunk)
                start = None


def build(fresh=False):
    """Cut every downloaded book into passages and save them with their meaning vectors.
    Can be stopped and restarted: books already in the database are skipped."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if fresh and os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS sources (id INTEGER PRIMARY KEY, author TEXT, title TEXT, year INTEGER,
                                            kind TEXT, url TEXT, clean_text TEXT, dates TEXT, translator TEXT);
        CREATE TABLE IF NOT EXISTS passages (id INTEGER PRIMARY KEY, source_id INTEGER, char_start INTEGER,
                                             char_end INTEGER, text TEXT, raw_vec BLOB);
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);""")
    db.execute("INSERT OR REPLACE INTO meta VALUES ('embedder', ?)", (MODEL,))
    model = load_model()
    done = {r[0] for r in db.execute("SELECT id FROM sources")}
    seen = {re.sub(r"[^a-z]", "", r[0].lower()) for r in db.execute("SELECT text FROM passages")}
    books = [list(b) + [None] for b in EXTRA_BOOKS]
    books += json.load(open(BOOK_LIST, encoding="utf-8")) if os.path.exists(BOOK_LIST) else choose_books()
    todo = [b for b in books if b[0] not in done and os.path.exists(os.path.join(TEXT_DIR, f"{b[0]}.txt"))]
    print(f"{len(done)} books already in the database, {len(todo)} to add")
    added = 0
    for n, (book_id, author, title, year, kind, dates) in enumerate(todo, 1):
        raw = download(book_id)
        text = clean(raw)
        surname = re.split(r"[ ,]", author.split(" and ")[0].strip())[-1].lower()
        spans = []
        for a, b in passages(text):
            key = re.sub(r"[^a-z]", "", text[a:b].lower())       # same passage in two editions
            names_writer = len(surname) > 2 and re.search(rf"\b{re.escape(surname)}\b", text[a:b].lower())
            if key not in seen and not names_writer:              # naming the writer = an editor talking
                seen.add(key)
                spans.append((a, b))
        translator = re.search(r"^Translators?:\s*(.+)$", raw[:6000], re.M)
        db.execute("INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?)",
                   (book_id, author, title, year, kind, f"https://www.gutenberg.org/ebooks/{book_id}",
                    text if spans else "", dates, translator.group(1).strip() if translator else None))
        if spans:
            vectors = encode(model, [text[a:b] for a, b in spans])
            db.executemany("INSERT INTO passages (source_id, char_start, char_end, text, raw_vec) VALUES (?,?,?,?,?)",
                           [(book_id, a, b, text[a:b], v.tobytes()) for (a, b), v in zip(spans, vectors)])
            added += len(spans)
        db.commit()
        if n % 10 == 0 or n == len(todo):
            print(f"  {n}/{len(todo)} books, +{added} passages", flush=True)
    print(f"done: {db.execute('SELECT COUNT(*) FROM passages').fetchone()[0]} passages in {DB_PATH}")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "fetch":
        fetch()
    elif command == "build":
        build(fresh="--fresh" in sys.argv)
    else:
        print(__doc__)
