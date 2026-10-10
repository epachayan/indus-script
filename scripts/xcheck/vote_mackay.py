"""Three-way vote for Mackay (1938) 'Further Excavations at Mohenjo-Daro'.

Compares:
  1. AI transcription          (outputs/mackay_seal_table.csv)
  2. Tesseract independent OCR (out_tess_mackay.csv)

For each seal row where both sources have a value, emits a verdict:
  AGREE   – both match
  DIFFER  – both read the field, but give different values

Fields checked: type, level_ft, field_no (numeric portion only).

Usage (from project root):
  python scripts/xcheck/vote_mackay.py \
      outputs/mackay_seal_table.csv out_tess_mackay.csv \
      --out vote_mackay.csv

Output columns:
  no, field, ai_value, tess_value, verdict, tess_raw
"""
import csv, re, sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Normalisation helpers (mirror agreement_mackay.py)
# ---------------------------------------------------------------------------

def norm_type(v):
    v = (v or '').strip().upper()
    return v[:1] if v else ''


def norm_level(v):
    """Return signed decimal string or 'surface'."""
    v = (v or '').strip()
    if not v:
        return ''
    if re.search(r'[Ss]ur', v, re.I):
        return 'surface'
    v = re.sub(r'(\d)-(\d)', r'\1.\2', v)
    m = re.search(r'[-+]?\d{1,3}[.,]\d', v)
    if m:
        return m.group(0).replace(',', '.')
    m2 = re.search(r'[-+]?\d{1,3}$', v)
    if m2:
        return m2.group(0)
    return ''


def norm_field_num(v):
    """Extract the 3-5 digit numeric portion (drop DK/SD/H prefix)."""
    v = (v or '').strip()
    m = re.search(r'(\d{3,5}[A-Za-z]?)$', v)
    return m.group(1) if m else ''


def try_int(s):
    try:
        return int(re.sub(r'[^0-9]', '', s or ''))
    except ValueError:
        return None


FIELDS = ['type', 'level_ft', 'field_no']

NORM = {
    'type':     norm_type,
    'level_ft': norm_level,
    'field_no': norm_field_num,
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    args = sys.argv[1:]
    out_idx   = args.index('--out')
    ai_path   = args[0]
    tess_path = args[1]
    out_path  = Path(args[out_idx + 1])
    out_path.parent.mkdir(exist_ok=True)

    # Load AI transcription
    ai = {}
    for r in csv.DictReader(open(ai_path, encoding='utf-8')):
        no = r['no'].strip()
        ai[no] = {
            'type':     norm_type(r.get('type', '')),
            'level_ft': norm_level(r.get('level_ft', '')),
            'field_no': norm_field_num(r.get('field_no', '')),
        }

    # Load Tesseract output
    tess_rows = list(csv.DictReader(open(tess_path, encoding='utf-8')))
    tess_by_no = {}
    for r in tess_rows:
        no_raw = re.sub(r'[^0-9A-Za-z]', '', r.get('no', ''))
        if no_raw:
            tess_by_no[no_raw] = r

    tess_int_map = {}
    for k, r in tess_by_no.items():
        n = try_int(k)
        if n is not None:
            tess_int_map[n] = r

    rows_out = []
    agree = differ = 0

    for no_str, a in sorted(ai.items()):
        t_row = tess_by_no.get(no_str)
        if t_row is None:
            n = try_int(no_str)
            if n is not None:
                t_row = tess_int_map.get(n)
        if t_row is None:
            continue   # Tesseract didn't find this row

        for f in FIELDS:
            av = a[f]
            if not av:
                continue

            raw = t_row.get(f + '_raw', '') or t_row.get(f, '')
            tv = NORM[f](raw)
            if not tv:
                continue

            verdict = 'AGREE' if tv == av else 'DIFFER'
            if verdict == 'AGREE':
                agree += 1
            else:
                differ += 1

            rows_out.append({
                'no':        no_str,
                'field':     f,
                'ai_value':  av,
                'tess_value': tv,
                'verdict':   verdict,
                'page':      t_row.get('page', ''),
                'row':       t_row.get('row', ''),
                'tess_raw':  t_row.get(f + '_raw', ''),
            })

    keys = ['no', 'field', 'ai_value', 'tess_value', 'verdict', 'page', 'row', 'tess_raw']
    with open(out_path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, keys)
        w.writeheader()
        w.writerows(rows_out)

    total = agree + differ
    pct = agree / total * 100 if total else 0
    print(f'Wrote {len(rows_out)} comparisons to {out_path}')
    print(f'  AGREE: {agree}/{total} ({pct:.1f}%)  DIFFER: {differ}/{total} ({100-pct:.1f}%)')

    # Per-field breakdown
    from collections import Counter
    by_field = {}
    for r in rows_out:
        f = r['field']
        if f not in by_field:
            by_field[f] = Counter()
        by_field[f][r['verdict']] += 1
    print()
    print(f'  {"field":12s}  {"agree":>6}  {"total":>6}  {"pct":>7}')
    for f in FIELDS:
        if f in by_field:
            c = by_field[f]
            tot = c['AGREE'] + c['DIFFER']
            p = c['AGREE'] / tot * 100 if tot else 0
            print(f'  {f:12s}  {c["AGREE"]:6d}  {tot:6d}  {p:6.1f}%')
