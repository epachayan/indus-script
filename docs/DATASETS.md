# Data dictionary

Every file in `outputs/` and `transcriptions/`, with its columns and provenance.
Provenance matters here: some files are TRANSCRIBED from public-domain books (our own
work, reusable), some are DERIVED from third-party corpora (subject to their licences),
and some are COMPUTED from either.

---
## transcriptions/ - hand transcription, our own work (CC BY 4.0)

### transcriptions/mackay1938_seal_table/p*.csv -> outputs/mackay_seal_table.csv
Mackay (1938) vol. I, "Tabulation of Seals", printed pp. 369-391. 709 rows, Nos. 1-704
plus 8 addenda. Read from page images; OCR was unusable on this table.

| column | meaning |
|---|---|
| `no` | Mackay's seal number; addenda carry a letter (378A, 686B...) |
| `type` | his seal type: B square with boss, F rectangular inscription-only, C, D, E, A cylinder, etc. |
| `dims_in` | size as printed, in inches; `?` where he prints `?` |
| `material` | steatite unless stated; "ditto after X (as printed)" marks an ambiguous ditto run |
| `block`, `house`, `room` | locus within the DK area |
| `street` | used instead of block/house/room for street, lane and "Bet. Bls." find-spots |
| `level_ft` | depth relative to the DK datum, as printed; `surface` where he prints "Surface" |
| `field_no` | excavation field number (DK nnnnn, SD nnnn, DK.H. nn) |
| `pdf_page` | page of the chapter-XI scan the row was read from |
| `area` | DERIVED from the field number: DK, SD or DK-H |
| `level_dk_ft` | DERIVED: level on the DK datum (SD levels shifted by +2.2 ft) |
| `phase_estimate` | DERIVED from level, using Mackay's average floor levels. APPROXIMATE - see the depth caveat in FINDINGS 22 |

Validation: Mackay's own totals (type B 558 vs 559 transcribed; type F 81 vs 84), his
narrative depths for Nos. 695-703, and the published data for the "Pashupati" seal (No.
420). Printing errors found in the book are listed in that folder's NOTES.md.

### transcriptions/marshall1931_seal_table/p*.csv -> outputs/marshall_seal_table_transcribed.csv
Marshall (1931) vol. II, "Tabulation of Seals", printed pp. 402-405. 560 rows, Nos. 1-557
plus 526b, 528b, 557b.

| column | meaning |
|---|---|
| `plate_no` | Marshall's plate number for the seal |
| `size_in` | size as printed, in inches |
| `level_ft`, `level_in` | depth BELOW THE MODERN SURFACE; `surface` where he prints "Sur."; `B.P.` is his bathing-pavement reference |
| `type` | seal type, as his scheme (the table is ordered by type) |
| `material` | steatite unless stated; colour noted in brackets |
| `area`, `serial` | excavation area (HR, VS, DK, C, E, SD, L, B, BJ, D, DM, F, A, MUS) and field serial |
| `depth_ft` | DERIVED: feet + inches as a decimal |
| `source_page` | which printed page and column the row came from |

**NOT poolable with the Mackay table**: different datum (below modern surface vs fixed
datum) and coarser locus (area only, no block/house/room).

### transcriptions/mackay1938_plates/photo_codings.csv
Text features read from Mackay's seal photographs (vol. II plates LXXXII-XCIX), at
full resolution from the Internet Archive. 531 seals from all thirteen seal plates.

| column | meaning |
|---|---|
| `mackay_no` | seal number, joins to `mackay_seal_table.csv` |
| `plate` | plate the photograph is on |
| `n_signs` | number of signs read; 0 = no inscription or none visible |
| `ends_jar` | does the text END with the jar sign: yes / likely / no / unclear. NB on an impression the reading runs right to left, so the ending appears at the LEFT edge |
| `has_fish`, `has_arrow` | fish and arrow signs, where confidently identifiable |
| `numeral_group` | a group of 2+ plain parallel strokes present |
| `confidence` | high / medium / low; low rows are excluded from all tests |
| `note` | what was seen, in words |
Also in that folder: `recode_sample.csv` (36 seals re-coded blind; kappa 0.89 for the jar
judgement, 97% agreement within one sign), plate box/label JSON, and NOTES.md.

### transcriptions/*/CHAPTER_NOTES.md
Statements from Marshall's and Mackay's narrative chapters that bear on the statistics,
each linked to the finding it supports or corrects.

---
## outputs/ - computed

| file | what it holds |
|---|---|
| `inscriptions_ml.csv` | the working corpus: inscription id, CISI number, site, object type, material, motif, sign count, signs in reading order, sign families, behaviour classes, and `first_occurrence` (the deduplication flag used throughout) |
| `indus_sign_tags.csv` | per sign: visual family, cluster, frequency, shape tags, behaviour class, and share of occurrences in initial / medial / final position |
| `constraints.csv` | 90 mined rules: kind, the signs involved, training support, held-out applications and violations |
| `conditioning_profile.csv`, `conditioning_decay.csv`, `length_control.csv`, `affix_profile.csv` | the cross-corpus structural comparisons, with nulls |
| `concordance_parpola_G.csv`, `concordance_m77_G_inferred.csv` | sign concordances between the corpora used |
| `typology_metrics.csv`, `seal_legend_comparison.csv` | writing-system typology and the Mesopotamian seal-legend comparison |
| `marshall_seal_table.csv` | SUPERSEDED OCR version of the Marshall table; kept only for comparison with the hand transcription |
| `findspots_mackay.csv` | seal mentions parsed from Mackay's narrative text (7 with explicit levels) |
| `*_atlas.png` | rendered sign atlases by family and by behaviour class |
