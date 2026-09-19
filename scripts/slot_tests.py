# Three tests around the fixed final slot (FINDINGS 28):
#  1. Is the ending a CLOSED class? (how many signs cover 90% of each position)
#  2. Does the opener PREDICT the ending? (mutual information vs a permutation null)
#  3. Does a meaningless IDENTIFIER system reproduce the asymmetry? (synthetic control)
import csv, collections, math, random, numpy as np
random.seed(23)
def H(seq):
    c=collections.Counter(seq); n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
def cover(seq,frac=0.9):
    c=collections.Counter(seq); n=sum(c.values()); run=0
    for i,(_,v) in enumerate(c.most_common(),1):
        run+=v
        if run>=frac*n: return i
    return len(c)
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']]
T=[r['signs_reading_order'].split() for r in rows if r['site']=='Mohenjo-daro']
T=[t for t in T if len(t)>=3]
print(f'Mohenjo-daro texts with 3+ signs: {len(T)}')

print('\n--- 1. Is the ending a closed class? ---')
first=[t[0] for t in T]; last=[t[-1] for t in T]; mid=[s for t in T for s in t[1:-1]]
for lab,seq in (('first position',first),('medial positions',mid),('final position',last)):
    print(f'  {lab:17s} distinct {len(set(seq)):4d}   signs covering 90% of tokens: {cover(seq):4d}   '
          f'commonest {collections.Counter(seq).most_common(1)[0][1]/len(seq):.0%}')
print('  (a closed class = few signs cover almost everything; open = many)')

print('\n--- 2. Does the opener predict the ending? ---')
def mi(pairs):
    a=[x for x,_ in pairs]; b=[y for _,y in pairs]
    return H(a)+H(b)-H(pairs)
pairs=[(t[0],t[-1]) for t in T]
obs=mi(pairs)
null=[]
for _ in range(500):
    b=[y for _,y in pairs]; random.shuffle(b)
    null.append(mi(list(zip([x for x,_ in pairs],b))))
print(f'  mutual information opener->ending: {obs:.3f} bits; shuffled mean {np.mean(null):.3f} '
      f'(sd {np.std(null):.3f}); z={(obs-np.mean(null))/np.std(null):+.1f}')
print(f'  as a share of ending entropy: {obs/H([y for _,y in pairs]):.1%} (shuffled {np.mean(null)/H([y for _,y in pairs]):.1%})')
# same for the sign immediately before the ending
pairs2=[(t[-2],t[-1]) for t in T]
obs2=mi(pairs2); null2=[]
for _ in range(500):
    b=[y for _,y in pairs2]; random.shuffle(b)
    null2.append(mi(list(zip([x for x,_ in pairs2],b))))
print(f'  penultimate sign -> ending: {obs2:.3f} bits vs shuffled {np.mean(null2):.3f}; '
      f'z={(obs2-np.mean(null2))/np.std(null2):+.1f}')

print('\n--- 3. Can a meaningless identifier system reproduce the asymmetry? ---')
# "registration plate" generator: random stems from a large pool + a small fixed suffix set,
# matched to the real corpus in text count and length distribution
lens=[len(t) for t in T]
stems=[f'S{i}' for i in range(400)]
sufs=['E1','E2','E3','E4','E5']
w=np.array([0.41,0.2,0.15,0.13,0.11])       # matched to the real top-5 ending shares
synth=[]
for L in lens:
    body=[random.choice(stems) for _ in range(L-1)]
    synth.append(body+[np.random.choice(sufs,p=w)])
def prof(name,X):
    f=[t[0] for t in X]; l=[t[-1] for t in X]
    print(f'  {name:24s} H(first)={H(f):5.2f}  H(last)={H(l):5.2f}  diff={H(l)-H(f):+5.2f}  '
          f'commonest last {collections.Counter(l).most_common(1)[0][1]/len(l):.0%}  '
          f'90% of endings in {cover(l)} signs')
prof('real (Mohenjo-daro)',T)
prof('synthetic ID system',synth)
# a second control: language-like, where endings are drawn from a few suffixes attached to
# stems that also appear elsewhere (so endings are not a disjoint set)
synth2=[]
pool=[f'S{i}' for i in range(120)]
for L in lens:
    body=[random.choice(pool) for _ in range(L-1)]
    synth2.append(body+[np.random.choice(pool[:5],p=w/w.sum())])
prof('synthetic shared-inventory',synth2)
print('\n  Note: the ID control is built to match the real ending shares, so matching them is')
print('  not evidence for it; what matters is whether the real corpus differs in the OTHER')
print('  columns, especially how many signs the endings are drawn from and the opener link.')
