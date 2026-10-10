"""Three-reader vote for Marshall (1931): AI transcription, Tesseract cell reader, repo's earlier line OCR.
Usage: python vote.py <ai_csv> <tess_csv> <old_ocr_csv> <out_csv>"""
import csv, re, sys
from collections import Counter
from agreement import printed_order, ai_fields, clean, FIELDS
ai = {r['plate_no']: ai_fields(r) for r in csv.DictReader(open(sys.argv[1], encoding='utf-8'))}
pos = printed_order()
tess = {}
for r in csv.DictReader(open(sys.argv[2], encoding='utf-8')):
    p = pos.get((r['page'], r['column'], r['row']))
    if p: tess[p] = r
old = {}
pat = re.compile(r"(\d{1,2})\s*[’'°`]\s*,?\s*(\d{1,2})\s*[”\"]")
for r in csv.DictReader(open(sys.argv[3], encoding='utf-8')):
    if r['repaired'] == 'yes': continue
    m = pat.search(r['ocr_line'])
    old[r['plate_no']] = {'type': r['type'], 'area': r['area'], 'serial': r['serial'],
                          'level_ft': m.group(1) if m else '', 'level_in': m.group(2) if m else ''}
rows, tally = [], Counter()
for p, a in ai.items():
    for f in FIELDS:
        if a['level_ft'] == 'surface' and f == 'level_in': continue
        av = clean(f, a[f])
        if av == '' and f != 'level_in': continue
        t = clean(f, tess.get(p, {}).get(f, '')); o = clean(f, old.get(p, {}).get(f, ''))
        others = [v for v in (t, o) if v]
        if not others: cat = 'AI only (no OCR reading)'
        elif all(v == av for v in others): cat = f'AI confirmed by {len(others)} OCR'
        elif any(v == av for v in others): cat = 'AI confirmed by 1 OCR, other OCR differs'
        elif len(others) == 2 and t == o: cat = 'both OCRs agree, AI differs'
        else: cat = 'unconfirmed: OCR differs'
        tally[(f, cat)] += 1
        rows.append([p, f, av, t, o, cat])
with open(sys.argv[4], 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['plate_no', 'field', 'ai', 'tesseract_cells', 'earlier_ocr', 'status']); w.writerows(rows)
cats = ['AI confirmed by 2 OCR', 'AI confirmed by 1 OCR', 'AI confirmed by 1 OCR, other OCR differs',
        'both OCRs agree, AI differs', 'unconfirmed: OCR differs', 'AI only (no OCR reading)']
print('field     ' + ' | '.join(c[:22] for c in cats))
for f in FIELDS:
    n = sum(tally[(f, c)] for c in cats)
    print(f'{f:9s} ' + ' | '.join(f'{tally[(f,c)]:4d}' for c in cats) + f'  (n={n}, confirmed {sum(tally[(f,c)] for c in cats[:3])/n:.0%})')
