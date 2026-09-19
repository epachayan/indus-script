# Methods: approach, rationale and controls

This file explains HOW the results in `FINDINGS.md` were produced and WHY each test was
built the way it was. Results live in `FINDINGS.md`; this is the reasoning behind them.

## The standing rule
No result is reported without a null. Every statistic that could be produced by chance,
by sample size, or by the pipeline itself is compared against at least one of:
- **Shuffled nulls** - same signs, order destroyed (tests whether sequence matters).
- **Frequency-matched nulls** - same text lengths, signs drawn from the same frequency
  distribution (tests whether a result follows from frequency alone).
- **Generative controls** - a bigram model trained on the same corpus (tests whether a
  result needs more than first-order structure).
- **Synthetic systems** - e.g. a meaningless identifier scheme with random stems and a
  fixed suffix set (tests whether a "language-like" result can be faked).
- **Held-out validation** - rules mined on one half of the corpus, scored on the other.

## Why each family of test exists
**Sign classification (1-3).** The corpus gives sign numbers, not shapes. Rendering each
sign from the font and clustering gives visual families, which lets "do look-alike signs
behave alike?" be asked at all. Answer: mostly no (AMI 0.096), which is why behaviour
classes are derived separately from position statistics.

**Deduplication (2).** Many inscriptions are near-duplicates. Apparent sign-motif
associations largely vanish after deduplication, so `first_occurrence` is used throughout.

**Comparison corpora (12, 15, 28, 31, 32, 33).** A number from the Indus corpus alone
means little. Every structural claim is placed against corpora whose properties are known:
Linear B (Mycenaean Greek, suffixing, syllabic), Sumerian administrative text and seal
legends (same genre as Indus seals), proto-cuneiform and Proto-Elamite (accounting, not
full language). Genre matters: Indus seal texts are compared with Mesopotamian SEAL
LEGENDS, not with tablets.

**Unit matching (28, 31).** An Indus inscription is a short phrase, so it is compared with
phrases (word sequences) as well as with words (sign sequences). Conclusions changed when
this was done properly - see section 28, where Greek word-level and phrase-level figures
sit either side of the Indus value.

**Size correction (31).** Mutual information is upward-biased in small samples. All
cross-corpus comparisons subsample to a common size and report the EXCESS over each
corpus's own null, never the raw value.

**Length correction (33).** Indus texts are short (median 4 signs). Where a difference
from a comparison corpus might follow from length alone, the comparison corpus is
truncated to the Indus length distribution and re-measured. This shrank one earlier claim.

## Manual steps, and why they were necessary
Two datasets were transcribed by hand because OCR failed on them:
- **Mackay (1938) seal table** - `transcriptions/mackay1938_seal_table/`. OCR mangled the
  numeric columns; the table was read from page images. Validation: Mackay's own type
  totals, his narrative depths, and published data for the Pashupati seal (No. 420).
- **Mackay plate coding** - `transcriptions/mackay1938_plates/`. Features were read from
  the seal photographs (sign count, jar ending, numerals). The printed seal numbers are
  hand-lettered and defeat OCR, so they were read by eye from generated label grids.
  Reliability was measured by blind re-coding 36 seals (FINDINGS 25).
- **Marshall (1931) seal table** - `transcriptions/marshall1931_seal_table/`. Transcribed
  from page images after an OCR pass proved unreliable (that pass is kept as
  `parse_marshall_table.py` for comparison only).
These steps need the source PDFs, which are not redistributed here; `README.md` gives the
Internet Archive identifiers and the page ranges.

## Known limitations
- **One coder.** The reliability check measures consistency, not accuracy.
- **Exploratory, not preregistered.** Hypotheses were formed while looking at the data.
  Where a marginal result later evaporated with more data, both figures are reported
  (FINDINGS 23).
- **Corpus disagreement.** Sources disagree on 10-20% of sign positions (FINDINGS 14).
- **Depth is not a calendar** (FINDINGS 22 caveat). Level below datum records debris
  accumulation, not intention; seals can be intrusive or residual.
- **Mackay and Marshall depths are not poolable**: different datums (fixed datum vs below
  the modern surface) and different locus resolution.
- **Most script-internal findings replicate published work** - see the novelty note in
  FINDINGS. The contributions are the datasets, the controls, and the held-out rule set.
