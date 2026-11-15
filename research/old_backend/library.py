"""
The passage library: public-domain letters and diaries from Project Gutenberg.

    python -m Backend.library fetch [N]   # download the archive books (cached, polite, resumable)
    python -m Backend.library build       # extract passages + embed; resumes, adds new books only
    python -m Backend.library build --fresh

Every passage is a character span of its cleaned source text, so anything shown
to a user can be checked word for word with verify().

Ported from the earlier prototype (Testing/hug.py). Books are chosen by the
Gutenberg catalogue's own subject headings, not by us.
"""
import csv
import json
import os

# Quiet the Hugging Face "unauthenticated requests" notice: the embedding model is public and cached.
os.environ.setdefault("HF_HUB_VERBOSITY", "error")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
import re
import sqlite3
import sys
import time
import urllib.request

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DB_PATH = os.environ.get("HUG_DB", os.path.join(DATA, "library.db"))
TEXT_DIR = os.environ.get("HUG_TEXT_DIR", os.path.join(DATA, "texts"))

# --------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------
# A few hand-picked personal books with a known year of writing (gid, author, title, year, kind).
# Philosophy and advice (Epictetus, Marcus Aurelius, Boethius, Pascal) are left out on purpose:
# they are not someone's own experience; they belong in a later "advice" collection.
SOURCES = [
    (2811, "Pliny the Younger", "Letters", 105, "letters"),
    (3296, "Augustine", "Confessions", 400, "memoir"),
    (9863, "Robert Burns", "Letters", 1790, "letters"),
    (35698, "John Keats", "Letters to His Family and Friends", 1819, "letters"),
    (10378, "John Stuart Mill", "Autobiography", 1873, "memoir"),
    (6408, "Anton Chekhov", "Letters to His Family and Friends", 1890, "letters"),
    (921, "Oscar Wilde", "De Profundis", 1897, "letter"),
]

MIRROR = "https://gutenberg.pglaf.org/cache/epub/{gid}/pg{gid}.txt"   # PG asks bulk users to use a mirror
CATALOG_URL = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv"
ARCHIVE_PATH = os.path.join(TEXT_DIR, "archive.json")
ARCHIVE_WANT = re.compile(r"\b(correspondence|diaries|letters)\b", re.I)
MEMOIR_WANT = re.compile(r"autobiograph|memoirs? of my|my life|recollections|reminiscences", re.I)
ARCHIVE_SKIP = re.compile(r"fiction|juvenile|poetry|drama|humor|stories|sermons|letter[- ]writing|"
                          r"business|commercial|form letters|etiquette|readers", re.I)
ROLE = re.compile(r"\[(editor|translator|compiler|contributor|annotator|commentator|"
                  r"illustrator|other|transcriber|introduction)[^\]]*\]", re.I)


def fetch_text(gid, timeout=60):
    """Return the raw book text, downloading once and caching in TEXT_DIR."""
    os.makedirs(TEXT_DIR, exist_ok=True)
    path = os.path.join(TEXT_DIR, f"{gid}.txt")
    if not os.path.exists(path):
        url = MIRROR.format(gid=gid)
        with urllib.request.urlopen(url, timeout=timeout) as r, open(path + ".part", "wb") as f:
            f.write(r.read())
        os.replace(path + ".part", path)
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def _person(entry):
    """'Keats, John, 1795-1821' -> ('John Keats', 1795, 1821). Dates may be missing or BCE."""
    entry = re.sub(r"\s*\([^)]*\)", "", entry).strip()
    m = re.search(r",\s*(\d{1,4})?\??\s*(BCE)?\s*-\s*(\d{1,4})?\??\s*(BCE)?\s*$", entry)
    birth = death = None
    if m:
        entry = entry[:m.start()]
        if m.group(1):
            birth = -int(m.group(1)) if m.group(2) else int(m.group(1))
        if m.group(3):
            death = -int(m.group(3)) if m.group(4) else int(m.group(3))
    parts = [p.strip() for p in entry.split(",") if p.strip()]
    if len(parts) > 1 and len(parts[1].split()) >= 3:      # 'Victoria, Queen of Great Britain'
        return f"{parts[0]}, {parts[1]}", birth, death
    name = " ".join(parts[1:2] + parts[:1]) if len(parts) > 1 else (parts[0] if parts else "Unknown")
    return name, birth, death


