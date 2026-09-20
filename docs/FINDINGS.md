# Findings log (Sep 2026)

Numbers are reproduced by `run_all.sh`; the log file for each is in brackets.
"Texts" means deduplicated inscriptions unless stated. The stated exception, found by
external review after first publication: sections 29-33 (`slot_tests.py`,
`slot_followups.py`, `conditioning_compare.py`, `conditioning_shape.py`) do not apply the
`first_occurrence` filter. The results survive deduplication at a smaller magnitude - see
the note at the head of section 29 and `docs/RESEARCH_NOTE.md` §3.

## 1. Visual classification [cluster, finalize, refine]
- 698 signs rendered; 36 shape clusters, refined to named families. 69 signs remain
  in "(mixed)" groups.
- Known variant pairs land in the same cluster 31% of the time vs 3% by chance.

## 2. Signs vs animal motifs [motif, motif_dedup, site, objtype, mj_motif]
- Apparent sign-animal links mostly vanish after deduplication
  (association 0.124 -> 0.087; shuffled baseline 0.075).
- G400 looked tied to fish/rhino motifs; it is really a Harappa TABLET habit
  (38% of Harappa tablets vs ~5% of seals everywhere; p ~ 6e-9).
- Mohenjo-daro: unicorn (603) vs other-animal (214) texts show no difference on
  any of 9 template features. Text and animal carry independent information.

## 3. Behaviour classes [functional, crosscheck]
- 123 signs (>=10 uses, 86% of tokens) fall into 10 classes: text-final markers
  (jar G740, G400, G520, side-loop figures; 75% final), pre-final (forked stems),
  openers (G861, G817, G820; 75% initial), fish core, strict medial connectors
  (G2, G1, G60), numerals, etc.
- Look-alike and behave-alike agree only weakly (AMI 0.096, p=0.002).
  Jar G740 is final, but look-alikes G741/G742/G760 are strictly medial: likely
  different signs, not variants.

## 4. Harappa tablet formula [g400]
- G400 is last in 95% of its tablet texts, after the jar in 61%.
- Most common tablet text: G176 G740 G400 (22 tablets).

## 5. Foreign finds [abroad]
- 15 inscriptions from Mesopotamia, Gulf, Oman, Iran, Central Asia scored against
  a sign-order model of 1,869 homeland texts.
- Kish, Gonur Depe, Ra's al-Junayz read as normal Indus (Kish/Gonur end in jar).
- All 5 Bahrain texts, Susa, Luristan and both Ur texts are atypical;
  8/15 below homeland 10th percentile (expected 1.5; p ~ 3e-5). No Gulf text ends
  in the jar.
- G91 (paired figures) on 3/5 Bahrain texts vs 0.3% of homeland texts, and always
  followed by a stroke numeral.

## 6. Mohenjo-daro text template [mj_segment, mj_subst, m77]
- 1,008 texts; 41% of signs sit in fixed pairs/triplets.
- Template: [opener + G2/G60/G1] ... [numeral + item] ... [pre-final + jar G740]
  + optional closer (G90 or G400).
- 128 minimal-pair texts: openers swap with each other; numerals G3/G4/G5 swap;
  G235/G240, G390/G407, G705/G706 swap (likely true variants); G740/G151 swap
  as endings.
- Replicated in M77 (1,761 lines): 3 mutually swapping openers, one marker after
  them 70% (vs 75%), jar final 74%, 45% of signs in blocks.

## 7. Numerals [numerals, stock]
- Values assigned: short strokes G1-G5, G7; tiered G16-G19 (6-9);
  long strokes G31, G32, G33, G35.
- G2 ("two short strokes") is used 505 times, mostly after openers: a marker,
  not a count.
- Short/tiered and long strokes are different systems (divergence 0.53 vs 0.23
  shuffled, p=0.003): forked stems take short/tiered (75:6 after merging
  variants); fish, jar, arrow take long.
- Forked stems take the widest range of values (2-8): best "unit" candidate.
- Main fish G220 takes 1, 2, 3, 4, 6; other fish variants 1-2 values only.

## 8. "Stock book" hypothesis [stock, size_tab]
- Not supported for seals or tablets: only 23-28% of texts have a count, at most
  2-3% have 2+ number-item entries, 84% of counts are <=3, max 9, no totals,
  34% of texts exactly duplicated (31% near-duplicated by one sign).
- Harappa tablets and seals number different items (tablets: jar, U-vessel,
  G156; seals: fish, G900, forked stems).
- Seal size: no difference between numbered and plain seals once text length is
  controlled (size vs length rho 0.37). ~98% steatite either way.

## 9. Robustness to errors [robust]
- Dropping uncertain readings (M77) or merging 17 variant groups leaves the main
  results unchanged (jar final 71%/74%, multi-entry 3%, numeral split intact).

## 10. Proto-Elamite comparison [proto_elamite]
- 1,343 Proto-Elamite tablets (mostly Susa) parsed from CDLI.
- Proto-Elamite is a true ledger: 96% of tablets have numbers, 80% have 2+
  numbered entries (median 4), 41% have a numbered line on the reverse (typical
  total position), repeat counts up to 11 and higher units in 47% of entries.
- Indus is not: 41% of texts have any stroke numeral, 3% have 2+ entries,
  no totals.
- Both tie number systems to commodities. Items sticking to one system >=90%:
  Proto-Elamite 48% (shuffled 14%); Indus 37% (shuffled 3%).
- Order differs: Proto-Elamite writes item then number; Indus writes number
  then item.
- Reading: the Indus script had commodity-specific counting like its western
  neighbour, but the surviving objects use it inside short formulaic titles,
  not accounts.

## 11. Sequence ML [ml_sequence]
- Next-sign prediction, 5-fold CV on 1,869 homeland texts: perplexity 86 (unigram)
  -> 37 (bigram); top-1 accuracy 21-24%, top-5 43-44%. Trigrams and behaviour-class
  back-off add nothing: texts are too short, most structure is between neighbours.
- A 10-state HMM, given no labels, recovers the template: opener state
  (G861/G820/G817, 91% initial) -> marker state (G2/G60/G741) 90% of the time;
  numeral and fish states mid-text; pre-final state -> jar state (G740/G520/G151)
  80%; closer state (G400/G90, 89% final) -> end. Agreement with the hand-built
  behaviour classes: AMI 0.39.
- Foreign texts rescored with the stronger model: same picture (8/15 below
  homeland 10th percentile). Kish, Gonur Depe and Ra's al-Junayz fit (50-74th
  pct); Ur, Susa, Luristan and Bahrain seals do not. Salut (Oman) now also
  scores atypical (3rd pct).

## 12. Indus vs deciphered seal legends [seal_legends]
- 10,965 distinct Sumerian (7,624) and Akkadian (3,341) seal legends from CDLI,
  c. 2300-1900 BCE. Typical template: NAME > (TITLE) > FILIATION > (SERVANT);
  first line is a name in 68%, a deity or king in 23%.
- Sign inventory: at 5,000 tokens Indus has 479 distinct signs, like cuneiform
  SIGNS (415-461), far below cuneiform WORDS (1,295-1,714).
- Sequencing: bigram/unigram perplexity ratio Indus 0.47, like cuneiform WORDS
  (0.40-0.60), not signs (0.17-0.23). Text length 5 signs ~ legend length in words
  (4.5). Fixed-block share 40%, between words (19-24%) and signs (61-67%).
- Reading: Indus signs pattern like whole words or morphemes drawn from a sign-sized
  inventory - consistent with largely logographic writing.
- Endings: Indus is far more fixed at the end (top closer 39%, end entropy 4.5)
  than Mesopotamian legends (top closer <=12%, 6.4-9.1). A fixed title or suffix
  on most texts fits better than a free name.
