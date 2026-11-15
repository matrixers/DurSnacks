# LOG: cause-aware matching for "A Hug from the Past"

Append-only. Newest entry at the bottom. Raw outputs are in `results/`.

## Decisions

| # | Decision | Chosen | Why (one line) | Evidence |
|---|----------|--------|----------------|----------|
| 1 | Where to work | new folder `HugCards/` with its own `.venv` | user asked for a new folder; keeps `Testing/` untouched | this log, entry Step 0 |
| 2 | Starting code | copy of `Testing/hug.py`, `app.py`, `index.html`, `test_app.py` | latest working version; only change is `import Testing.x` -> `import x` so it runs from this folder | `results/step0_*.txt` |
| 3 | Safety threshold CRISIS_Z | left at 2.3 | rule 5; a safety setting is the user's call | `results/step0_test_app.txt`: false alarms 6/6 |
| 4 | Embedder | all-mpnet-base-v2 | MiniLM scored lower on Test A (blend 0.65 vs 0.75) | LOG entry "Prior evidence" |

## 2026-11-14 20:05  Step 0: setup
Did:      Created `HugCards/` with copies of the four project files, `.gitignore` (.env, .venv/, hug.db, texts/, cards/, __pycache__/), `results/`, and this log. Creating a fresh venv next.
Result:   no numbers yet.
Decision: baseline is the `Testing/` code as it stands, which already includes the `chat` command, the `archive` command (not used here: no archive list in this folder, so `build` uses the 11 hand-listed SOURCES only), the optional "specific problem" field, and weighted text+tile queries.
Why:      measure from the code that actually runs today, so every later number has a real before.
Next:     venv, install, build, eval, demo.

## 2026-11-14 20:10  Step 0: baseline
Did:      New venv (`.venv`, Python 3.14.6); installed sentence-transformers 6.3.0, numpy 2.5.4, fastapi 0.163.0, uvicorn 0.54.0, httpx 0.28.1, transformers 5.23.0 (torch 2.15.0, CPU only). Ran `hug.py build`, `eval`, `demo`, and `test_app.py`. Files: `results/step0_build.txt`, `step0_eval.txt`, `step0_demo.txt`, `step0_test_app.txt`, `step0_pip_freeze.txt`.
Result:   Library: 11 sources, 2012 passages, 12 anchors, embedder all-mpnet-base-v2.
          Test A (8 problems x 3 wordings; share of 2 nearest neighbours with same problem; chance 0.09)
            raw text only 0.75 | anchor profile only 0.75 | blend (w=0.6) 0.75
          Test B (4 topics x 3 problems; nearest neighbour shares PROBLEM / shares only TOPIC)
            raw text only 0.33 / 0.67 | anchor profile only 0.83 / 0.00 | blend (w=0.6) 0.42 / 0.50
          Demo: detected top concern correct for 5/5 demo phrases (my reading); top passage on the underlying problem for 1/5 (Keats, "a dead silence is our only answer"). Judged by me, not by a test.
          test_app.py: FAILS (exit 1). Safety net: missed 0/5 crisis sentences, false alarms 6/6 ordinary sentences (ordinary z = +2.7 to +3.3, crisis z = +4.1 to +5.4, threshold CRISIS_Z = 2.3). The "tiles + text" request ("my dad died this year") is flagged, so the test hits KeyError 'heard'.
Decision: Accept these as the baseline. Do not change CRISIS_Z (rule 5: thresholds are not tuned to improve a number); flagged for the user to decide.
Why:      Tests A and B use 24 self-written sentences: tiny sets, so a change of one sentence moves Test A by 0.04 and Test B by 0.08. Neither test ranks library passages, so neither measures what the user sees; Step 1 (Test C, pairs.json top-5) addresses that.
Next:     STOP. Report to the user. Then Step 1, evaluation harness.

## 2026-11-14 20:12  Prior evidence carried over from the `Testing/` session (not part of this plan's steps)
Did:      Before this plan, two experiments on the same 11 books. (1) Passage length: current 25-85 word chunks vs 1-2 sentence windows, top-1 passage for 10 queries; raw output `results/pre_chunk_length_experiment.txt`, script `.py` beside it. (2) Embedder all-MiniLM-L6-v2 instead of all-mpnet-base-v2 on the same eval.
Result:   (1) My reading of the 10 top-1 results: short windows better on 4, current better on 1, 5 ties or both bad. One generic short sentence ("I fear there is no one can give me any comfort.") was top-1 for two different problems. 2012 vs 4804 passages; mean 45 vs 35 words. 10 self-written queries, judged by one person (me): weak evidence.
          (2) all-MiniLM-L6-v2: Test A raw 0.50 | profile 0.60 | blend 0.65. Test B raw 0.17 / 0.83 | profile 0.75 / 0.08 | blend 0.50 / 0.33. Embedding speed on this PC: 93 vs 15 passages/s (mpnet).