def _fmt_year(y):
    return f"{-y} BC" if y < 0 else str(y)


def select_archive():
    """Every English letters/diaries book in the PG catalogue, by its subject headings."""
    os.makedirs(TEXT_DIR, exist_ok=True)
    cat = os.path.join(TEXT_DIR, "pg_catalog.csv")
    if not os.path.exists(cat):
        print(f"  downloading {CATALOG_URL}")
        urllib.request.urlretrieve(CATALOG_URL, cat)
    hand = {s[0] for s in SOURCES}
    books = []
    for r in csv.DictReader(open(cat, encoding="utf-8")):
        if r["Type"] != "Text" or r["Language"] != "en" or int(r["Text#"]) in hand:
            continue
        if ARCHIVE_SKIP.search(r["Subjects"] + " " + r["Bookshelves"]):
            continue
        writers = [a for a in r["Authors"].split(";") if a.strip() and not ROLE.search(a)]
        if not writers:            # editor-only anthologies: we could not say who wrote a passage
            continue
        surname = writers[0].split(",")[0].strip()
        letters = bool(ARCHIVE_WANT.search(r["Subjects"]))
        # memoirs: the catalogue must list the author as the book's own subject (an autobiography)
        memoir = (not letters and bool(MEMOIR_WANT.search(r["Title"] + " " + r["Subjects"]))
                  and len(surname) > 2 and surname in r["Subjects"]
                  and not re.search(r"personal narratives", r["Subjects"], re.I))
        if not (letters or memoir):
            continue
        people = [_person(a) for a in writers[:2]]
        author = " and ".join(p[0] for p in people)
        birth, death = people[0][1], people[0][2]
        year = death if death is not None else (birth + 40 if birth is not None else None)
        if year is None:           # no date at all: we could not place it in time
            continue
        dates = (f"{_fmt_year(birth) if birth is not None else '?'}-"
                 f"{_fmt_year(death) if death is not None else '?'}")
        kind = ("memoir" if memoir else
                "diary" if re.search(r"diaries", r["Subjects"], re.I) else "letters")
        title = re.sub(r"\s+", " ", r["Title"]).strip()
        books.append([int(r["Text#"]), author, title, year, kind, dates])
    return books


def fetch_archive(max_books=None, delay=1.0):
    """Download the archive books (cached), one at a time with a pause, and record the list."""
    books = select_archive()[:max_books] if max_books else select_archive()
    print(f"archive: {len(books)} letters/diaries books selected from the PG catalogue", flush=True)
    ok = []
    for n, b in enumerate(books, 1):
        have = os.path.exists(os.path.join(TEXT_DIR, f"{b[0]}.txt"))
        try:
            fetch_text(b[0])
            ok.append(b)
        except Exception as e:
            print(f"  skip {b[0]} ({type(e).__name__})", flush=True)
        if not have:
            time.sleep(delay)
        if n % 25 == 0:
            print(f"  {n}/{len(books)}", flush=True)
            _write_archive(ok)
    _write_archive(ok)
    print(f"archive: {len(ok)} books cached in {TEXT_DIR}", flush=True)


def _write_archive(books):
    with open(ARCHIVE_PATH, "w", encoding="utf-8") as f:
        json.dump(books, f)


def cached_archive():
    """Archive books whose text is already on disk."""
    if os.path.exists(ARCHIVE_PATH):
        books = json.load(open(ARCHIVE_PATH, encoding="utf-8"))
    else:
        books = select_archive()
    return [b for b in books if os.path.exists(os.path.join(TEXT_DIR, f"{b[0]}.txt"))]