- Openers: fixed Indus openers start 22% of texts, close to the 23% of
  Mesopotamian legends that open with a deity or king (suggestive only).
- Numbers: 0% of Mesopotamian seal legends vs 42% of Indus seals. If Indus seals
  are name/title legends, their numbers belong to titles or names - unlike
  Mesopotamia.

## 13. Where would names be? [name_slot, numbered_titles]
- Indus seal texts split by the template into OPENER unit, CORE (middle) and
  ENDING unit, compared with Mesopotamian legend slots (sign level).
- CORE behaves like the Mesopotamian NAME slot: its most common value covers only
  1% of uses (NAME 1%), mean length 4.2 signs (NAME 3.8), mostly built from
  recurring pieces (68%; NAME 89%). It is even more varied: 96% of core strings
  occur once (NAME 75%), so the core probably holds a name plus other elements
  (43% of cores contain a count sign).
- ENDING behaves like a fixed title slot: 13 distinct forms, the top one 67% of
  uses (Mesopotamian TITLE: top form 58%). OPENER: 12 forms, top 27% (like the
  ROYAL/SERVANT slots, 22-27%).
- Numbered ranks exist in cuneiform admin texts but are rare and round:
  "overseer of 60" 126x, "overseer of 10" 23x, among ~613,000 numbered lines.
  Indus counts are small, not round (1-3 = 80% of values; nothing above 9), so
  they do not look like group-size ranks.
- Number order: Sumerian admin lines put the number first in 81% of numbered
  lines (Akkadian 54%), matching Indus number-before-item order; Proto-Elamite
  puts the item first.
- Working model: [opener/affiliation] + [name-like core, often with a small
  number] + [fixed title/ending]. Small counts inside the core could be part of
  names, or a counted item in a role description.

## 14. Corpus alignment and sign concordances [align_cisi, align_m77]
- G corpus vs Parpola-numbered CISI digitisation: 161 shared Mohenjo-daro seals,
  same storage direction. Position-wise agreement 90% on equal-length texts;
  79% of 895 aligned sign pairs follow the dominant mapping; 21/161 seals differ
  in length (a sign read or omitted in only one corpus).
- Parpola lumps signs we found to be interchangeable: P385 = G861/G817 (openers),
  P086 = G390/G405/G407 (forked stems), P230 = G550/G798/G555. Independent
  confirmation of the minimal-pair results (section 6).
- G vs Mahadevan (M77), no shared IDs: mapping inferred from behaviour, then
  self-trained on near-identical texts. 153 signs mapped (91% of M77 tokens);
  188/1,501 M77 texts of 4+ signs become verbatim G texts (frequency-rank
  baseline: 0). Recovered: M342=G740 jar, M99=G2, M123=G60, M1=G90,
  M176=G400, M150=G692; M267 and M391 both map to G820 (openers).
- Reading disagreement between corpora is real (~10-20% of sign positions) and
  should be treated as noise in any model.

## 15. Writing-system typology [typology]
- Same metrics for 10 corpora: Indus, Linear A (sealings, other), Linear B
  (signs, words), proto-cuneiform, Proto-Elamite, Sumerian admin, Sumerian seals
  (signs, words). Samples of up to 1,500 distinct texts each.
- Sign inventory at 4,000 tokens: Indus 437, in the logo-syllabic range
  (Sumerian 387-474, Proto-Elamite 620, proto-cuneiform 673), well above the
  syllabaries (Linear A 234, Linear B 131) and far below word vocabularies
  (1,164-2,108).
- Sequencing (predictability gain, block structure, start/end entropy): Linear B
  signs is Indus's nearest neighbour under every leave-one-feature-out test;
  second place varies (Linear A, Proto-Elamite, Sumerian).
- Reading: Indus statistics sit inside the range of real, language-writing
  systems that mix signs and numerals, with a logo-syllabic-sized inventory.
  Not evidence of any particular language. Linear A sealings (63 texts) too small
  to use.

## 16. Neural next-sign model and leakage [neural_nextsign]
- MLP (previous two signs + their shape family and behaviour class + position),
  top-150 targets, 3 folds.
- Random split: MLP 38.7% vs bigram 36.5% top-1. Near-duplicate-grouped split:
  MLP 35.9% vs bigram 37.0%. The apparent neural gain is leakage from
  near-identical texts; with current data a neural model adds nothing.
- Grouping by one-edit neighbours chains into one large group (618 texts): a
  stricter grouping is a refinement to consider.

## 17. Inside the Mohenjo-daro core [mj_core]
706 distinct MJ seal texts (3+ signs), split into opener unit / core / ending,
cores segmented with strong sign pairs (3.4 units per core).
- The last core unit is NOT a closed title set: 242 forms, commonest 5%, top-10
  cover 22% (Mesopotamian titles: commonest 58%). "Name + title" inside the core
  is not supported in that simple form.
- But the last unit depends strongly on the ending (p ~ 3e-40): G760/G923/G100
  before the jar; G390 when there is no ending; fish G220 and "G705/G706 + G33"
  before the arrow G520. Pre-final sign + ending behave as fixed pairs, so the
  ending is best treated as a two-part unit.
- A jar inside the text (14% of MJ seals) is mostly followed by the closer G90
  (31 of 97), and what follows almost never looks like a text start (2% vs 10%
  baseline). No evidence of two texts joined; the ending can stack
  (pre-final + jar + closer).
- Openers G820/G817/G861/G692 are indistinguishable on everything tested (core
  length p=0.46, ending p=0.62, counts, motif) - consistent with Parpola treating
  some of them as one sign.
- Texts with an opener have the same total length (5.2-5.9) as texts without
  (5.4) but shorter cores (2.6-3.3 vs 4.7): the opener unit takes the place of
  about 1.5 core signs, i.e. it fills the first core slot rather than being an
  extra element.
- Counts sit mid-core (mean relative position 0.51). Short-stroke counts go with
  forked stem G390, fish G220, G585, G900; long-stroke counts mostly with fish
  G220 (28 of 154).
- Two-part endings (pre-final + ending) are not a closed set either: 156 forms,
  top-10 cover 35% (the ending sign alone: 13 forms, top-1 67%). The fixed part is
  the ending sign; the sign before it varies but prefers particular endings.
  Counts sometimes stand right before the ending ("G33 G520" 19x, "G32 G740" 9x),
  so the jar/arrow may at times be the counted item. Tested: when a count stands
  right before the ending, the ending is the arrow G520 in 54% of cases (12%
  otherwise; p ~ 2e-10), almost always with long-stroke 3 (G33, 20x) or 2 (G32,
  10x). "2/3 + arrow" is a formula in which the arrow behaves like a counted item
  or unit, not only a closing sign.
- No second kind of opener: without an opener the first core sign is open
  (196 forms, top-5 cover 19%; commonest G920), and the same signs (G235, G32,
  G803) start the core whether or not an opener precedes it.
- Openers look like an optional prefix. The shorter cores beside them are not a
  space limit: seal width (27.9 vs 27.5, p=0.21) and signs per unit width
  (p=0.38) are the same. Texts seem held to a conventional length of about 5
  signs, so an opener displaces part of the core.
- Revised model: [optional opener unit] + [open core, often with a count] +
  [constrained pre-final sign] + [fixed ending sign] (+ closer).

## 18. The "3 + arrow" formula across sites [count_arrow]
- The count before the arrow G520 is almost always long-stroke 3 (G33):
  26 of 27 at Mohenjo-daro, 10 of 11 at Harappa.
- It is a seal formula: 26% of arrow texts on MJ seals and 35% on Harappa seals
  use it, but only 11% on Harappa tablets and none on seals from other sites.
- The arrow replaces the jar: the jar appears in only 7% of arrow texts at MJ
  (57% of other texts; p ~ 4e-23) and 2% at Harappa (54%; p ~ 4e-13).
  The arrow is last in 138 of 167 arrow texts.