Decision: Keep all-mpnet-base-v2 (MiniLM lower on Test A for all three methods and on Test B profile). Passage length not changed yet.
Why:      Test A and profile results are lower with MiniLM; speed alone does not justify that. The length result is suggestive but rests on my own judgement of 10 queries; it should be re-tested with Test C and pairs.json from Step 1.
Next:     as above.

## 2026-11-14 20:30  User clarification: the user-side flow
Did:      Recorded the intended user flow, as stated by the user: (1) the user follows the feelings-wheel tree (Neurodivergent Insights wheel, JSON on GitHub, link not yet supplied) and gets an output; (2) a quick conversation / prompted diary entry refines the problem into a form useful for comparing with texts.
Result:   no numbers.
Decision: Proposed (awaiting confirmation): the wheel supplies the card's `feeling`; short prompted diary questions supply `event`, `cause` and `meaning` in the user's own words; a templated reflect-back is confirmed before matching. This gives the query-side card without an LLM; an LLM follow-up question is an optional later addition (Step 5).
Why:      The card fields are exactly what the diary needs to ask for, so the user can state the cause rather than us inferring it, which also satisfies rule 2 on the query side.
Next:     Wait for the user's confirmation and the wheel JSON link; then Step 1.

## 2026-11-14 21:02  Check: would field-by-field cards fix Test C? (no API)
Did:      On Test C's 24 sentences (self-written, tiny), split each at " because " into situation+feeling and cause, and compared nearest neighbours with all-mpnet-base-v2 under four set-ups. No library involved; plain cosine.
Result:   nearest neighbour shares the CAUSE / shares the feeling+situation (chance 0.30 / 0.09)
            whole sentence:                                   0.00 / 1.00
            planned card weights (.45 situation+feeling, .30 cause, rescaled): 0.00 / 1.00
            cause field alone:                                0.54 / 0.25
            cause field -> 3-type cause profile (anchors I wrote AFTER seeing Test C, so biased upward): 0.42; type picked right 0.62
          Example failure: "I've been too shy to talk to anyone" is nearest to "I work night shifts and never get to meet anyone" (same topic, different cause).
Decision: The plan's card scoring, as specified (fixed weights), does NOT fix Test C. Comparing the cause on its own helps (0.54 vs chance 0.30) but literal wording still pulls same-topic causes together. Proposed change: shortlist on feeling+situation, then rank on the cause/meaning fields; and test whether an LLM restating the cause in general terms (e.g. "others reject me" / "my own fault" / "outside my control") lifts Test C, with a ~1 cent user-approved test before building passage cards.
Why:      Fields only help if the cause is compared on its own and expressed at the level of "kind of cause", not topic words. Local embeddings do not do that reliably here.
Next:     Report to the user; wait for "go" on the 1-cent test.

## 2026-11-14 21:05  Methodology check against the EmpathicStories paper
Did:      Read the full method section of Shen et al., "Modeling Empathic Similarity in Personal Narratives", EMNLP 2023 (arxiv.org/html/2305.14246v2) and the dataset repo (github.com/mitmedialab/empathic-stories).
Result:   Paper: event / emotion / moral are what HUMANS annotated to define empathic similarity (1,500 stories, 2,000 rated pairs). Retrieval itself is a bi-encoder (whole story -> one embedding, cosine) FINE-TUNED on the human pair ratings with MSE. Table 4 (x100): SBERT Spearman 29.86, SBERT+finetune 35.21, BART+finetune 34.43 (best Kendall tau 24.68, P@1 65.84); ChatGPT+5 examples prompted pairwise Spearman 28.07 but P@1 85.15 (authors: too costly to prompt every pair for retrieval). User study n=150: more empathy for BART-finetuned retrievals than SBERT, t(149)=2.43, d=0.26. Annotator agreement low (Krippendorff alpha 0.14). Repo shows no licence; a BART checkpoint is released.
Decision: My plan's "compare card fields with fixed weights" is NOT the paper's method (and the Test C check above shows it does not work as specified). Methods that follow the paper: (1) fine-tune the embedding model on the EmpathicStories pairs (licence must be cleared first); (2) use an LLM only to re-rank a short list (where the paper found prompted LLMs strong at picking the top match). "Cause" is our addition, not in the paper. Paused for the user to choose.
Why:      Stay with the published, measured method; our own additions must earn their place on our eval.
Next:     Explain to the user; wait.

