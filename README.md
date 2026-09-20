# Indus script: seal catalogues and text-structure analysis

Machine-readable catalogues of the Mohenjo-daro seals, text features coded from the
excavation plates, and a reproducible pipeline of structural analyses - approached
statistically, without assuming any language.

**No decipherment is offered here, and none is claimed to be reachable from this
evidence.** The analytical results are largely negative and are documented as such.

## What is in it

| | |
|---|---|
| **Mackay (1938) seal table** | 709 rows: type, size, material, block/house/room, level, field number. Hand-transcribed; validated against Mackay's own totals |
| **Marshall (1931) seal table** | 560 rows: type, size, material, excavation area, depth |
| **Plate codings** | 531 seals from all thirteen seal plates, 419 joined to find-spots; blind re-coding gives kappa 0.89 |
| **Constraint set** | 90 distributional rules, mined on half the corpus and scored on the held-out half (1.08% violations) |
| **Comparisons** | Sumerian seal legends and administrative text, Egyptian (Old/Middle and Later), Linear A/B, proto-cuneiform, Proto-Elamite - genre-, size- and length-matched |

## Documentation

**Primary document:** [docs/RESEARCH_NOTE.md](docs/RESEARCH_NOTE.md) - the full preprint:
background, data, method, results and limitations in one place. See also
[docs/ABSTRACT.md](docs/ABSTRACT.md) for a short abstract.

| file | what it is for |
|---|---|
| [docs/RESEARCH_NOTE.md](docs/RESEARCH_NOTE.md) | the preprint: full method, results and limitations |
| [docs/SUMMARY.md](docs/SUMMARY.md) | the findings in one page |
| [docs/FINDINGS.md](docs/FINDINGS.md) | all 41 numbered findings, with figures and caveats |
| [docs/STATUS.md](docs/STATUS.md) | every finding marked standing / qualified / retired / replicates published work |
| [docs/APPROACH.md](docs/APPROACH.md) | how the tests are built and why; the controls used |
| [docs/PRIOR_WORK.md](docs/PRIOR_WORK.md) | what replicates published work and what does not |
| [docs/DATASETS.md](docs/DATASETS.md) | data dictionary for every file |
| [docs/REPRODUCING.md](docs/REPRODUCING.md) | how to run it; what needs manual downloads |
| [docs/LIMITATIONS.md](docs/LIMITATIONS.md) | what bounds the conclusions |
| [docs/GLOSSARY.md](docs/GLOSSARY.md) | terms and sign names |
| [docs/ROADMAP.md](docs/ROADMAP.md) | what is still open |
| [docs/DATA_NOTICE.md](docs/DATA_NOTICE.md) | licences of the third-party corpora |

## Running it

```bash
./setup.sh     # clone the pinned corpora
./run_all.sh   # run the pipeline (~1-2 min without optional data)
```
Steps whose optional inputs are absent are skipped with a message. See
[docs/REPRODUCING.md](docs/REPRODUCING.md).

## Licences
- **Code**: MIT ([LICENSE](LICENSE)).
- **Transcribed and coded data**: CC BY 4.0 ([LICENSE-DATA](LICENSE-DATA)). These are our
  transcriptions of public-domain excavation reports.
- **Third-party corpora**: not redistributed; their own terms apply. See
  [docs/DATA_NOTICE.md](docs/DATA_NOTICE.md).

## A note on how this repo is kept
Results that were later corrected, qualified or retired are marked in place rather than
deleted. A reader following the numbers will see the type F trend fail to replicate, the
"3 + arrow" formula reinterpreted, and a periodicity claim shrink after a length control.
Those corrections are part of the evidence.

## Pipeline order (run_all.sh)
extract > features > cluster > finalize (visual families) > motif, motif_dedup,
site, objtype (sign/animal/site/object tests) > functional, crosscheck, g400,
finalize2 (behaviour classes) > abroad (foreign finds) > mj_segment, mj_subst
(Mohenjo-daro template) > m77 (replication) > numerals, stock, size_tab, robust,
mj_motif > refine, rename_families (shape refinement) > export_ml > ml_sequence > align_cisi, align_m77 > neural_nextsign > mj_core > count_arrow > build_mackay_table > mackay_context, mackay_spatial, match_feasibility, phase_test, neighbourhood_test, numeral_test, object_parts, recode_agreement, build_marshall_table, marshall_test, constraint_miner, affix_test, slot_tests, slot_followups, conditioning_compare, conditioning_shape, length_control, two_register, astral_test
> [if CDLI present] proto_elamite, seal_legends, name_slot, numbered_titles, typology
> [if Mackay text present] parse_mackay, findspots

