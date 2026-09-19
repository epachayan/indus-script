# Roadmap 3e: the "2/3 + arrow (G520)" formula across sites and object types.
import csv, collections, numpy as np
from scipy.stats import fisher_exact
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['first_occurrence']=='True' and int(r['n_signs'])>=2]
NUM={'G1','G3','G4','G5','G7','G16','G17','G18','G19','G31','G32','G33','G35'}
def has_formula(t): return any(a in NUM and b=='G520' for a,b in zip(t,t[1:]))
def has_arrow(t): return 'G520' in t
grp=collections.defaultdict(lambda:[0,0,0])
for r in rows:
    t=r['signs_reading_order'].split()
    k=(r['site'] if r['site'] in('Mohenjo-daro','Harappa') else 'other sites', r['object_type'])
    g=grp[k]; g[0]+=1; g[1]+=has_arrow(t); g[2]+=has_formula(t)
print(f'{"site / object":32s}{"texts":>7s}{"arrow":>8s}{"count+arrow":>13s}{"share of arrows":>17s}')
for k,(n,a,f) in sorted(grp.items(),key=lambda x:-x[1][0]):
    if n<20: continue
    print(f'{" / ".join(k):32s}{n:7d}{a/n:8.1%}{f/n:13.1%}{(f/a if a else 0):17.0%}')
# which counts, by site
for site in ('Mohenjo-daro','Harappa'):
    c=collections.Counter(a for r in rows if r['site']==site for a,b in zip(r['signs_reading_order'].split(),r['signs_reading_order'].split()[1:]) if a in NUM and b=='G520')
    print(site,'counts before arrow:',c.most_common(5))
# arrow texts: jar present?
for site in ('Mohenjo-daro','Harappa'):
    T=[r['signs_reading_order'].split() for r in rows if r['site']==site]
    a=[t for t in T if 'G520' in t]; o=[t for t in T if 'G520' not in t]
    ja=sum('G740' in t for t in a); jo=sum('G740' in t for t in o)
    print(f'{site}: jar present in {ja/len(a):.0%} of arrow texts vs {jo/len(o):.0%} of others (p={fisher_exact([[ja,len(a)-ja],[jo,len(o)-jo]]).pvalue:.2g})')
# position of the arrow
pos=collections.Counter('last' if t[-1]=='G520' else 'first' if t[0]=='G520' else 'mid' for t in (r['signs_reading_order'].split() for r in rows) if 'G520' in t)
print('arrow position (all sites):',dict(pos))
