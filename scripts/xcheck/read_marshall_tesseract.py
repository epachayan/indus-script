"""Independent reader 1 for Marshall (1931) "Tabulation of Seals", pp. 402-405.

Reads the printed table with Tesseract, one cell at a time, using no information
from the AI transcription. Output: one row per printed row, in page order.

Usage: python read_marshall_tesseract.py <pages_dir> <out.csv>
  pages_dir holds marshall_p402.jpg ... marshall_p405.jpg (any resolution).
"""
import csv, re, sys
from pathlib import Path
import cv2, numpy as np, pytesseract
from scipy.signal import find_peaks
import os, shutil
# Windows: Tesseract is usually not on PATH after a winget install
if not shutil.which('tesseract'):
    for c in (os.environ.get('TESSERACT_CMD', ''), r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        if c and os.path.exists(c): pytesseract.pytesseract.tesseract_cmd = c; break

# Column bands of the LEFT half, in pixels at the reference width (p.402, 2014 px),
# measured from the start of the printed table. The right half repeats them.
REF_W = 2014
COLS = {  # name: (x_from, x_to) relative to the left edge of the plate-no column
    'plate_no': (-6, 38), 'size': (50, 180), 'level': (203, 287),
    'type': (318, 352), 'serial': (582, 692),
}
CFG = {
    'plate_no': "--psm 7 -c tessedit_char_whitelist=0123456789b",
    'level':    "--psm 7 -c tessedit_char_whitelist=0123456789Sur.?",
    'digits':   "--psm 7 -c tessedit_char_whitelist=0123456789",
    'type':     "--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJ?",
    'serial':   "--psm 7 -c tessedit_char_whitelist=ABCDEFHJKLMRSUVa0123456789",
    'size':     "--psm 7 -c tessedit_char_whitelist=0123456789.x?",
}

def ink(g): return (g < 150).astype(np.uint8)

def table_starts(g):
    """x where the left table starts and where the right table starts."""
    h, w = g.shape
    col = ink(g[int(h*.30):int(h*.90)]).sum(0)
    on = np.where(col > 6)[0]
    left = on[0]
    # widest blank run in the middle third = gap between the two halves
    best, run = (0, 0), None
    for x in range(int(w*.40), int(w*.62)):
        if col[x] <= 3:
            run = x if run is None else run
        elif run is not None:
            if x - run > best[1] - best[0]: best = (run, x)
            run = None
    return int(left), int(best[1])

def row_ys(g, x0, x1, n=70):
    """n row centres: regular grid fitted to the projection peaks, refined locally."""
    h = g.shape[0]
    prof = np.convolve(ink(g[:, x0:x1]).sum(1).astype(float), np.ones(5)/5, 'same')
    pk, _ = find_peaks(prof, distance=15, height=prof.max()*0.15)
    runs, cur = [], [pk[0]]
    for a, b in zip(pk, pk[1:]):
        if 16 <= b - a <= 34: cur.append(b)
        else: runs.append(cur); cur = [b]
    runs.append(cur)
    body = max(runs, key=len)
    pitch = float(np.median(np.diff(body)))
    # anchor on the first and last confident peaks of the table body
    first = [r for r in runs if len(r) >= 10][0][0]
    last = body[-1] if len(body) > 40 else pk[-1]
    pitch = (last - first) / (n - 1)
    return [first + k*pitch for k in range(n)], pitch

def refine(g, y, x0, x1, pitch):
    """Re-centre a row inside one column band (handles slight skew)."""
    a, b = int(y - pitch*.6), int(y + pitch*.6)
    prof = ink(g[a:b, x0:x1]).sum(1)
    if prof.max() == 0: return int(y)
    k = np.convolve(prof, np.ones(7), 'same')
    return a + int(np.argmax(k))

def ocr_cell(g, x0, x1, yc, pitch, cfg):
    a, b = int(yc - pitch*.48), int(yc + pitch*.48)
    crop = g[max(a, 0):b, max(x0, 0):x1]
    if crop.size == 0 or ink(crop).sum() < 15: return ''
    crop = cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    _, crop = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    crop = cv2.copyMakeBorder(crop, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
    return pytesseract.image_to_string(crop, config=cfg).strip()

def read_level(g, x0, x1, yc, pitch):
    """Feet and inches are printed apart (3' 0"): split at the widest blank gap."""
    whole = ocr_cell(g, x0, x1, yc, pitch, CFG['level'])
    if whole[:1] in 'S' and whole: return 'surface', '', whole
    a, b = int(yc - pitch*.48), int(yc + pitch*.48)
    prof = ink(g[a:b, x0:x1]).sum(0)
    xs = np.where(prof > 0)[0]
    if len(xs) == 0: return '', '', whole
    best, run = (0, 0), None
    for x in range(xs[0], xs[-1]):
        if prof[x] == 0: run = x if run is None else run
        elif run is not None:
            if x - run > best[1] - best[0]: best = (run, x)
            run = None
    if best[1] - best[0] < 6: return '', '', whole
    cut = (best[0] + best[1]) // 2
    ft = re.sub(r'\D', '', ocr_cell(g, x0, x0 + cut, yc, pitch, CFG['digits']))
    inch = re.sub(r'\D', '', ocr_cell(g, x0 + cut, x1, yc, pitch, CFG['digits']))
    # the foot and inch marks can be read as an extra digit: keep the leading 1-2 / 1-2 digits
    return ft[:2], inch[:2], whole

def norm_level(s):
    s = s.replace(' ', '')
    if s.lower().startswith('sur'): return 'surface', ''
    m = re.match(r"^(\d{1,2})['\"]?(\d{1,2})", s)
    return (m.group(1), m.group(2)) if m else ('', '')

def norm_serial(s):
    m = re.match(r"^([A-Z]{1,3})\s*(\d+[a]?)$", s.replace(' ', ''))
    return (m.group(1), m.group(2)) if m else ('', '')

_REF = {}
def col_profile(g, x0, scale):
    h = g.shape[0]
    a, b = x0 - int(60*scale), x0 + int(760*scale)
    p = ink(g[int(h*.30):int(h*.90), max(a,0):b]).sum(0).astype(float)
    p = cv2.resize(p.reshape(1,-1), (820, 1)).ravel()   # to reference scale
    return (p - p.mean()) / (p.std() + 1e-9)

def align(g, x0, scale):
    """Shift x0 so this half's column profile best matches the reference half."""
    if 'p' not in _REF: return x0
    best = max(range(-50, 51), key=lambda d: float(np.dot(col_profile(g, x0 + int(d*scale), scale), _REF['p'])))
    return x0 + int(best*scale)

def set_reference(path):
    g = cv2.imread(str(path), 0); scale = g.shape[1] / REF_W
    _REF['p'] = col_profile(g, table_starts(g)[0], scale)

def read_page(path, page):
    g = cv2.imread(str(path), 0)
    scale = g.shape[1] / REF_W
    lx, rx = table_starts(g)
    lx, rx = align(g, lx, scale), align(g, rx, scale)
    out = []
    for half, x0 in (('L', lx), ('R', rx)):
        band = (x0 + int(COLS['plate_no'][0]*scale), x0 + int(COLS['serial'][1]*scale))
        ys, pitch = row_ys(g, *band)
        for i, y in enumerate(ys):
            rec = {'page': page, 'column': half, 'row': i + 1}
            for name, (a, b) in COLS.items():
                xa, xb = x0 + int(a*scale), x0 + int(b*scale)
                yc = refine(g, y, xa, xb, pitch)
                rec[name + '_raw'] = ocr_cell(g, xa, xb, yc, pitch, CFG[name])
            xa, xb = x0 + int(COLS['level'][0]*scale), x0 + int(COLS['level'][1]*scale)
            rec['level_ft'], rec['level_in'], rec['level_raw'] = read_level(g, xa, xb, refine(g, y, xa, xb, pitch), pitch)
            rec['area'], rec['serial'] = norm_serial(rec['serial_raw'])
            rec['type'] = rec['type_raw'][:1]
            rec['plate_no'] = rec['plate_no_raw']
            out.append(rec)
    return out

if __name__ == '__main__':
    pages, dest = Path(sys.argv[1]), sys.argv[2]
    rows = []
    set_reference(pages / 'marshall_p402.jpg')
    for p in (402, 403, 404, 405):
        f = pages / f'marshall_p{p}.jpg'
        if f.exists():
            rows += read_page(f, p); print('read', f.name, file=sys.stderr)
    keys = ['page', 'column', 'row', 'plate_no', 'type', 'level_ft', 'level_in', 'area', 'serial',
            'plate_no_raw', 'size_raw', 'level_raw', 'type_raw', 'serial_raw']
    with open(dest, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, keys, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