- mwenge/lineara.xyz @ 43fe7cf and mwenge/linearb.xyz @ 84e0b00 (code dedicated to
  the public domain; inscription transcriptions from GORILA / DAMOS-type sources):
  only `LinearAInscriptions.js` and `LinearBInscriptions.js` are fetched (sparse).
- CISI digitisation (mayig/indus-valley-script-corpus, via indus_decipher):
  `cisi_real_corpus.csv`, 179 Mohenjo-daro seals with Parpola sign numbers.

## Optional data: Egyptian comparison corpus
Thesaurus Linguae Aegyptiae, CC-BY-SA 4.0, as JSONL at `data/tla_egyptian.jsonl`
(columns: hieroglyphs, transliteration, lemmatization, UPOS, glossing, translation,
dateNotBefore/After). `egyptian_compare.py` runs the structural measures on it. Egyptian
matters here because it is a MIXED system (phonetic signs, logograms, determinatives) with
a large inventory, and because its part-of-speech tags allow the measures to be checked
against grammatical category on a language where the answer is known.

## Optional data: Marshall (1931) vol. II
Marshall's own "Tabulation of Seals" (printed pp. 402-405 = PDF pages 56-59) covers the
1922-27 seasons, i.e. seals independent of Mackay's. Save the volume as
`data/marshall1931_vol2.pdf`; source (out of copyright):
https://archive.org/details/in.ernet.dli.2015.107493
`transcriptions/marshall1931_seal_table/` holds the hand transcription (COMPLETE: 560
rows, Nos. 1-557 plus three suffixed), merged by `build_marshall_table.py` into
`outputs/marshall_seal_table_transcribed.csv`. `parse_marshall_table.py` also OCRs the
table into `outputs/marshall_seal_table.csv`, PROVISIONAL:
the OCR recovers 356 of roughly 450 rows, plate numbers for half of them, levels for 239
and sizes for 67. The table is ordered by seal type, so types can be recovered from block
boundaries. A visual transcription pass (about ten page-column views) would make it solid,
as was done for Mackay.
Note: Marshall gives level BELOW THE MODERN SURFACE and only the excavation area (HR, VS,
DK, C, E, SD...), not block/house/room, so it is not directly comparable with Mackay's
datum levels.

## Optional data: Mackay (1938) find-spots
- Save the OCR text of *Further Excavations at Mohenjo-daro*, vol. I (out of copyright)
  as `data/mackay1938_vol1.txt`. Source (Internet Archive full text):
  https://archive.org/stream/dli.jZY9lup2kZl6TuXGlZQdjZM9k0Iy.TVA_BOK_0009130/TVA_BOK_0009130_Further_excavations_at_mohenjo-daro_djvu.txt
- `parse_mackay.py` extracts seal number, field number, area, block/street, level and an
  estimated phase to `outputs/findspots_mackay.csv` (the `context` column lets you check
  each row by eye). Test: `python3 tests/test_parse_mackay.py`.
- Joining find-spots to texts needs `data/concordance_cisi_mackay.csv` (template in
  `tests/concordance_template.csv`): Mackay's numbers are not CISI numbers. The mapping is
  printed in CISI vol. 1 (Joshi & Parpola 1987); it has to be transcribed by hand.

## Mackay (1938) seal table (in repo)
`transcriptions/mackay1938_seal_table/` holds a hand transcription of Mackay's
"Tabulation of Seals" (number, type, size, material, block/house/room or street, level,
field number) - complete, 709 rows. `build_mackay_table.py` merges and checks it into
`outputs/mackay_seal_table.csv` and adds area, DK-datum level and an estimated phase. See the NOTES file there for conventions and progress.
