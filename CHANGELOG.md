# Changelog

## 0.2.5 - 2026-09-20
An external review of the published record found one claim that had to be retracted and
one that had to be qualified. Landed here as a corrected Zenodo version rather than a
silent edit, per the release policy now in `CONTRIBUTING.md`.

- **RETRACTED**: the "corpus is strongly directional" claim (Summary, §9 Direction, §13,
  FINDINGS §32c, §36) is retracted. `dirs()` in `conditioning_shape.py` computes
  H(next|prev) and H(prev|next) by subtracting the same mutual-information term from each,
  so the two cancel algebraically and the 0.50-bit gap it reports is exactly the positional
  entropy gradient already covered in §8/FINDINGS §29a/31 - not an independent measurement,
  and not evidence for reading direction (the quantity flips sign under text reversal).
  Verified numerically against the committed corpus. `docs/RESEARCH_NOTE.md`,
  `docs/FINDINGS.md`, `docs/STATUS.md` and `docs/SUMMARY.md` corrected in place; the code
  is left unretouched with an explanatory comment, since the derivation needs to stay
  visible.
- **QUALIFIED**: the jar/arrow "not co-occurring" claim, previously listed as replicating
  Mahadevan (2011), is corrected to a qualification of it - they co-occur in 3 of 2,585
  held-out applications of the validated constraint set (FINDINGS §27, which already said
  this correctly; `docs/STATUS.md` and `docs/PRIOR_WORK.md` did not match it and are now
  fixed).
- Four scripts behind the ending-slot and cross-corpus conditioning results
  (`slot_tests.py`, `slot_followups.py`, `conditioning_compare.py`,
  `conditioning_shape.py`) do not apply the `first_occurrence` deduplication filter used
  elsewhere. The results survive deduplication at a smaller magnitude (e.g. the
  ending-conditioning excess drops from 26.8% to 22.1%, n=1,028 to n=872) - both figures
  are now reported together in `docs/RESEARCH_NOTE.md` §3/§8/§9, `docs/FINDINGS.md` and
  `docs/APPROACH.md`, rather than only the higher one.
- Several numeric slips fixed in `docs/RESEARCH_NOTE.md`: a mistyped 0.3% corrected to
  0.1% (3 of 2,299) for the second-line arrow-ending rate; two different z-scores for the
  same statistic (from independently-shuffled runs of two different scripts) reconciled
  with a note rather than presented as one number; the three different denominators
  behind Mackay-table counts (709 rows / 693 distinct seals / 697 with a usable level)
  defined at first use; unique-text-share percentages (88-95%) given their denominators.
- `docs/RESEARCH_NOTE.md` §11 and its Summary bullet now report statistical power
  alongside the depth null (uninformative below roughly a 20-point difference in
  jar-ending rate or 0.5 signs in mean length), matching detail already in
  `docs/FINDINGS.md`.
- `conditioning_compare.py` now also reports/records excess conditioning in raw bits
  alongside the normalised percentage, confirming the normaliser is not driving the
  cross-corpus ranking. `conditioning_shape.py` now prints and records the sample size (n)
  used at each distance in the decay curve, since distance 5 draws on a minority tail of
  longer texts.
- Added `.gitattributes` (`*.csv text eol=lf`): the committed output CSVs are LF, but
  Python's `csv` module writes `\r\n` regardless of file-open mode, so a clean re-run
  produced a 1,686-line phantom diff across five tracked files on any platform without
  Windows-style `core.autocrlf`. Verified fixed.
- Removed the hand-maintained version string from the preprint's own subtitle (this is the
  second time it went stale; `CITATION.cff` is now the only place version is tracked).
- Added a release checklist and the Zenodo-versioning policy to `CONTRIBUTING.md`.

## Unreleased
- Both Zenodo deposits published: dataset/code
  (https://doi.org/10.5281/zenodo.22852769, concept DOI) and companion preprint
  (https://doi.org/10.5281/zenodo.22852774, concept DOI). DOI badges and a Citation
  section added to README.md; `doi` field added to CITATION.cff; `.zenodo.json`'s
  related identifiers updated with the live preprint DOI.

## 0.2.4 - 2026-09-20
- `requirements.txt` was missing two direct dependencies that scripts import:
  `pandas` (`export_ml.py`, in the core `run_all.sh` loop - was working only because
  `statsmodels` happens to pull it in transitively, which is fragile) and `pytesseract`
  (`parse_marshall_table.py`, invoked whenever the optional Marshall PDF is present -
  nothing else in the file pulls this one in, so it was a genuine gap). Both are now
  pinned explicitly; both were already claimed as dependencies in `docs/REPRODUCING.md`.
  That file's dependency list also corrected to match the full `requirements.txt`.

## 0.2.3 - 2026-09-20
- Fixed a stale "v0.2.1" version string left in the preprint's subtitle.

## 0.2.2 - 2026-09-20
- Added `docs/RESEARCH_NOTE.md`, a preprint synthesising the background, data, method,
  results and limitations into one document for external submission (Zenodo, and any
  future preprint server), and `docs/ABSTRACT.md`. README and `.zenodo.json` updated to
  point at it.

## 0.2.1 - 2026-09-19
- Zenodo readiness fixes: seven `outputs/` files with verified clean provenance are
  now committed instead of git-ignored, so they're actually present in a
  tagged/archived snapshot - `mackay_seal_table.csv`, `marshall_seal_table.csv`,
  `marshall_seal_table_transcribed.csv`, `findspots_mackay.csv`,
  `concordance_parpola_G.csv`, `concordance_m77_G_inferred.csv` (own transcriptions,
  or the MIT-licensed `indus_decipher` corpus only), and `constraints.csv` (the 90
  held-out validated constraints - confirmed clean by tracing every column
  `constraint_miner.py` reads).
- `docs/DATA_NOTICE.md` now names exactly which `outputs/` files stay git-ignored and
  why, including a previously-undocumented GPL-3.0 taint path: `export_ml.py` pulls
  `object_type`/`material` from the `indus-website` SQL dump into `inscriptions_ml.csv`.
  `constraints.csv` never reads those two columns so it escapes the taint; four other
  files built from `inscriptions_ml.csv` additionally pull in CDLI or Linear B data and
  stay excluded on that basis instead - `affix_profile.csv`, `conditioning_profile.csv`,
  `conditioning_decay.csv`, `length_control.csv`.
- `LICENSE-DATA` updated to name the newly-committed files explicitly.
- `CITATION.cff` license field corrected from `MIT` alone to `[MIT, CC-BY-4.0]`,
  matching the repo's actual code/data split and `.zenodo.json`.

## 0.2.0 - 2026-09-19
- Mackay (1938) seal table transcribed in full: 709 rows with locus and level.
- Marshall (1931) seal table transcribed in full: 560 rows.
- All thirteen Mackay seal plates coded: 531 seals, 419 with find-spots.
- Blind re-coding of 36 seals: kappa 0.89 for jar endings.
- Constraint miner with held-out validation (90 rules).
- Cross-corpus structural comparisons: Sumerian, Linear B, Egyptian (Earlier and Later),
  with size and length corrections and synthetic controls.
- Findings 22-41 added; findings 18, 24, 32 corrected; the type F trend retired after a
  failed replication.
- Documentation restructured: docs/ with APPROACH, PRIOR_WORK, DATASETS, REPRODUCING,
  LIMITATIONS, STATUS, GLOSSARY.

## 0.1.0 - 2026-09-17
- Initial pipeline: sign classification, corpus building, text-structure analysis,
  comparisons with Proto-Elamite, Linear A/B and cuneiform.