# --------------------------------------------------------------------------
# Cleaning and passage extraction
# --------------------------------------------------------------------------
AFFECT = set("""
alone lonely solitude solitary forsaken forgotten abandoned grief grieve sorrow
sorrows mourn weep tears wept sad sadness melancholy miserable misery wretched
unhappy despair hopeless hope fear afraid dread anxious anxiety trouble troubled
ashamed shame guilt guilty fault regret remorse envy jealous heart love loved
longing miss absent absence death die dying dead grave ill illness sick pain
suffer suffering weary tired poor poverty debt fail failure failed useless
worthless lost comfort console consolation friend friendless home exile
""".split())
FIRST_PERSON = {"i", "me", "my", "myself", "mine"}
# Do not split after titles or initials ("Mr. Smith", "Sir W. Pen"). Each lookbehind includes the
# dot: the earlier prototype's guard omitted it and never fired.
ABBREV = "".join(rf"(?<!\b{a}\.)" for a in (
    "Mr", "Mrs", "Dr", "St", "MS", "No", "vol", "Esq", "Rev", "Col", "Capt", "Gen", "Lieut", "Prof",
    "Hon", "Messrs", "Mme", "Mlle", "Sr", "Jr", "viz", "Gov", "Sen", "Ld", "Bp")) + r"(?<!\b[A-Z]\.)"
SENT_SPLIT = re.compile(ABBREV + r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z])")


def clean(raw):
    """Strip the Gutenberg header/footer and normalise whitespace (one paragraph per line)."""
    start = re.search(r"\*\*\* ?START OF.*?\*\*\*", raw, flags=re.S)
    end = re.search(r"\*\*\* ?END OF", raw)
    body = raw[start.end() if start else 0: end.start() if end else len(raw)]
    body = body.replace("\r\n", "\n").replace("_", "")
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", body)]
    return "\n".join(p for p in paras if p)


QUOTES = "\"'“‘«"


def keep(chunk):
    """Rule-based pre-filter (not labelling): the writer's own words, first person,
    mentioning an inner state; no editor notes or quoted letters from someone else."""
    words = re.findall(r"[a-z']+", chunk.lower())
    if re.search(r"\d{3,}|\(\d+\)", chunk):      # dates, page numbers, footnote marks
        return False
    if chunk.lstrip()[:1] in QUOTES:              # opens with a quotation: maybe someone else's words
        return False
    if re.search(r"\([^)]{25,}\)", chunk):        # long parenthetical: usually an editor's note
        return False
    return any(w in FIRST_PERSON for w in words) and any(w in AFFECT for w in words)


def dedupe_key(text):
    """The same passage in two editions differs only in punctuation, quotes or spacing."""
    return re.sub(r"[^a-z]", "", text.lower())


def translator_of(raw):
    """The book's own header line 'Translator: ...', if there is one."""
    m = re.search(r"^Translators?:\s*(.+)$", raw[:6000], re.M)
    return m.group(1).strip() if m else None


def extract_passages(text, min_words=15, max_words=60):
    """Yield (start, end) spans of short units: one sentence, or a few short consecutive
    sentences, from one paragraph (15-60 words). Units do not overlap; the sentences
    around a unit are shown as context, not indexed with it."""
    pos = 0
    for para in text.split("\n"):
        p_start = text.index(para, pos)
        pos = p_start + len(para)
        if len(para.split()) < 8 or "[" in para or para.isupper():
            continue
        cuts = [0] + [m.end() for m in SENT_SPLIT.finditer(para)] + [len(para)]
        spans = [(a, b) for a, b in zip(cuts, cuts[1:]) if para[a:b].strip()]
        cur_a, cur_words = None, 0
        for a, b in spans:
            if cur_a is None:
                cur_a, cur_words = a, 0
            cur_words += len(para[a:b].split())
            if cur_words >= min_words:
                chunk = para[cur_a:b].strip()
                if cur_words <= max_words and keep(chunk):
                    s = p_start + para.index(chunk, cur_a)
                    yield s, s + len(chunk)
                cur_a = None


