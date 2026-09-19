import json, collections, csv
d=json.load(open('mj.json')); T=[tuple(t) for t in d['T']]
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
# 1) minimal pairs: same length, differ in exactly one position
by=collections.defaultdict(list)
for t in set(T):
    for i in range(len(t)): by[(len(t),i,t[:i],t[i+1:])].append(t[i])
swap=collections.Counter(); slotpos=collections.Counter()
for (L,i,a,b),fill in by.items():
    f=sorted(set(fill))
    if len(f)<2: continue
    pos='start' if i==0 else 'end' if i==L-1 else 'mid'
    for x in range(len(f)):
        for y in range(x+1,len(f)):
            swap[(f[x],f[y])]+=1; slotpos[(f[x],f[y],pos)]+=1
print('minimal-pair texts found:',sum(1 for k,v in by.items() if len(set(v))>1))
print('\nMost frequent swaps (sign A <-> sign B, times seen, where):')
for (x,y),c in swap.most_common(15):
    where=max(['start','mid','end'],key=lambda p:slotpos[(x,y,p)])
    same='same visual family' if tags[x]['family']==tags[y]['family'] else f"{tags[x]['family']} / {tags[y]['family']}"
    print(f'  {x} <-> {y}  x{c}  mostly {where:5s}  ({same})')
# 2) slot fillers for the two strongest frames
def fillers(pred):
    c=collections.Counter()
    for t in T:
        for i,s in enumerate(t):
            if pred(t,i): c[s]+=1
    return c.most_common(10)
print('\nSlot after an opener (G861/G817/G820/G692):',fillers(lambda t,i:i==1 and t[0] in('G861','G817','G820','G692')))
print('Slot before final jar G740:',fillers(lambda t,i:i<len(t)-1 and t[i+1]=='G740' and i==len(t)-2))
print('Sign after G740 when jar is not last:',fillers(lambda t,i:i>0 and t[i-1]=='G740'))
print('Sign after a stroke numeral:',fillers(lambda t,i:i>0 and t[i-1] in('G31','G32','G33','G3','G4','G5')))
