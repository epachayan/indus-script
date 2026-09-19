import re, csv, collections, numpy as np
from scipy.stats import mannwhitneyu
exec(open('../scripts/numerals.py').read().split('cnt=collections.Counter')[0])
sql=open('../data/indus-website/population-script.sql',encoding='utf8').read()
b=sql[sql.index('INSERT INTO SEAL ('):]; b=b[:b.index(');\n')+1]
dims={c:(m,float(w),float(h)) for _,_,m,c,w,h in re.findall(r'\((\d+),\s*"([^"]*)",\s*"([^"]*)",\s*"([^"]*)",\s*[^,]*,\s*([\d.]+),\s*([\d.]+)',b)}
exec(open('../scripts/objtype.py').read().split("exec(open('../scripts/motif_dedup.py')")[0])
kind=lambda r:(lambda o:'TAB' if 'TAB' in o else 'SEAL' if 'SEAL' in o else '?')(bycisi.get(r['cisi_number'],([],''))[0])
rows=list(csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')))
LONG={s for s in VAL if s!='G2'}
sz=collections.defaultdict(list); mats=collections.defaultdict(collections.Counter); ln=[]
for r in rows:
    if kind(r)!='SEAL' or r['cisi_number'] not in dims: continue
    m,w,h=dims[r['cisi_number']]
    t=r['sign_sequence'].split(); g='numbered' if any(s in LONG for s in t) else 'plain'
    mats[g][m]+=1
    if w>0 and h>0: sz[g].append(w*h); ln.append((w*h,len(t)))
print({g:len(v) for g,v in sz.items()}, 'seals with size')
if sz['numbered'] and sz['plain']:
    print('median area numbered %.1f vs plain %.1f  p=%.3f'%(np.median(sz['numbered']),np.median(sz['plain']),mannwhitneyu(sz['numbered'],sz['plain']).pvalue))
    a=np.array(ln); from scipy.stats import spearmanr; print('area vs text length rho=%.2f p=%.1e'%spearmanr(a[:,0],a[:,1]))
print('materials:',{g:dict(c.most_common(3)) for g,c in mats.items()})
# Harappa tablets vs seals: what gets numbered
FS={'G390','G405','G407'}; fish={s for s,r in tags.items() if r['family']=='fish'}
for k in ('TAB','SEAL'):
    c=collections.Counter()
    for r in rows:
        if r['site']!='Harappa' or kind(r)!=k: continue
        t=[s for s in r['sign_sequence'].split() if s in tags][::-1]
        for a,b_ in zip(t,t[1:]):
            if a in LONG and b_ not in VAL: c[b_]+=1
    n=sum(c.values()); print(f'Harappa {k}: {n} number+item; top',c.most_common(5),
      f"| forked {sum(c[s] for s in FS)/max(n,1):.0%} fish {sum(c[s] for s in fish)/max(n,1):.0%}")
