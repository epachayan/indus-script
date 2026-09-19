# Roadmap A1-A3 (Mohenjo-daro seals only):
# A1 sub-structure of the name-like core; A2 what the opener choice correlates with;
# A3 counts inside cores.
import csv, re, collections, math, numpy as np
from scipy.stats import chi2_contingency, kruskal
rows=list(csv.DictReader(open('../outputs/inscriptions_ml.csv')))
MJ=[r for r in rows if r['site']=='Mohenjo-daro' and r['object_type']=='SEAL' and r['first_occurrence']=='True' and int(r['n_signs'])>=3]
OPEN={'G861','G817','G820','G692'}; MARK={'G2','G60','G1','G741'}; END={'G740','G400','G90','G151','G520'}
SHORT={'G1','G3','G4','G5','G7','G16','G17','G18','G19'}; LONG={'G31','G32','G33','G35'}; NUM=SHORT|LONG
def split(t):
    i=0; op=()
    if t[0] in OPEN:
        j=2 if len(t)>1 and t[1] in MARK else 1; op=tuple(t[:j]); i=j
    k=len(t)
    while k>i and t[k-1] in END: k-=1
    return op,tuple(t[i:k]),tuple(t[k:])
S=[(r,)+split(r['signs_reading_order'].split()) for r in MJ]
cores=[c for _,_,c,_ in S if c]
print(f'MJ distinct seal texts: {len(S)}; with a core: {len(cores)}')
# ---- A1: segment cores with strong adjacent pairs (learned on all texts) ----
allT=[r['signs_reading_order'].split() for r in rows if r['first_occurrence']=='True']
uni=collections.Counter(s for t in allT for s in t); N=sum(uni.values())
big=collections.Counter((a,b) for t in allT for a,b in zip(t,t[1:])); NB=sum(big.values())
strong={p for p,c in big.items() if c>=5 and math.log2((c/NB)/((uni[p[0]]/N)*(uni[p[1]]/N)))>=3}
def segs(c):
    out=[[c[0]]]
    for a,b in zip(c,c[1:]):
        if (a,b) in strong: out[-1].append(b)
        else: out.append([b])
    return [tuple(x) for x in out]
SEG=[segs(c) for c in cores]
multi=[s for s in SEG if len(s)>=2]
print(f'\n[A1] cores with 2+ units: {len(multi)}/{len(SEG)}; units per core {np.mean([len(s) for s in SEG]):.1f}')
def prof(vals):
    c=collections.Counter(vals); n=len(vals)
    return dict(uses=n,forms=len(c),top=c.most_common(1)[0][1]/n,once=sum(v==1 for v in c.values())/len(c),
                top5=' '.join('+'.join(k) for k,_ in c.most_common(5)))
for lab,vals in (('LAST unit (before ending)',[s[-1] for s in multi]),('FIRST unit',[s[0] for s in multi]),
                 ('MIDDLE units',[u for s in multi for u in s[1:-1]])):
    p=prof(vals); print(f'  {lab:26s} uses {p["uses"]:4d} forms {p["forms"]:4d} top {p["top"]:4.0%} seen-once {p["once"]:4.0%} | {p["top5"]}')
last=collections.Counter(s[-1] for s in multi)
# how concentrated: share of last-units covered by the 10 commonest forms, vs first-units
for lab,c in (('last',last),('first',collections.Counter(s[0] for s in multi))):
    print(f'  top-10 forms cover {sum(v for _,v in c.most_common(10))/sum(c.values()):.0%} of {lab} units')
# does the last unit depend on the ending? (title agreeing with ending)
ends=collections.Counter()
for (r,op,c,e),s in zip([x for x in S if x[2]],SEG):
    if len(s)>=2: ends[(e[:1] or ('none',))[0]]+=1
print('  endings of multi-unit cores:',ends.most_common(4))
tab=collections.defaultdict(collections.Counter)
for (r,op,c,e),s in zip([x for x in S if x[2]],SEG):
    if len(s)>=2: tab[(e[:1] or ('none',))[0]][s[-1]]+=1