# --------------------------------------------------------------------------
# Context: the sentences around a passage, sliced from the same source
# --------------------------------------------------------------------------
def _para_bounds(src, i):
    a = src.rfind("\n", 0, i) + 1
    b = src.find("\n", i)
    return a, len(src) if b < 0 else b


def _sentence_spans(src, a, b):
    para = src[a:b]
    cuts = [0] + [m.end() for m in SENT_SPLIT.finditer(para)] + [len(para)]
    out = []
    for x, y in zip(cuts, cuts[1:]):
        seg = para[x:y]
        if seg.strip():
            lead = len(seg) - len(seg.lstrip())
            out.append((a + x + lead, a + x + len(seg.rstrip())))
    return out


def _prose(para):
    return len(para.split()) >= 4 and not para.isupper() and "[" not in para


def context_span(src, a, b, n=2):
    """Widen src[a:b] by up to n sentences each side, crossing into a neighbouring
    paragraph only when it is prose (so context stays inside one letter)."""
    pa, pb = _para_bounds(src, a)
    before = [s for s in _sentence_spans(src, pa, pb) if s[1] <= a]
    qa = pa
    while len(before) < n and qa > 0:
        qa, qb = _para_bounds(src, qa - 2)
        if not _prose(src[qa:qb]):
            break
        before = _sentence_spans(src, qa, qb) + before
    pa, pb = _para_bounds(src, b - 1)
    after = [s for s in _sentence_spans(src, pa, pb) if s[0] >= b]
    qb = pb
    while len(after) < n and qb < len(src):
        qa, qb = _para_bounds(src, qb + 1)
        if not _prose(src[qa:qb]):
            break
        after += _sentence_spans(src, qa, qb)
    before, after = before[-n:], after[:n]
    return (before[0][0] if before else a), (after[-1][1] if after else b)


def words_before(src, a, n_words=300):
    """Up to n_words of source text before offset a (for card extraction later)."""
    start = max(0, a - n_words * 8)
    chunk = src[start:a]
    words = chunk.split()
    return " ".join(words[-n_words:])


