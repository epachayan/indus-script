# Roadmap B4: find-spots from Mackay (1938) joined to inscriptions.
# Needs outputs/findspots_mackay.csv (parse_mackay.py). The join to texts needs
# data/concordance_cisi_mackay.csv with columns: cisi,mackay_no  (e.g. M-305,420)
import csv, os, collections, numpy as np
from scipy.stats import chi2_contingency, fisher_exact
F=list(csv.DictReader(open('../outputs/findspots_mackay.csv')))
F=[r for r in F if r['level_ft']!='']
print(f'seals with a level: {len(F)}')
print('by area:',dict(collections.Counter(r['area'] or '?' for r in F)))
print('by phase (estimated from level):',dict(collections.Counter(r['phase_estimate'] for r in F)))
print('busiest blocks/streets:',collections.Counter((r['area'],r['block']) for r in F if r['block']).most_common(8))
conc='../data/concordance_cisi_mackay.csv'
if not os.path.exists(conc):
    print('\nNo concordance file yet: texts cannot be joined to find-spots.'); raise SystemExit
cm={}
for r in csv.DictReader(open(conc)):
    if r['mackay_no'].strip(): cm[int(r['mackay_no'])]=r['cisi'].strip().upper().replace(' ','')
T={r['cisi'].upper().replace(' ',''):r['signs_reading_order'].split() for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']}
J=[(r,T[cm[int(r['mackay_no'])]]) for r in F if int(r['mackay_no']) in cm and cm[int(r['mackay_no'])] in T]
print(f'\njoined seals with text: {len(J)}')
if len(J)<30: print('too few joined seals for tests'); raise SystemExit
OPEN={'G861','G817','G820','G692'}
feat={'opener':lambda t:t[0] in OPEN,'ends in jar':lambda t:t[-1]=='G740','arrow':lambda t:'G520' in t,
      '3 + arrow':lambda t:any(a=='G33' and b=='G520' for a,b in zip(t,t[1:])),'fish':lambda t:any(s in('G220','G235','G240','G233','G231') for s in t),
      '6+ signs':lambda t:len(t)>=6}
for grp_name,key in (('phase',lambda r:'Late' if r['phase_estimate'].startswith('Late') else 'Intermediate/Early'),
                     ('area',lambda r:r['area'] or '?')):
    groups=collections.defaultdict(list)
    for r,t in J: groups[key(r)].append(t)
    gs=[g for g in groups if len(groups[g])>=10]
    if len(gs)<2: continue
    print(f'\nby {grp_name}: '+', '.join(f'{g} n={len(groups[g])}' for g in gs))
    for k,f in feat.items():
        tab=np.array([[sum(f(t) for t in groups[g]),sum(not f(t) for t in groups[g])] for g in gs])
        p=chi2_contingency(tab).pvalue if (tab.sum(0)>0).all() else float('nan')
        print(f'  {k:12s} '+'  '.join(f'{g}: {tab[i,0]/tab[i].sum():.0%}' for i,g in enumerate(gs))+f'   p={p:.2g}')
