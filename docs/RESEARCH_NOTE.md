# Indus script: machine-readable seal catalogues from Mackay (1938) and Marshall (1931), with photo-coded text features and a reproducible analysis pipeline

## No decipherment. Two hand-transcribed catalogues, a held-out validated constraint set, and controlled structural comparisons against six other writing systems — v0.2.1

Nitin Stephen Koshy

## Summary

This note documents two machine-readable catalogues of Mohenjo-daro seals built from the
excavation reports (Mackay 1938: 709 rows with block/house/room/level; Marshall 1931: 560
rows with excavation area and depth), text features hand-coded from all thirteen of
Mackay's seal plates (531 seals, 419 joined to find-spots, blind re-coding kappa 0.89), a
held-out validated set of 90 distributional constraints on Indus sign sequences, and a
reproducible pipeline of genre- and size-matched structural comparisons against Sumerian,
Egyptian, Linear A/B, proto-cuneiform and Proto-Elamite corpora.

**No decipherment is offered, and none is claimed to be reachable from this evidence**: the
texts are short (median 4-5 signs), there is no bilingual, and the language is unknown. What
follows is data plus controlled statistical constraints that any future reading has to
satisfy — and a set of readings the data rule out.

Headline results:
- Indus sign sequences carry dependencies a first-order (bigram) model of the same corpus
  cannot produce: 7-8% excess conditioning survives out to distance 5, where the bigram
  control collapses to 0.4% (§9 below; FINDINGS §32-33).
- Adjacent signs constrain each other about as tightly as syllables inside a Mycenaean Greek
  word (26.5% excess mutual information vs 19.8% for Linear B words, 14% for Sumerian), and
  far more tightly than words inside a phrase (Greek phrases 4.2%) (§9; FINDINGS §31).
- The corpus is strongly directional: forward prediction is easier than backward by 0.50
  bits, an order of magnitude larger than in Linear B, Sumerian or Egyptian, in the assumed
  reading direction (§9; FINDINGS §32c, 36).
- The text-final position is a strongly preferred but open slot — 133 different signs occur
  there, 44 cover 90% of occurrences, the jar sign alone takes 43% — and a synthetic
  fixed-suffix identifier scheme overshoots the real asymmetry, so it is not a closed
  terminator set (§8; FINDINGS §29-30).
- This asymmetry replicates independently at Harappa, 600 km away (§8; FINDINGS §30c).
- Genre-matched Egyptian title-and-name labels — the same function, the same centuries —
  put the fixed element FIRST and the variable name LAST; Indus does the opposite (§10;
  FINDINGS §37). This is the strongest evidence here about where fixity sits in an Indus
  text, though it does not by itself identify what that fixity encodes.
- Text form does not vary with archaeological depth or neighbourhood anywhere in the
  complete coded corpus (419 seals, six sample sizes up to n=419) (§11; FINDINGS §22-23).
  One earlier positive result — inscription-only seals becoming commoner near the surface —
  failed to replicate on Marshall's independent data (rho +0.001 vs +0.127, p=0.98) (§11;
  FINDINGS §26). It is documented as retired, not deleted.
- Readings requiring a small closed inventory of recurring names — deities, months,
  commodities, measures, ledger entries — are not supported: 88-95% of distinct texts occur
  exactly once, mutual-exclusion groups sit at chance, and the corpus fails all three
  distributional predictions of an astral/calendrical reading (§12; FINDINGS §8, 10, 35).
- Most script-internal findings replicate published work (Yadav et al. 2010; Mahadevan;
  Mukhopadhyay; Kriger & Hunt 2026); see §14 and `docs/PRIOR_WORK.md`. The contribution here
  is the datasets, the controls, and the held-out constraint set, not new script-internal
  discoveries.

### Suggested reading order
For the headline results only: this Summary, then §8-10 (structure and cross-corpus
comparisons) and §13 (readings ruled out). For the full evidentiary trail, including
findings later qualified or retired, `docs/FINDINGS.md` has all 41 numbered sections in the
order they were produced, and `docs/STATUS.md` marks each one standing / qualified / retired
/ replicates-published-work.

---

## 1. Background

