"""Compare the AI Mackay transcription with the Tesseract independent reader.

Matches rows by seal number (the 'no' field), not by position, so OCR errors
in the no. column are tolerated via nearest-integer fallback.

Usage:
  python agreement_mackay.py <ai_csv> <tess_csv> --out <dir>

  ai_csv  : outputs/mackay_seal_table.csv from the repo
  tess_csv: output of read_mackay_tesseract.py

Fields compared:
  type      - single letter A-I
  level_ft  - depth in feet (decimal, 'surface')
  field_no  - 4-5 digit field number (numeric part only)
"""
import csv, re, sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

def norm_type(v):
    v = (v or '').strip().upper()
    return v[:1] if v else ''


def norm_level(v):
    """Normalise level_ft to a signed decimal string or 'surface'."""
    v = (v or '').strip()
    if not v:
        return ''
    if re.search(r'[Ss]ur', v, re.I):
        return 'surface'
    # Middle dot printed as '-' by Tesseract: digit-hyphen-digit → digit.digit
    v = re.sub(r'(\d)-(\d)', r'\1.\2', v)
    # Grab the last decimal-looking number (handles room bleed like '47 -19.4')
    m = re.search(r'[-+]?\d{1,3}[.,]\d', v)
    if m:
        s = m.group(0).replace(',', '.')
        return s
    # Plain integer that looks like a level?
    m2 = re.search(r'[-+]?\d{1,3}$', v)
    if m2:
        return m2.group(0)
    return ''


def norm_field_num(v):
    """Extract the 4-5 digit numeric portion of a field_no value.
    AI gives 'DK 7374'; Tesseract gives '7374' directly.
    """
    v = (v or '').strip()
    # Pull out the trailing digit run
    m = re.search(r'(\d{3,5}[A-Za-z]?)$', v)
    return m.group(1) if m else ''


def try_int(s):
    try:
        return int(re.sub(r'[^0-9]', '', s or ''))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

FIELDS = ['type', 'level_ft', 'field_no']   # fields to cross-check

if __name__ == '__main__':
    args = sys.argv[1:]
    out_idx  = args.index('--out')
    ai_path  = args[0]
    tess_path = args[1]
    out_dir  = Path(args[out_idx + 1])
    out_dir.mkdir(exist_ok=True)

    # Load AI transcription keyed by seal number
    ai = {}
    for r in csv.DictReader(open(ai_path, encoding='utf-8')):
        no = r['no'].strip()
        ai[no] = {
            'type':     norm_type(r.get('type', '')),
            'level_ft': norm_level(r.get('level_ft', '')),
            'field_no': norm_field_num(r.get('field_no', '')),
        }

    # Load Tesseract output; build index by normalised no.
    tess_rows = list(csv.DictReader(open(tess_path, encoding='utf-8')))
    # Map Tesseract no → row (string and int)
    tess_by_no = {}
    for r in tess_rows:
        no_raw = re.sub(r'[^0-9A-Za-z]', '', r.get('no', ''))
        if no_raw:
            tess_by_no[no_raw] = r

    # Build int-keyed map for nearest-match fallback
    tess_int_map = {}
    for k, r in tess_by_no.items():
        n = try_int(k)
        if n is not None:
            tess_int_map[n] = r

    stats = defaultdict(lambda: [0, 0, 0])   # field → [ai_rows, tess_read, agree]
    plate_check = [0, 0]
    disagreements = []

    for no_str, a in sorted(ai.items()):
        # Exact match first, then nearest int
        t_row = tess_by_no.get(no_str)
        if t_row is None:
            n = try_int(no_str)
            if n is not None:
                t_row = tess_int_map.get(n)
        if t_row is None:
            continue   # Tesseract didn't detect this seal's row

        # Plate check: did Tesseract read the right seal number?
        tess_no = re.sub(r'[^0-9]', '', t_row.get('no', ''))
        ai_no   = re.sub(r'[^0-9]', '', no_str)
        if tess_no:
            plate_check[0] += 1
            plate_check[1] += (tess_no == ai_no)

        # Compare fields
        for f in FIELDS:
            av = a[f]
            if not av:
                continue   # AI has no value; skip

            stats[f][0] += 1   # AI has a value

            # Get Tesseract value for this field
            raw = t_row.get(f + '_raw', '') or t_row.get(f, '')
            if f == 'type':
                tv = norm_type(raw)
            elif f == 'level_ft':
                tv = norm_level(raw)
            else:  # field_no
                tv = norm_field_num(raw)

            if not tv:
                continue   # Tesseract couldn't read it
            stats[f][1] += 1

            if tv == av:
                stats[f][2] += 1
            else:
                disagreements.append([no_str, f, av, tv,
                                       t_row.get('page', ''), t_row.get('row', ''),
                                       t_row.get(f + '_raw', '')])

    # Write summary
    with open(out_dir / 'agreement_mackay.csv', 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['field', 'ai_rows', 'tess_read', 'coverage', 'agree', 'agreement_pct'])
        for f in FIELDS:
            n, k, ag = stats[f]
            row = [f, n, k,
                   f'{k/n:.0%}' if n else '',
                   ag,
                   f'{ag/k:.1%}' if k else '']
            w.writerow(row)
            print(f'{f:12s}  ai_rows {n:4d}  tess_read {k:4d} ({k/n if n else 0:4.0%})  agree {ag:4d} ({ag/k if k else 0:5.1%})')

    print(f'\nalignment check: Tesseract seal# matches AI in {plate_check[1]}/{plate_check[0]} matched rows')

    with open(out_dir / 'disagreements_mackay.csv', 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['no', 'field', 'ai_value', 'tess_value', 'page', 'row', 'tess_raw'])
        w.writerows(disagreements)
    print(f'Disagreements written: {len(disagreements)} rows to {out_dir}/disagreements_mackay.csv')
