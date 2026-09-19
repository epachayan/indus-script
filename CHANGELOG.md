# Changelog

## 0.2.1 - 2026-09-19
- Zenodo readiness fixes: the six `outputs/` files with verified clean provenance
  (own transcriptions plus the MIT-licensed `indus_decipher` corpus only) are now
  committed instead of git-ignored, so they're actually present in a tagged/archived
  snapshot - `mackay_seal_table.csv`, `marshall_seal_table.csv`,
  `marshall_seal_table_transcribed.csv`, `findspots_mackay.csv`,
  `concordance_parpola_G.csv`, `concordance_m77_G_inferred.csv`.
- `docs/DATA_NOTICE.md` now names exactly which `outputs/` files stay git-ignored and
  why, including a previously-undocumented GPL-3.0 taint path: `export_ml.py` pulls
  `object_type`/`material` from the `indus-website` SQL dump into `inscriptions_ml.csv`,
  which taints everything built from it (`constraints.csv`, `affix_profile.csv`,
  `conditioning_profile.csv`, `conditioning_decay.csv`, `length_control.csv`).
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