# --------------------------------------------------------------------------
# Embeddings and the concern profile
# --------------------------------------------------------------------------
# The fundamental emotions come from the team's wheel (wheel.json: core -> specific -> tags).
# Each tag gets a few plain sentences (no period detail) so passages can be scored for how
# strongly they express it. The tags are the wheel's; the sentences are hand-written input.
WHEEL_PATH = os.path.join(ROOT, "wheel.json")
TAG_ANCHORS = {
    "loneliness": ["I am alone and have no one to talk to.", "I feel cut off from everyone around me.",
                   "Nobody here really knows me."],
    "homesickness": ["I am far from home and long to go back.", "I miss my family and the place I come from.",
                     "Everything here is strange and I ache for what is familiar."],
    "grief": ["Someone I loved has died and I cannot bear it.", "I mourn the one I have lost.",
              "Since the death I cannot stop weeping."],
    "heartbreak": ["The one I love does not love me back.", "We have parted and I cannot stop thinking about them.",
                   "My love was rejected and my heart is broken."],
    "not_belonging": ["I do not fit in with the people around me.", "Everyone else belongs here except me.",
                      "I am always on the outside of things."],
    "anxiety": ["I am anxious about what is going to happen.", "Worry keeps me awake at night.",
                "I dread what tomorrow will bring."],
    "overwhelm": ["There is far too much for me to do and I cannot cope.", "Everything is crowding in on me at once.",
                  "I am overwhelmed and do not know where to begin."],
    "uncertainty": ["I do not know what to do next with my life.", "I cannot decide which way to turn.",
                    "My future is unclear and it unsettles me."],
    "pressure": ["Everyone expects so much of me.", "I am under great pressure to succeed.",
                 "If I fail now, everything will be lost."],
    "anger": ["I am furious and cannot calm myself.", "What they did makes my blood boil.",
              "I am so angry I can hardly write."],
    "injustice": ["I have been treated unfairly.", "It is unjust and nobody will put it right.",
                  "They blamed me for what I did not do."],
    "rejection": ["They turned me away.", "I was not wanted.", "My offer was refused and I feel cast aside."],
    "imposter_feeling": ["I feel like a fraud and they will find me out.",
                         "I do not deserve the place I have been given.",
                         "Everyone thinks I am able, but I am only pretending."],
    "failure": ["I have failed at what I set out to do.", "All my efforts have come to nothing.",
                "I have made a mess of everything."],
    "self_doubt": ["I doubt that I am good enough.", "I have no confidence in my own abilities.",
                   "I fear I have no talent at all."],
    "shame": ["I am ashamed of what happened.", "I cannot show my face after this.",
              "I have been humiliated in front of everyone."],
    "feeling_unseen": ["Nobody notices me or what I do.", "My work goes unrecognised.",
                       "I feel invisible to the people around me."],
    "burnout": ["I am worn out and have nothing left to give.", "I am exhausted by work that never ends.",
                "I am too tired to go on as I have been."],
    "stuck": ["I am stuck where I am and nothing changes.", "Every day is the same and I cannot get out.",
              "I feel trapped in my situation."],
    "restlessness": ["I cannot settle to anything.", "I long to be somewhere else, doing something else.",
                     "I am restless and dissatisfied with everything."],
    "regret": ["I wish I had acted differently.", "I regret what I did and cannot undo it.",
               "If only I could go back and choose again."],
}


def load_wheel(path=WHEEL_PATH):
    """wheel.json -> list of cores: {id, label, plain, specifics: [{label, tags}]}.
    Only the labels and tags are used (no scoring, intensity or routing rules)."""
    data = json.load(open(path, encoding="utf-8"))
    return [{"id": c.get("id"), "label": c["label"], "plain": c.get("plain", ""),
             "specifics": [{"label": s["label"], "deeper": s.get("deeper"), "tags": s.get("tags", [])}
                           for s in c.get("specifics", [])]}
            for c in data["cores"]]


def wheel_tags(path=WHEEL_PATH):
    """Every tag the wheel uses, in wheel order. Fails loudly if a tag has no anchor sentences."""
    tags = []
    for c in load_wheel(path):
        for s in c["specifics"]:
            tags += [t for t in s["tags"] if t not in tags]
    missing = [t for t in tags if t not in TAG_ANCHORS]
    assert not missing, f"wheel tags without anchor sentences: {missing}"
    return tags


def normalise(m):
    n = np.linalg.norm(m, axis=-1, keepdims=True)
    return m / np.where(n == 0, 1, n)


class Embedder:
    """encode(list[str]) -> L2-normalised float32 matrix (sentence-transformers)."""

    def __init__(self, name=None):
        from sentence_transformers import SentenceTransformer
        self.name = name or os.environ.get("HUG_MODEL", "all-mpnet-base-v2")
        self.model = SentenceTransformer(self.name)

    def encode(self, texts):
        v = self.model.encode(list(texts), normalize_embeddings=True, batch_size=64,
                              show_progress_bar=False)
        return np.asarray(v, dtype=np.float32)


