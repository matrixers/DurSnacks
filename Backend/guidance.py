# Words of guidance: short passages from philosophy and wisdom books (Marcus Aurelius, Seneca,
# Epictetus, Boethius, Montaigne, Emerson, ...), kept apart from the letters and diaries.
# The letters show someone who went through the same thing; these give advice about it.
#
#     python -m Backend.guidance build            download the books and save data/guidance.db (once)
#     python -m Backend.guidance try "sentence"   the closest passages for a sentence
import os
import re
import sqlite3
import sys
import urllib.request

import numpy as np

from Backend.library import ROOT, SENTENCE_END, encode, load_model, normalise

DB_PATH = os.path.join(ROOT, "data", "guidance.db")
TEXT_DIR = os.path.join(ROOT, "data", "guidance_texts")
MIRROR = "https://gutenberg.pglaf.org/cache/epub/{id}/pg{id}.txt"

# (Gutenberg id, writer, years, book, where the writer's own text starts, where it stops)
# A marker is the exact text of a heading; "~" in front means "starts with". Everything before the
# start (the translator's introduction) and from the stop on (notes, index) is left out.
BOOKS = [
    (2680, "Marcus Aurelius", "121–180", "Meditations", "THE FIRST BOOK", "APPENDIX@last"),
    (10661, "Epictetus", "c. 50–135", "Discourses", "~A SELECTION FROM THE DISCOURSES", None),
    (56075, "Seneca", "c. 4 BC–65", "Of a Happy Life", "SENECA OF BENEFITS.", None),
    (64576, "Seneca", "c. 4 BC–65", "Dialogues", "OF ANGER.", "THE END."),
    (14328, "Boethius", "c. 480–524", "The Consolation of Philosophy", "THE SORROWS OF BOETHIUS.@last", "EPILOGUE."),
    (2808, "Cicero", "106–43 BC", "On Friendship and Old Age", "ON FRIENDSHIP", None),
    (1653, "Thomas à Kempis", "1380–1471", "The Imitation of Christ", "THE IMITATION OF CHRIST", None),
    (18269, "Blaise Pascal", "1623–1662", "Pensées", "SECTION I", "APPENDIX: POLEMICAL FRAGMENTS"),
    (2944, "Ralph Waldo Emerson", "1803–1882", "Essays", "HISTORY", None),
    (2945, "Ralph Waldo Emerson", "1803–1882", "Essays", "I. THE POET.", None),
    (205, "Henry David Thoreau", "1817–1862", "Walden", "WALDEN@last", "THE END"),
    (3330, "Confucius", "551–479 BC", "The Analects", "~CONFUCIAN ANALECTS", None),
    (216, "Laozi", "6th century BC", "Tao Te Ching", "THE TAO AND ITS CHARACTERISTICS", None),
    (2017, "The Dhammapada", "c. 3rd century BC", "Dhammapada", "DHAMMAPADA", None),
    (10715, "Arthur Schopenhauer", "1788–1860", "Counsels and Maxims", "~GENERAL RULES", None),
    (10741, "Arthur Schopenhauer", "1788–1860", "The Wisdom of Life", "THE WISDOM OF LIFE.@last", None),
    (58585, "Kahlil Gibran", "1883–1931", "The Prophet", "THE PROPHET@last", None),
    (575, "Francis Bacon", "1561–1626", "Essays", "Of Truth", "~A Glossary"),
    (3600, "Michel de Montaigne", "1533–1592", "Essays", "~THE AUTHOR TO THE READER", None),
]
# sections inside the text that are not the writer's own words
NOT_THE_WRITER = re.compile(r"^(FOOTNOTES|NOTES?\b|SUMMARY|ETEXT EDITOR|CONTENTS)", re.I)
NUMBERING = re.compile(r"^(?:(?:CHAPTER|CHAP\.|Ch\.)\s+[IVXLC\d]+\.\s+)?(?:(?:\d+|[IVXLC]{2,})\.\s+)?")


def download(book_id):
    os.makedirs(TEXT_DIR, exist_ok=True)
    path = os.path.join(TEXT_DIR, f"{book_id}.txt")
    if not os.path.exists(path):
        with urllib.request.urlopen(MIRROR.format(id=book_id), timeout=60) as r:
            open(path, "wb").write(r.read())
    return open(path, encoding="utf-8", errors="replace").read()


def _find(paras, marker, after):
    """Where a heading is: '~' in front = starts with, '@last' at the end = its last appearance
    (the first one is in the table of contents)."""
    last = marker.endswith("@last")
    marker = marker.removesuffix("@last")
    hits = [i for i, p in enumerate(paras) if i >= after and
            (p.startswith(marker[1:]) if marker.startswith("~") else p == marker)]
    return (hits[-1] if last else hits[0]) if hits else None


