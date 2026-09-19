# Do stroke-group numerals appear more in one part of the sequence than another?
# Coded from the plate photographs; 'depth' here is only a rough ordering (see FINDINGS 23).
import csv, numpy as np, collections
from scipy.stats import fisher_exact, mannwhitneyu
C=[r for r in csv.DictReader(open('../transcriptions/mackay1938_plates/photo_codings.csv')) if r.get('numeral_group') in ('yes','no')]
T={r['no']:r for r in csv.DictReader(open('../outputs/mackay_seal_table.csv'))}
g=collections.defaultdict(list)
for r in C:
    t=T.get(r['mackay_no'])
    if not t or r['confidence'] not in ('high','medium'): continue
    g[r['plate']].append((r['numeral_group']=='yes',int(r['n_signs'])))
for k,v in g.items():
    print(f"{k:9s} n={len(v):3d}  stroke-group present {np.mean([x[0] for x in v]):.0%}")
a=g['LXXXIII']; b=g['XCIX']
ya,yb=sum(x[0] for x in a),sum(x[0] for x in b)
print(f'shallow vs deep: {ya}/{len(a)} vs {yb}/{len(b)}, p={fisher_exact([[ya,len(a)-ya],[yb,len(b)-yb]]).pvalue:.3f}')
la=[x[1] for x in a if x[0]]; lb=[x[1] for x in a if not x[0]]
print(f'texts with a stroke group are {np.mean(la):.1f} signs vs {np.mean(lb):.1f} without (shallow plate)')
allnum=[x for v in g.values() for x in v]
wn=[x[1] for x in allnum if x[0]]; wo=[x[1] for x in allnum if not x[0]]
print(f'all coded: with {np.mean(wn):.1f} signs (n={len(wn)}) vs without {np.mean(wo):.1f} (n={len(wo)}), p={mannwhitneyu(wn,wo).pvalue:.3f}')