The Indus script is attested on roughly 4,000-6,000 short inscriptions from sites across
the Indus Civilization (c. 2600-1900 BCE), overwhelmingly on stone seals and their sealings.
It remains undeciphered: the language is unknown, there is no bilingual text, and the
inscriptions are very short (median 4-5 signs, longest about 17). Whether the sign system
constitutes writing at all has been argued in both directions (Rao et al. 2009; Farmer,
Sproat & Witzel 2004), and this project does not adjudicate that debate — §9 below shows
language-like conditioning, but §"Egyptian: a mixed system" (FINDINGS §36) shows that high
conditioning does not by itself imply syntax, which cuts against over-reading such results
either way.

This project was carried out statistically, from the digitised sign sequences and the
excavation reports, deliberately without first reading the decipherment literature, so as
to see what the corpora say on their own terms. A novelty audit was then run to find out
which results were already known (§14). Most were. Two things had not, as far as could be
determined, been done before: joining coded text features to archaeological find-spots at
Mohenjo-daro, and publishing a held-out validated set of machine-readable positional
constraints.

## 2. Data

**Digitised sign sequences.** The working corpus (`indus_decipher`, MIT-licensed) supplies
the G-numbered sign sequences used for most structural tests, cross-checked against two
independent digitisations: the CISI corpus (Joshi & Parpola 1987, Parpola sign numbers,
161 seals shared with the G corpus) and Mahadevan's 1977 corpus (M77, 1,761 lines, no
shared IDs — mapped by behaviour and self-training; §see FINDINGS §14). The three sources
disagree on 10-20% of sign positions, which is treated throughout as noise rather than
resolved.

**Two hand-transcribed excavation-report catalogues**, produced because OCR failed on both:
- **Mackay (1938) seal table** — 709 rows (693 distinct seals): type, size, material,
  block/house/room or street, level relative to the DK datum, field number. Read by eye from
  page images of "Tabulation of Seals" (vol. I, pp. 369-391). Validated against Mackay's own
  published totals (type B 558 vs 559 transcribed; type F 81 vs 84), his narrative depths,
  and the published data for the "Pashupati" seal (No. 420).
- **Marshall (1931) seal table** — 560 rows (Nos. 1-557 plus three suffixed): plate number,
  size, level below the modern surface, type, material, excavation area and serial. Read
  from page images of "Tabulation of Seals" (vol. II, pp. 402-405), covering the 1922-27
  seasons, independent of Mackay's. Not directly poolable with the Mackay table: different
  depth datum (below the modern surface vs a fixed datum) and coarser locus resolution
  (area only, not block/house/room).

**Photo-coded text features** — 531 seals coded by eye from all thirteen of Mackay's seal
plates (vol. II, Pls. LXXXII-XCIX) at full IIIF resolution, joined to find-spots for 419 of
them: sign count, whether the text ends with the jar sign, presence of fish/arrow signs,
numeral groups, and a confidence flag (low-confidence rows excluded from all tests). Coder
reliability was measured by blind re-coding 36 seals: sign-count agreement within one sign
97%, jar-ending kappa 0.89 (§FINDINGS 25).

**A validated constraint set** — 90 positional/adjacency/co-occurrence rules mined on a
random half of 954 Mohenjo-daro texts and scored on the other half: 2,585 held-out
applications, 28 violations (1.08%); 56 of the 90 rules have 10 or more held-out
applications and zero violations (`outputs/constraints.csv`; §FINDINGS 27).

**Comparison corpora**, chosen for genre and size matching rather than convenience: Sumerian
and Akkadian seal legends and administrative text (CDLI, c. 2300-1900 BCE, 10,965 distinct
legends), Egyptian — both Later Egyptian (-1539 to -332, a script-type comparand) and
Earlier Egyptian (-3350 to -1539, contemporary with the mature Indus phase, via the
Thesaurus Linguae Aegyptiae, CC-BY-SA 4.0), Linear A and Linear B (Mycenaean Greek),
proto-cuneiform and Proto-Elamite (1,343 tablets parsed from CDLI). Full provenance and
licensing for every file is in `docs/DATASETS.md` and `docs/DATA_NOTICE.md`; third-party
corpora are fetched at pinned commits by `setup.sh`, never redistributed.

## 3. Method

