# Where seal types cluster at Mohenjo-daro, and whether multi-seal rooms are single deposits.
import csv, collections, re, numpy as np
from scipy.stats import chi2_contingency, fisher_exact
R=[r for r in csv.DictReader(open('../outputs/mackay_seal_table.csv')) if r['no'].isdigit()]
seen=set(); rows=[]
for r in R:
    if r['field_no'] in seen: continue
    seen.add(r['field_no']); rows.append(r)
lev=lambda r: float(r['level_dk_ft']) if r['level_dk_ft'] not in('','None') else None
# 1. indoor vs outdoor by type
out=[r for r in rows if r['street']]; ind=[r for r in rows if r['block'] and not r['street']]
for lab,g in (('indoors (block/house/room)',ind),('streets, lanes, between blocks',out)):
    n=len(g); print(f'{lab:34s} n={n:4d}  type B {sum(r["type"]=="B" for r in g)/n:4.0%}  type F {sum(r["type"]=="F" for r in g)/n:4.0%}')
a=sum(r['type']=='F' for r in ind); b=sum(r['type']=='F' for r in out)
print('  inscription-only seals indoors vs outdoors: p=%.2f'%fisher_exact([[a,len(ind)-a],[b,len(out)-b]]).pvalue)
# 2. type F share by block (blocks with >=15 seals)
byb=collections.defaultdict(list)
for r in ind: byb[r['block']].append(r)
big={k:v for k,v in byb.items() if len(v)>=15}
print('\ntype F share by block (blocks with 15+ seals):')
for k,v in sorted(big.items(),key=lambda x:-sum(r['type']=='F' for r in x[1])/len(x[1])):
    print(f'  Block {k:3s} n={len(v):3d}  F {sum(r["type"]=="F" for r in v)/len(v):4.0%}  median level {np.median([lev(r) for r in v if lev(r) is not None]):6.1f} ft')
T=np.array([[sum(r['type']=='F' for r in v),sum(r['type']!='F' for r in v)] for v in big.values()])
print('  differs between blocks: p=%.2g'%chi2_contingency(T).pvalue)
# 3. multi-seal rooms: single deposit or repeated use?
rooms=collections.defaultdict(list)
for r in ind:
    if r['room']: rooms[(r['block'],r['house'],r['room'])].append(r)
multi={k:v for k,v in rooms.items() if len(v)>=4}
print(f'\nrooms with 4+ seals: {len(multi)}')
spreads=[]
for k,v in sorted(multi.items(),key=lambda x:-len(x[1])):
    ls=[lev(r) for r in v if lev(r) is not None]
    if len(ls)<2: continue
    spreads.append(max(ls)-min(ls))
    print(f'  Bl.{k[0]:3s} {k[1]:4s} rm {k[2]:3s}: {len(v)} seals, levels {min(ls):.1f} to {max(ls):.1f} ft (spread {max(ls)-min(ls):.1f}), types {"".join(sorted(r["type"] for r in v))}')
print(f'median depth spread in multi-seal rooms: {np.median(spreads):.1f} ft')
rng=np.random.default_rng(0); L=[lev(r) for r in ind if lev(r) is not None]
sizes=[len(v) for v in multi.values()]
null=[]
for _ in range(2000):
    for k in sizes:
        s_=rng.choice(L,k,replace=False); null.append(s_.max()-s_.min())
print(f'same-size groups of random indoor seals span {np.median(null):.1f} ft (10th pct {np.percentile(null,10):.1f})')
print(f'share of real rooms tighter than the random median: {np.mean(np.array(spreads)<np.median(null)):.0%}')
