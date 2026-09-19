import csv, collections, math, numpy as np, json
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
rows=[r for r in csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')) if r['site']=='Mohenjo-daro']
seen=set(); T=[]
for r in rows:
    if r['sign_sequence'] in seen: continue
    seen.add(r['sign_sequence'])
    t=[s for s in r['sign_sequence'].split() if s in tags][::-1]
    if len(t)>=2: T.append(t)
uni=collections.Counter(s for t in T for s in t); N=sum(uni.values())
big=collections.Counter((a,b) for t in T for a,b in zip(t,t[1:])); NB=sum(big.values())
def pmi(a,b): return math.log2((big[(a,b)]/NB)/((uni[a]/N)*(uni[b]/N)))
# strong pairs: count>=5 and PMI>=3
strong={p:(c,round(pmi(*p),1)) for p,c in big.items() if c>=5 and pmi(*p)>=3}
print('MJ unique texts',len(T),'tokens',N,'distinct bigrams',len(big),'strong bigrams',len(strong))
# grow to trigrams / 4-grams that are chains of strong pairs
ng=collections.Counter()
for t in T:
    for n in (3,4):
        for i in range(len(t)-n+1):
            g=tuple(t[i:i+n])
            if all((g[j],g[j+1]) in strong for j in range(n-1)): ng[g]+=1
blocks={g:c for g,c in ng.items() if c>=4}
# segment: cut between signs unless the pair is strong
segs=collections.Counter(); seglen=collections.Counter(); textsegs=[]
for t in T:
    cur=[t[0]]; out=[]
    for a,b in zip(t,t[1:]):
        if (a,b) in strong: cur.append(b)
        else: out.append(tuple(cur)); cur=[b]
    out.append(tuple(cur)); textsegs.append(out)
    for s in out:
        if len(s)>1: segs[s]+=1
    seglen[len(out)]+=1
cover=sum(len(s) for o in textsegs for s in o if len(s)>1)/N
print(f'share of tokens inside multi-sign blocks: {cover:.0%}; segments per text:',dict(sorted(seglen.items())))
pos=collections.defaultdict(collections.Counter)
for o in textsegs:
    for i,s in enumerate(o):
        if len(s)>1: pos[s]['start' if i==0 else 'end' if i==len(o)-1 else 'mid']+=1
print('\nTop building blocks (reading order):')
for s,c in segs.most_common(25):
    p=pos[s]; n=sum(p.values())
    cls=' + '.join(tags[x]['behaviour_class'].split(' (')[0] or '-' for x in s)
    print(f'{c:4d}  {" ".join(s):28s} start {p["start"]/n:4.0%} end {p["end"]/n:4.0%}   [{cls}]')
json.dump(dict(T=T,strong=[list(k) for k in strong],segs=[[list(k),v] for k,v in segs.items()]),open('mj.json','w'))
