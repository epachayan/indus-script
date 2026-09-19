# First test combining text and archaeology: do seal texts differ between phases?
# Uses features read from the plate photographs (transcriptions/.../photo_codings.csv)
# joined to find-spots and levels from Mackay's table.
import csv, collections, numpy as np
from scipy.stats import mannwhitneyu, fisher_exact
C=list(csv.DictReader(open('../transcriptions/mackay1938_plates/photo_codings.csv')))
T={r['no']:r for r in csv.DictReader(open('../outputs/mackay_seal_table.csv'))}
rows=[]
for r in C:
    t=T.get(r['mackay_no'])
    if not t or not t['level_dk_ft']: continue
    if r['confidence'] not in ('high','medium') or int(r['n_signs'])==0: continue
    rows.append(dict(no=r['mackay_no'],n=int(r['n_signs']),jar=r['ends_jar']=='likely',
                     lvl=float(t['level_dk_ft']),phase=t['phase_estimate'],
                     block=t['block'],street=t['street'],typ=t['type'],conf=r['confidence']))
print(f'seals with a coded text and a find-spot: {len(rows)}')
def band(r):
    if r['phase'] in ('surface','Late I','Late II'): return '1 shallow (Late I-II)'
    if r['phase']=='Late III': return '2 Late III'
    if r['phase'].startswith('Intermediate I') and r['phase']!='Intermediate III': return '3 Intermediate I-II'
    return '4 deep (Int III / Early)'
g=collections.defaultdict(list)
for r in rows: g[band(r)].append(r)
g=dict(sorted(g.items()))
for k,v in g.items():
    print(f"  {k:13s} n={len(v):3d}  levels {min(x['lvl'] for x in v):6.1f} to {max(x['lvl'] for x in v):6.1f}  "
          f"signs mean {np.mean([x['n'] for x in v]):.1f} median {np.median([x['n'] for x in v]):.0f}  "
          f"jar ending {np.mean([x['jar'] for x in v]):.0%}")
A,B=g['1 shallow (Late I-II)'],g['4 deep (Int III / Early)']
u=mannwhitneyu([x['n'] for x in A],[x['n'] for x in B])
a,b=sum(x['jar'] for x in A),sum(x['jar'] for x in B)
f=fisher_exact([[a,len(A)-a],[b,len(B)-b]])
print(f'\nshallowest vs deepest\nsign count: p={u.pvalue:.3f}')
print(f'jar ending: {a}/{len(A)} vs {b}/{len(B)}, odds {f.statistic:.2f}, p={f.pvalue:.3f}')
# high-confidence only
hi=[r for r in rows if r['conf']=='high']
ga=[r for r in hi if band(r)=='1 shallow (Late I-II)']; gb=[r for r in hi if band(r)=='4 deep (Int III / Early)']
if len(ga)>=5 and len(gb)>=5:
    print(f'high-confidence only ({len(ga)} vs {len(gb)}): signs p={mannwhitneyu([x["n"] for x in ga],[x["n"] for x in gb]).pvalue:.3f}')
# text length vs depth across all coded seals
lv=[r['lvl'] for r in rows]; n=[r['n'] for r in rows]
from scipy.stats import spearmanr
rho,p=spearmanr(lv,n); print(f'\ntext length vs depth (all {len(rows)}): rho={rho:.2f}, p={p:.3f}')
# seal type
for k,v in g.items():
    print(f"  {k:13s} type F share {np.mean([x['typ']=='F' for x in v]):.0%}")

# how big a difference could this sample have detected?
from statsmodels.stats.power import NormalIndPower, TTestIndPower
from statsmodels.stats.proportion import proportion_effectsize
na,nb=len(A),len(B)
pw=NormalIndPower()
for d in (0.15,0.20,0.25,0.30):
    es=proportion_effectsize(0.42+d/2,0.42-d/2)
    print(f'jar-ending difference of {d:.0%}: power {pw.power(es,na,0.05,ratio=nb/na):.0%}')
need=pw.solve_power(proportion_effectsize(0.52,0.32),power=0.8,alpha=0.05)
print(f'to detect a 20-point difference with 80% power: about {need:.0f} seals per group')
t=TTestIndPower()
print(f'sign count: detectable difference at 80% power = {t.solve_power(None,nobs1=na,alpha=0.05,power=0.8,ratio=nb/na)*np.std([x["n"] for x in rows]):.1f} signs')

# trend across the four depth bands
from scipy.stats import spearmanr as _sp
order={k:i for i,k in enumerate(sorted(g))}
bn=[order[band(r)] for r in rows]
print('\ntrend across the four bands (0 = shallowest):')
for name,vec in (('sign count',[r['n'] for r in rows]),('jar ending',[int(r['jar']) for r in rows]),
                 ('type F',[int(r['typ']=='F') for r in rows])):
    rho,p=_sp(bn,vec); print(f'  {name:11s} rho={rho:+.2f}, p={p:.3f}')
# type F trend on the whole table, for comparison (not just coded seals)
allr=[r for r in csv.DictReader(open('../outputs/mackay_seal_table.csv')) if r['no'].isdigit() and r['level_dk_ft'] not in ('','None')]
lv=[float(r['level_dk_ft']) for r in allr]; tf=[int(r['type']=='F') for r in allr]
rho,p=_sp(lv,tf); print(f'  type F vs level, all {len(allr)} seals: rho={rho:+.2f}, p={p:.4f} (positive = commoner nearer the surface)')
