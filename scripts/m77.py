import csv, collections, math
rs=list(csv.DictReader(open('../data/indus_decipher/data/m77_indusscript_real_corpus.csv')))
seen=set(); T=[]
for r in rs:
    t=r['sign_sequence'].split()
    if 'MSg0' in t or len(t)<2 or r['sign_sequence'] in seen: continue   # MSg0 = unidentified sign
    seen.add(r['sign_sequence']); T.append(t)
print('clean distinct lines',len(T))
jp=collections.Counter('last' if t[-1]=='MSg342' else 'first' if t[0]=='MSg342' else 'mid' for t in T if 'MSg342' in t)
print('M342 (jar) position as stored:',jp)
uni=collections.Counter(s for t in T for s in t); N=sum(uni.values())
big=collections.Counter((a,b) for t in T for a,b in zip(t,t[1:])); NB=sum(big.values())
pmi=lambda a,b: math.log2((big[(a,b)]/NB)/((uni[a]/N)*(uni[b]/N)))
strong={p for p,c in big.items() if c>=5 and pmi(*p)>=3}
inblk=sum(1 for t in T for i,s in enumerate(t) if (i>0 and (t[i-1],s) in strong) or (i<len(t)-1 and (s,t[i+1]) in strong))/N
print(f'tokens inside strong blocks: {inblk:.0%}')
# openers: signs with >=70% initial position and freq>=20
P=collections.defaultdict(collections.Counter)
for t in T:
    for i,s in enumerate(t): P[s]['i' if i==0 else 'f' if i==len(t)-1 else 'm']+=1
op=[s for s,c in P.items() if sum(c.values())>=20 and c['i']/sum(c.values())>=0.7]
print('openers (>=70% initial):',op)
after=collections.Counter(t[1] for t in T if t[0] in op)
print('  slot after openers:',after.most_common(5), f"top filler share {after.most_common(1)[0][1]/sum(after.values()):.0%}")
pre=collections.Counter(t[-2] for t in T if t[-1]=='MSg342'); print('pre-jar slot:',pre.most_common(6))
post=collections.Counter(t[i+1] for t in T for i,s in enumerate(t[:-1]) if s=='MSg342'); print('after jar when not last:',post.most_common(5), 'share of jars not last', f"{sum(post.values())/uni['MSg342']:.0%}")
# minimal pairs among openers
by=collections.defaultdict(set)
for t in set(map(tuple,T)): by[(len(t),t[1:])].add(t[0])
sw=collections.Counter()
for f in by.values():
    f=sorted(f)
    for i in range(len(f)):
        for j in range(i+1,len(f)): sw[(f[i],f[j])]+=1
print('top start-slot swaps:',sw.most_common(6))