class Engine:
    """raw  : centred passage embeddings (what the text is about)
    prof : similarity to each anchor concern, standardised over the library
    score: w * cos(profiles) + (1 - w) * cos(raw)"""

    def __init__(self, embedder, raw_lib, anchor_names=None, anchor_sents=None):
        anchor_names = anchor_names or wheel_tags()
        anchor_sents = anchor_sents or [TAG_ANCHORS[n] for n in anchor_names]
        self.emb, self.names = embedder, anchor_names
        self.mean = raw_lib.mean(0, keepdims=True)          # the "sounds old" direction
        self.raw = normalise(raw_lib - self.mean)
        self.anchors = normalise(np.stack([
            normalise(embedder.encode(s) - self.mean).mean(0) for s in anchor_sents]))
        sims = self.raw @ self.anchors.T
        self.mu, self.sd = sims.mean(0), sims.std(0) + 1e-6
        self.z = (sims - self.mu) / self.sd                 # how strongly each passage expresses each emotion
        self.prof = normalise(self.z)

    def embed(self, texts):
        raw = normalise(self.emb.encode(texts) - self.mean)
        prof = normalise((raw @ self.anchors.T - self.mu) / self.sd)
        return raw, prof

    def scores(self, text, w=0.6, tags=None, tag_weight=0.5):
        """Score every passage against `text`. If the user chose wheel emotions (`tags`),
        their anchor meaning is added to the query, so the chosen emotion pulls too."""
        raw, prof = self.embed([text])
        q = raw[0]
        idx = [self.names.index(t) for t in (tags or []) if t in self.names]
        if idx:
            q = normalise(q + tag_weight * self.anchors[idx].mean(0))
            prof = normalise((q @ self.anchors.T - self.mu) / self.sd)[None, :]
        return w * (self.prof @ prof[0]) + (1 - w) * (self.raw @ q), prof[0]

    def concerns(self, prof, k=3):
        order = np.argsort(prof)[::-1][:k]
        return [(self.names[i], float(prof[i])) for i in order]


# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (id INTEGER PRIMARY KEY, author TEXT, title TEXT, year INTEGER,
                      kind TEXT, url TEXT, clean_text TEXT, dates TEXT, translator TEXT);
CREATE TABLE IF NOT EXISTS passages (id INTEGER PRIMARY KEY, source_id INTEGER REFERENCES sources(id),
                       char_start INTEGER, char_end INTEGER, text TEXT, raw_vec BLOB);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""


def build(fresh=False):
    """Extract and embed every cached book not yet in the database. Resumable."""
    os.makedirs(DATA, exist_ok=True)
    if fresh and os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA)
    emb = Embedder()
    row = db.execute("SELECT value FROM meta WHERE key='embedder'").fetchone()
    if row and row[0] != emb.name:
        sys.exit(f"database was built with {row[0]}; run build --fresh")
    db.execute("INSERT OR REPLACE INTO meta VALUES ('embedder', ?)", (emb.name,))
    done = {r[0] for r in db.execute("SELECT id FROM sources")}
    seen = {dedupe_key(r[0]) for r in db.execute("SELECT text FROM passages")}
    books = [list(s) + [None] for s in SOURCES] + cached_archive()
    todo = [b for b in books if b[0] not in done]
    print(f"build: {len(done)} sources already in the database, {len(todo)} to add", flush=True)
    t0, added = time.time(), 0
    for n, (gid, author, title, year, kind, dates) in enumerate(todo, 1):
        try:
            raw = fetch_text(gid)
        except Exception as e:
            print(f"  skip {gid} ({type(e).__name__})", flush=True)
            continue
        text = clean(raw)
        # the writer's surname inside a passage usually means an editor is talking about them
        surname = re.split(r"[ ,]", author.split(" and ")[0].strip())[-1].lower()
        spans = []
        for a, b in extract_passages(text):
            key = dedupe_key(text[a:b])
            if key in seen or (len(surname) > 2 and re.search(rf"\b{re.escape(surname)}\b", text[a:b].lower())):
                continue
            seen.add(key)
            spans.append((a, b))
        # a book with nothing new (e.g. a duplicate edition) is still recorded, so it is not retried
        db.execute("INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?)",
                   (gid, author, title, year, kind, f"https://www.gutenberg.org/ebooks/{gid}",
                    text if spans else "", dates, translator_of(raw)))
        if spans:
            vecs = emb.encode([text[a:b] for a, b in spans])
            db.executemany("INSERT INTO passages (source_id, char_start, char_end, text, raw_vec) "
                           "VALUES (?,?,?,?,?)",
                           [(gid, a, b, text[a:b], v.tobytes()) for (a, b), v in zip(spans, vecs)])
            added += len(spans)
        db.commit()
        if n % 10 == 0 or n == len(todo):
            print(f"  {n}/{len(todo)} books, +{added} passages, {(time.time() - t0) / 60:.0f} min",
                  flush=True)
    total = db.execute("SELECT COUNT(*) FROM passages").fetchone()[0]
    n_src = db.execute("SELECT COUNT(*) FROM sources WHERE clean_text != ''").fetchone()[0]
    print(f"built {DB_PATH}: {n_src} sources, {total} passages, embedder {emb.name}", flush=True)


