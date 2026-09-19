# Blind re-coding of a random sample: how reliable is a single pass of photo coding?
import csv, numpy as np
from sklearn.metrics import cohen_kappa_score
A={(r['plate'],r['mackay_no']):r for r in csv.DictReader(open('../transcriptions/mackay1938_plates/photo_codings.csv'))}
B=list(csv.DictReader(open('recode.csv')))
pairs=[(A[(r['plate'],r['mackay_no'])],r) for r in B if (r['plate'],r['mackay_no']) in A]
print(f'seals re-coded blind: {len(pairs)}')
d=[int(b['n_signs'])-int(a['n_signs']) for a,b in pairs]
print(f'sign count: exact agreement {np.mean([x==0 for x in d]):.0%}, within 1 {np.mean([abs(x)<=1 for x in d]):.0%}, '
      f'mean difference {np.mean(d):+.2f}, sd {np.std(d):.2f}')
ja=[a['ends_jar']=='likely' for a,b in pairs]; jb=[b['ends_jar']=='likely' for a,b in pairs]
print(f'jar ending: agreement {np.mean([x==y for x,y in zip(ja,jb)]):.0%}, kappa {cohen_kappa_score(ja,jb):.2f} '
      f'(pass 1 said yes {np.mean(ja):.0%}, pass 2 {np.mean(jb):.0%})')
dis=[(a['plate'],a['mackay_no'],a['n_signs'],b['n_signs'],a['ends_jar'],b['ends_jar']) for a,b in pairs
     if abs(int(a['n_signs'])-int(b['n_signs']))>1 or (a['ends_jar']=='likely')!=(b['ends_jar']=='likely')]
print(f'disagreements ({len(dis)}):')
for x in dis: print('  ',x)