**No result is reported without a null.** Every statistic that could plausibly be produced
by chance, sample size, or an artefact of the pipeline itself is compared against at least
one of: a shuffled null (same signs, order destroyed), a frequency-matched null (same
lengths, signs drawn from the corpus's own frequency distribution), a generative control
(a bigram model trained on the same corpus), a synthetic system (e.g. a meaningless
identifier scheme with random stems and a fixed suffix set, built to test whether a
"language-like" result can be faked), or held-out validation (rules mined on one half of
the corpus, scored on the other).

**Deduplication.** Roughly a third of inscriptions are exact or near-exact repeats.
Apparent sign-to-motif associations largely vanish once duplicates are removed, so
`first_occurrence` (one representative per group) is used throughout unless stated.

**Size and length correction.** Mutual information is upward-biased in small samples, so
every cross-corpus comparison subsamples to a common size (typically 1,000 sequences, 20
draws) and reports the EXCESS over that corpus's own shuffled null, never a raw value.
Where a difference might follow from Indus texts simply being short (median 4 signs), the
comparison corpus is truncated to the Indus length distribution and re-measured — this
correction shrank one earlier claim about long-range periodicity (§9c below; FINDINGS §33).

**Unit and genre matching.** Because an Indus inscription is a short phrase, it is compared
with phrases as well as with words in the comparison languages, and — where the genre
allows — with texts of the same social function (seal legends, name-and-title labels)
rather than with running prose or administrative tablets. Conclusions changed materially
when this was done properly (§10; FINDINGS §28, 37).

**Manual transcription.** Both seal tables and the plate codings were produced by reading
page images by eye because OCR was unusable on them (numeric tabulation columns; hand-
lettered plate captions). These are one-coder efforts; reliability, not accuracy, was
checked by blind re-coding (§FINDINGS 25). This is stated as a limitation in §15.

## 4. Sign classification and behaviour

698 signs were rendered from the corpus font and clustered into 36 shape families
(refined into named groups; 69 signs remain in mixed clusters). Known variant pairs land
in the same visual cluster 31% of the time against a 3% chance baseline — weak but real
signal. Separately, 123 signs with 10 or more uses (86% of all tokens) were classed by
where they occur — text-final markers, pre-final signs, openers, a "fish" core, strict
medial connectors, numerals, and others — purely from position statistics. Look-alike and
behave-alike agree only weakly (adjusted mutual information 0.096, p=0.002): the jar sign
(G740) is reliably text-final, but its visual look-alikes are strictly medial, suggesting
they are functionally distinct signs rather than graphic variants of one sign (FINDINGS
§1-3).

Text content and animal motif on a seal carry independent information: unicorn-seal and
other-animal-seal texts at Mohenjo-daro show no difference on any of nine template features
once near-duplicates are removed (FINDINGS §2). This is corroborated 90 years later by
Marshall's own narrative report of the same inscription occurring over two entirely
different animals on one seal's two faces (§13; FINDINGS §40).

## 5. The Mohenjo-daro text template

1,008 Mohenjo-daro texts resolve into a template: **[opener + a strict medial marker] ...
[numeral + item] ... [pre-final sign + the jar G740] + optional closer**, with 41% of
signs sitting in fixed pairs or triplets. 128 minimal-pair texts show specific sign groups
swapping with each other in a single slot (openers with openers, numerals with numerals,
and three sign pairs that behave as likely true graphic variants). The template
independently replicates in the 1,761-line Mahadevan (M77) corpus: three mutually
swapping openers, a marker following them 70% of the time (vs 75% in the primary corpus),
the jar final in 74% of texts, and 45% of signs in fixed blocks (FINDINGS §6).

A closer look inside the core (706 texts of 3+ signs, split into opener/core/ending units)
refines this: the last core unit is not a closed title set (242 distinct forms, the
commonest covering only 5%), but it depends strongly on which ending follows (p ~ 3e-40),
so the pre-final sign and the ending behave as a fixed two-part unit rather than
independent slots. Openers are optional and, when present, displace part of the core rather
than adding to overall text length — inscriptions hold to a conventional length of about
five signs regardless. The revised model: **[optional opener] + [an open core, often
carrying a small count] + [a constrained pre-final sign] + [a fixed ending sign]** (+ an
optional closer) (FINDINGS §17).

A related seal-specific formula — a fixed count of three (long-stroke G33) immediately
before the arrow sign (G520) — occurs on a quarter to a third of arrow-final seal texts at
both Mohenjo-daro and Harappa, but almost never on tablets or at other sites. §8 below
shows this formula is largely the closing element of a *second inscribed line*, not an
alternative ending competing with the jar within one line, which revises the original
reading (FINDINGS §18, 24).

## 6. Numerals and the "stock book" hypothesis ruled out

Two apparently distinct numeral systems are used: short and tiered strokes (values 1-9)
attach mainly to a class of "forked stem" signs, while long strokes attach mainly to fish,
jar and arrow signs — the two systems diverge far more than a shuffled baseline would
produce (0.53 vs 0.23, p=0.003). The commonest single stroke-group (G2, "two short
strokes") follows openers so consistently that it behaves as a marker rather than a live
count (FINDINGS §7).

Despite this genuine counting apparatus, the corpus does not read as a stock or ledger
record: only 23-28% of texts carry any numeral at all, at most 2-3% carry two or more
number-item pairs, 84% of counts are three or less (maximum nine), there are no totals, and
a third of texts are exact duplicates. This is thrown into sharp relief by a direct
comparison against 1,343 genuine Proto-Elamite accounting tablets, where 96% of texts carry
numbers, 80% carry two or more entries, and 41% preserve a numbered total line on the
reverse — none of which the Indus corpus shows. Both systems tie specific numeral types to
specific commodities more than chance predicts (Proto-Elamite 48% vs Indus 37%, against
14% and 3% shuffled respectively), but write the number and the item in opposite orders.
Reading: the Indus script had commodity-linked counting like its western neighbour, but the
surviving objects deploy it inside short formulaic titles, not accounts (FINDINGS §8, 10).

## 7. Sequence prediction and a neural-leakage negative result

Next-sign prediction on 1,869 homeland texts improves substantially from a unigram model
(perplexity 86) to a bigram model (37; top-1 accuracy 21-24%), but adding trigrams or
behaviour-class back-off adds nothing — texts are too short and most of the structure sits
between immediate neighbours. An unsupervised 10-state HMM, given no labels, recovers the
hand-built template on its own (opener state → marker state 90% of the time → numeral/fish
states mid-text → pre-final → jar-family closing state), agreeing with the hand-built
behaviour classes at AMI 0.39 (FINDINGS §11).

A small multilayer perceptron appears to beat the bigram baseline under a naive random
train/test split (38.7% vs 36.5% top-1 accuracy), but the gain disappears — and reverses —
once texts are split so that near-duplicates cannot appear on both sides (35.9% vs 37.0%).
The apparent neural improvement was leakage from near-identical texts, not learned
structure; with the data currently available, a neural model adds nothing over a bigram
(FINDINGS §16).

## 8. The ending: a preferred but open, strongly conditioned, cross-site slot

Three follow-up tests on 1,028 Mohenjo-daro texts of three or more signs establish the
character of the final position precisely:

**(a) It is narrowed but not closed.** The first position draws on 225 distinct signs (123
needed to cover 90% of tokens); the final position draws on only 133 signs, and just 44 of
them cover 90% of occurrences, with the single commonest (the jar) taking 43% on its own.
That is far too open for a small closed suffix or title set, while being much narrower than
either the first or medial positions.

**(b) The slots are not independent.** The opener predicts the ending (mutual information
2.27 bits vs 1.90 shuffled, z=+12.0), and the penultimate sign predicts it far more strongly
(2.99 vs 1.89 bits, z=+39.7) — an effect that gets STRONGER, not weaker, after the
commonest stock phrases are removed from the sample (3.68 bits on the remaining 631 texts
after dropping the top 20 formulas, vs 3.05 shuffled, z=+21.9). This dependency running
through the whole corpus, not concentrated in a few memorised phrases, is the single
strongest structural result in this project (FINDINGS §29b, 30b).

**(c) A synthetic control overshoots the real asymmetry.** A meaningless identifier scheme
— random stems attached to five fixed suffixes, matched to the real corpus in count, length
and top-ending share — produces a SHARPER first/last entropy gap (-6.18 bits) than the real
texts show (-2.29 bits), because its ending set is genuinely closed at five forms. The real
corpus sits between an unconstrained sequence and a closed-suffix identifier system: neither
extreme fits (FINDINGS §29c).

**(d) It replicates independently at Harappa**, roughly 600 km from Mohenjo-daro: the same
front-open/back-fixed asymmetry (-2.83 bits vs -2.29), the same strength of penultimate-to-
ending conditioning (z=+37.8 vs +39.3), and — if anything — a MORE constrained ending set
(24 signs cover 90% of Harappa endings, vs 44 at Mohenjo-daro), so the effect is not an
artefact of one city or one dominant sign (FINDINGS §30c).

Whatever governs the end of an Indus text is a property of the writing system shared across
sites, conditioned pairwise across the whole corpus rather than memorised as a handful of
fixed phrases.

## 9. How the conditioning compares with known writing systems

**Strength.** Measured as the excess mutual information between the last two elements of a
sequence over each corpus's own shuffled null, after subsampling to a common size: Indus
signs in an inscription reach 26.5% excess — higher than syllable-in-a-word conditioning in
Mycenaean Greek (19.8%), word- or sign-level conditioning in Sumerian (14.1-14.7%), and far
higher than Greek phrase-level conditioning (4.2%). A bigram-generated control built from
the Indus corpus itself reaches only 15.3%, so the real texts exceed what first-order
structure alone would produce (FINDINGS §31).

**Range.** The dependency is not confined to adjacent signs. Indus sequences retain 7-8%
excess conditioning out to a distance of five signs; the bigram control collapses to 0.4%
by distance three, as any first-order process must. This is the cleanest evidence that
Indus sequences carry structure beyond nearest-neighbour pairs (FINDINGS §32a). The SHAPE
of that decay differs from real languages, though: Greek and Sumerian both dip at distance
2 and rise again at distances 4-5 (the signature of word- or phrase-length periodicity),
while Indus decays monotonically. A length-matched control shows part of that difference is
an artefact of Indus texts being short — truncating the comparison corpora to the Indus
length distribution weakens their mid-range rise — but even after truncation the comparison
corpora still show some recovery at distance 4, while Indus does not (FINDINGS §33). The
non-first-order result survives; the periodicity claim is qualified rather than standing.

**Direction.** Forward prediction (next sign given previous) is easier than backward
prediction by 0.50 bits in Indus, against 0.17 in Linear B, 0.03-0.05 in Sumerian, and 0.02
in Egyptian at both sign and word level — no other corpus tested shows anything close to
the Indus asymmetry, in the direction the assumed right-to-left reading order predicts
(FINDINGS §32c, 36).

**Frequency structure.** Frequent Indus signs (50+ uses) condition their neighbours far
more (22.5%) than rare signs (<10 uses, 8.1%) — a split also seen in Egyptian (21.8% vs
16.8%), a known mixed logo-syllabic system, and consistent with an inventory of roughly
400-700 signs containing both combinatorially active core signs and a longer tail that
behaves more like free-standing labels (FINDINGS §32b, 36).

**Calibration.** Run on Egyptian part-of-speech tags, where the grammatical answer is
known, the same conditioning measure gives 10.5% excess — LOWER than Egyptian's own
sign-level conditioning (18.8%). High conditioning at the sign level, in other words, does
not by itself imply syntax even in a language we can read; this bounds how much can be
inferred from the Indus conditioning figures alone (FINDINGS §36).

## 10. Genre-matched comparisons: where is the fixity?

The comparisons above use running text or single-word corpora as controls. Two further
comparisons match Indus seal texts on FUNCTION as well as size:

**Sumerian and Akkadian seal legends** (10,965 distinct legends, CDLI, c. 2300-1900 BCE)
follow a NAME > (TITLE) > FILIATION > (SERVANT) template; a name opens 68% of legends. The
Indus sign inventory (479 distinct signs at 5,000 tokens) and its sequencing statistics
(bigram/unigram perplexity ratio 0.47) both sit closer to cuneiform WORDS (1,295-1,714
signs; ratio 0.40-0.60) than to cuneiform SIGNS, suggesting Indus signs pattern like whole
words or morphemes drawn from a sign-sized inventory — consistent with a largely
logographic system. Indus texts are far more fixed at the end (top closer 39-43%, end
entropy 4.1-4.5 bits) than Mesopotamian legends (top closer ≤12%, entropy 6.4-9.1), which
argues for a fixed title or suffix on most Indus texts rather than a free personal name
(FINDINGS §12-13).

**Egyptian title-and-name labels** (3,925 rows from Earlier Egyptian, -3350 to -1539,
contemporary with the mature Indus phase, glossed as titles, personal/royal/divine names,
or bare nouns — the closest Egyptian equivalent of a seal legend, as opposed to running
prose) give the sharpest contrast in the project. At sign level Egyptian labels show almost
no end constraint (-0.05 bits, vs Indus -2.29); at word level they show the OPPOSITE
asymmetry (+1.54 bits): their fixed element (titles, royal names) comes FIRST and their
variable element (a personal name) comes LAST. Indus does the mirror image. Conditioning
strength is comparable between the two corpora (Indus 20.9%, Egyptian labels 24.9%), so
what distinguishes the Indus profile is WHERE the fixity sits, not how tightly the text is
conditioned. This also shows the "fixed final slot" is not simply a property of short
name-and-title genres in general — a genre-matched control does not produce it by itself —
strengthening the case that it is specific to the Indus material. Repetition also differs
sharply: 95% of distinct Indus seal texts occur exactly once, against 84% of Egyptian
labels (Egyptian royal names recur up to 234 times), so whatever the Indus variable element
encodes, it is closer to unique-per-object than an Egyptian personal name is (FINDINGS §37).

**Determinative-like signs.** Egyptian determinatives — unpronounced category markers —
have a measurable distributional fingerprint: word-final, attaching to many unrelated
words. Applying the same functional test (not a visual one — cross-script glyph-shape
matching is unfalsifiable and has a poor track record) finds that 6.4% of frequent Indus
sign tokens match this fingerprint (four signs, including G400 and the arrow G520),
against 7.8% of frequent Egyptian tokens (seventeen glyphs) — a strikingly similar budget of
end-position category markers in two independently mixed scripts with large sign
inventories, though the Indus signs are far more sharply polarised toward final position
than the Egyptian ones (FINDINGS §38).

## 11. Text and archaeology

**Depth.** Using features read directly from plate photographs and joined to Mackay's
recorded levels, text form does not vary with depth at Mohenjo-daro. The null holds at six
successive sample sizes (n=69 through n=419, the complete coded corpus): mean sign count is
5.5-5.6 signs and jar-ending rate 27-36% at every depth band tested, with no monotonic
trend (FINDINGS §22). The one property that DOES shift with depth is the seal OBJECT, not
its text: inscription-only rectangular seals (type F) grow from about 5% of the earliest
phase to 13-19% of the latest across Mackay's complete 697-seal table (rho=+0.13,
p=0.0008) (FINDINGS §19, 22). **This trend failed to replicate on Marshall's independent
560-seal table** (rho=+0.001, p=0.98; no individual excavation area shows it either), and
is documented as retired rather than removed (§14; FINDINGS §26). Depth itself is a rough
ordering with substantial error — level below datum records debris accumulation, not
intention, and seals can be intrusive or residual — so a null result of this kind is the
expected outcome of that error and should not be read as a strong claim either way
(FINDINGS §22 caveat).

**Neighbourhood.** Text length and jar-ending rate show no difference between indoor and
street find-spots, nor between city blocks, at any sample size tested (an early p=0.06
hint at n=127 disappeared by n=190 and n=254) (FINDINGS §23).

**Multi-line texts.** A fifth (21%) of inscriptions run to two lines. The second line is a
distinct register, not a continuation: it draws from a partly different sign stock (rank
correlation with single-line frequencies only rho=0.57), is shorter (2.5 vs 3.3 signs for
the first line of a two-line text), and ends with the arrow sign 46% of the time against
0.3% for single-line texts. The two lines are nonetheless coupled — the ending of line 1
predicts the start of line 2 (MI 2.63 bits vs 1.92 shuffled) — though conditioning within
each line is stronger still, so the line break is a real division, not a seam (FINDINGS
§24, 34).

## 12. Readings the data do not support

Three specific readings were tested against distributional predictions and each fails:

- **Ledgers or stock records.** Counts are present but small (median ≤3, max 9), rarely
  repeated in the same text, and never totalled; the direct Proto-Elamite comparison (§6)
  shows what a genuine accounting corpus looks like by every one of these measures, and the
  Indus corpus does not match it (FINDINGS §8, 10).
- **Container or object labels.** 93-95% of distinct texts occur exactly once, which is a
  poor fit for a small set of category labels reused across many objects (FINDINGS §37, 39).
- **Astral or calendrical content** (e.g. numbered fish as constellations). None of three
  specific distributional predictions of this reading are met: numbered-fish combinations
  are not a small closed set (85 combinations, 41% singleton); no mutually exclusive sign
  group of characteristic size (7, 12, 27-28) rises above a chance-matched null (largest
  observed group 35, chance-matched null 28); and 88% of texts occur exactly once, which a
  repeating calendar applied across thousands of objects would not produce (FINDINGS §35).
- More generally, **any reading requiring a short list of recurring names** — deities,
  months, commodities, standard measures — runs into the same repetition test and fails it.

A complementary positive test finds that texts ARE systematically related to each other far
beyond chance — 185 one-sign substitution pairs and 38 single-sign extensions among 897
distinct Mohenjo-daro texts, against a null of about 21 and 2 respectively (enrichment
8.9x and 24.5x) — with variation concentrated in the middle of a text and the fixed ending
almost never varying. But these families are small (688 of 897 texts have no one-sign
relative at all; the largest family has 24 members), which fits a system that generates
largely individual identifiers within shared rules better than one marking membership in a
small number of named groups or lineages (FINDINGS §39). This is corroborated by Marshall's
own narrative report of the same inscription appearing on two demonstrably different seals
— evidence that a text can be reproduced across objects, so it is unlikely to function as a
strict per-object serial number (FINDINGS §40).

## 13. The excavators' own words

A late addition mined the excavators' narrative chapters — not the tabulated data — for
statements bearing on the statistics above (`transcriptions/*/CHAPTER_NOTES.md`). Four
points corroborate the distributional findings independently, 90 years apart:
- Marshall reports the same inscription over two entirely different animals on one seal's
  two faces, and two demonstrably different seals carrying the same text — independent
  qualitative confirmation of §4 (text and motif carry independent information) and §12
  (texts recur across objects) (FINDINGS §40).
- Mackay reads the upper line of a two-line seal as the owner's name and the lower line as
  something added, referring elsewhere — independent agreement with §11's finding that the
  second line is a distinct register with its own sign stock (FINDINGS §41).
- Mackay states explicitly that a long inscription would have been written right to left,
  matching the direction assumed throughout and confirmed distributionally in §9 (FINDINGS
  §41).
- Genuine sealings attached to bales or matting do occur at Mohenjo-daro (about seven of
  them), which Mackay attributes to poor preservation of the underlying clay rather than
  absence of the practice — a caution against reading too much into the general scarcity of
  sealings at the site, including in this project's own earlier framing (FINDINGS §40-41).

## 14. Relation to prior work

A novelty audit, run after the analysis rather than before it, found that most
script-internal results here replicate published work: positional structure and the text
template (Yadav, Vahia, Mahadevan, Joglekar, Adhikari, Rao et al., *PLOS ONE* 2010, using
the same M77 corpus, and Koskenniemi & Parpola); inscriptions overwhelmingly unique and
strict positional rules (Kriger & Hunt 2026, the same 179-seal Mohenjo-daro corpus); the jar
and arrow signs not co-occurring (Mahadevan 2011, read as gender markers); multi-line
inscription structure (Mukhopadhyay 2019, 2023); two stroke-numeral systems (Mahadevan);
and Indus statistics falling within the range of genuine writing systems (Rao et al. 2009
and the debate that followed).

What this project adds, as far as a literature check could determine: two machine-readable
excavation-report seal tables with find-spots (the books are public domain; the tabulated
data, so far as could be found, was not previously available in machine-readable form);
text features tested directly against find-spots at Mohenjo-daro (addressing Kenoyer's
criticism that Indus statistical corpora often draw on "chronologically mixed contexts");
a held-out validated constraint set published in machine-readable form with violation
counts, rather than positional rules stated only in prose; genre-matched comparisons
(Sumerian seal legends, Egyptian title-and-name labels) with explicit size and length
corrections; and a measured figure (10-20%) for how much the available digitisations
disagree on sign position, a fact that is widely known informally but which this project
did not find stated quantitatively elsewhere.

This work takes no position on whether the Indus system constitutes writing in the full
linguistic sense, and it neither supports nor refutes the Dravidian hypothesis — §8-9 rule
out a prefixing profile but cannot distinguish genuine suffixing morphology from a
phrase-final formula common to a non-suffixing language. Full detail is in
`docs/PRIOR_WORK.md`.

## 15. Limitations

- **The texts are very short** (median 4-5 signs, longest about 17), **there is no
  bilingual**, and the language is unknown — script, language and content are all unknown
  simultaneously, unlike e.g. Linear B, where only the script was. No decipherment has ever
  been achieved from material this short without a bilingual, and none is claimed here.
- **The sign inventory (roughly 400-700 signs) is too large for a syllabary**, so many signs
  necessarily carry word- or morpheme-level meaning that distributional analysis alone
  cannot recover.
- **Depth is not a calendar.** Level below datum reflects debris accumulation and rebuilding,
  not intention; seals can be intrusive or residual, and phase labels are averages of floor
  levels, not dated horizons. Mackay's and Marshall's depths are not poolable with each
  other (different datums, different locus resolution).
- **Sources disagree on 10-20% of sign positions**, and sign numbering here (the G corpus)
  is a convenience identifier, not a published standard — the standard sign lists are
  Mahadevan's and Parpola's.
- **One coder** transcribed both seal tables and coded all plate features. Reliability
  (kappa 0.89, sign counts within one) was checked by blind re-coding, which measures
  consistency, not accuracy; a second reader might read the photographs differently. Fish
  and arrow signs specifically are not reliably readable at plate resolution and are flagged
  "likely"/"unclear" rather than counted.
- **Exploratory, not preregistered.** Hypotheses were formed while looking at the data.
  Where a marginal result later evaporated with more data, both figures are reported
  (FINDINGS §23), and multiple comparisons are not formally corrected.
- **Most script-internal findings replicate published work** (§14); the contribution is the
  datasets, the controls, and the held-out rule set, not new script-internal discoveries.
- **One positive result failed to replicate** on independent data (§11; FINDINGS §26) and is
  marked retired rather than removed — kept visible as part of the evidentiary record.
- **High conditioning does not imply syntax.** In Egyptian, where the answer is known,
  sign-level conditioning exceeds grammatical-category conditioning (§9; FINDINGS §36); the
  Indus conditioning figures in §9-10 should be read with that calibration in mind.

Full detail: `docs/LIMITATIONS.md`.

## 16. Reproducibility

```bash
./setup.sh     # clone the pinned third-party corpora
./run_all.sh   # run the pipeline (~1-2 min without optional data)
```
Every script that samples or permutes sets an explicit seed. Steps whose optional inputs
(the CDLI dump, the Marshall vol. II PDF, the TLA Egyptian corpora) are absent are skipped
with a message rather than failing; `docs/REPRODUCING.md` lists exactly what each optional
input unlocks. Three components cannot be automated and are not re-derived by the pipeline:
the two seal tables and the plate codings were produced by reading page images by eye
because OCR was unusable on them; the results are committed in `transcriptions/` and used
as-is on every run. Full data provenance and licensing — what is committed, what is
regenerated locally, and under what licence — is in `docs/DATASETS.md` and
`docs/DATA_NOTICE.md`.

## 17. Selected references

- Farmer, S., Sproat, R. & Witzel, M. (2004) "The collapse of the Indus-script thesis: the
  myth of a literate Harappan civilization", *Electronic Journal of Vedic Studies* 11(2).
- Jamison, G. & Uesugi, A. (2022) "Mohenjo-daro and interregional connections in the Indus
  Civilization: evidence from inscribed seals".
- Joshi, J. P. & Parpola, A., eds. (1987) *Corpus of Indus Seals and Inscriptions*, vol. 1.
  Helsinki: Suomalainen Tiedeakatemia.
- Kriger, C. & Hunt (2026) "Positional constraints, sequence uniqueness, and stroke
  numerals in Indus seal inscriptions from Mohenjo-Daro".
- Mackay, E. J. H. (1938) *Further Excavations at Mohenjo-daro*, 2 vols. Delhi: Government
  of India.
- Mahadevan, I. (1977) *The Indus Script: Texts, Concordance and Tables*. New Delhi:
  Archaeological Survey of India.
- Mahadevan, I. (2011) on the jar and arrow signs as gender markers.
- Marshall, J., ed. (1931) *Mohenjo-daro and the Indus Civilization*, 3 vols. London:
  Arthur Probsthain.
- Mukhopadhyay, B. (2019, 2023) on Indus inscriptions as formalised data carriers.
- Rao, R. P. N. et al. (2009) "Entropic evidence for linguistic structure in the Indus
  script", *Science* 324(5931).
- Yadav, N., Vahia, M. N., Mahadevan, I., Joglekar, H., Adhikari, R. et al. (2010)
  "Statistical analysis of the Indus script using n-grams", *PLOS ONE* 5(3).

---

**Data availability.** Code: MIT (`LICENSE`). Transcribed and coded data: CC BY 4.0
(`LICENSE-DATA`) — these are original transcriptions of public-domain excavation reports.
Third-party corpora are not redistributed; see `docs/DATA_NOTICE.md` for sources and terms.
Repository: https://github.com/epachayan/indus-script

**AI usage.** This work was carried out with AI assistance across data transcription
support, pipeline scripting, and drafting of this document; all reported statistics are
produced by the scripts in `scripts/` against the committed data in `transcriptions/` and
`outputs/`, and are reproducible independently of any AI tool via `run_all.sh`.
