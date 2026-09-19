# Section 24 found that ~21% of inscriptions run to two lines, the second short and
# formulaic. The template work (section 6) never separated the registers. Here the two
# are modelled separately: are line 1 of a two-line text and a single-line text the same
# kind of object, and does line 2 behave like a text at all?
import csv, collections, math, random, numpy as np
from scipy.stats import mannwhitneyu, fisher_exact
random.seed(71)
def H(s):
    c=collections.Counter(s); n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
def mi(p): return H([a for a,_ in p])+H([b for _,b in p])-H(p)
rows=list(csv.DictReader(open('../data/indus_decipher/data/m77_indusscript_real_corpus.csv')))
obj=collections.defaultdict(list)
for r in rows:
    b,p=r['inscription_id'].split('.')
    obj[b].append((int(p),[s for s in r['sign_sequence'].split() if s!='MSg0']))
for v in obj.values(): v.sort()
SINGLE=[v[0][1] for v in obj.values() if len(v)==1 and v[0][1]]
L1=[v[0][1] for v in obj.values() if len(v)==2 and all(t for _,t in v)]
L2=[v[1][1] for v in obj.values() if len(v)==2 and all(t for _,t in v)]
JAR,ARROW='MSg342','MSg328'
print(f'single-line texts {len(SINGLE)}; two-line texts {len(L1)}')

print('\n--- Is line 1 of a two-line text the same object as a single-line text? ---')
for lab,X in (('single-line',SINGLE),('line 1 of two',L1),('line 2 of two',L2)):
    lens=[len(t) for t in X]
    print(f'  {lab:15s} n={len(X):5d}  mean {np.mean(lens):4.1f} signs  '
          f'distinct signs {len({s for t in X for s in t}):4d}  '
          f'jar-final {np.mean([t[-1]==JAR for t in X]):5.0%}  arrow-final {np.mean([t[-1]==ARROW for t in X]):5.0%}  '
          f'unique forms {len({tuple(t) for t in X})/len(X):5.0%}')
print(f'  length, single vs line 1: p={mannwhitneyu([len(t) for t in SINGLE],[len(t) for t in L1]).pvalue:.3g}')
a=sum(t[-1]==JAR for t in SINGLE); b=sum(t[-1]==JAR for t in L1)
print(f'  jar-final, single vs line 1: {a}/{len(SINGLE)} vs {b}/{len(L1)}, '
      f'p={fisher_exact([[a,len(SINGLE)-a],[b,len(L1)-b]]).pvalue:.3g}')

print('\n--- Do the registers share an inventory? ---')
s1=collections.Counter(s for t in SINGLE for s in t); s2=collections.Counter(s for t in L2 for s in t)
sh=set(s1)&set(s2)
print(f'  signs in single-line texts {len(s1)}, in second lines {len(s2)}, shared {len(sh)}')
top2=[s for s,_ in s2.most_common(10)]
print('  commonest second-line signs and their share of tokens in each register:')
for s in top2[:6]:
    print(f'    {s:8s} second lines {s2[s]/sum(s2.values()):5.1%}   single-line texts {s1.get(s,0)/sum(s1.values()):5.1%}')
# is the second line drawn from the same distribution?
common=[s for s in sh if s1[s]+s2[s]>=20]
r1=np.array([s1[s]/sum(s1.values()) for s in common]); r2=np.array([s2[s]/sum(s2.values()) for s in common])
from scipy.stats import spearmanr
rho,p=spearmanr(r1,r2)
print(f'  rank correlation of sign frequencies between registers: rho={rho:.2f}, p={p:.3g} '
      f'({len(common)} signs) - low means the second line uses different signs')

print('\n--- Does line 2 condition on line 1, or stand alone? ---')
pairs=[(a[-1],b[0]) for a,b in zip(L1,L2) if a and b]
o=mi(pairs); nl=[]
for _ in range(400):
    y=[q for _,q in pairs]; random.shuffle(y); nl.append(mi(list(zip([x for x,_ in pairs],y))))
print(f'  end of line 1 -> start of line 2: MI {o:.2f} bits vs shuffled {np.mean(nl):.2f} '
      f'(z={(o-np.mean(nl))/np.std(nl):+.1f})')
# within-line conditioning for comparison
for lab,X in (('inside line 1',L1),('inside line 2',L2)):
    p2=[(t[i],t[i+1]) for t in X for i in range(len(t)-1)]
    if len(p2)<200: continue
    oo=mi(p2); n2=[]
    for _ in range(200):
        y=[q for _,q in p2]; random.shuffle(y); n2.append(mi(list(zip([x for x,_ in p2],y))))
    print(f'  {lab:14s} adjacent signs: MI {oo:.2f} vs shuffled {np.mean(n2):.2f} '
          f'(z={(oo-np.mean(n2))/np.std(n2):+.1f}, n={len(p2)})')