keysE=[k for k,_ in ends.most_common(3)]; topL=[k for k,_ in last.most_common(12)]
M=np.array([[tab[e][l] for l in topL] for e in keysE])
M=M[:,M.sum(0)>0]; chi=chi2_contingency(M)
print(f'  last unit vs ending (top 3 endings x top 12 last units): p={chi.pvalue:.2g}')
for e in keysE: print(f'    ending {e:5s}: top last units {[ "+".join(k) for k,_ in tab[e].most_common(4)]}')
# ---- A2: opener choice vs text features ----
print('\n[A2] opener choice at MJ')
grp=collections.defaultdict(list)
for r,op,c,e in S:
    grp[op[0] if op else 'no opener'].append((int(r['n_signs']),len(c),any(s in NUM for s in c),e[:1][0] if e else 'none',r['motif_group']))
for k,v in sorted(grp.items(),key=lambda x:-len(x[1])):
    if len(v)<15: continue
    print(f'  {k:10s} n={len(v):4d} len {np.mean([x[0] for x in v]):.1f} core {np.mean([x[1] for x in v]):.1f} has-count {np.mean([x[2] for x in v]):4.0%} ends-in-jar {np.mean([x[3]=="G740" for x in v]):4.0%} unicorn {np.mean([x[4]=="unicorn" for x in v]):4.0%}')
ops=[k for k in grp if k in OPEN and len(grp[k])>=15]
print(f'  core length differs between openers: p={kruskal(*[[x[1] for x in grp[k]] for k in ops]).pvalue:.2g}')
T2=np.array([[sum(x[3]==e for x in grp[k]) for e in ('G740','none','G400')] for k in ops]); T2=T2[:,T2.sum(0)>0]
print(f'  ending differs between openers: p={chi2_contingency(T2).pvalue:.2g}')
# ---- A3: counts inside MJ cores ----
print('\n[A3] counts inside MJ cores')
pair=collections.Counter(); after=collections.defaultdict(collections.Counter)
for c in cores:
    for a,b in zip(c,c[1:]):
        if a in NUM and b not in NUM:
            sysn='short' if a in SHORT else 'long'; pair[sysn]+=1; after[sysn][b]+=1
    pos=[i for i,s in enumerate(c) if s in NUM]
print(f'  count+item pairs: {dict(pair)}')
for k in after: print(f'  {k:5s} counts go with: {after[k].most_common(6)}')
posn=[(i/(len(c)-1)) for c in cores if len(c)>=3 for i,s in enumerate(c) if s in NUM]
print(f'  relative position of counts inside cores (0=start,1=end): mean {np.mean(posn):.2f}; in first third {np.mean(np.array(posn)<1/3):.0%}, last third {np.mean(np.array(posn)>2/3):.0%}')

# ---- A1b: internal jar = boundary between two sub-texts? ----
print('\n[A1b] jar inside texts (MJ seals)')
full=[r['signs_reading_order'].split() for r in MJ]
inner=[t for t in full if 'G740' in t[:-1]]
print(f'  texts with a non-final jar: {len(inner)}/{len(full)} ({len(inner)/len(full):.0%})')
# compare the sign right before an inner jar vs before a final jar
pre_in=collections.Counter(t[i-1] for t in inner for i,s in enumerate(t[:-1]) if s=='G740' and i>0)
pre_fin=collections.Counter(t[-2] for t in full if t[-1]=='G740' and len(t)>1)
shared=set(k for k,_ in pre_in.most_common(10))&set(k for k,_ in pre_fin.most_common(10))
print(f'  before inner jar: {pre_in.most_common(5)}')
print(f'  before final jar: {pre_fin.most_common(5)}')
print(f'  overlap of top-10 preceding signs: {len(shared)}/10')
post=collections.Counter(t[i+1] for t in inner for i,s in enumerate(t[:-1]) if s=='G740')
print(f'  after inner jar: {post.most_common(6)}')
# do the two halves each look like complete texts? (score halves against whole-text start/end habits)
starts=collections.Counter(t[0] for t in full); endsC=collections.Counter(t[-1] for t in full)
def split_first(t):
    i=t.index('G740'); return t[:i+1],t[i+1:]
