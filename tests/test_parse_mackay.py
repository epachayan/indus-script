# Run from repo root: python3 tests/test_parse_mackay.py
import csv, subprocess, sys, os
out='/tmp/_mackay_test.csv'
subprocess.run([sys.executable,'scripts/parse_mackay.py','tests/mackay_sample.txt',out],check=True)
rows={int(r['mackay_no']):r for r in csv.DictReader(open(out))}
expect={701:('-1.1','SD 3192','1'),698:('0.1','SD 3058','1'),697:('1.2','','Main Street'),695:('2.1','','Main Street'),
        703:('-1.1','','10'),78:('-5.9','','1A'),376:('-11.8','','1A'),488:('-14.5','','1A')}
bad=[]
for k,(lv,fd,bl) in expect.items():
    r=rows.get(k)
    if not r or r['level_ft']!=lv or r['field_no']!=fd or r['block']!=bl: bad.append((k,r and (r['level_ft'],r['field_no'],r['block'])))
print('OK' if not bad else f'FAILED: {bad}'); sys.exit(1 if bad else 0)
