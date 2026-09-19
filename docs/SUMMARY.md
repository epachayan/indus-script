# Summary of findings (19 September 2026)

Full detail: `FINDINGS.md` (41 sections). Method and controls: `APPROACH.md`.
Which findings stand, and which were retired: `STATUS.md`.

## Datasets produced
- **Mackay 1938 seal table**: 709 rows, machine-readable, with block, house, room, level
  and field number. Validated against Mackay's own totals and the published data for the
  "Pashupati" seal.
- **Marshall 1931 seal table**: 560 rows with excavation area and depth below surface.
- **531 seals coded from all thirteen plates** (419 usable with find-spots) - the complete
  set of Mackay's photographed Mohenjo-daro seals; coder reliability kappa 0.89.
- **90 held-out validated constraints** (`outputs/constraints.csv`).

## Strongest structural results
- Indus sequences carry dependencies **a first-order model cannot produce**: 7-8% excess
  conditioning out to distance 5, where a bigram model of the same corpus gives 0.4%.
- Adjacent signs constrain each other **as tightly as syllables inside a Greek word**
  (26.5% excess vs 19.8% Linear B words, 14% Sumerian), and far more tightly than words
  inside a line (Greek phrases 4.2%).
- **Strongly directional**: forward prediction easier than backward by 0.50 bits, an order
  of magnitude more than Greek or Sumerian, in the assumed reading direction.
- **The ending is a preferred but open slot**: 133 signs occur there, 44 cover 90%, the
  jar takes 43%. A synthetic identifier scheme overshoots the asymmetry, so it is not a
  closed terminator set.
- **Replicated at Harappa** (743 texts): same asymmetry, same conditioning strength.
- **Frequent and rare signs differ** (22-26% vs 8% conditioning): consistent with a mixed
  system rather than one uniform sign type.
- **Two registers**: a fifth of inscriptions have a second line from a partly different
  sign stock, coupled to how the first line ends.

## Readings the data do not support
- **Ledgers / stock records**: counts are small, rarely repeated, never totalled; Proto-
  Elamite accounting tablets differ sharply on every measure.
- **Container or section labels**: 93% of Mohenjo-daro texts occur exactly once.
- **Astral or calendrical**: no closed name inventory of any size (mutual-exclusion groups
  sit at chance), and "numbered fish" is productive, not a fixed catalogue.
- More generally, **any reading needing a short list of recurring names** - deities,
  months, commodities, measures - fails the repetition test.

## Claims retired during the work
- The type F trend over depth **failed to replicate** on Marshall's independent data.
- The "3 + arrow" ending was reinterpreted once line structure became visible.
- The periodicity claim shrank after a length control.
- A novelty audit found most script-internal findings replicate Yadav et al. (2010),
  Mahadevan, Mukhopadhyay, and Kriger & Hunt (2026).

## Added after the first summary
- **Genre-matched Egyptian control (37)**: Egyptian title-and-name labels, same centuries,
  same function, put the FIXED element first and the variable name last. Indus does the
  opposite. The fixed-final slot is not a property of label texts in general.
- **Determinative-like signs (38)**: 6.4% of Indus tokens match the distributional
  fingerprint of Egyptian determinatives (7.8% there), but Indus signs are far more
  polarised between final and non-final.
- **Text families (39)**: minimal pairs run 9x above chance and variation sits in the
  middle slot, but families are small - most texts have no one-sign relative.
- **The excavators' own words (40, 41)**: Marshall and Mackay independently report the same
  inscription over different animals, the same text on two different seals, two-line seals
  read as name-plus-addition, and right-to-left writing. Four agreements with measurements
  made 90 years later.

## Position
No decipherment, and none reachable from this evidence: the texts are too short, there is
no bilingual, and the language is unknown. What is offered here is data plus controlled
constraints that any proposed reading must satisfy.