class Library:
    """The loaded library: rows, source texts, and the matching engine."""

    def __init__(self, embedder=None):
        if not os.path.exists(DB_PATH):
            sys.exit(f"no library at {DB_PATH}; run: python -m Backend.library build")
        self.db = sqlite3.connect(DB_PATH, check_same_thread=False)
        rows = self.db.execute("""SELECT p.id, p.text, p.raw_vec, s.author, s.title, s.year, s.url,
                                         p.source_id, p.char_start, p.char_end, s.dates, s.translator,
                                         s.kind
                                  FROM passages p JOIN sources s ON s.id = p.source_id
                                  ORDER BY p.id""").fetchall()
        self.rows = [dict(id=r[0], text=r[1], author=r[3], title=r[4], year=r[5], url=r[6],
                          source_id=r[7], start=r[8], end=r[9], dates=r[10], translator=r[11],
                          kind=r[12]) for r in rows]
        raw = np.stack([np.frombuffer(r[2], dtype=np.float32) for r in rows])
        self.emb = embedder or Embedder()
        built = self.db.execute("SELECT value FROM meta WHERE key='embedder'").fetchone()[0]
        assert built == self.emb.name, "library was built with a different embedder; rebuild"
        self.engine = Engine(self.emb, raw)
        self._src = {}

    def source_text(self, sid):
        if sid not in self._src:
            self._src[sid] = self.db.execute("SELECT clean_text FROM sources WHERE id=?",
                                             (sid,)).fetchone()[0]
        return self._src[sid]

    def verify(self, row):
        """Every word shown must exist in the source at the stored offsets."""
        return self.source_text(row["source_id"])[row["start"]:row["end"]] == row["text"]

    def context(self, row, n=2):
        """Up to n sentences either side, verbatim. Stops at a neighbouring paragraph that names the
        writer (an editor talking about them, not their own words)."""
        src = self.source_text(row["source_id"])
        ca, cb = context_span(src, row["start"], row["end"], n)
        before, after = src[ca:row["start"]], src[row["end"]:cb]
        surname = re.split(r"[ ,]", row["author"].split(" and ")[0].strip())[-1].lower()
        if len(surname) > 2:
            named = re.compile(rf"\b{re.escape(surname)}\b", re.I)
            lines = after.split("\n")
            keep = [lines[0]]
            for ln in lines[1:]:
                if named.search(ln):
                    break
                keep.append(ln)
            after = "\n".join(keep)
            lines = before.split("\n")
            keep = [lines[-1]]
            for ln in reversed(lines[:-1]):
                if named.search(ln):
                    break
                keep.insert(0, ln)
            before = "\n".join(keep)
        return before.strip(), after.strip()

    def when(self, row):
        if row["dates"]:
            return row["dates"].replace("-", "–")
        y = row["year"]
        return f"c. {y}" if y < 1500 else str(y)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "fetch":
        fetch_archive(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    elif cmd == "build":
        build(fresh="--fresh" in sys.argv)
    else:
        print(__doc__)
