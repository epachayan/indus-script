"""Independent Tesseract reader for Mackay (1938) 'Further Excavations at Mohenjo-Daro',
Tabulation of Seals, pp. 369-391.

Reads the table cell-by-cell with no information from the AI transcription.
Focuses on the cross-checkable fields: No., Type, Level (ft.), Field No.

Usage: python read_mackay_tesseract.py <pages_dir> <out.csv>
  pages_dir holds mackay_p369.jpg ... mackay_p391.jpg
"""
import csv, re, sys
from pathlib import Path
import cv2, numpy as np, pytesseract
from scipy.signal import find_peaks
from scipy.ndimage import uniform_filter1d

# All our saved images are the same scan resolution: 1803 x 2576 px
REF_W = 1803

# Column x-bands in pixels at REF_W, measured from p389 reference image.
# We only extract the four fields useful for cross-checking.
COLS = {
    'no':       (90,  220),   # Seal number
    'type':     (220, 300),   # Single letter A-I
    'level_ft': (1375, 1510), # Depth in feet (negative decimals + "surface")
    'field_no': (1510, 1720), # Area prefix (DK/SD/H) + field number
}

CFG = {
    'no':       '--psm 7  -c tessedit_char_whitelist=0123456789ABCb',
    'type':     '--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJ',
    'level_ft': '--psm 7  -c tessedit_char_whitelist=0123456789.-+Sur',
    'field_no': '--psm 7  -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ',
}


def ink(g):
    return (g < 150).astype(np.uint8)


def ocr_cell(g, x0, x1, yc, half_h, cfg):
    a, b = max(0, int(yc - half_h)), min(g.shape[0], int(yc + half_h))
    crop = g[a:b, max(0, x0):x1]
    if crop.size == 0 or ink(crop).sum() < 5:
        return ''
    crop = cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    _, crop = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    crop = cv2.copyMakeBorder(crop, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
    return pytesseract.image_to_string(crop, config=cfg).strip()


def find_data_rows(g):
    """Return list of y-centres for data rows, using the No. column ink projection."""
    x0, x1 = COLS['no']
    col_strip = g[:, x0:x1]
    proj = uniform_filter1d(ink(col_strip).sum(1).astype(float), 7)
    peaks, _ = find_peaks(proj, height=proj.max() * 0.06, distance=20)
    if len(peaks) < 2:
        return list(peaks)

    # Filter: keep only peaks in the regular-pitch body of the table
    diffs = np.diff(peaks.astype(float))
    pitch = float(np.median(diffs))
    tol = pitch * 0.35

    # Grow a run of consistent-pitch peaks
    runs, cur = [], [0]
    for i, d in enumerate(diffs):
        if abs(d - pitch) < tol:
            cur.append(i + 1)
        else:
            if len(cur) > 1:
                runs.append(cur)
            cur = [i + 1]
    if len(cur) > 1:
        runs.append(cur)
    if not runs:
        return [int(p) for p in peaks]

    best = max(runs, key=len)

    # Also include adjacent peaks that are one-pitch away from body ends
    body_ys = [int(peaks[i]) for i in best]
    first_y, last_y = body_ys[0], body_ys[-1]

    # One row before body?
    extra_before = [int(p) for p in peaks if abs(p - (first_y - pitch)) < tol]
    # Rows after body?
    extra_after  = [int(p) for p in peaks if p > last_y and abs((p - last_y) % pitch) < tol]

    return extra_before + body_ys + extra_after


def norm_level(s):
    """Normalise OCR output for level_ft.

    The 1938 book uses a raised middle dot (·) as decimal separator, which
    Tesseract reads as a hyphen.  Convert '19-4' → '19.4', then restore sign.
    """
    s = s.strip().replace(' ', '')
    if not s:
        return ''
    if re.search(r'[Ss]', s, re.I):
        return 'surface'
    # restore decimal: digit-hyphen-digit → digit.digit
    s = re.sub(r'(\d)-(\d)', r'\1.\2', s)
    # if leading digit without sign, assume negative (all depths in this table are ≤ +7.3)
    # keep explicit '+' or '-' if present
    return s


def norm_field(s):
    """Normalise OCR output for field_no.

    Expected: 'DK 7374' or 'SD 2823'.  OCR often reads the column rule as '1'
    giving 'DK17374'.  Strip spurious characters between prefix and digits.
    """
    s = s.strip()
    # Find 2-letter area prefix
    m = re.match(r'^([A-Z]{1,3})\s*1?\s*(\d{3,5}[A-Za-z]?)$', s)
    if m:
        return f'{m.group(1)} {m.group(2)}'
    # If no prefix found, try just returning the numeric part
    m2 = re.match(r'^[A-Z0-9 ]+$', s)
    return s if m2 else ''


def read_page(path, printed_page):
    g = cv2.imread(str(path), 0)
    if g is None:
        print(f'  could not read {path}', file=sys.stderr)
        return []

    # Scale column bands to actual image width
    scale = g.shape[1] / REF_W
    cols_scaled = {k: (int(x0 * scale), int(x1 * scale)) for k, (x0, x1) in COLS.items()}

    row_ys = find_data_rows(g)
    if not row_ys:
        print(f'  no rows found on page {printed_page}', file=sys.stderr)
        return []

    pitch = float(np.median(np.diff(row_ys))) if len(row_ys) > 1 else 30
    half_h = pitch * 0.45

    rows = []
    row_idx = 0
    for yc in row_ys:
        vals = {}
        for field, (x0, x1) in cols_scaled.items():
            raw = ocr_cell(g, x0, x1, yc, half_h, CFG[field])
            vals[field + '_raw'] = raw

        # Normalise
        no_raw = vals['no_raw']
        # Accept variants like '636A', '636B', '636C'
        no_clean = re.sub(r'[^0-9A-Za-z]', '', no_raw)
        vals['no'] = no_clean

        vals['type'] = (vals['type_raw'] or '')[:1].upper()
        vals['level_ft'] = norm_level(vals['level_ft_raw'])
        vals['field_no'] = norm_field(vals['field_no_raw'])

        row_idx += 1
        rows.append({
            'page': printed_page,
            'row':  row_idx,
            **vals,
        })

    return rows


if __name__ == '__main__':
    pages_dir, dest = Path(sys.argv[1]), sys.argv[2]
    all_rows = []
    for p in range(369, 392):
        f = pages_dir / f'mackay_p{p}.jpg'
        if f.exists():
            rows = read_page(f, p)
            all_rows += rows
            print(f'  page {p}: {len(rows)} rows', file=sys.stderr)
        else:
            print(f'  page {p}: missing', file=sys.stderr)

    keys = ['page', 'row', 'no', 'type', 'level_ft', 'field_no',
            'no_raw', 'type_raw', 'level_ft_raw', 'field_no_raw']
    with open(dest, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, keys, extrasaction='ignore')
        w.writeheader()
        w.writerows(all_rows)
    print(f'Wrote {len(all_rows)} rows to {dest}')
