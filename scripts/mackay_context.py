# What Mackay's seal table says about Mohenjo-daro by itself (no texts yet):
# seal shapes and sizes by phase, and where seals concentrate.
import csv, collections, re, numpy as np
from scipy.stats import chi2_contingency, spearmanr
R=[r for r in csv.DictReader(open('../outputs/mackay_seal_table.csv')) if r['no'].isdigit()]
seen=set(); rows=[]
for r in R:                                   # drop repeated entries of the same seal
    k=r['field_no']
    if k in seen: continue
    seen.add(k); rows.append(r)
order=['Late I','Late II','Late III','Intermediate I','Intermediate II','Intermediate III','Early']
ph=[r for r in rows if r['phase_estimate'] in order]
print(f'distinct seals {len(rows)}; with a phase {len(ph)}')
print(f'{"phase":18s}{"seals":>6s}{"type B":>8s}{"type F":>8s}{"other":>7s}{"median B width in":>19s}')
for p in order:
    g=[r for r in ph if r['phase_estimate']==p]
    w=[float(m.group(1)) for r in g if r['type']=='B' for m in [re.match(r'([\d.]+)x',r['dims_in'])] if m]
    print(f'{p:18s}{len(g):6d}{sum(r["type"]=="B" for r in g)/len(g):8.0%}{sum(r["type"]=="F" for r in g)/len(g):8.0%}{sum(r["type"] not in "BF" for r in g)/len(g):7.0%}{np.median(w):19.2f}')
T=np.array([[sum(r['type']==t for r in ph if r['phase_estimate']==p) for t in ('B','F')] for p in order])
T=T[T.sum(1)>0]
print(f'type B vs F across phases: p={chi2_contingency(T).pvalue:.2g}')
bw=[(-float(r['level_dk_ft']),float(m.group(1))) for r in ph if r['type']=='B' for m in [re.match(r'([\d.]+)x',r['dims_in'])] if m]
rho,p=spearmanr([a for a,b in bw],[b for a,b in bw])
print(f'type-B seal width vs depth: rho={rho:.2f}, p={p:.2g}  (positive = deeper seals are larger)')
loc=collections.Counter()
for r in rows:
    if r['block']: loc['Block '+r['block']]+=1
    elif r['street']: loc[re.sub(r'\s*\(.*?\)','',r['street'])]+=1
print('\nwhere seals were found (top 10):')
for k,v in loc.most_common(10): print(f'  {v:4d}  {k}')
rooms=collections.Counter((r['block'],r['house'],r['room']) for r in rows if r['block'] and r['room'])
print('rooms with 4+ seals:',[(f'Bl.{b} {h} rm {rm}',n) for (b,h,rm),n in rooms.most_common() if n>=4])
st=sum(1 for r in rows if r['street']); print(f'seals from streets, lanes or between blocks: {st}/{len(rows)} ({st/len(rows):.0%})')
