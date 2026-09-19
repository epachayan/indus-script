import csv, collections, numpy as np
from scipy.stats import fisher_exact
exec(open('../scripts/numerals.py').read().split('seen=set(); T=[]')[0])
rows=[r for r in csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')) if r['site']=='Mohenjo-daro' and r['motif'] not in ('unknown','')]
grp=lambda m:'unicorn' if m.startswith('Bull1') else 'other'
seen=set(); D=[]
for r in rows:
    t=[s for s in r['sign_sequence'].split() if s in tags][::-1]
    k=(grp(r['motif']),tuple(t))
    if len(t)>=2 and k not in seen: seen.add(k); D.append((grp(r['motif']),r['motif'],t))
n=collections.Counter(g for g,_,_ in D); print('MJ texts with motif:',dict(n))
LONG={s for s in VAL if VAL[s][0]=='long'}; SHORT={s for s in VAL if VAL[s][0]!='long' and s!='G2'}
feat={
 'starts with opener':lambda t:t[0] in('G861','G817','G820','G692'),
 'opener + G2 unit':lambda t:t[0] in('G861','G817','G820') and t[1]=='G2',
 'ends with jar G740':lambda t:t[-1]=='G740',
 'jar + closer (G90/G400)':lambda t:any(a=='G740' and b in('G90','G400') for a,b in zip(t,t[1:])),
 'has long-stroke count':lambda t:any(s in LONG for s in t),
 'has short-stroke count':lambda t:any(s in SHORT for s in t),
 'has fish':lambda t:any(tags[s]['family']=='fish' for s in t),
 'has forked stem':lambda t:any(s in('G390','G405','G407') for s in t),
 'long text (6+)':lambda t:len(t)>=6}
print(f'{"feature":26s} unicorn  other   p')
for k,f in feat.items():
    a=sum(f(t) for g,_,t in D if g=='unicorn'); b=sum(f(t) for g,_,t in D if g=='other')
    p=fisher_exact([[a,n['unicorn']-a],[b,n['other']-b]]).pvalue
    print(f'{k:26s} {a/n["unicorn"]:6.0%} {b/n["other"]:6.0%}  {p:.3f}{" *" if p<0.05/len(feat) else ""}')
# which openers by motif
for g in ('unicorn','other'):
    print(g,'openers:',collections.Counter(t[0] for gg,_,t in D if gg==g and t[0] in('G861','G817','G820','G692')))
print('other-animal breakdown:',collections.Counter(m for g,m,_ in D if g=='other').most_common(6))
