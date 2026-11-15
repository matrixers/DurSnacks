"""
The passage library: short pieces (15-60 words) of real letters, diaries and
autobiographies from Project Gutenberg, stored in data/library.db.

Every passage keeps its exact position in the book, so we can always check that
what we show is word for word what the writer wrote (verify).

To build the database, see build_library.py.
"""
import os
import re
import sqlite3

import numpy as np

# hide the Hugging Face download notices (the model is public and cached after the first run)
os.environ.setdefault("HF_HUB_VERBOSITY", "error")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "library.db")
MODEL = "all-mpnet-base-v2"     # turns a sentence into 768 numbers that capture its meaning (runs locally)

# A few plain sentences for each emotion. Every passage gets a score for how strongly it
# expresses each one, and the feeling picked on the tree pulls the search towards it.
EMOTIONS = {
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

# Split text into sentences, but not after titles or initials ("Mr. Smith", "Sir W. Pen").
NOT_AFTER = ("Mr", "Mrs", "Dr", "St", "MS", "No", "vol", "Esq", "Rev", "Col", "Capt", "Gen", "Lieut", "Prof",
             "Hon", "Messrs", "Mme", "Mlle", "Sr", "Jr", "viz", "Gov", "Sen", "Ld", "Bp")
SENTENCE_END = re.compile("".join(rf"(?<!\b{a}\.)" for a in NOT_AFTER) + r"(?<!\b[A-Z]\.)"
                          r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z])")


def normalise(m):
    n = np.linalg.norm(m, axis=-1, keepdims=True)
    return m / np.where(n == 0, 1, n)


def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL)


def encode(model, texts):
    return np.asarray(model.encode(list(texts), normalize_embeddings=True, batch_size=64,
                                   show_progress_bar=False), dtype=np.float32)


class Library:
    def __init__(self):
        if not os.path.exists(DB_PATH):
            raise SystemExit(f"No library at {DB_PATH}. Build it with: python -m Backend.build_library build")
        self.db = sqlite3.connect(DB_PATH, check_same_thread=False)
        rows = self.db.execute("""
            SELECT p.id, p.text, p.raw_vec, s.author, s.title, s.year, s.url, p.source_id,
                   p.char_start, p.char_end, s.dates, s.translator
            FROM passages p JOIN sources s ON s.id = p.source_id ORDER BY p.id""").fetchall()
        self.rows = [dict(id=r[0], text=r[1], author=r[3], title=r[4], year=r[5], url=r[6], source_id=r[7],
                          start=r[8], end=r[9], dates=r[10], translator=r[11]) for r in rows]
        vectors = np.stack([np.frombuffer(r[2], dtype=np.float32) for r in rows])
        self.model = load_model()
        self._books = {}

        # Every old passage shares an "old-fashioned writing" direction; take it out so we compare meaning.
        self.mean = vectors.mean(0, keepdims=True)
        self.vectors = normalise(vectors - self.mean)
        # One direction per emotion, and each passage's emotional profile (how it compares to the rest).
        self.emotions = list(EMOTIONS)
        self.anchors = normalise(np.stack([normalise(encode(self.model, s) - self.mean).mean(0)
                                           for s in EMOTIONS.values()]))
        sims = self.vectors @ self.anchors.T
        self.mu, self.sd = sims.mean(0), sims.std(0) + 1e-6
        self.profiles = normalise((sims - self.mu) / self.sd)

    def scores(self, sentence, emotions=()):
        """How close every passage is to the sentence: 60% emotional profile + 40% meaning.
        `emotions` (from the tree) pull the sentence towards those feelings."""
        q = normalise(encode(self.model, [sentence]) - self.mean)[0]
        picked = [self.emotions.index(e) for e in emotions if e in self.emotions]
        if picked:
            q = normalise(q + 0.5 * self.anchors[picked].mean(0))
        profile = normalise((q @ self.anchors.T - self.mu) / self.sd)
        return 0.6 * (self.profiles @ profile) + 0.4 * (self.vectors @ q)

    def book(self, source_id):
        if source_id not in self._books:
            self._books[source_id] = self.db.execute("SELECT clean_text FROM sources WHERE id=?",
                                                     (source_id,)).fetchone()[0]
        return self._books[source_id]

    def verify(self, row):
        """True if the passage is exactly what the book says at that position."""
        return self.book(row["source_id"])[row["start"]:row["end"]] == row["text"]

    def context(self, row, n=4):
        """Up to n sentences before and after the passage, word for word from the same book.
        Stops at a paragraph that names the writer (that is an editor talking, not the writer)."""
        text = self.book(row["source_id"])
        a, b = surrounding(text, row["start"], row["end"], n)
        before, after = text[a:row["start"]].split("\n"), text[row["end"]:b].split("\n")
        surname = re.split(r"[ ,]", row["author"].split(" and ")[0].strip())[-1]
        if len(surname) > 2:
            names_writer = re.compile(rf"\b{re.escape(surname)}\b", re.I).search
            first = next((i for i in range(1, len(after)) if names_writer(after[i])), len(after))
            after = after[:first]
            last = next((i for i in range(len(before) - 2, -1, -1) if names_writer(before[i])), -1)
            before = before[last + 1:]
        return "\n".join(before).strip(), "\n".join(after).strip()

    def when(self, row):
        """The writer's dates, e.g. '1880–1968'."""
        if row["dates"]:
            return row["dates"].replace("-", "–")
        return f"c. {row['year']}" if row["year"] < 1500 else str(row["year"])


# --- finding the sentences around a passage -------------------------------------------------
def _paragraph(text, i):
    a = text.rfind("\n", 0, i) + 1
    b = text.find("\n", i)
    return a, len(text) if b < 0 else b


def _sentences(text, a, b):
    para = text[a:b]
    cuts = [0] + [m.end() for m in SENTENCE_END.finditer(para)] + [len(para)]
    spans = []
    for x, y in zip(cuts, cuts[1:]):
        piece = para[x:y]
        if piece.strip():
            spans.append((a + x + len(piece) - len(piece.lstrip()), a + x + len(piece.rstrip())))
    return spans


def _is_prose(para):
    return len(para.split()) >= 4 and not para.isupper() and "[" not in para


def surrounding(text, a, b, n):
    """Widen text[a:b] by up to n sentences each side. It only crosses into the next or previous
    paragraph if that is ordinary prose, so the context stays inside one letter."""
    pa, pb = _paragraph(text, a)
    before = [s for s in _sentences(text, pa, pb) if s[1] <= a]
    while len(before) < n and pa > 0:
        pa, pb = _paragraph(text, pa - 2)
        if not _is_prose(text[pa:pb]):
            break
        before = _sentences(text, pa, pb) + before
    pa, pb = _paragraph(text, b - 1)
    after = [s for s in _sentences(text, pa, pb) if s[0] >= b]
    while len(after) < n and pb < len(text):
        pa, pb = _paragraph(text, pb + 1)
        if not _is_prose(text[pa:pb]):
            break
        after += _sentences(text, pa, pb)
    before, after = before[-n:], after[:n]
    return (before[0][0] if before else a), (after[-1][1] if after else b)