def _heading(para):
    letters = [c for c in para if c.isalpha()]
    return len(para.split()) <= 8 and len(letters) > 3 and sum(c.isupper() for c in letters) >= 0.6 * len(letters)


def writer_text(raw, start, stop):
    """The cleaned book, with only the writer's own part kept (other paragraphs become blank lines,
    so every passage still sits at its true place in the cleaned text)."""
    from Backend.build_library import clean
    paras = clean(raw).split("\n")
    a = _find(paras, start, 0) if start else 0
    b = _find(paras, stop, a + 1) if stop else None
    b = len(paras) if b is None else b
    keep, skipping = [], False
    for i, p in enumerate(paras):
        if _heading(p):
            skipping = bool(NOT_THE_WRITER.match(p))
        keep.append(p if a < i < b and not skipping else "")
    return "\n".join(keep)


def is_wisdom(chunk):
    return (not re.search(r"\d|CHAP", chunk) and chunk.lstrip()[:1] not in "\"'“‘«(" and "[" not in chunk
            and not re.search(r"\([^)]{25,}\)", chunk))


def passages(text, min_words=15, max_words=60):
    pos = 0
    for para in text.split("\n"):
        p_start = text.index(para, pos) if para else pos
        pos = p_start + len(para) + 1
        if len(para.split()) < 8 or para.isupper():
            continue
        skip = NUMBERING.match(para).end()
        body = para[skip:]
        cuts = [0] + [m.end() for m in SENTENCE_END.finditer(body)] + [len(body)]
        start, words = None, 0
        for x, y in zip(cuts, cuts[1:]):
            if not body[x:y].strip():
                continue
            if start is None:
                start, words = x, 0
            words += len(body[x:y].split())
            if words >= min_words:
                chunk = body[start:y].strip()
                if words <= max_words and is_wisdom(chunk):
                    s = p_start + skip + body.index(chunk, start)
                    yield s, s + len(chunk)
                start = None


def build():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE sources (id INTEGER PRIMARY KEY, author TEXT, years TEXT, title TEXT, url TEXT, clean_text TEXT);
        CREATE TABLE passages (id INTEGER PRIMARY KEY, source_id INTEGER, char_start INTEGER, char_end INTEGER,
                               text TEXT, raw_vec BLOB);""")
    model = load_model()
    for book_id, author, years, title, start, stop in BOOKS:
        text = writer_text(download(book_id), start, stop)
        spans = list(passages(text))
        db.execute("INSERT INTO sources VALUES (?,?,?,?,?,?)",
                   (book_id, author, years, title, f"https://www.gutenberg.org/ebooks/{book_id}", text))
        vectors = encode(model, [text[a:b] for a, b in spans])
        db.executemany("INSERT INTO passages (source_id, char_start, char_end, text, raw_vec) VALUES (?,?,?,?,?)",
                       [(book_id, a, b, text[a:b], v.tobytes()) for (a, b), v in zip(spans, vectors)])
        db.commit()
        print(f"  {author}, {title}: {len(spans)} passages", flush=True)
    print(f"done: {db.execute('SELECT COUNT(*) FROM passages').fetchone()[0]} passages in {DB_PATH}")


class Guidance:
    def __init__(self, model):
        self.db = sqlite3.connect(DB_PATH, check_same_thread=False)
        rows = self.db.execute("""SELECT p.text, p.raw_vec, p.source_id, p.char_start, p.char_end,
                                         s.author, s.years, s.title, s.url
                                  FROM passages p JOIN sources s ON s.id = p.source_id ORDER BY p.id""").fetchall()
        self.rows = [dict(text=r[0], source_id=r[2], start=r[3], end=r[4], author=r[5], years=r[6],
                          title=r[7], url=r[8]) for r in rows]
        vectors = np.stack([np.frombuffer(r[1], dtype=np.float32) for r in rows])
        self.mean = vectors.mean(0, keepdims=True)
        self.vectors = normalise(vectors - self.mean)
        self.model = model
        self.books = dict(self.db.execute("SELECT id, clean_text FROM sources"))

    def verify(self, row):
        return self.books[row["source_id"]][row["start"]:row["end"]] == row["text"]

    def search(self, sentence, n=10):
        """The n closest passages, one per writer."""
        q = normalise(encode(self.model, [sentence]) - self.mean)[0]
        found, writers = [], set()
        for i in np.argsort(self.vectors @ q)[::-1]:
            row = self.rows[i]
            if row["author"] in writers:
                continue
            assert self.verify(row), "a guidance passage does not match its book"
            found.append(row)
            writers.add(row["author"])
            if len(found) == n:
                break
        return found


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1:2] == ["build"]:
        build()
    elif sys.argv[1:2] == ["try"]:
        g = Guidance(load_model())
        for r in g.search(" ".join(sys.argv[2:]), 5):
            print(f"\n{r['text']}\n    — {r['author']}, {r['title']}")