A=[split_first(t) for t in inner]
second_start=np.mean([starts[b[0]]/len(full)>=0.02 for a,b in A if b])
rand_start=np.mean([starts[t[len(t)//2]]/len(full)>=0.02 for t in full if len(t)>=3])
print(f'  second half starts with a common text-opening sign: {second_start:.0%} (vs {rand_start:.0%} for a mid-text sign)')

# ---- 3a: ending as a two-part unit (pre-final + ending) ----
print('\n[3a] two-part endings (pre-final sign + ending unit)')
pairs=collections.Counter()
for r,op,c,e in S:
    if c and e: pairs[(c[-1],)+e]+=1
n=sum(pairs.values())
print(f'  texts with an ending: {n}; distinct two-part endings: {len(pairs)}; top-10 cover {sum(v for _,v in pairs.most_common(10))/n:.0%}')
print('  commonest:',[' '.join(k)+f' ({v})' for k,v in pairs.most_common(8)])
single=collections.Counter(e for r,op,c,e in S if e)
print(f'  for comparison, ending alone: {len(single)} forms, top-1 {single.most_common(1)[0][1]/n:.0%}')
# ---- 3b: first core slot when there is no opener ----
print('\n[3b] first slot when there is no opener')
first_no=collections.Counter(c[0] for r,op,c,e in S if not op and len(c)>=2)
first_after=collections.Counter(c[0] for r,op,c,e in S if op and len(c)>=2)
nn=sum(first_no.values())
print(f'  texts: {nn}; distinct first signs: {len(first_no)}; top-5 cover {sum(v for _,v in first_no.most_common(5))/nn:.0%}: {first_no.most_common(8)}')
print(f'  first core sign after an opener: {first_after.most_common(6)}')
FI={'G31','G32','G33','G3','G4','G5','G1'}
print(f'  first slot is a count sign: no opener {sum(first_no[s] for s in FI|NUM)/nn:.0%} vs after opener {sum(first_after[s] for s in FI|NUM)/max(sum(first_after.values()),1):.0%}')

# ---- 3c: is the shorter core beside an opener a space limit? ----
print('\n[3c] opener texts and seal size')
import re as _re
sql=open('../data/indus-website/population-script.sql',encoding='utf8').read()
b=sql[sql.index('INSERT INTO SEAL ('):]; b=b[:b.index(');\n')+1]
dims={c:(float(w),float(h)) for _,_,_,c,w,h in _re.findall(r'\((\d+),\s*"([^"]*)",\s*"([^"]*)",\s*"([^"]*)",\s*[^,]*,\s*([\d.]+),\s*([\d.]+)',b)}
from scipy.stats import mannwhitneyu
w_op=[dims[r['cisi']][0] for r,op,c,e in S if op and r['cisi'] in dims and dims[r['cisi']][0]>0]
w_no=[dims[r['cisi']][0] for r,op,c,e in S if not op and r['cisi'] in dims and dims[r['cisi']][0]>0]
print(f'  seal width: with opener median {np.median(w_op):.1f} (n={len(w_op)}), without {np.median(w_no):.1f} (n={len(w_no)}), p={mannwhitneyu(w_op,w_no).pvalue:.2f}')
dens_op=[int(r['n_signs'])/dims[r['cisi']][0] for r,op,c,e in S if op and r['cisi'] in dims and dims[r['cisi']][0]>0]
dens_no=[int(r['n_signs'])/dims[r['cisi']][0] for r,op,c,e in S if not op and r['cisi'] in dims and dims[r['cisi']][0]>0]
print(f'  signs per unit width: with opener {np.median(dens_op):.3f}, without {np.median(dens_no):.3f}, p={mannwhitneyu(dens_op,dens_no).pvalue:.2f}')
# ---- 3d: is the ending sometimes the counted item? ----
print('\n[3d] count directly before the ending')
cb=[(c,e) for r,op,c,e in S if c and e and c[-1] in NUM]
nc=[(c,e) for r,op,c,e in S if c and e and c[-1] not in NUM]
for lab,g in (('count before ending',cb),('other',nc)):
    ec=collections.Counter(e[0] for c,e in g); n_=len(g)
    print(f'  {lab:20s} n={n_:3d} ending: '+', '.join(f'{k} {v/n_:.0%}' for k,v in ec.most_common(4)))
vals=collections.Counter(c[-1] for c,e in cb)
print('  counts used there:',vals.most_common(6))
T3=np.array([[sum(e[0]==k for c,e in g) for k in ('G740','G520','G400','G90')] for g in (cb,nc)]); T3=T3[:,T3.sum(0)>0]
print(f'  ending distribution differs: p={chi2_contingency(T3).pvalue:.2g}')
