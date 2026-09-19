# Reproducing the results

## Quick start
```bash
./setup.sh      # clones the pinned corpora and fetches the Aegean inscription files
./run_all.sh    # runs the pipeline; ~1-2 minutes without the optional data
```
`run_all.sh` skips any step whose optional input is absent and says so. Logs land in
`work/logs/`.

## What runs without any manual downloads
Sign classification, corpus building, the Mohenjo-daro text structure work, the
constraint miner, the conditioning and affix comparisons (Aegean parts), the seal-table
builders and every test based on them.

## Optional inputs, and what each unlocks
| place this file | source | unlocks |
|---|---|---|
| `data/cdliatf_unblocked.atf` | CDLI, `media.githubusercontent.com/media/cdli-gh/data/master/cdliatf_unblocked.atf` (87 MB) | Sumerian comparisons, seal legends, proto-cuneiform, Proto-Elamite |
| `data/mackay1938_vol1.txt` | archive.org `TVA_BOK_0009130`, djvu.txt | narrative find-spot parsing, chapter notes |
| `data/marshall1931_vol2.pdf` | archive.org `in.ernet.dli.2015.107493` | the Marshall table OCR comparison |
| `data/tla_egyptian.jsonl` | Thesaurus Linguae Aegyptiae, Later Egyptian (CC BY-SA 4.0) | Egyptian script-type comparison |
| `data/tla_egyptian_earlier.jsonl` | TLA, Earlier Egyptian (CC BY-SA 4.0) | genre-matched Egyptian labels, determinative test |

## Steps that are NOT automated, and cannot be
Three datasets were produced by reading page images by eye, because OCR failed on them:
the two seal tables and the plate codings. `scripts/plate_labels.py` and
`scripts/plate_segment.py` prepare the images; the reading itself is manual, and the
results are committed in `transcriptions/`. Re-running the pipeline uses those committed
files; it does not re-derive them.

## Randomness
Every script that samples or permutes sets an explicit seed. Null distributions use 20-500
permutations depending on cost; the counts are in the scripts.

## Environment
Python 3.12, `requirements.txt` (numpy, scipy, pandas, scikit-learn, Pillow, pytesseract,
statsmodels). Tesseract is needed only for the plate-label helper.
