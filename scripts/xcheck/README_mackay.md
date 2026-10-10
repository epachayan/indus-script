# Cross-check: Mackay (1938) Seal Table

Scripts to verify the AI-assisted transcription of **E.J.H. Mackay, *Further
Excavations at Mohenjo-daro* (1938), "Tabulation of Seals", pp. 369-391**.

All commands are run from the project root `indus-script/`.

---

## Files

| File | Description |
|------|-------------|
| `scripts/xcheck/read_mackay_tesseract.py` | Independent Tesseract OCR reader |
| `scripts/xcheck/agreement_mackay.py` | Compares AI vs. Tesseract, by seal number |
| `scripts/xcheck/vote_mackay.py` | Emits AGREE/DIFFER rows for every comparison |
| `scripts/xcheck/results/out_tess_mackay.csv` | Tesseract output (775 rows, 23 pages) |
| `scripts/xcheck/results/vote_mackay.csv` | Per-row comparison results |
| `scripts/xcheck/results/agreement_mackay.csv` | Agreement summary |
| `scripts/xcheck/results/disagreements_mackay.csv` | All differing rows |

---

## Running the pipeline

**Step 1 - OCR the table pages** (~7 min; pages already in `downloads/mackay_table/`)

```bash
python scripts/xcheck/read_mackay_tesseract.py \
    downloads/mackay_table \
    scripts/xcheck/results/out_tess_mackay.csv
```

**Step 2 - Agreement analysis**

```bash
python scripts/xcheck/agreement_mackay.py \
    outputs/mackay_seal_table.csv \
    scripts/xcheck/results/out_tess_mackay.csv \
    --out scripts/xcheck/results/mackay
```

**Step 3 - Vote file** (AGREE/DIFFER per comparison)

```bash
python scripts/xcheck/vote_mackay.py \
    outputs/mackay_seal_table.csv \
    scripts/xcheck/results/out_tess_mackay.csv \
    --out scripts/xcheck/results/vote_mackay.csv
```

---

## Results (596 matched seals, of 709 total)

Row matching: exact seal number - nearest integer fallback.
Alignment check: Tesseract seal numbers match AI in **596/596** matched rows.

| Field | AI rows | Tess reads | Coverage | Agree (exact) | Agreement |
|-------|--------:|----------:|--------:|-------------:|----------:|
| type (letter A-I) | 596 | 421 | 71 % | 403 | **95.7 %** |
| level_ft (depth) | 596 | 448 | 75 % | 175 | 39.1 % |
| field_no (numeric) | 591 | 400 | 68 % | 200 | 50.0 % |

### Interpreting the level_ft result

The 1938 printing uses a **raised middle dot (·) as decimal separator**
instead of a period. Tesseract reads it as a hyphen, producing `-6-5` for
`-6.5`. The reader script post-processes this, but two additional artefacts
reduce exact-match rate:

- **Missing minus sign** (80 of 273 disagreements): Tesseract drops the
  leading sign, reading `-6.3` as `6.3`.
- **Merged decimal** (~40 cases): `-6.5` is read as `-65` when Tesseract
  misses the separator entirely.

Much of the remaining gap looks like OCR digit errors, but this has not been measured,
and an agreement check cannot separate OCR errors from AI errors.

### Interpreting the field_no result

Field numbers are 4-5-digit codes (e.g., `11378`, `4695`). Tesseract
frequently reads the column-rule vertical line as a leading `1`, and
confuses visually similar digits (6-8, 3-2). Exact-match rate is 50 %;
single-digit-error rate accounts for the bulk of disagreements.

### What this means for the AI transcription

**Type** is the most reliable cross-checkable field: the single-letter seal
classification (A through I) agrees with Tesseract in **95.7 %** of
comparisons. No systematic misclassification was found.

---

## Comparison with Marshall (1931)

See `scripts/xcheck/README.md` for the Marshall pipeline and results.
Marshall shows 97.5 % agreement on type, 96.4 % on area and 76.7 % on serial.