- Reading: "3 + arrow" is an alternative ending to the jar, shared by the two
  big cities' seals. The fixed number 3 suggests a set phrase (a title or
  standard quantity), not a live count.
  SUPERSEDED IN PART by section 24: in the corpus that preserves object parts, these
  arrow formulas are mostly SECOND inscriptions on an object, not endings within the
  main text.

## 19. Mackay's seal table: context without texts [build_mackay_table, mackay_context]
- Complete hand transcription of Mackay (1938) "Tabulation of Seals": Nos. 1-704 plus
  8 addenda (709 rows, 693 distinct seals by field number). Validated against Mackay's
  own totals (type B 558 vs 559 transcribed; type F 81 vs 84), his rare-type lists
  (differences traced to the book itself), his narrative depths, and the published
  data for the "Pashupati" seal (No. 420).
- Inscription-only rectangular seals (type F) become more common over time: about 5%
  of seals in Intermediate II-III, 10% in Intermediate I, 13-19% in the Late phases
  (B vs F across phases p=0.019). The square boss seal (B) dominates throughout
  (73-84%).
- Square-seal size does not change with depth (width vs depth rho=-0.06, p=0.17).
- Seals concentrate in Blocks 7 (83), 9 (75) and 1 (70); First Street yields 38.
  26% of seals come from streets, lanes or gaps between blocks. Several rooms hold
  5-6 seals each (e.g. Bl. 4 rm 13, Bl. 9 VII rm 17, Bl. 1 III rm 1) - candidates for
  offices, workshops or stores.
- Phases are estimated from Mackay's average floor levels, so they are approximate;
  "Early" has only 18 seals.

## 20. Before the plates: matching feasibility and seal geography [match_feasibility, mackay_spatial]
- Size is a filter, not an identifier. 639 Mackay seals have two dimensions; 967 CISI
  Mohenjo-daro seals have measurements. The two sources differ systematically
  (Mackay median 26.2 x 23.1 mm vs CISI 27.9 x 24.0); after calibrating (scale 1.015,
  offset -0.5 mm) a +/-0.5 mm window still leaves a median of 10 candidates and gives a
  unique match for only 14%. Reading the signs on the plates is therefore necessary;
  size and shape will serve to confirm.
- Seal types are spread evenly across the city: type F (inscription-only) is 12%
  indoors and 11% in streets (p=0.79), and its share does not differ between blocks
  (4-20%, p=0.84). Whatever type F marks, it is not tied to a quarter or to
  indoor/outdoor use.
- Multi-seal rooms are not single deposits. The 18 rooms with 4+ seals span a median of
  6.9 ft of depth, against 10.8 ft for random same-size groups: tighter than chance but
  still centuries apart. Two are genuinely tight (Bl. 16 II rm 11: 0.6 ft, 4 seals;
  Bl. 1 I rm 74: 2.8 ft). The rest look like the same spot used again and again, which
  is itself evidence that certain houses kept their function over time.

## 21. The plates: what they give and what they don't [vol. II scan]
- Mackay's plates of seals (vol. II, Pls. LXXXII onwards, pages ~178-212 of the scan)
  number each photograph with the SAME numbers as the seal table (Pl. LXXXIV starts at
  No. 54). So every photographed seal already carries a find-spot, depth and phase.
- Full plate coverage secured at high resolution (IIIF `full/full`, ~4855 x 6782 px):
  LXXXII (687-704, seals not impressions), LXXXIII-LXXXIX (1-378, upper levels),
  XCIV-XCIX (379-686, lower levels). Plates XC-XCIII are amulets and copper tablets
  with their own numbering.
- The 300 dpi PDF is too soft for sign reading; at the resolutions above the signs are
  legible. (Earlier note retained: the available scan is ~300 dpi for the whole page,
  so a 1-inch seal's sign band is
  only a few dozen pixels.)
- CISI's M-numbering is NOT Mackay's sequence shifted: testing every offset from -50 to
  1400, the best gives 7% size agreement against a 3.6% chance level, with a median
  size difference of 15 mm. A concordance cannot be derived this way.
- Mackay vol. I now available as text: the narrative parser finds 263 seal mentions but
  only 7 with an explicit level, so the tabulation (section 19) remains the source for
  find-spots.

## 22. Text and archaeology [phase_test]
CAVEAT ON DEPTH, applies to sections 19, 22 and 23: level below datum is a by-product of
debris and rebuilding accumulating, not something the inhabitants controlled. A seal can
be intrusive from above (pits, robbing) or residual from below (redeposited fill), and
Mackay's phases are averages of floor levels, not dated horizons. Depth is treated here
as a rough ordering with error, never as a calendar, and a null result is the expected
outcome if that error is large.

Method: features read directly from the plate photographs (sign count, jar ending),
joined to Mackay's find-spots and levels. 90 seals coded from two plates, 69 usable
(low-confidence, worn and uninscribed seals excluded).
- Two phases compared: Pl. LXXXVIII, 35 seals at -9.4 to -10.8 ft ("Late III"), and
  Pl. XCIV, 34 seals at -12.0 to -13.0 ft ("Intermediate I").
- NO difference found. Sign count 5.8 vs 6.1 (p=0.38); jar ending 40% vs 44% (p=0.81);
  text length vs depth across all 69 seals rho=-0.16 (p=0.18); type F share 17% vs 18%.
- The observed jar-ending rate (40-44%) is close to the corpus-wide 36%, a useful check
  that photo coding agrees with the digitised texts.
- Power: this sample could detect a 30-point difference in jar endings (73% power) or a
  1-sign difference in length, but not smaller ones. A 20-point difference would need
  about 94 seals per group.
- ALL THIRTEEN seal plates now coded (LXXXIII-LXXXIX, XCIV-XCIX): **531 seals coded, 419
  usable with find-spots** - every Mohenjo-daro seal Mackay photographed that carries a
  readable inscription.
  shallow n=135: 5.6 signs, jar 29% | Late III n=82: 5.5, 35% |
  Intermediate n=147: 5.6, 27% | deep n=55: 5.6, 36%.
  Shallowest vs deepest: sign count p=0.56, jar ending p=0.39. Blocks: length p=0.19,
  jar ending p=0.88.
  The null now holds at six successive sample sizes (69, 127, 190, 254, 291, 419) and on
  the COMPLETE coded corpus, not a sample of it. Mean sign count is 5.5-5.6 in every band.
- (Earlier 127-seal figures, superseded:
  shallow (Late I-II, -4.9 to +2.0 ft) n=32: 6.0 signs, jar 28%
  Late III (-9.4 to -10.8) n=35: 5.8 signs, jar 40%
  Intermediate I-II (-12.0 to -13.0) n=34: 6.1 signs, jar 44%
  deep (Int III / Early, -20.0 to -24.4) n=26: 5.9 signs, jar 42%)
- Shallowest vs deepest: sign count p=0.41, jar ending 28% vs 42% (p=0.28). No trend
  across the four bands (sign count rho=-0.04, jar rho=+0.11, both n.s.), and text
  length does not track depth (rho=0.01, p=0.91).
- The one real change is in the OBJECT, not the text: inscription-only type F seals grow
  from 12% of the deepest band to 25% of the shallowest, and on the full table of 697
  seals type F becomes commoner nearer the surface (rho=+0.13, p=0.0008). This confirms
  section 19 from an independent angle.
- Reading: over roughly 26 ft of deposit - most of the city's occupation - seal TEXTS at
  Mohenjo-daro look stable in length and in their endings, while the mix of seal SHAPES
  shifts. The writing formula outlasted the object conventions.
- Power: with these group sizes a 30-point difference in jar endings would be caught
  (65% power); 20 points needs about 94 per group.

