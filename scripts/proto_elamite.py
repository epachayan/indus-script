# Proto-Elamite (CDLI) vs Indus: entry structure and numeral systems.
# Needs data/cdliatf_unblocked.atf (CDLI dump, Aug 2022).
import re, collections, csv, numpy as np
txt=open('../data/cdliatf_unblocked.atf',encoding='utf8',errors='replace').read()
blocks=[b for b in re.split(r'\n(?=&P\d+)',txt) if len(re.findall(r'\bM\d{3}',b))>=2]
COUNT={'N01','N14','N34','N45','N48','N51','N08','N08A','N8A','N8B','N02','N46','N54','N51G','N1B','N14B'}
CAP={'N39A','N39B','N39C','N30C','N30D','N24','N23','N29B'}
tabs=[]; item_sys=collections.defaultdict(collections.Counter)
for b in blocks:
    ents=[]; side='obverse'
    for l in b.split('\n'):
        if l.startswith('@reverse'): side='reverse'
        m=re.match(r"^\d+'?\.\s*(.*)",l)
        if not m or ',' not in m.group(1): continue
        item,num=m.group(1).split(',',1)
        units=re.findall(r'(\d+)\((N\w+?)\)',num)
        signs=re.findall(r'M\d{3}',item)
        ents.append(dict(item=signs,units=units,side=side))
        if units and signs:
            sys_={('cap' if u in CAP else 'count' if u in COUNT else 'other') for _,u in units}
            for s in set(signs): item_sys[s]['/'.join(sorted(sys_))]+=1
    if ents: tabs.append(ents)
numbered=[[e for e in t if e['units']] for t in tabs]
print(f'Proto-Elamite tablets parsed: {len(tabs)}')
print(f'  with any number: {np.mean([len(n)>0 for n in numbered]):.0%}')
print(f'  with 2+ numbered entries: {np.mean([len(n)>=2 for n in numbered]):.0%}   median entries (numbered tablets): {np.median([len(n) for n in numbered if n]):.0f}')
allu=[(int(k),u) for n in numbered for e in n for k,u in e['units']]
print(f'  entries using a higher unit (N14 and up, not N01 alone): {np.mean([any(u!="N01" for _,u in e["units"]) for n in numbered for e in n]):.0%}')
print(f'  largest single repeat count: {max(k for k,_ in allu)}')
rev=[t for t in tabs if any(e['side']=='reverse' and e['units'] for e in t)]
print(f'  tablets with a numbered line on the reverse (typical total position): {len(rev)/len(tabs):.0%}')
print(f'  signs per item (median): {np.median([len(e["item"]) for t in tabs for e in t if e["item"]]):.0f}')
# commodity-specific systems
mixed=sum(c.get('cap/count',0) for c in item_sys.values()); tot=sum(sum(c.values()) for c in item_sys.values())
print(f'\nnumbered entries mixing both systems in one entry: {mixed/tot:.0%}')
strong=[(s,c) for s,c in item_sys.items() if sum(c.values())>=15]
pure=[s for s,c in strong if max(c.values())/sum(c.values())>=0.9]
print(f'item signs (>=15 numbered uses) using one system >=90% of the time: {len(pure)}/{len(strong)}')
for s,c in sorted(strong,key=lambda x:-sum(x[1].values()))[:10]: print('  ',s,dict(c))

# --- commodity specificity, whole item string, vs shuffled baseline ---
rng=np.random.default_rng(0)
def purity(pairs, minn=10):
    c=collections.defaultdict(list)
    for it,cap in pairs: c[it].append(cap)
    v=[np.mean(x) for x in c.values() if len(x)>=minn]
    return np.mean([(m<=0.1 or m>=0.9) for m in v]), len(v)
pe_pairs=[(' '.join(e['item']), int(any(u in CAP for _,u in e['units']))) for n in numbered for e in n if e['item']]
obs,k=purity(pe_pairs); caps=[c for _,c in pe_pairs]
null=[purity([(i,c) for (i,_),c in zip(pe_pairs,rng.permutation(caps))])[0] for _ in range(200)]
print(f'\nPE: items (>=10 uses) that stick to one system >=90%: {obs:.0%} of {k}; shuffled {np.mean(null):.0%}')
# Indus: item after a numeral; system = short/tiered vs long
exec(open('../scripts/numerals.py').read().split('cnt=collections.Counter')[0])
ind=[(t[i+1], int(VAL[s][0]!='long')) for t in T for i,s in enumerate(t[:-1]) if s in VAL and s!='G2' and t[i+1] not in VAL]
obs,k=purity(ind,5); caps=[c for _,c in ind]
null=[purity([(i,c) for (i,_),c in zip(ind,rng.permutation(caps))],5)[0] for _ in range(200)]
print(f'Indus: items (>=5 uses) that stick to one stroke system >=90%: {obs:.0%} of {k}; shuffled {np.mean(null):.0%}')
# side-by-side
ind_num=[any(s in VAL and s!='G2' for s in t) for t in T]
ind_multi=[sum(1 for a,b in zip(t,t[1:]) if a in VAL and a!='G2' and b not in VAL)>=2 for t in T]
print('\n                        Proto-Elamite   Indus')
print(f'texts with numbers        {np.mean([len(n)>0 for n in numbered]):6.0%}      {np.mean(ind_num):6.0%}')
print(f'texts with 2+ entries     {np.mean([len(n)>=2 for n in numbered]):6.0%}      {np.mean(ind_multi):6.1%}')
print(f'order                     item, number   number, item')
