# Results

Appended by `python -m Backend.eval`. Newest at the bottom.

### step1 (2026-11-14 21:41) - library 44640 passages, embedder all-mpnet-base-v2

| method | Test A same problem, top-2 (chance 0.06, n=33) | Test B NN problem / topic only (n=18) | Test C NN cause / feeling+situation only (chance 0.30 / 0.09, n=24) | pairs.json top-5 |
|---|---|---|---|---|
| raw (w=0.0) | 0.67 | 0.56 / 0.44 | 0.00 / 1.00 | missing |
| profile (w=1.0) | 0.70 | 0.83 / 0.06 | 0.17 / 0.83 | missing |
| blend (w=0.6) | 0.67 | 0.56 / 0.33 | 0.00 / 1.00 | missing |

### v2 (2026-11-14 23:06) - library 115380 passages, embedder all-mpnet-base-v2

| method | Test A same problem, top-2 (chance 0.06, n=33) | Test B NN problem / topic only (n=18) | Test C NN cause / feeling+situation only (chance 0.30 / 0.09, n=24) | pairs.json top-5 |
|---|---|---|---|---|
| raw (w=0.0) | 0.68 | 0.56 / 0.44 | 0.00 / 1.00 | missing |
| profile (w=1.0) | 0.62 | 0.78 / 0.00 | 0.17 / 0.79 | missing |
| blend (w=0.6) | 0.68 | 0.61 / 0.39 | 0.00 / 1.00 | missing |

