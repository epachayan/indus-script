"""Compare the AI transcription of Marshall (1931) with independent readers.

Usage: python agreement.py <ai_csv> <reader_csv> [<reader_csv> ...] --out <dir>

Rows are matched by printed position (page, half, row), not by content: the table
prints plate numbers 1-557 in order, with 526b and 528b after 526 and 528, and 557b
last. A reader's own plate-number reading is reported as a check on that alignment.
"""
import csv, re, sys
from collections import defaultdict
from pathlib import Path

def printed_order():
    seq = [str(i) for i in range(1, 491)]
    right = []
    for i in range(491, 558):
        right.append(str(i))
        if i in (526, 528): right.append(f'{i}b')
    right.append('557b')
    seq += right
    pos = {}
    k = 0
    for page in (402, 403, 404, 405):
        for half in 'LR':
            for row in range(1, 71):
                pos[(str(page), half, str(row))] = seq[k]; k += 1
    return pos

def ai_fields(r):
    return {'type': r['type'], 'area': r['area'], 'serial': r['serial'],
            'level_ft': r['level_ft'] if r['level_ft'] != 'surface' else 'surface',
            'level_in': '' if r['level_ft'] == 'surface' else (r['level_in'] or '0')}

def clean(field, v):
    v = (v or '').strip()
    if field == 'level_in' and v == '': return ''
    if field in ('serial', 'level_ft', 'level_in'): v = v.lstrip('0') or ('0' if v else '')
    return v

FIELDS = ['type', 'area', 'serial', 'level_ft', 'level_in']

if __name__ == '__main__':
    args = sys.argv[1:]
    out = Path(args[args.index('--out') + 1]); readers = args[1:args.index('--out')]
    out.mkdir(exist_ok=True)
    ai = {r['plate_no']: ai_fields(r) for r in csv.DictReader(open(args[0], encoding='utf-8'))}
    pos = printed_order()
    stats = defaultdict(lambda: [0, 0, 0])   # field -> [ai rows, reader read it, agree]
    plate_check = [0, 0]
    disagreements = []
    for rpath in readers:
        name = Path(rpath).stem
        for r in csv.DictReader(open(rpath, encoding='utf-8')):
            plate = pos.get((r['page'], r['column'], r['row']))
            if plate is None or plate not in ai: continue
            if r.get('plate_no'):
                plate_check[0] += 1; plate_check[1] += r['plate_no'] == plate
            a = ai[plate]
            for f in FIELDS:
                av, rv = clean(f, a[f]), clean(f, r.get(f, ''))
                if f == 'level_in' and a['level_ft'] == 'surface': continue
                if av == '' and f != 'level_in': continue
                s = stats[(name, f)]; s[0] += 1
                if rv == '': continue
                s[1] += 1
                if rv == av: s[2] += 1
                else:
                    disagreements.append([name, plate, r['page'], r['column'], r['row'], f, av, rv,
                                          r.get(f.split('_')[0] + '_raw', '') or r.get('serial_raw', '')])
    with open(out / 'agreement_summary.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['reader', 'field', 'rows', 'read_by_reader', 'coverage', 'agree', 'agreement'])
        for (name, f), (n, k, ag) in sorted(stats.items()):
            w.writerow([name, f, n, k, f'{k/n:.0%}' if n else '', ag, f'{ag/k:.1%}' if k else ''])
            print(f'{name:28s} {f:9s} rows {n:3d}  read {k:3d} ({k/n:4.0%})  agree {ag:3d} ({(ag/k if k else 0):5.1%})')
    print(f'alignment check: reader plate numbers match printed order in {plate_check[1]}/{plate_check[0]} rows read')
    with open(out / 'disagreements.csv', 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['reader', 'plate_no', 'page', 'column', 'row', 'field', 'ai_value', 'reader_value', 'reader_raw'])
        w.writerows(disagreements)
