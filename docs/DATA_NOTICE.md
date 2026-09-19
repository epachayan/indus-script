# Data notice

The MIT licence covers the code in `scripts/` only. No third-party data is stored
in this repository; `setup.sh` fetches it from the original sources at pinned commits.

| Source | Licence / terms | Used for |
|---|---|---|
| joyboseroy/indus_decipher | MIT | Indus corpora (G, M77, CISI) |
| yajnadevam/indus-website | GPL-3.0 | SQL dump (object types, sizes, variant pairs), sign font mapping |
| SK Indus Script font (in indus-website) | (c) Shabir Kumbhar, all rights reserved | Rendering signs for shape analysis only |
| mwenge/lineara.xyz, linearb.xyz | code dedicated to the public domain; transcriptions of published corpora | Typology comparison |
| Mackay 1938, Further Excavations at Mohenjo-daro (Internet Archive OCR) | out of copyright | Seal find-spots |
| CDLI data dump (cdli-gh/data) | CDLI terms of use | Proto-Elamite, seal legends, admin texts |

Notes before publishing outputs:
- `outputs/*.png` render glyphs from the SK Indus Script font. They are git-ignored;
  do not publish them without the font owner's permission.
- All of `outputs/` is git-ignored: several tables are derived partly from the GPL-3.0
  SQL dump. Users regenerate them with `run_all.sh`; CI uploads them as build artifacts.
- Readings of individual inscriptions ultimately come from Parpola (CISI), Mahadevan
  (1977) and related corpora; cite them in any write-up.

## Thesaurus Linguae Aegyptiae (Egyptian comparison corpus)
Source: https://huggingface.co/datasets/thesaurus-linguae-aegyptiae (TLA v18).
Licence: CC-BY-SA 4.0. Not redistributed here; place the JSONL as
`data/tla_egyptian.jsonl`. Attribution: Thesaurus Linguae Aegyptiae, Berlin-
Brandenburgische Akademie der Wissenschaften. Any derivative distribution of this
corpus or of data derived from it must carry the same licence.
Two sets are used: LATER Egyptian (-1539 to -332) as `data/tla_egyptian.jsonl`
(FINDINGS 36) and EARLIER Egyptian (-3350 to -1539, contemporary with the mature Indus
phase) as `data/tla_egyptian_earlier.jsonl` (FINDINGS 37).
