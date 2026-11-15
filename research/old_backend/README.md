# Backend

Finds passages from real historical letters and diaries where the writer faces the same problem as the user.
Plain Python; it never imports the frontend. The frontend can later call `questions()`, `refine()` and `find()`
in `Backend/Backend.py`, which return plain dicts.

## Set up (once)

```powershell
pip install -r Backend/requirements.txt
$env:HUG_TEXT_DIR = "C:\...\texts"     # optional: where downloaded books are cached (default data/texts)
python -m Backend.library fetch        # download the ~645 letters/diaries/autobiography books from a Gutenberg mirror
python -m Backend.library build        # cut into passages and index them (resumable; re-run after fetch)
python -m Backend.check                # set-up checks: must say ALL PASS
```

## Try it in the terminal

```powershell
python -m Backend.Backend chat           # pick a feeling, answer 3 questions, LLM rewrite, read a passage
python -m Backend.Backend chat --judge   # same, but the LLM judge picks from a short list of 20 (or says none)
python -m Backend.Backend chat --no-llm  # no API at all: plain search on your words
python -m Backend.Backend demo           # five fixed cases
python -m Backend.eval --label NAME --review   # tests A/B/C -> RESULTS.md, blind review sheet in results/
```

## How a match is found

1. **The tree** (`wheel.json`, labels and tags only): the user picks a core feeling and a specific one,
   e.g. Heavy > lonely, which carries the emotion tag `loneliness`.
2. **Three questions** (`questions()`): "What's happened?", "Why do you think you feel {feeling}?",
   "Anything else?" (optional). The answers form a card (`cards.py`).
2b. **Rewrite** (`refine()`, `llm.rephrase`, cheap model): the answers become one general first-person
   sentence, as someone might write it in an old letter ("the friend I was closest to has gone silent"),
   which is what the search compares. Without a key, the answers are joined by a template instead.
   (The safety check is switched off for now; `safety.py` is kept but not called.)
3. **The library** (`library.py`): Project Gutenberg letters, diaries and autobiographies (chosen by the
   catalogue's own subject headings), cut into **short units of 15-60 words** (one or a few sentences). A unit is
   kept only if it is the writer's own first-person words about an inner state: units opening with a quotation,
   containing a long editor's note or naming the writer in the third person are dropped, and the same text in
   two editions is kept once. Each unit is stored with its exact position in the book (verified on every
   use) and its meaning as 768 numbers (`all-mpnet-base-v2`, run locally, no API).
4. **Rough search** (`shortlist()`): the card becomes one sentence; the chosen emotion's tag pulls the query
   towards that emotion; every unit is scored (0.6 emotion profile over the wheel's tags + 0.4 meaning) and the
   20 best, one per author, are kept, each with two sentences of context either side.
5. **Judge** (`judge.py`, `--judge`): reads the person's own answers, the rewrite and the 20 candidates and keeps only real matches:
   same emotion, same kind of situation, same kind of cause, same fear; and prefers a writer who is
   struggling but coping. It may say "none".

## Turning on the LLM steps (just the key)

All LLM calls are in `Backend/llm.py` (Anthropic Python SDK). Set the key once, then open a new terminal:

```powershell
setx ANTHROPIC_API_KEY "sk-ant-..."      # never put it in code or commit it
```

Models: rewrite `claude-haiku-5-5` ($0.10 / $0.50 per million tokens), judge `claude-opus-5-5`
($4 / $20). Change with the env vars `REPHRASE_MODEL` / `JUDGE_MODEL` (e.g. `claude-fable-5-2`, $8 / $40).
Without a key everything still runs as plain search and says so. `python -m Backend.check` never calls the API.

With a key: `python -m Backend.judge export --label NAME --rephrase` then `python -m Backend.judge run --label NAME`
(paid: one call per review case, 10 cases) writes the verdicts and prints the scores.

To test the judge without code: `python -m Backend.judge export --label NAME` writes
`results/judge_input_NAME.json` / `.md`; whoever judges writes `results/judge_output_NAME.json`
(`{"cases": [{"case": 1, "verdicts": [...], "best": 3}]}`), then
`python -m Backend.judge score results/judge_output_NAME.json --label NAME` prints the numbers and a blind
review sheet.