## 23. Space, numerals and the remaining photo features [neighbourhood_test, numeral_test]
- Space rather than depth: 127 coded seals, 94 found indoors and 32 in streets or between
  blocks. No difference in text length (5.9 vs 6.2 signs, p=0.21) or jar endings
  (37% vs 44%).
- Across blocks: with 127 coded seals text length looked marginally different between
  blocks (p=0.06); at 190 it did not (p=0.28) and at 254 it still does not (six blocks
  with 8+ seals, p=0.13; jar endings p=0.55). The earlier hint was noise, which is worth recording as a warning about
  reading marginal p-values in this material.
- Stroke-group numerals coded on the two extreme plates (58 usable seals): present in 55%
  of the shallow set and 37% of the deep set (p=0.20), so no demonstrable change.
- Validity check: texts containing a stroke group are longer than those without
  (6.3 vs 5.1 signs, p=0.025), the arithmetic you would expect if the strokes are part
  of the text rather than decoration.
- Fish and arrow signs could only be identified confidently on a handful of seals at this
  resolution; they are recorded as "likely"/"unclear" rather than counted, and no test
  was run on them.
- Corrections applied: the seal first recorded as No. 1 on Pl. LXXXIII is No. 40; the
  flagged No. 287 on Pl. LXXXVIII was rechecked and is correct.