## 2026-11-14 21:31  Audit: is the index sound and useful?
Did:      Audited the index mid-build (27,343 passages). Read a random sample of 40 passages (seed 7; results/index_sample.txt) and rated each myself: does the writer express a personal problem someone could relate to? Counted defects across all passages with simple patterns.
Result:   Sample (my judgement, n=40): clearly useful 3 (Burney grieving, Chekhov afraid of Tolstoy's death, Darwin's illness), partly 6, not useful 31 (office business, gossip, travel, politics).
          Whole library: cut mid-sentence on an abbreviation or initial 1,983 (7%); starts with a quotation mark (possibly someone else's words) 697 (3%); long parenthetical editor notes 236 (1%); near-duplicates ignoring punctuation 2,213; Pepys 7,308 (27%), Walpole 2,654 (10%); from Life/Memoir-type books (editor narration likely) 2,080 (8%).
          Bug confirmed: SENT_SPLIT's abbreviation guard never fires (lookbehind checks "Mr" before the position after the dot); "Mr. Smith" and "Sir W. Pen" are split. Inherited from the original hug.py.
          Found in the sample: an editor's sentence ("Miss Burney describes this conversation...") and a letter written TO Keats, both indexed under the famous author: verbatim but wrongly attributed.
Decision: Index is mechanically sound (verbatim, no exact duplicates) but most passages are not useful and some are misattributed. Proposed fixes before any further use: (1) fix sentence splitting; (2) drop passages that open with a quote or contain editor notes; (3) dedupe ignoring punctuation (Pepys editions); (4) replace the word-list filter with a data-driven one (keep passages whose strongest concern-anchor score is high), checked on a new random sample; (5) cap any single author's share. Then rebuild --fresh.
Why:      Search can only return what the index holds; a 75% mundane, 37% Pepys/Walpole library makes good matches rare and wrong attribution possible.
Next:     Report to the user; wait for go.

## 2026-11-14 21:48  Rebuild v2: wheel.json emotions, guiding questions, short units, index hygiene
Did:      On the user's instructions: (1) emotions now come from the team's wheel.json (5 cores, 22 specific feelings, 21 tags; labels and tags only, no scoring/intensity rules); the 12 hand-made concerns are replaced by the 21 wheel tags, each with 3 hand-written anchor sentences; the chosen feeling's tag is added to the search query. (2) Guiding questions after the tree: what happened, why, the fear (worded per core), and how they have been coping (optional). (3) Library scope: letters + diaries + autobiographies (645 books selected: 240 letters, 190 diaries, 215 memoirs); philosophy books (Epictetus, Marcus Aurelius, Boethius, Pascal) removed. (4) Index: short non-overlapping units of 15-60 words instead of 25-85; sentence-split bug fixed (Mr./initials); units opening with a quote, containing a long parenthetical, or naming the writer's surname are dropped; dedupe ignores punctuation; translator recorded from each book's header. (5) Judge rubric adds emotion and coping ("struggling but coping" preferred, per the NEON research).
Result:   Build running; numbers to follow. Earlier eval/judge-export files from the old, partial index (results/eval_step1.txt, judge_input_step1.*) are superseded and must not be compared as like-for-like.
Decision: Old index discarded (rebuild --fresh).
Why:      Audit showed the old index was mostly mundane, 37% Pepys/Walpole, with split errors and misattribution.
Next:     When built: check, sample 40 units for usefulness (compare with 3/40 clearly useful before), eval, judge export.


## 2026-11-14 (time from shell: see below): small set-up changes while the v2 build runs
- check.py: the passage length check now says 15+ words (the v2 units are 15-60 words); this is a set-up check, not an eval test.
- check.py: the judge checks swap in a stand-in call_llm that raises, so check.py never makes a paid call even after call_llm is implemented.
- judge.py: new `run --label NAME` command: sends each exported review case (10) to call_llm, saves raw replies to results/judge_raw_NAME.json and verdicts to judge_output_NAME.json, then scores. Paid; not run.
- No API calls made.
Sat Nov 14 22:00:44 GMTST 2026

## 2026-11-14 22:10 : 3 questions, LLM rewrite, judge call wired, safety off (user's decision)
- User asked: questions "What's happened?" / "Why do you think you feel {emotion}?" / "Anything else?"; an LLM rewrites
  the answers into a general first-person statement that is searched; the judge sees the original answers too;
  "get rid of safety check for now"; write the LLM call so only the key is needed.
- New Backend/llm.py (Anthropic SDK, key from ANTHROPIC_API_KEY only): rephrase() with claude-haiku-5-5, judge call
  with claude-opus-5-5 (env REPHRASE_MODEL / JUDGE_MODEL). No key -> NoLLM -> plain search, said in the terminal.
- cards.Card gains `extra` and `statement`; as_query() returns the statement when present, else the template.
- judge.call_llm now calls llm.call; prompt shows the person's own answers plus the rewrite. `export --rephrase` added.
- Safety check removed from refine()/find() at the user's request (deviation from CLAUDE_CODE_INSTRUCTIONS rule);
  safety.py kept, unused. check.py safety section removed; rewrite wiring checks added with fake replies.
- Eval (eval.py) unchanged: still the no-LLM template path, so earlier numbers stay comparable.
- Tested without the index (old DB lacks the v2 schema): questions, fallback message, fake rewrite, judge prompt OK.
  Full check.py waits for the v2 build. No API calls made.

## 2026-11-14 23:06 : v2 build results
- fetch: 642 of 645 selected books cached (1 HTTPError skip, 79044). build --fresh: 649 sources listed, 639 with passages,
  115,380 short units (15-60 words) in 53 min. By kind: letters 54,472 (+63 tagged "letter"), memoir 40,646, diary 20,199.
  Largest authors: Pepys 4,551, Walpole 3,246, Stevenson 1,965, Burney 1,929, Balzac 1,885.
- check.py: ALL PASS (115,380 verbatim, 0 duplicates, 0 under 15 words). results/check_v2.log.
- Random 40 units (seed 2026, results/index_sample_v2.txt), my rating: clearly useful 3/40 (Stanley, Adams, Trollope),
  partly 12/40, not useful 25/40. Same as step1's 3/40: a random unit is still mostly narrative. Not a measure of search.
- eval v2 (RESULTS.md): blend A 0.68, B 0.61/0.39, C 0.00/1.00; profile A 0.62 (step1 0.70), B 0.78/0.00 (0.83/0.06),
  C 0.17/0.79. Raw/blend about unchanged; profile slightly lower.
- judge export v2 (no rewrite, no API): read the top 5 of each of the 10 cases (not blind). A real match is in the
  top 5 in about 7/10 (lonely, grief, homesick, stuck, rejected strongest: e.g. Thoreau "Is it all my fault?");
  weak for money (rent/overdraft) and medical tests, and regret-to-brother. Top-1 plain search is right in about 4/10.
  Modern words (overdraft, tests) are a likely cause: the LLM rewrite is meant to fix that. Not yet measured.

## 2026-11-14 23:30 : first live run (user's key, user asked to run the demo)
- `showcase` (2 cases, rewrite Haiku 5.5 + judge Opus 5.5): results/showcase_1.log. Both judged and shown:
  grandad/never said goodbye -> Helen Keller "My father is dead ... and I was not there" (judge: emotion/situation/cause yes,
  coping struggling); friend stopped replying -> Balzac "Either it is very bad of you to cut me off..." (situation yes, fear yes).
- Problem seen: the rewrite ADDED things the person never said ("I am afraid of what that silence means, and I have not
  told anyone how much it hurts"; "though I am afraid to ask"). Tightened REPHRASE_PROMPT (every part must come from their
  words, max 40 words). Re-ran the rewrite only: both sentences now stay within what was said.
- Added .env loading in llm.py (.env is git-ignored), showcase.bat / chat.bat launchers, `showcase` command.

## 2026-11-14 23:33 : cost tracking, progress messages
- llm.call records usage tokens and $ per call (PRICES table from the model docs) to SPENT and results/usage.log; chat and showcase print the running cost. Optional JUDGE_EFFORT env (low/medium/high) passed as output_config.effort.
- chat/showcase print progress (loading library, rewriting, judging) so a silent wait is not mistaken for nothing happening. showcase.bat tested with no valid key: runs, falls back to plain search, prints results.
- Judge prompt size measured: 14,287-18,235 characters (about 4k tokens) for the 10 review cases.

## 2026-11-14 23:37 : measured cost, longer passages shown
- showcase re-run (results/showcase_2.log, results/usage.log): 4 calls, $0.122 total. Haiku rewrite 366-371 in / 32-48 out = $0.0001 each; Opus judge 5,582-5,772 in / 1,727-2,105 out = $0.058-0.064 each. Both cases matched as before (Keller, Balzac).
- User reported a failure on their own run; not reproduced here (error text not yet seen).
- User: passages feel short. Final results now show 4 sentences either side (SHOW_SENTENCES; the judge still reads 2). Library.context stops at a neighbouring paragraph that names the writer (an editor's note), seen in Keller: 'On the first of October Miss Keller entered...'. Still verbatim slices of the source.
- JUDGE_POOL (.env, default 20) sets how many passages the judge reads; .env.example lists the cheaper options. 2026-11-14 23:39
- 2026-11-14 23:45 User: wants the philosophy and advice books added later (not now).
- 2026-11-14 23:49 library.py sets HF_HUB_VERBOSITY/TRANSFORMERS_VERBOSITY=error to hide the harmless 'unauthenticated requests to the HF Hub' warning.
- 2026-11-15 00:18 Menu accepts '1 lonely' / 'lonely' (user typed '1 Lonely' and lost the emotion tag). User: rewrite 'way too long' -> one sentence, max 25 words.

## 2026-11-15: judge reads the full context; short sentence + 3-line poem

- Judge: candidates now carry the same context the person sees (SHOW_SENTENCES = 4 sentences each side, was 2),
  and INSTRUCTIONS tell it to use the context to see who is writing, about whom, and what is going on; a match
  found only in the context is "partly" at most. Prompt size for Heavy>lonely, 20 candidates: 15,034 -> 22,255 chars
  (~+1.8k input tokens, ~+$0.007 per search on Opus 5.5).
- Rewrite: one Haiku call now returns SENTENCE (<= 15 words, searched, also given to the judge) and POEM
  (3 lines, <= 6 words each, shown to the person as the reflect-back). New Card field `poem`; llm.rewrite();
  llm.rephrase() still returns just the sentence.
- Live test (2 Haiku calls, $0.00072 total):
  - lonely: "The friend I was closest to has gone silent, and I think I did wrong." /
    "My closest friend has gone quiet. / I think I did something wrong. / I feel heavy and lonely now."
  - grieving: "My grandfather died last month, and I never got to say goodbye." /
    "My grandfather died last month. / I could not say goodbye. / Everyone around me seems fine."
  Nothing added that the person did not say.
- Library make-up (why Wagner shows up): 115,380 passages, 393 authors; letters 54,535, memoir 40,646, diary 20,199.
  Richard Wagner has 1,526 + 1,182 (with Liszt) = 2,708 passages. No soldier authors in the library.
- python -m Backend.check: ALL PASS.

## 2026-11-15: shorter quotation

- The judge now also returns `quote` for yes/partly candidates: the 1-2 sentences of the PASSAGE that show the
  feeling, <= 30 words, copied word for word. judge.checked_quote() keeps it only if it is an exact substring of
  the (already verified) passage, has no "..." and is <= 40 words; otherwise the full passage is shown.
- Terminal shows just the quote + author line; "Read the letter around it? [y/N]" shows the passage with
  4 sentences of context. Without the judge the whole passage (15-60 words) is the quote.
- 3 new checks (quote kept / dropped / returned by find with a fake judge). python -m Backend.check: ALL PASS.
- Not yet tested with a live judge call (costs ~$0.07).

## 2026-11-15: cleanup (simpler backend)

- Backend rewritten from 11 files / 2,322 lines to 7 files / ~1,190 lines. Old code kept in research/old_backend/,
  this log + RESULTS.md + results/ moved to research/. Removed: cards.py, judge.py (merged into llm.py),
  safety.py (unused), eval.py, check.py (replaced by tests.py), app_api.py (merged into Backend.py),
  the raw/profile/blend switch (blend kept), the old wheel.json fallback, the 5-case demo.
- library.py split into library.py (load + score) and build_library.py (one-off build). Search checked
  identical to before: same top-10 passages and same context for 3 test sentences.
- Judge reply simplified: only matching passages are listed, each with match yes/partly, quote, why
  (was 7 fields for every candidate). Fewer output tokens.
- Live showcase (2 cases): $0.036 total (was ~$0.12 for 2 cases). Grandad case: Helen Keller "My father is dead.
  He died last Saturday at my home in Tuscumbia, and I was not there." (only 1 result: judge kept no
  lesser-known passage). Friend case: Balzac (well known) + Hester Piozzi (lesser known).
- python -m Backend.tests: ALL OK.
