"""
Crisis check on the user's own words. Runs before anything else (and before any
LLM call). It errs towards showing support; it is a net, not a clinical screen.

Only the explicit-phrase layer is on. The earlier embedding layer (closeness to
crisis statements, as a z-score against the library) flagged 6 of 6 ordinary
sad sentences in testing, so it stays off until it is recalibrated on a proper
test set. See LOG.md.
"""
import re

CRISIS_RE = re.compile(
    r"\b(kill(ing)? myself|suicid\w*|end(ing)? my life|end it all|want to die|wish i was dead|"
    r"wish i were dead|better off without me|better off dead|hurt(ing)? myself|self[- ]?harm\w*|"
    r"no reason to live|can'?t go on|cannot go on|not worth living|"
    r"don'?t want to (be here|be alive|live|exist|wake up)|"
    r"notice if i (just |was |were )?(disappear\w*|gone)|disappear for ?ever|"
    r"(no|any) (way|reason) to (keep|go on) living)\b", re.I)

SUPPORT = [
    {"name": "Samaritans", "how": "call 116 123", "note": "free, any time, day or night (UK)"},
    {"name": "Shout", "how": "text SHOUT to 85258", "note": "free, any time, if you would rather not speak (UK)"},
    {"name": "Emergency services", "how": "call 999", "note": "if you are in immediate danger (UK)"},
]


def check(*texts):
    """True if any of the user's texts contains an explicit crisis phrase."""
    return any(CRISIS_RE.search(t or "") for t in texts)
