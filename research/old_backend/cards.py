"""
Story cards (after EmpathicStories, Shen et al. 2023: people relate to stories
that share the main event, the emotional reaction and the moral/meaning).

    event:    what happened, one plain sentence
    feeling:  one or two words
    meaning:  what it means to the person, or what they fear it means
    cause:    why they feel this
    coping:   how they are dealing with it (used to judge usefulness, not to search)
    extra:    the person's "anything else" answer, as written
    statement: the LLM's general first-person rewrite of the problem (Backend/llm.py);
              when present it is what the search compares
    evidence: exact words from the source that show the cause (passages only)

A field nobody stated is NOT_STATED; it is never guessed.
"""
from dataclasses import asdict, dataclass

NOT_STATED = "NOT STATED"
FIELDS = ("event", "feeling", "meaning", "cause")
WEIGHTS = {"event": 0.30, "feeling": 0.15, "meaning": 0.25, "cause": 0.30}


@dataclass
class Card:
    event: str = NOT_STATED
    feeling: str = NOT_STATED
    meaning: str = NOT_STATED
    cause: str = NOT_STATED
    coping: str = NOT_STATED
    extra: str = NOT_STATED
    statement: str = NOT_STATED
    poem: str = ""
    evidence: str = ""

    def stated(self, field):
        v = getattr(self, field)
        return bool(v) and v.strip().upper() != NOT_STATED

    def to_dict(self):
        return asdict(self)

    def as_query(self):
        """The text the search compares: the LLM statement if there is one, else a template."""
        if self.stated("statement"):
            return self.statement
        parts = []
        if self.stated("feeling"):
            parts.append(f"I feel {self.feeling}.")
        if self.stated("event"):
            parts.append(self.event.rstrip(".") + ".")
        if self.stated("cause"):
            parts.append(f"I feel this because {self.cause.rstrip('.')}.")
        if self.stated("meaning"):
            parts.append(f"I am afraid it means {self.meaning.rstrip('.')}.")
        if self.stated("extra"):
            parts.append(self.extra.rstrip(".") + ".")
        return " ".join(parts)


def feeling_from_path(path):
    """('Sad', 'Lonely', 'Isolated') -> 'isolated (lonely, sad)'."""
    words = [w.strip().lower() for w in path if w and w.strip()]
    if not words:
        return NOT_STATED
    deepest, rest = words[-1], list(reversed(words[:-1]))
    return f"{deepest} ({', '.join(rest)})" if rest else deepest


def from_answers(path, answers):
    """The no-LLM user card: the person's own words go straight into the fields."""
    answers = answers or {}

    def get(k):
        v = (answers.get(k) or "").strip()
        return v if v else NOT_STATED

    return Card(event=get("event"), feeling=feeling_from_path(path),
                meaning=get("meaning"), cause=get("cause"), coping=get("coping"), extra=get("extra"))


def reflect_back(path, card):
    """Template reflect-back sentence (used when no LLM is available)."""
    deepest = path[-1].lower() if path else "this way"
    lines = [f"You feel {deepest}."]
    if card.stated("event"):
        lines.append(f'What happened: "{card.event}"')
    if card.stated("cause"):
        lines.append(f'Because: "{card.cause}"')
    if card.stated("meaning"):
        lines.append(f'You are afraid: "{card.meaning}"')
    if card.stated("coping"):
        lines.append(f'So far you have been: "{card.coping}"')
    if card.stated("extra"):
        lines.append(f'Also: "{card.extra}"')
    if card.poem.strip():
        poem = "\n".join("    " + line for line in card.poem.splitlines())
        return f"So what you're saying is:\n\n{poem}\n\nIs that right?"
    if card.stated("statement"):
        return f'In other words: "{card.statement}" Is that right?'
    return " ".join(lines) + " Is that right?"
