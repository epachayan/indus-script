# Do coded text features differ across the city (blocks and streets vs indoors)?
# Space is a safer variable than depth: a block is where the seal was used, while depth
# only records how much debris had accumulated by then.
import csv, collections, numpy as np
from scipy.stats import chi2_contingency, kruskal, mannwhitneyu
C=list(csv.DictReader(open('../transcriptions/mackay1938_plates/photo_codings.csv')))
T={r['no']:r for r in csv.DictReader(open('../outputs/mackay_seal_table.csv'))}
rows=[]
for r in C:
    t=T.get(r['mackay_no'])
    if not t or r['confidence'] not in ('high','medium') or int(r['n_signs'])==0: continue
    rows.append(dict(no=r['mackay_no'],n=int(r['n_signs']),jar=r['ends_jar']=='likely',
                     block=t['block'],street=t['street'],typ=t['type'],area=t['area']))
print(f'coded seals with a find-spot: {len(rows)}')
ind=[r for r in rows if r['block']]; out=[r for r in rows if r['street'] and not r['block']]
print(f"indoors {len(ind)} vs streets/between blocks {len(out)}")
if len(out)>=10:
    print(f"  signs {np.mean([r['n'] for r in ind]):.1f} vs {np.mean([r['n'] for r in out]):.1f}, "
          f"p={mannwhitneyu([r['n'] for r in ind],[r['n'] for r in out]).pvalue:.2f}")
    a=sum(r['jar'] for r in ind); b=sum(r['jar'] for r in out)
    print(f"  jar ending {a/len(ind):.0%} vs {b/len(out):.0%}")
byb=collections.defaultdict(list)
for r in ind: byb[r['block']].append(r)
big={k:v for k,v in byb.items() if len(v)>=8}
print(f'\nblocks with 8+ coded seals: {len(big)}')
for k,v in sorted(big.items(),key=lambda x:-len(x[1])):
    print(f"  Block {k:3s} n={len(v):3d}  signs {np.mean([r['n'] for r in v]):.1f}  jar {np.mean([r['jar'] for r in v]):.0%}")
if len(big)>=3:
    print(f"  sign count differs between blocks: p={kruskal(*[[r['n'] for r in v] for v in big.values()]).pvalue:.2f}")
    T2=np.array([[sum(r['jar'] for r in v),sum(not r['jar'] for r in v)] for v in big.values()])
    if (T2.sum(0)>0).all(): print(f"  jar ending differs between blocks: p={chi2_contingency(T2).pvalue:.2f}")
