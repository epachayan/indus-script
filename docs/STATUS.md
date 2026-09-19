# Status of every finding

Each of the 41 sections in `FINDINGS.md` is marked here as **standing**, **qualified**,
**retired**, or **replicates published work**. A finding is *standing* if it has a null or
control, survived any test we ran against it, and is not known to duplicate the literature.

## Standing
| # | finding | why it holds |
|---|---|---|
| 8 | Not a stock book | 5 independent measures; Proto-Elamite contrast |
| 9 | Robust to reading errors | result unchanged when uncertain signs dropped |
| 14 | Corpus alignment and concordances | verified against 161 shared seals |
| 19 | Mackay seal table as data | validated against Mackay's own totals |
| 25 | Coding reliability | blind re-coding, kappa 0.89 |
| 27 | Validated constraint set | held-out: 2,585 applications, 1.08% violations |
| 30 | Ending slot: class, dependency, replication | replicated at Harappa; dependency survives dropping stock pairs |
| 31 | Conditioning strength vs real writing | size-corrected, excess over own null |
| 34 | Two registers modelled separately | large effects, independent corroboration in 41 |
| 37 | Genre-matched Egyptian labels | the key contrast: Egyptian labels are title-first, Indus fixed-last |
| 38 | Determinative-like signs | functional not visual; Egyptian fingerprint applied |
| 39 | Text families | x8.9 and x24.5 over null; families small |
| 40, 41 | Excavators' narrative | primary-source statements, four independent agreements |

## Qualified (true as stated, but narrower than first reported)
| # | finding | the qualification |
|---|---|---|
| 2 | Signs vs animal motifs | holds after deduplication; corroborated by Marshall (40) |
| 5 | Foreign finds | small n (15 texts); suggestive not conclusive |
| 11, 16 | Sequence ML | near-duplicate leakage; neural adds nothing |
| 17 | Mohenjo-daro core | pooled registers (see 34); single-line figures hold |
| 18 | "3 + arrow" | REINTERPRETED by 24: a second-line formula, not an ending inside one line |
| 20 | Matching feasibility | negative result: size alone cannot identify seals |
| 21 | What the plates give | superseded in part: full-resolution images later obtained |
| 22, 23 | Text vs archaeology | nulls at 6 sample sizes up to n=419 (complete coded corpus); depth is a weak proxy (caveat in 22) |
| 24 | Two-line texts | CORRECTED: parts are lines, not object faces |
| 26 | Marshall table | the table stands; the type F trend it tested does NOT (see Retired) |
| 28 | Suffixing or prefixing | rules out prefixing; does not evidence suffixing |
| 29 | What kind of slot | synthetic control overshoots, so not a closed-suffix ID system |
| 32 | Shape of the conditioning | (a) and (b) stand; the periodicity reading is qualified by 33 |
| 33 | Length control | shrank 32's claim; the non-first-order result survives |
| 35 | Astral reading | distributional evidence only; does not touch iconographic arguments |
| 36 | Egyptian comparison | Later Egyptian, so script-type not chronological; POS calibration is the useful part |

## Retired
| # | claim | why |
|---|---|---|
| 19/22 | Type F seals commoner nearer the surface | FAILED to replicate on Marshall's independent data (rho +0.001, p=0.98) |
| 23 | Text length differs between blocks (p=0.06 at n=127) | vanished at n=190 and n=254 |
| 32 | Indus lacks mid-range periodicity because it is formulaic | partly a length artefact (33) |

## Replicates published work (keep as calibration, do not claim)
| # | finding | prior work |
|---|---|---|
| 3, 6 | Positional classes, text template | Yadav/Rao/Mahadevan 2010; Koskenniemi & Parpola |
| 7 | Two stroke systems as numerals | Mahadevan; Kriger & Hunt 2026 |
| 12, 13 | Name-slot uniqueness | Kriger & Hunt 2026 (98.3% unique, same corpus) |
| 15 | Statistics within the range of writing systems | Rao et al. 2009 and the debate after it |
| 18 | Jar and arrow not co-occurring | Mahadevan 2011 (read as gender markers) |
| 1, 4, 10 | Sign families, Harappa tablet habit, Proto-Elamite contrast | broadly known; our versions are quantified |

## What the project actually contributes
1. Two machine-readable seal tables (Mackay 709 rows, Marshall 560 rows) with find-spots.
2. A held-out validated constraint set any proposed reading must satisfy.
3. Genre-matched and script-type-matched structural comparisons (Sumerian seal legends,
   Egyptian labels, Linear B, Egyptian running text) with size and length corrections.
4. A set of well-controlled negative results, including one failed replication of our own.