## 24. Two-line texts have a main line and a formulaic second line [object_parts]
Prompted by the question of whether a seal is read as an independent unit. The Mahadevan
corpus keeps the parts of an inscription (ids "1001.1", "1001.2"); the G-numbered
digitisation does not.
FIRST CHECK (what the parts are): every M77 row has line_count = 1 and the parts of an
object share site and reading direction, so the parts are the LINES of one inscription,
not the faces of an object. The earlier wording of this section ("one inscription is not
one message") overstated it: this is about line structure, not separate inscriptions.
The face question remains open and needs CISI or the plates.
- 607 of 2,906 inscriptions (21%) run to more than one line, usually two.
- The second line is not a continuation of the first. Joining them in either order fails
  to reproduce a normal text: line1+line2 ends with the jar 13% of the time and
  line2+line1 21%, against 34% for single-line texts. Line 1 alone (21%) is the closest.
- Second parts are short (2.5 signs vs 3.3 for first parts, p~2e-19) and highly formulaic:
  the three commonest are M89+M328, M87+M328 and M95+M328 - in our sign numbering
  G742+G520, G32+G520 and G231+G520, that is [jar variant | "two" | fish] + ARROW.
- 46% of second lines end with the arrow G520, against 0.1% of single-line texts. The
  arrow formula is therefore not an alternative ENDING competing with the jar inside one
  line (as section 18 assumed) but the ending of a second line whose main text is the
  line above.
- The G-numbered corpus behaves like the single-line population (4.6 signs, jar-final 35%,
  arrow-final 7%), so it appears to record mostly single lines rather than joining them.
  Our template work therefore describes single lines, which is coherent, but it says
  nothing about how a second line relates to the first.
- The two lines are not independent: when the second line is the arrow formula, the first
  line ends with the jar more often (26% vs 17%, p=0.007).
- Revises section 18. Reading: a fifth of inscriptions are a main line plus a short
  standard second line, the second usually ending in the arrow. Whether that second line
  is an endorsement, a category label or a quantity cannot be told from form alone.
- The face question, pursued as far as our sources allow:
  * Mackay's own type list marks types C and D as "frequently inscribed on both sides":
    33 of 701 seals (5%).
  * His plates publish only ONE face per seal, including for those 33 (checked visually
    for Nos. 292, 327, 329, 405, 414, 636, 643, 658). The second face is not illustrated.
  * The CISI digitisation in this repo uses face letters in its ids but contains only
    "A" faces for all 179 seals, so it records no second faces either.
  * Conclusion: with open sources, two-sided objects can be counted (about 5% of seals)
    but their second texts cannot be read. Answering it needs the CISI volumes or museum
    photographs of the reverses.

## 25. How reliable is the photo coding? [recode_agreement]
36 coded seals drawn at random across the eight plates and re-coded blind.
- Sign count: exact agreement 61%, within one sign 97%; mean difference +0.14 signs
  (sd 0.67), so no systematic drift between passes.
- Jar ending: agreement 97%, Cohen's kappa 0.89.
- Only two disagreements: No. 316 (jar ending judged differently) and No. 412 (one pass
  saw no signs, the other two).
- Reading: the binary judgement (does it end with the jar) is reliable; exact sign counts
  are not, but are accurate to within one sign, which is the precision the tests in
  sections 22-23 actually use. The nulls in those sections are therefore not explained by
  coding noise.
- Caveat that remains: both passes are by the same coder, so this measures consistency,
  not accuracy. A second person could still read these photographs differently.

## 26. Marshall (1931): an independent seal table, and a failed replication
[build_marshall_table, marshall_test]
- Marshall vol. II has its own "Tabulation of Seals" (pp. 402-405) for the 1922-27
  seasons: plate no., size, level below the modern surface, type, material and
  site+serial (HR, VS, DK, C, E, SD, L, B, BJ, DM). Roughly 450 seals.
- Unlike Mackay's tables this one OCRs reasonably: 356 rows recovered, with area and
  serial reliable, levels for 239, sizes for 67, printed plate numbers for about half.
- The table is ordered by seal TYPE (type B runs at least to no. 350), so types can be
  assigned from block boundaries rather than read row by row.
- Two things make it NOT directly comparable with Mackay: levels are below the modern
  surface, not a fixed datum, and the locus is only the excavation area, not block and
  room. It is best used as an independent sample for within-Marshall tests.
- Transcription COMPLETE: 560 rows (Nos. 1-557 plus 526b, 528b, 557b), no gaps or
  duplicate numbers, 516 with a depth. Areas: HR 201, VS 85, DK 62, C 61, E 57, the rest
  smaller. Types: B 413, F 68, E 20, C 15, D 8, plus singletons.
- THE TYPE F TREND DOES NOT REPLICATE. On Mackay's 697 seals, inscription-only type F
  seals are commoner nearer the surface (rho=+0.127, p=0.0008). On Marshall's 511 seals
  with a type and a depth, the correlation is zero (rho=+0.001, p=0.98; median depth
  3.5 ft for type F vs 4.0 ft for the rest, p=0.98), and the banded pattern is
  non-monotonic (21% F in the top 2 ft, 12%, 8%, then 17% below 6 ft). No individual
  area shows it either (five areas with 25+ seals, all |rho| < 0.07).
- This was the one positive result in the project. It now has an independent test that
  fails. Possible reasons, none verified: the two dig teams measured depth differently
  (fixed datum vs below the modern surface, which mixes in mound topography); they worked
  different parts of the site; or Mackay's trend is an artifact of his areas and levels.
  Whichever it is, the honest position is that the trend is not established.
- What remains solid from this section is the DATA: two independent, machine-readable
  seal tables (Mackay 709 rows with block/house/room; Marshall 560 rows with area), which
  did not exist in this form before.

## 27. A validated constraint set: what any reading must satisfy [constraint_miner]
Rules are mined on a random half of the 954 Mohenjo-daro texts and scored on the other
half, so every rule below is a prediction tested on texts it was not derived from.
Six relationship types are searched: positional, forbidden adjacency, obligatory
adjacency, precedence, co-occurrence exclusion, cardinality.
- 90 rules mined; across 2,585 held-out applications there are 28 violations (1.08%).
  56 rules have 10+ held-out applications and ZERO violations.
- Positional: the jar G740 is never text-initial (245 held-out texts, 1 violation);
  G400, G100, G1, G60 never initial; the fish G220, G240, G233, G235, G176, G705, G803
  never final.
- Forbidden adjacency: 26 pairs that never occur although chance predicts 5 or more. The
  jar G740 is never directly before G2, G32, G220, G520, G861, G390 or G741 - it takes a
  very restricted right neighbour.
- Obligatory adjacency: G100 and G760 are followed immediately by the jar in 96-97% of
  occurrences (1 held-out violation each).
- Precedence: ten signs (G2, G220, G741, G233, G861, G176, G760, G920 among them) always
  appear BEFORE the jar when both are present; G820 always before G2. Held-out
  violations: 2 across 303 applicable texts.
- Cardinality: G2, G240, G861, G741, G1, G233, G235, G400 occur at most once per text.
- No co-occurrence exclusions survive the threshold: notably the jar and the arrow DO
  co-occur (3 held-out texts), which qualifies Mahadevan's mutual-exclusivity reading.
- Use: this is a falsifiable filter. Any proposed reading of these signs must explain why
  the jar cannot open a text, why it refuses specific right neighbours, and why a dozen
  signs always precede it. Output: outputs/constraints.csv (rule, support, held-out score).
- Caveat: these restate and extend known positional results (Yadav et al. 2010; Kriger &
  Hunt 2026); what is added here is the held-out validation and the machine-readable form.

## 28. Suffixing or prefixing? A positional-constraint profile [affix_test]
Prompted by the Dravidian hypothesis: Dravidian is exclusively suffixing, so if the script
wrote a Dravidian-type language its ENDINGS should be far more constrained than its
beginnings. Measured as H(last element) - H(first element) over short sequences, with the
commonest element's share at each end.

| corpus | unit | H(first) | H(last) | difference | commonest last |
|---|---|---|---|---|---|
| Indus, all sites | inscription | 6.95 | 4.51 | -2.44 | 35% |
| Indus, Mohenjo-daro | inscription | 6.64 | 4.22 | -2.42 | 41% |
| Indus shuffled (null) | inscription | 6.76 | 6.70 | -0.05 | 12% |
| Linear B (Mycenaean Greek) | word | 5.25 | 5.03 | -0.22 | 11% |
| Linear B (Mycenaean Greek) | phrase | 8.83 | 5.91 | -2.92 | 24% |
| Sumerian (CDLI admin) | word | 7.32 | 7.23 | -0.09 | 5% |
| Sumerian (CDLI admin) | line | 5.05 | 5.05 | +0.01 | 42% |

- The Indus asymmetry is real: -2.44, against -0.05 for the same signs shuffled.
- But it is NOT word-level morphology. In Linear B, a language we know is suffixing, the
  word-level asymmetry is only -0.22. The Indus figure resembles the PHRASE-level Greek
  value (-2.92), where the constraint comes from phrase structure, not from suffixes.
- Sumerian lines show no asymmetry at all (+0.01) despite a high top-share at the end,
  showing the measure separates the two cases rather than tracking frequency alone.
- Reading: the Indus end-constraint looks like a fixed final SLOT in a formula (a closing
  element that most texts carry) rather than a grammatical ending on a word. This is
  compatible with a suffixing language but does not evidence one: a phrase-final title or
  marker in a non-suffixing language would look the same.
- What it does rule out: a prefixing profile. Whatever the texts are, their variability
  sits at the front and their fixity at the back.

## 29. What kind of slot is the ending? [slot_tests]
NOTE (sections 29-33): these scripts do not apply the `first_occurrence` deduplication
filter used elsewhere (found by external review). The penultimate-to-ending MI in (b), the
strongest single result in the project, drops from z=+39.7 (n=1,028) to z=+31.2 (MI 3.12 vs
2.17 shuffled, n=872) once deduplicated - smaller, still far beyond chance. See
`docs/RESEARCH_NOTE.md` §3 for the full comparison and rationale for reporting both figures.

Three follow-ups to section 28, on 1,028 Mohenjo-daro texts of 3+ signs.

**(a) The ending is narrowed but NOT a closed class.**
| position | distinct signs | signs covering 90% of tokens | commonest |
|---|---|---|---|
| first | 225 | 123 | 7% |
| medial | 328 | 113 | 9% |
| final | 133 | 44 | 43% |
So the final position draws on 133 different signs and needs 44 of them to cover 90% of
cases. That is far too open for a grammatical suffix set or a short list of titles, while
being much narrower than the other positions. The single commonest ending (the jar) takes
43%, so the position is dominated by one sign with a long tail behind it.

**(b) The opener predicts the ending, and the penultimate sign predicts it strongly.**
Mutual information opener->ending 2.273 bits vs 1.904 shuffled (z=+12.0); penultimate
sign->ending 2.988 vs 1.891 (z=+39.7). The slots are not independent: what comes before
constrains what closes the text. That is agreement-like behaviour, though it does not
establish grammatical agreement.

**(c) A meaningless identifier system OVERSHOOTS the asymmetry.**
Matched to the real texts in count, length and top-5 ending shares:
| corpus | H(first) | H(last) | difference | 90% of endings in |
|---|---|---|---|---|
| real | 6.40 | 4.11 | -2.29 | 44 signs |
| synthetic ID (random stems + 5 fixed suffixes) | 8.33 | 2.15 | -6.18 | 5 signs |
| synthetic shared inventory | 6.84 | 2.15 | -4.68 | 5 signs |
A registration-plate scheme produces a much SHARPER asymmetry (-6.2) than the real corpus
(-2.3), because its ending set is genuinely closed. The Indus profile sits between an
unconstrained sequence and a fixed-suffix identifier system.
- Reading: the final position is a strongly preferred but open slot, coupled to what
  precedes it. That rules out both extremes - it is not a free lexical position, and it is
  not a small closed set of terminators - and it is the first result here that a
  meaningless control fails to reproduce by being too regular rather than too irregular.

## 30. The ending slot: class, dependency, and replication [slot_followups]

**(a) A final-preferring group, not a closed terminator class.** Of the 44 signs covering
90% of Mohenjo-daro endings: 4 never occur anywhere else (G161, G842, G423, G592), 13
occur elsewhere but are 70%+ final (the jar G740, arrow G520, G400, G90, G527, G151...),
and 27 occur freely elsewhere. The 17 final-preferring signs take 70% of all endings. So
the position is dominated by a group of signs that specialise in it, with a further third
of endings filled by ordinary signs.

**(b) The dependency is broad, not a few stock phrases.** Penultimate-to-ending mutual
information is 2.99 bits. Dropping the commonest pairs makes it go UP, not down: 3.18
after dropping the top 5 (17% of texts), 3.33 after the top 10, 3.68 after the top 20
(39% of texts). On the remaining 631 texts it is still 3.68 vs 3.05 shuffled (z=+21.9).
The stock formulas are, if anything, diluting a dependency that runs through the whole
corpus. This is the strongest structural result in the project.

**(c) It replicates at Harappa.**
| site | n | H(first) | H(last) | difference | commonest ending | 90% of endings | penult->end z |
|---|---|---|---|---|---|---|---|
| Mohenjo-daro | 1028 | 6.40 | 4.11 | -2.29 | 43% | 44 signs | +39.3 |
| Harappa | 743 | 6.48 | 3.65 | -2.83 | 31% | 24 signs | +37.8 |
Two cities, ~600 km apart, give the same profile: the same front-open/back-fixed
asymmetry and the same strong conditioning of the ending on its neighbour. Harappa is
slightly MORE constrained (24 signs cover 90% of endings vs 44), and its commonest ending
takes a smaller share, so the effect is not driven by one dominant sign.
- Reading: whatever governs the end of an Indus text is a property of the writing system,
  not of one city's scribal habit, and it conditions signs pairwise across the corpus
  rather than through a handful of memorised phrases.

## 31. How strong is the conditioning, compared with real writing? [conditioning_compare]
Mutual information between the last two elements of a sequence, as the share of the
ending's entropy that its neighbour removes. MI is upward-biased in small samples, so
every corpus is subsampled to 1,000 sequences (20 draws) and scored as the EXCESS over its
own shuffled null.

| corpus | unit | excess |
|---|---|---|
| Indus, Mohenjo-daro | signs in an inscription | **26.5%** |
| Linear B words (Mycenaean Greek) | syllabograms in a word | 19.8% |
| Sumerian lines (CDLI admin) | words in a line | 14.7% |
| Sumerian words | signs in a word | 14.1% |
| Indus bigram-generated (control) | signs | 15.3% |
| Linear B phrases (Greek) | words in a phrase | 4.2% |
| Indus signs shuffled (null) | signs | 1.9% |

- The null is near zero (1.9%), so the measure does not manufacture the effect.
- Indus conditioning (26.5%) is at the HIGH end: stronger than word-internal conditioning
  in Mycenaean Greek (19.8%) and than sign- or word-level conditioning in Sumerian
  (14%), and far stronger than Greek phrase-level conditioning (4.2%).
- A bigram-generated control reaches 15.3%, which is the level to beat for "pairwise
  structure only"; the real corpus exceeds it, so the ending is conditioned more tightly
  than a first-order model of the same corpus produces.
- Reading: whatever unit an Indus sign corresponds to, adjacent signs constrain each other
  about as tightly as syllables inside a Greek word - tighter than words inside a line in
  either comparison corpus. That is consistent with an Indus sign being a sub-word unit
  (a syllable-like piece of a longer form) rather than a whole word, though it does not
  prove it: a tightly formulaic word-level system would look similar.

## 32. The shape of the conditioning [conditioning_shape]

**(a) Decay with distance** (excess MI over each corpus's own null):
| corpus | d=1 | d=2 | d=3 | d=4 | d=5 |
|---|---|---|---|---|---|
| Indus (all sites) | 18.9% | 9.3% | 8.5% | 7.8% | 7.1% |
| Linear B words (Greek) | 15.2% | 9.4% | 8.8% | 13.3% | 17.7% |
| Sumerian words (signs) | 10.0% | 9.5% | 13.2% | 15.9% | 15.3% |
| Sumerian lines (words) | 13.4% | 9.9% | 10.4% | 12.8% | 16.4% |
| Indus bigram-generated (control) | 22.2% | 5.3% | 1.7% | 0.7% | 0.4% |
| Indus shuffled (null) | 3.3% | 2.7% | 2.3% | 1.3% | 1.2% |
- The bigram control collapses to nothing by d=3 (0.7%), as a first-order process must.
  The Indus corpus does NOT: it holds 7-8% out to distance 5, so the structure is not
  first-order. That is the cleanest evidence yet that these sequences carry dependencies
  beyond adjacent pairs.
- But the SHAPE differs from the real-language corpora. Greek and Sumerian both dip at
  d=2 and then RISE again at d=4-5 (word-length and phrase periodicity: elements recur at
  a characteristic spacing). Indus decays monotonically and never comes back up.
- Reading: Indus texts have real long-range structure, but they lack the periodic signature
  that marks repeating units of a typical length. SEE SECTION 33: the length control
  resolves which explanation holds.

**(b) Frequent and rare signs behave differently.** How much a sign pins down its
successor, by the frequency of the first sign (Mohenjo-daro):
frequent (50+ uses) 22.5%, mid (10-49) 25.9%, rare (<10) 8.1%.
- Rare signs constrain their neighbours much less. If everything were one uniform system,
  frequency alone should not change conditioning this much. This is consistent with a
  MIXED system - a core of signs with tight combinatorial behaviour plus a tail of signs
  that behave more like free-standing labels - which is what an inventory of 400-700 signs
  would predict.

**(c) Direction - RETRACTED as a directional-predictability claim; see correction below.**
H(next|previous) vs H(previous|next):
Indus 3.02 vs 3.53 (forward easier by 0.50 bits); Linear B words 3.85 vs 4.01 (0.17);
Sumerian words 2.88 vs 2.91 (0.03); Sumerian lines 2.89 vs 2.84 (backward by 0.05).
- ~~The Indus asymmetry is an order of magnitude larger than in either comparison corpus,
  in the direction our stored reading order assumes. The corpus reads consistently in one
  direction, and much more so than known systems - again pointing to a fixed formula whose
  later elements are determined by its earlier ones.~~
- CORRECTION (added after external review, v0.2.5): both conditionals here subtract the
  same mutual information term (`dirs()` in `conditioning_shape.py`), so algebraically
  H(prev|next) - H(next|prev) = H(first-element pool) - H(second-element pool) exactly -
  verified on the committed corpus (MI = 3.396 cancels identically both ways; the 0.502-bit
  gap equals the marginal-entropy difference to three decimal places). This is not an
  independent measurement of predictability; it is the SAME positional entropy gradient
  already reported in FINDINGS 29a/31 (H(first) 6.40 vs H(last) 4.11 at Mohenjo-daro), and
  citing both double-counts one effect as two. It also cannot confirm reading direction: the
  quantity flips sign under reversing every text, so it shows only that fixed material sits
  at one end, and which end is called "last" is the assumption under test, not something
  this statistic can settle - see FINDINGS 37, where a genre-matched Egyptian control shows
  fixity sitting at the FRONT instead. The cross-corpus comparison is further confounded:
  Linear B and Sumerian sequences are longer and closer to stationary, which pushes this
  quantity toward zero in those corpora regardless of any directional structure. Retired in
  `docs/STATUS.md`.

## 33. Was the missing periodicity just short texts? [length_control]
Section 32 found the comparison corpora rising again at distance 4-5 while the Indus
corpus decays monotonically. Indus texts are short (median 4 signs, mean 4.4), so the
comparison corpora were truncated to the Indus length distribution and re-measured.

| corpus | d=1 | d=2 | d=3 | d=4 | d=5 |
|---|---|---|---|---|---|
| Indus (all sites) | 19.7% | 9.9% | 8.7% | 8.1% | 7.1% |
| Linear B words (Greek) | 15.7% | 10.2% | 9.3% | 14.2% | 17.6% |
| Linear B words, truncated | 16.1% | 10.5% | 9.1% | 11.3% | - |
| Sumerian words (signs) | 10.8% | 10.4% | 14.5% | 15.9% | 15.3% |
| Sumerian words, truncated | 13.3% | 10.2% | 14.6% | 10.9% | - |
| Sumerian lines (words) | 14.0% | 10.6% | 11.0% | 13.6% | 17.3% |
| Sumerian lines, truncated | 12.8% | 10.2% | 9.6% | 11.4% | 10.1% |

- Truncation WEAKENS the far-distance rise but does not remove it: truncated Linear B
  still turns up at d=4 (9.1% -> 11.3%), truncated Sumerian words still peak at d=3
  (14.6%), truncated Sumerian lines still rise at d=4 (9.6% -> 11.4%). The Indus corpus
  alone keeps falling at every distance.
- So the difference is real but SMALLER than section 32 implied: part of the gap was a
  length artefact, and the honest statement is that Indus sequences lack the mid-range
  recovery that shortened real-language sequences still show.
- What survives from section 32 unchanged: the Indus corpus holds 7-8% excess conditioning
  out to distance 5 where a bigram model of the same corpus collapses to 0.4%. The
  structure is not first-order; it just does not repeat at a characteristic spacing.

## 34. Two registers, modelled separately [two_register]
Section 24 showed a fifth of inscriptions run to two lines. The template work (section 6)
treated every text as one object. Here the registers are separated: 2,299 single-line
texts, 550 two-line texts.

| | n | mean signs | distinct signs | jar-final | arrow-final | unique forms |
|---|---|---|---|---|---|---|
| single-line text | 2299 | 4.2 | 378 | 34% | 0% | 79% |
| line 1 of a two-line text | 550 | 3.3 | 203 | 21% | 0% | 65% |
| line 2 of a two-line text | 550 | 2.5 | 168 | 13% | 46% | 41% |

- **Line 1 is not just a shorter single-line text.** It is shorter (3.3 vs 4.2 signs,
  p~4e-21), ends with the jar far less often (21% vs 34%, p~2e-09) and repeats itself more
  (65% unique forms vs 79%). Adding a second line changes the first one.
- **The second line is a different register, not a continuation.** Its commonest sign,
  M328 (the arrow G520), takes 18.9% of its tokens but 0.3% of single-line tokens - a
  60-fold difference. M95 is 3.9% vs 0.1%. The jar runs the other way (7.3% vs 10.4%).
  Across 83 signs common to both, frequency ranks correlate only rho=0.57.
- **But the two lines are coupled.** The end of line 1 predicts the start of line 2
  (MI 2.63 bits vs 1.92 shuffled, z=+15.3). Conditioning WITHIN each line is stronger
  (z=+61 and +48), so the boundary is a real break, but not a wall.
- Reading: a two-line inscription is a main statement plus a second element drawn from a
  partly different sign stock, chosen with reference to how the first ends. The closest
  everyday analogue would be a statement plus a countersignature or category mark, though
  form alone cannot settle what it means.
- Consequence for earlier sections: any measurement pooling the registers (sections 6, 17,
  and the template work generally) mixes two populations that differ in length, ending and
  repetition. The single-line figures quoted elsewhere hold, since the G-numbered corpus
  records mostly single lines (FINDINGS 24), but the M77-based figures should be read as
  register-mixed.

## 35. An astral or calendrical reading: three predictions, none met [astral_test]
Parpola's reading takes fish signs as star names (Dravidian *min* = "fish" and "star"),
with numbered fish as specific constellations. Three things that reading predicts:

**(1) Numbered fish should be a small, closed, recurring set.** It is not. There are 448
number+fish adjacencies in 85 distinct combinations, 41% of which occur exactly once. The
attached signs are not a bounded count series either: 30 different stroke-family signs
appear in the slot, and the two commonest are G2 (which FINDINGS 7 showed is a marker, not
a count) and G32. This is the profile of a productive modifier+item pattern, not a fixed
catalogue of star names.

**(2) A calendar needs a name inventory of characteristic size** (7 Saptarishi, 12 months,
27-28 nakshatras), which should appear as a set of mutually exclusive alternatives in one
slot. The largest mutually exclusive groups are 31 (initial), 25 (final) and 35 (medial) -
but a null with the same text lengths and sign frequencies produces 28. The observed
groups are at or near chance, so there is no paradigm of any size here, let alone one of
7, 12 or 27.

**(3) Names repeat; these texts do not.** 88% of the 2,536 texts occur exactly once. A
12-month or 27-star inventory applied across 2,536 objects would repeat heavily.

- Conclusion: the corpus does not support an astral or calendrical reading at the level
  these tests can see. That is not a refutation of Parpola's work, which rests on
  iconography and comparative linguistics as much as on distribution; it means the
  distributional evidence does not corroborate it.
- The same tests would equally fail for any reading that needs a small closed inventory of
  recurring names - deities, months, commodities, measures. Whatever the texts encode, it
  is mostly one-off, not drawn from a short list.

## 36. Egyptian: a mixed system with a large inventory [egyptian_compare]
Thesaurus Linguae Aegyptiae (CC-BY-SA 4.0), 3,586 sentences. The file used is LATER
Egyptian (-1539 to -332), so it post-dates the Indus cities; it is a script-type
comparand, not a chronological one. Hieroglyphs are Unicode, so sentences can be split
into individual signs and run through the same measures.

| corpus | unit | H(first) | H(last) | difference | commonest last | conditioning excess |
|---|---|---|---|---|---|---|
| Indus (Mohenjo-daro) | signs in a text | 6.40 | 4.11 | -2.29 | 43% | 26.5% |
| Egyptian | signs in a word | 6.33 | 4.77 | -1.56 | 20% | 18.8% |
| Egyptian | signs in a sentence | 5.41 | 4.71 | -0.70 | 18% | 19.6% |
| Egyptian | words in a sentence | 7.78 | 8.16 | +0.38 | 13% | 5.0% |

- Indus remains the most end-constrained and the most tightly conditioned of every corpus
  tested. Egyptian sign sequences sit between Indus and the word-level corpora.
- Egyptian words-in-a-sentence show NO end constraint (+0.38) and weak conditioning (5.0%),
  matching Greek phrases (4.2%). Word-level sequences behave alike across languages; the
  Indus profile is not a word-level profile.
- **Direction - RETRACTED as an independent measure, see FINDINGS 32c.** Egyptian is almost
  symmetric: H(next|prev) - H(prev|next) is +0.02 at both sign and word level, against Greek
  0.17, Sumerian 0.03 and Indus 0.50. This is the same algebraically-degenerate quantity
  corrected at FINDINGS 32c: it reduces to the positional entropy gradient (H(first) vs
  H(last)), so the "Indus asymmetry" language here restates that finding rather than adding
  an independent one. The Egyptian figure (+0.02, sign and word level both close to
  symmetric) remains a fair description of Egyptian's own positional entropy gradient, which
  is genuinely small compared with Indus's - but "direction" is not the right frame for
  either number.
- **The measures do track grammatical category.** Run on the UPOS tag sequences (where the
  answer is known), conditioning excess is 10.5%, with NOUN and PRON dominating final
  position and VERB and PART initial. So the measure detects grammar where grammar exists -
  but sign-level conditioning in Egyptian (18.8%) is HIGHER than its own grammatical-category
  conditioning (10.5%), which is a useful calibration: high conditioning does not by itself
  imply syntax.
- **Frequency classes.** Egyptian: frequent 21.8%, mid 49.3%, rare 16.8%. Indus: frequent
  22.5%, mid 25.9%, rare 8.1%. Both show rare signs conditioning least, so that pattern
  (FINDINGS 32b) is shared with a known mixed system rather than being peculiar to the Indus
  corpus - which supports the mixed-system reading of it.

## 37. Genre-matched: Egyptian title-and-name labels vs Indus seal texts [egyptian_labels]
TLA Earlier Egyptian (-3350 to -1539, contemporary with the mature Indus phase), 12,773
rows, of which 3,925 are label texts whose glossing contains only titles, personal, royal,
divine or place names and bare nouns - the Egyptian equivalent of a seal legend.

| corpus | n | mean len | H(first) | H(last) | diff | top last | conditioning | unique |
|---|---|---|---|---|---|---|---|---|
| Indus seal texts (signs) | 1028 | 5.3 | 6.40 | 4.11 | **-2.29** | 43% | 20.9% | 95% |
| Egyptian label texts (signs) | 3454 | 7.7 | 5.36 | 5.30 | -0.05 | 22% | 24.9% | 59% |
| Egyptian label texts (words) | 2579 | 2.8 | 6.23 | 7.77 | **+1.54** | 9% | 16.3% | 53% |
| Egyptian running text (signs) | 8514 | 18.1 | 6.01 | 5.93 | -0.08 | 13% | 14.5% | 89% |

- **The end-constraint is NOT a property of name-and-title labels.** Egyptian labels, the
  same genre on the same kind of object in the same centuries, show no end constraint at
  sign level (-0.05) and the OPPOSITE asymmetry at word level (+1.54): their beginnings are
  the fixed part (TITL 1241, ROYLN 889 lead) and their endings the variable part (PERSN
  1789 closes). Egyptian labels are TITLE-then-NAME; the Indus pattern is the mirror image.
- This is the strongest thing said so far about Indus word order: if these texts are
  name-and-title, they put the fixed element LAST, like Sumerian seal legends read
  right-to-left would, and unlike Egyptian. It also means FINDINGS 28's "fixed final slot"
  survives a genre-matched control - short formulaic labels do not produce it by themselves.
- **Conditioning is comparable** (Indus 20.9%, Egyptian labels 24.9%), so the tightness of
  Indus sign sequences is unremarkable for this genre: labels condition tightly in both.
  What distinguishes Indus is WHERE the fixity sits, not how much there is.
- **Repetition differs sharply.** 95% of Indus seal texts occur once (commonest 29 copies);
  Egyptian labels 84% (commonest 234 copies - royal names repeated across objects). Even in
  a genre built on names, Egyptian reuses a stock far more than the Indus corpus does. This
  strengthens FINDINGS 13: whatever the Indus variable element is, it is more nearly unique
  per object than Egyptian personal names are.

## 38. Does the Indus script have determinative-like signs? [determinative_test]
A functional comparison between scripts, not a comparison of shapes (look-alike matching
across scripts with 400-1000+ signs is unfalsifiable and has a poor record). Egyptian
determinatives - unpronounced category markers - have a distributional fingerprint: they
sit at the END of a word and attach to MANY unrelated words. That fingerprint is measured
on Egyptian, then looked for in the Indus corpus.

**Egyptian** (69,870 words with glyphs and lemmas): of 329 glyphs with 30+ tokens, **17**
are 80%+ word-final and attach to 20+ different lemmas. They are **7.8%** of all glyph
tokens. The median final-share across all frequent glyphs is 29%, so these stand well
clear of the rest.

**Indus** (same criteria, text-final and 20+ different preceding signs): of 74 signs with
30+ tokens, **4** match - G400 (328 tokens, 89% final, 62 different signs before it),
G520 the arrow (233, 85%, 27), G156 (80, 85%, 20) and G151 (67, 88%, 36). They are
**6.4%** of all Indus sign tokens. One near miss: the jar G740 at 69% final.

- The proportions are strikingly close: 7.8% of Egyptian tokens vs 6.4% of Indus tokens
  behave this way. A script with a large sign inventory appears to carry a similar budget
  of end-position category markers in both cases.
- But the Indus corpus is far more POLARISED. The median frequent Egyptian glyph is 29%
  word-final; the median frequent Indus sign is 3% text-final. Indus signs are either
  final or they are not, with little in between, whereas Egyptian glyphs distribute across
  positions. That is consistent with Indus texts being single formulaic units rather than
  strings of words each with its own internal structure.
- Caution: "determinative-like" here means DISTRIBUTIONALLY like a determinative. The test
  cannot show that G400 or G520 was unpronounced or that it classified what preceded it.
  What it does show is that the positions these signs occupy are occupied, in a known mixed
  script, by category markers.

## 39. Do texts form families sharing a base? [minimal_pairs_test]
If seals marked households or lineages, related bearers should share a base and vary in
one slot (surname + given name). That predicts an excess of MINIMAL PAIRS - texts
differing in exactly one position. Null: texts of the same lengths built from the same
sign pool, which destroys shared-base structure but keeps the inventory.
- 897 distinct Mohenjo-daro texts of 3+ signs give **185 substitution pairs** and **38
  single-sign extensions**, against a null of 21 +/- 5 and 2 +/- 1. Enrichment x8.9 and
  x24.5. Texts are systematically related to each other, far beyond chance.
- **The varying slot is mostly the middle** (114 pairs), then the first position (61), and
  almost never the last (10). The fixed final element stays fixed; variation happens inside.
- But the families are SMALL: 688 of 897 texts have no one-sign relative at all. Only 55
  texts sit in families of 2+, and the largest family has 24 members. The distribution is
  31 families of 2, 10 of 3, 5 of 4, then a thin tail.
- Reading: there is a productive system here - texts are built by varying one element of a
  shared frame - but it does not carve the corpus into a few large houses or clans. Most
  texts stand alone even under this generous test. That fits a system generating largely
  individual identifiers within shared rules better than one marking membership of a small
  number of groups.
- Caveat: near-duplicate seals were deduplicated earlier, so genuine repeats are not being
  counted as families; and a lineage system could vary in ways this test cannot see
  (two-sign differences, different lengths).

## 40. What Marshall's text says, and what it does to our readings
Mining the narrative of Marshall (1931) vol. II's seals chapter (notes in
`transcriptions/marshall1931_seal_table/CHAPTER_NOTES.md`). Four points matter.
- **The same inscription appears over two entirely different animals** on the two faces of
  one seal (Nos. 252/378). Independent confirmation of FINDINGS 2: the text does not label
  the animal.
- **Two different seals carry the same inscription** (two potsherds, demonstrably not
  impressed by the same seal). This is important for FINDINGS 39: a text is reproducible
  across objects, so it is not a per-object serial number. It names something that can
  have more than one seal cut for it - a person, an office, an entity.
- **Two-sided seals can carry different inscriptions on their two faces** (seal L 323).
  The face question raised in FINDINGS 24/26 is therefore real, and no corpus records it.
- **Marshall reports that no true sealing had then been found at Mohenjo-daro** - no
  impression on clay still attached to something - and argues against the amulet reading
  because most seals have a boss at the back. The strongest use-evidence he cites is a
  sealing found in Mesopotamia bearing an Indus bull and script, whose back preserves the
  impression of woven material, i.e. a bale from India.
  -> This qualifies the "seals closed bundles and doors" reading used earlier in this
  project: for Mohenjo-daro itself the direct evidence was, at least in 1931, absent.
- Method note: this is the first section here drawn from excavation NARRATIVE rather than
  from the corpora. It cost one afternoon and corrected one of our framings, which is a
  fair argument for reading the reports as well as counting the signs.

## 41. Mackay's text: sealings exist, and he reads two-line seals as we measured them
Notes in `transcriptions/mackay1938_notes/CHAPTER_NOTES.md`. Mackay dug four seasons after
Marshall, so this updates FINDINGS 40.
- **Sealings attached to bales or matting DO occur at Mohenjo-daro - about seven of them.**
  The rest of the stamped clay objects "were never attached to anything else, nor did they
  serve to mark merchandize, as did sealings of other countries." So the bale-sealing use
  is attested on site, but rare in what survives.
- **Mackay attributes the scarcity to preservation**: the material impressed was "probably
  ordinary clay, which has not survived the damp and saltiness of the soil". Arguments from
  the absence of sealings are therefore weak in both directions - including the one this
  project made in an earlier session.
- **He reads the upper line of a two-line seal as the owner's name**, with the lower line
  added and referring to something else ("the owner's name being in the usual place above").
  That is independent qualitative agreement with FINDINGS 34, which found the second line to
  be a distinct register with its own sign stock, not a continuation of the first.
- **He states the direction**: a long inscription "would apparently have been written on the
  actual seal from right to left", matching the forward/backward asymmetry in FINDINGS 32c.
- **The same inscription recurs across objects**, including with a different device in place
  of the animal - consistent with the 35 texts we found on more than one object type, and
  with Marshall's two-potsherds observation (FINDINGS 40).
- Net effect: on four separate points the excavators' qualitative reading and our
  distributional measurements agree, having been arrived at independently and 90 years
  apart. Where they disagreed - the amulet-versus-seal question - the disagreement turns on
  preservation, which neither statistics nor a 1938 excavator can settle from the objects.

## Open tracks
1. Linear Elamite: only 11 sign-only texts in CDLI; needs Desset et al. 2022 corpus.
   (Done since: corpus alignment, typology, neural baseline - sections 14-16.)
2. More Gulf / Dilmun seals from excavation reports (test G91 + numeral).
3. Find-spots from Marshall and Mackay reports (area/layer for Mohenjo-daro).
4. Trained image model for the remaining mixed families.
5. ML next: neural sequence model once more data (near-duplicate-aware splits),
   and HMM with sign-shape features.
