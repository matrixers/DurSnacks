# Backend

Finds passages from real old letters, diaries and autobiographies where the writer went through
the same thing as the person using the app.

## How it works

1. The person picks a feeling on the tree (`tree.json`, the same labels as the app), e.g. Sad > Lonely > Isolated.
2. They answer three questions: *What's happened?*, *Why do you think you feel …?*, *Anything else?*
3. **Rewrite** (Claude Haiku): their answers become one short, general sentence to search with,
   and a 3-line poem to show back to them.
4. **Search**: every passage in the library is scored against that sentence (by meaning, and by how
   strongly it shows the chosen feeling). The best 10 from well-known writers and the best 10 from
   lesser-known ones are kept.
5. **Judge** (Claude Opus): reads those 20 with the sentences around them, keeps only the real
   matches and picks a short quote from each.
6. The person sees one well-known writer and two lesser-known ones.

Every passage shown is checked word for word against the book it came from.
Without an API key, steps 3 and 5 are skipped and the search uses the person's own words.

## Files

| File | What it does |
|---|---|
| `Backend.py` | What the app calls: `questions()`, `find()`, `find_in_background()`, `as_text()` |
| `llm.py` | The two Claude calls: rewrite and judge |
| `library.py` | Loads the passages and scores them |
| `fame.py` | Works out who is well known (from Wikipedia), saved in `data/fame.json` |
| `build_library.py` | Downloads the books and builds `data/library.db` (only needed once) |
| `chat.py` | Try it in the terminal |
| `tests.py` | Quick checks (free, no API calls) |

## Using it

```powershell
pip install -r Backend/requirements.txt
python -m Backend.chat              # try it yourself
python -m Backend.chat showcase     # two ready-made examples
python -m Backend.tests             # checks
```

The API key goes in a `.env` file in the project folder: `ANTHROPIC_API_KEY=sk-ant-...` (never commit it).
A search costs about $0.07 (almost all of it the judge). To make it cheaper, add `JUDGE_POOL=10` or
`JUDGE_MODEL=claude-sonnet-5-5` to `.env`.

## From the app

```python
from Backend import Backend

Backend.find_in_background(["Sad", "Lonely", "Isolated"],
                           {"event": "...", "cause": "...", "extra": "..."},
                           on_done=show_results)          # in Kivy, mark show_results with @mainthread

def show_results(result):
    label.text = Backend.as_text(result)
```

## Building the library (once, about 1.5 hours)

```powershell
python -m Backend.build_library fetch    # download the books from Project Gutenberg
python -m Backend.build_library build    # cut them into passages and save data/library.db
python -m Backend.fame build             # look up who is well known
```
