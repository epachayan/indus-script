# If seals marked houses/lineages, related bearers should share a base and vary in one
# slot (like surname + given name). That predicts far more MINIMAL PAIRS - texts differing
# in exactly one position - than chance. Null: texts of the same lengths built from the
# same sign frequencies (destroys any shared-base structure, keeps the inventory).
import csv, collections, random, numpy as np
random.seed(113)
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']]
T=[tuple(r['signs_reading_order'].split()) for r in rows if r['site']=='Mohenjo-daro']
T=sorted({t for t in T if len(t)>=3})          # distinct texts only
print(f'distinct Mohenjo-daro texts of 3+ signs: {len(T)}')
def count_minimal(texts):
    by=collections.defaultdict(list)
    for t in texts: by[len(t)].append(t)
    n_sub=n_ins=0
    for L,group in by.items():
        # substitution: differ in exactly one position
        for i in range(L):
            key=collections.Counter(tuple(t[:i]+t[i+1:]) for t in group)
            n_sub+=sum(v*(v-1)//2 for v in key.values())
    # insertion/deletion: one text is another with a single extra sign
    S=set(texts)
    for t in texts:
        for i in range(len(t)):
            if t[:i]+t[i+1:] in S: n_ins+=1
    return n_sub,n_ins
obs_sub,obs_ins=count_minimal(T)
print(f'observed: {obs_sub} substitution pairs, {obs_ins} single-sign extensions')
pool=[s for t in T for s in t]
sub_null=[];ins_null=[]
for _ in range(20):
    fake=sorted({tuple(random.sample(pool,len(t))) for t in T})
    a,b=count_minimal(fake); sub_null.append(a); ins_null.append(b)
print(f'null (same lengths, same sign pool): {np.mean(sub_null):.0f} +/- {np.std(sub_null):.0f} substitutions, '
      f'{np.mean(ins_null):.0f} +/- {np.std(ins_null):.0f} extensions')
print(f'enrichment: substitutions x{obs_sub/max(np.mean(sub_null),1):.1f}, extensions x{obs_ins/max(np.mean(ins_null),1):.1f}')
# where does the varying slot sit?
by=collections.defaultdict(list)
for t in T: by[len(t)].append(t)
pos=collections.Counter()
for L,group in by.items():
    for i in range(L):
        key=collections.defaultdict(list)
        for t in group: key[tuple(t[:i]+t[i+1:])].append(t)
        for v in key.values():
            if len(v)>1: pos[('first' if i==0 else 'last' if i==L-1 else 'middle')]+=len(v)*(len(v)-1)//2
print('varying position in minimal pairs:',dict(pos))
# how big are the families? (texts linked by one-sign differences)
import itertools
parent={t:t for t in T}
def find(x):
    while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
    return x
def union(a,b):
    ra,rb=find(a),find(b)
    if ra!=rb: parent[ra]=rb
for L,group in by.items():
    for i in range(L):
        key=collections.defaultdict(list)
        for t in group: key[tuple(t[:i]+t[i+1:])].append(t)
        for v in key.values():
            for a,b in itertools.combinations(v,2): union(a,b)
S=set(T)
for t in T:
    for i in range(len(t)):
        if t[:i]+t[i+1:] in S: union(t,t[:i]+t[i+1:])
fam=collections.Counter(find(t) for t in T)
sizes=collections.Counter(fam.values())
print(f'families of related texts: {sum(1 for v in fam.values() if v>1)} texts in families of 2+, '
      f'largest family {max(fam.values())}')
print('family size distribution:',dict(sorted(sizes.items())[:8]))
