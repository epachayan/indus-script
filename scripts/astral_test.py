# Does an astral/calendrical reading fit? Three predictions it makes:
#  1. NUMBERED FISH should be a small closed set of recurring combinations (star names),
#     with counts in a bounded range (Pleiades 6/7, Saptarishi 7, nakshatras 27/28...).
#  2. A calendar/star-name system needs a NAME INVENTORY of a characteristic size
#     (7, 12, 27/28), visible as a set of mutually exclusive alternatives in one slot.
#  3. Names REPEAT: a limited inventory used over and over, not mostly-unique texts.
import csv, collections, itertools, numpy as np
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']]
T=[r['signs_reading_order'].split() for r in rows]
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
FISH=[s for s,t in tags.items() if 'fish' in t.get('family','')]
NUM=[s for s,t in tags.items() if 'numeral' in t.get('behaviour_class','').lower() or 'stroke' in t.get('family','')]
print(f'fish-family signs: {len(FISH)}; stroke/numeral signs: {len(NUM)}')

print('\n--- 1. Numbered fish: is it a closed, recurring set? ---')
combos=collections.Counter()
for t in T:
    for i in range(len(t)-1):
        if t[i] in NUM and t[i+1] in FISH: combos[(t[i],t[i+1])]+=1
        if t[i] in FISH and t[i+1] in NUM: combos[(t[i+1],t[i])]+=1   # either order
tot=sum(combos.values())
print(f'  number+fish adjacencies: {tot} in {len(combos)} distinct combinations')
if tot:
    print('  commonest:',[(f'{a}+{b}',n) for (a,b),n in combos.most_common(8)])
    once=sum(1 for v in combos.values() if v==1)
    print(f'  combinations occurring once: {once}/{len(combos)} ({once/len(combos):.0%})')
    print('  a closed star-name set would repeat; a productive count+item pattern would not')
# which numerals attach to fish, and how high do they go?
numseen=collections.Counter(a for (a,b),n in combos.items() for _ in range(n))
print('  numerals used with fish:',[(s,n) for s,n in numseen.most_common()])

print('\n--- 2. Is there a slot with a 7/12/27-sized set of alternatives? ---')
# candidate paradigms: signs that occupy the same position and never co-occur in a text
def slot_sets(pos,corpus=None):
    C=corpus if corpus is not None else T
    if pos=='final': occ={s for t in C for s in [t[-1]]}
    elif pos=='initial': occ={s for t in C for s in [t[0]]}
    else: occ={s for t in C for s in t[1:-1]}
    occ={s for s in occ if sum(s in t for t in C)>=10}
    never=collections.defaultdict(set)
    for a,b in itertools.combinations(sorted(occ),2):
        if not any(a in t and b in t for t in C): never[a].add(b); never[b].add(a)
    # greedy maximal mutually-exclusive group
    best=[]
    for seed in sorted(occ,key=lambda s:-len(never[s])):
        grp=[seed]
        for c in sorted(never[seed],key=lambda s:-len(never[s])):
            if all(c in never[g] for g in grp): grp.append(c)
        if len(grp)>len(best): best=grp
    return len(occ),best
import random
random.seed(83)
def null_group(reps=10):
    # texts of the same lengths, signs drawn from the same frequency distribution
    pool=[s for t in T for s in t]
    sizes=[]
    for _ in range(reps):
        fake=[random.sample(pool,len(t)) for t in T]
        sizes.append(len(slot_sets('medial',fake)[1]))
    return float(np.mean(sizes))
nullsize=null_group()
for pos in ('initial','final','medial'):
    n,grp=slot_sets(pos)
    print(f'  {pos:8s}: {n} signs used there (10+ texts); largest mutually exclusive group: {len(grp)}')
    print(f'           {grp[:14]}')
print(f'  null (same lengths, signs drawn at random): largest group {nullsize:.0f}')
print('  (a 12-month or 27-nakshatra name set would show up as a group of that size)')

print('\n--- 3. Do texts repeat the way a name inventory would? ---')
c=collections.Counter(tuple(t) for t in T)
print(f'  {len(T)} texts, {len(c)} distinct, {sum(1 for v in c.values() if v==1)/len(c):.0%} occur once')
print(f'  a 27-name or 12-name inventory used across {len(T)} objects would repeat heavily')
