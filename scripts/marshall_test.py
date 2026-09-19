# Independent test of the Mackay result (FINDINGS 19/22): are inscription-only rectangular
# seals (type F) commoner nearer the surface? Marshall's 1922-27 seals, his own depths.
# Mackay's data predict: F commoner nearer the surface, i.e. a NEGATIVE correlation with
# depth below surface here (his datum runs the other way).
import csv, collections, numpy as np
from scipy.stats import spearmanr, mannwhitneyu, fisher_exact
R=[r for r in csv.DictReader(open('../outputs/marshall_seal_table_transcribed.csv')) if r['depth_ft']!='' and r['type']]
d=np.array([float(r['depth_ft']) for r in R]); F=np.array([r['type']=='F' for r in R])
print(f'Marshall seals with a type and a depth: {len(R)} (F: {F.sum()})')
rho,p=spearmanr(d,F.astype(int))
print(f'type F vs depth below surface: rho={rho:+.3f}, p={p:.4f} (negative = F nearer the surface)')
print(f'  median depth: type F {np.median(d[F]):.1f} ft vs others {np.median(d[~F]):.1f} ft; '
      f'p={mannwhitneyu(d[F],d[~F]).pvalue:.4f}')
for lo,hi in ((0,2),(2,4),(4,6),(6,20)):
    m=(d>=lo)&(d<hi)
    if m.sum(): print(f'  {lo}-{hi} ft below surface: n={m.sum():3d}, type F {F[m].mean():.0%}')
# the same test on Mackay's data, for comparison
M=[r for r in csv.DictReader(open('../outputs/mackay_seal_table.csv')) if r['no'].isdigit() and r['level_dk_ft'] not in ('','None')]
lv=np.array([float(r['level_dk_ft']) for r in M]); MF=np.array([r['type']=='F' for r in M])
r2,p2=spearmanr(lv,MF.astype(int))
print(f'\nMackay, for comparison: rho={r2:+.3f}, p={p2:.4f} (positive = F nearer the surface, his datum)')
print('Directions agree' if (rho<0)==(r2>0) else 'Directions DISAGREE')
# areas differ between the two excavations; check the trend is not one area
print('\nby area (Marshall, areas with 25+ seals):')
for a,v in collections.Counter(r['area'] for r in R).most_common():
    if v<25: continue
    m=np.array([r['area']==a for r in R])
    rr,pp=spearmanr(d[m],F[m].astype(int))
    print(f'  {a:3s} n={m.sum():3d}  type F {F[m].mean():.0%}  rho={rr:+.2f} p={pp:.3f}')
