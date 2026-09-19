import csv, collections
VAL={'G1':('short',1),'G2':('short',2),'G3':('short',3),'G4':('short',4),'G5':('short',5),'G7':('short',7),
     'G16':('tiered',6),'G17':('tiered',7),'G18':('tiered',8),'G19':('tiered',9),
     'G31':('long',1),'G32':('long',2),'G33':('long',3),'G35':('long',5)}
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
seen=set(); T=[]
for r in csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')):
    if r['sign_sequence'] in seen: continue
    seen.add(r['sign_sequence']); t=[s for s in r['sign_sequence'].split() if s in tags][::-1]
    if t: T.append(t)
cnt=collections.Counter(s for t in T for s in t if s in VAL)
for ser in ('short','tiered','long'):
    print(ser, {VAL[s][1]:cnt[s] for s in VAL if VAL[s][0]==ser})
# position and what follows, by series
for ser in ('short','long'):
    pos=collections.Counter(); nxt=collections.Counter(); prv=collections.Counter()
    for t in T:
        for i,s in enumerate(t):
            if s in VAL and VAL[s][0]==ser:
                pos['start' if i==0 else 'end' if i==len(t)-1 else 'mid']+=1
                if i<len(t)-1: nxt[t[i+1]]+=1
                if i>0: prv[tags[t[i-1]]['behaviour_class'] or 'rare']+=1
    n=sum(pos.values())
    print(f'\n{ser}: start {pos["start"]/n:.0%} mid {pos["mid"]/n:.0%} end {pos["end"]/n:.0%}')
    print('  followed by:',nxt.most_common(6)); print('  preceded by class:',prv.most_common(4))
# G2 specifically vs G32
for s in ('G2','G32'):
    pr=collections.Counter(t[i-1] for t in T for i,x in enumerate(t) if x==s and i>0)
    print(f'\n{s} preceded by:',pr.most_common(5), ' opener share', f"{sum(pr[o] for o in ('G861','G817','G820','G692'))/sum(pr.values()):.0%}")
# countable items: signs following numerals, with how many distinct values
items=collections.defaultdict(collections.Counter)
for t in T:
    for i,s in enumerate(t[:-1]):
        if s in VAL and t[i+1] not in VAL: items[t[i+1]][VAL[s][1]]+=1
print('\nSigns counted with the most distinct values:')
for s,c in sorted(items.items(),key=lambda x:(-len(x[1]),-sum(x[1].values())))[:10]:
    print(f'  {s:6s} ({tags[s]["family"]}): values {dict(sorted(c.items()))}')
