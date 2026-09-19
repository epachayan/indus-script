# Is one inscription one message? The Mahadevan corpus keeps object parts (id "1001.1",
# "1001.2"), so we can ask whether the parts of an object are independent texts or
# segments of one. Test: the jar sign (M342) ends a text; if parts are independent, every
# part should end with it at the usual rate; if they are segments, only the last should.
import csv, collections, numpy as np
from scipy.stats import fisher_exact, mannwhitneyu
rows=[r for r in csv.DictReader(open('../data/indus_decipher/data/m77_indusscript_real_corpus.csv'))]
obj=collections.defaultdict(list)
for r in rows:
    base,part=r['inscription_id'].split('.')
    t=[s for s in r['sign_sequence'].split() if s!='MSg0']
    obj[base].append((int(part),t,r))
for v in obj.values(): v.sort()
single={k:v for k,v in obj.items() if len(v)==1}
multi={k:v for k,v in obj.items() if len(v)>1}
print(f'objects: {len(obj)}; single-part {len(single)}; multi-part {len(multi)} ({len(multi)/len(obj):.0%})')
print('parts per object:',collections.Counter(len(v) for v in multi.values()).most_common(5))
JAR='MSg342'
def endsjar(t): return bool(t) and t[-1]==JAR
s_rate=np.mean([endsjar(v[0][1]) for v in single.values() if v[0][1]])
last=[v[-1][1] for v in multi.values() if v[-1][1]]
notlast=[t for v in multi.values() for _,t,_ in v[:-1] if t]
print(f'\nends with the jar sign:')
print(f'  single-part objects      {s_rate:.0%}  (n={len(single)})')
print(f'  LAST part of multi-part  {np.mean([endsjar(t) for t in last]):.0%}  (n={len(last)})')
print(f'  earlier parts            {np.mean([endsjar(t) for t in notlast]):.0%}  (n={len(notlast)})')
a=sum(endsjar(t) for t in last); b=sum(endsjar(t) for t in notlast)
print(f'  last vs earlier parts: p={fisher_exact([[a,len(last)-a],[b,len(notlast)-b]]).pvalue:.2g}')
print(f'\nlength: single {np.mean([len(v[0][1]) for v in single.values()]):.1f} signs; '
      f'multi-part parts {np.mean([len(t) for v in multi.values() for _,t,_ in v]):.1f}; '
      f'multi-part total per object {np.mean([sum(len(t) for _,t,_ in v) for v in multi.values()]):.1f}')
p1=[len(v[0][1]) for v in multi.values()]; p2=[len(v[1][1]) for v in multi.values() if len(v)>1]
print(f'  first part {np.mean(p1):.1f} vs second part {np.mean(p2):.1f} signs, p={mannwhitneyu(p1,p2).pvalue:.2g}')
# do the parts repeat each other?
same=sum(1 for v in multi.values() if len({tuple(t) for _,t,_ in v})==1)
print(f'\nall parts identical: {same}/{len(multi)} ({same/len(multi):.0%})')
# what the second parts look like
sec=collections.Counter(' '.join(v[1][1]) for v in multi.values() if len(v)>1 and v[1][1])
print('commonest second parts:',[(t,n) for t,n in sec.most_common(6)])
print('second parts that are a single sign:',sum(1 for v in multi.values() if len(v)>1 and len(v[1][1])==1),f'of {len(multi)}')

# The short second parts are the "arrow" formula (M328 = G520). How do they pair with part 1?
ARROW='MSg328'
pairs=[(v[0][1],v[1][1]) for v in multi.values() if len(v)>1 and v[0][1] and v[1][1]]
arrow2=[(a,b) for a,b in pairs if b and b[-1]==ARROW]
other2=[(a,b) for a,b in pairs if not (b and b[-1]==ARROW)]
print(f'\ntwo-part objects: {len(pairs)}; second part ends with the arrow: {len(arrow2)} ({len(arrow2)/len(pairs):.0%})')
print(f'  when it does, part 1 ends with the jar in {np.mean([a[-1]==JAR for a,_ in arrow2]):.0%} of cases')
print(f'  when it does not, part 1 ends with the jar in {np.mean([a[-1]==JAR for a,_ in other2]):.0%}')
a1=sum(a[-1]==JAR for a,_ in arrow2); b1=sum(a[-1]==JAR for a,_ in other2)
print(f'  p={fisher_exact([[a1,len(arrow2)-a1],[b1,len(other2)-b1]]).pvalue:.2g}')
print(f'  arrow second parts are {np.mean([len(b) for _,b in arrow2]):.1f} signs; others {np.mean([len(b) for _,b in other2]):.1f}')
print('  signs before the arrow:',collections.Counter(b[-2] for _,b in arrow2 if len(b)>1).most_common(5))
# do single-part objects ever carry the arrow formula?
one=[v[0][1] for v in single.values() if v[0][1]]
print(f'\narrow-final texts: {np.mean([t[-1]==ARROW for t in one]):.1%} of single-part objects '
      f'vs {len(arrow2)/len(pairs):.0%} of two-part second parts')
