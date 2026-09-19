# Sequence ML on inscriptions_ml.csv: next-sign prediction, HMM slot discovery, foreign-text scoring.
import csv, collections, math, numpy as np
from sklearn.metrics import adjusted_mutual_info_score as ami
rng=np.random.default_rng(0)
rows=list(csv.DictReader(open('../outputs/inscriptions_ml.csv')))
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
FOREIGN={'Ur','Kish','Tell Umma','Susa','Luristan','Karzakan','Hajar',"Qala'at al-Bahrain",'Saar',"Ra's al-Junayz",'Salut','Gonur Depe','Altyn Depe'}
home=[r['signs_reading_order'].split() for r in rows if r['first_occurrence']=='True' and r['site'] not in FOREIGN|{'Unknown','Shortughai'} and int(r['n_signs'])>=2]
far=[(r['site'],r['signs_reading_order'].split()) for r in rows if r['site'] in FOREIGN and r['n_signs']!='0']
cls=lambda s: tags[s]['behaviour_class'] or 'rare'
class WB:   # Witten-Bell interpolated n-gram (order n), optional class back-off
    def __init__(s,texts,n=3,use_cls=False):
        s.n=n; s.c=collections.defaultdict(collections.Counter); s.use_cls=use_cls
        s.vocab=set(x for t in texts for x in t)|{'</s>'}
        s.cc=collections.defaultdict(collections.Counter); s.wc=collections.defaultdict(collections.Counter)
        for t in texts:
            p=['<s>']*(n-1)+t+['</s>']
            for i in range(n-1,len(p)):
                for k in range(n): s.c[tuple(p[i-k:i])][p[i]]+=1
            q=['<s>']+[cls(x) for x in t]+['</s>']
            for a,b in zip(q,q[1:]): s.cc[a][b]+=1
            for x in t+['</s>']: s.wc[cls(x) if x!='</s>' else '</s>'][x]+=1
    def p(s,h,w):
        V=len(s.vocab)+1; pr=1/V
        if s.use_cls:
            hc=cls(h[-1]) if h[-1] not in('<s>',) else '<s>'; wc=cls(w) if w!='</s>' and w in tags else '</s>'
            cc=s.cc[hc]; wcn=s.wc[wc]
            if cc and wcn: pr=0.5*pr+0.5*(cc[wc]+0.1)/(sum(cc.values())+1)*(wcn[w]+0.1)/(sum(wcn.values())+1)
        for k in range(0,s.n):
            ctx=tuple(h[len(h)-k:]) if k else (); c=s.c[ctx]; N=sum(c.values()); T=len(c)
            if N: lam=N/(N+T); pr=lam*c[w]/N+(1-lam)*pr
        return pr
    def score(s,t):
        p=['<s>']*(s.n-1)+t+['</s>']
        return [math.log(s.p(p[i-s.n+1:i],p[i])) for i in range(s.n-1,len(p))]
    def rank(s,h,w):
        pw=s.p(h,w); return sum(1 for v in s.vocab if s.p(h,v)>pw)
# ---- 1. next-sign prediction, 5-fold CV ----
idx=rng.permutation(len(home)); folds=np.array_split(idx,5)
models={'unigram':dict(n=1),'bigram':dict(n=2),'trigram':dict(n=3),'trigram+class':dict(n=3,use_cls=True)}
res={m:[[],[],[]] for m in models}; heldout=[]
for f in folds:
    test=[home[i] for i in f]; fs=set(f); train=[home[i] for i in range(len(home)) if i not in fs]
    for m,kw in models.items():
        M=WB(train,**kw)
        for t in test:
            lp=M.score(t); res[m][0]+=lp
            if m=='trigram+class': heldout.append(np.mean(lp))
            if m in('bigram','trigram+class','unigram'):
                p=['<s>']*(M.n-1)+t
                for i in range(M.n-1,len(p)):
                    if len(res[m][1])<3000:
                        r_=M.rank(p[i-M.n+1:i],p[i]); res[m][1].append(r_==0); res[m][2].append(r_<5)
print(f'homeland distinct texts: {len(home)}  (5-fold CV)')
print(f'{"model":15s} perplexity  top1   top5')
for m,(lp,t1,t5) in res.items():
    extra=f'{np.mean(t1):5.0%}  {np.mean(t5):5.0%}' if t1 else '   -      -'
    print(f'{m:15s} {math.exp(-np.mean(lp)):8.1f}   {extra}')
# ---- 2. HMM slot discovery ----
from hmmlearn.hmm import CategoricalHMM
cnt=collections.Counter(x for t in home for x in t); V=[x for x,c in cnt.items() if c>=5]+['<unk>','</s>']; vi={x:i for i,x in enumerate(V)}
enc=lambda t:[vi.get(x,vi['<unk>']) for x in t]+[vi['</s>']]
X=np.concatenate([enc(t) for t in home]).reshape(-1,1); L=[len(t)+1 for t in home]
best=None
for seed in range(4):
    h=CategoricalHMM(n_components=10,n_iter=200,random_state=seed,init_params='ste',n_features=len(V)); h.fit(X,L)
    sc=h.score(X,L)
    if best is None or sc>best[0]: best=(sc,h)
h=best[1]; st=h.predict(X,L)
pos=collections.defaultdict(collections.Counter); sgn=collections.defaultdict(collections.Counter); k=0
for t in home:
    for i,x in enumerate(t+['</s>']):
        s=st[k]; k+=1
        if x=='</s>': pos[s]['END']+=1; continue
        pos[s]['start' if i==0 else 'end' if i==len(t)-1 else 'mid']+=1; sgn[s][x]+=1
print('\nHMM states (10), ordered by typical position:')
order=sorted(pos,key=lambda s:(pos[s]['END']>max(pos[s]['start'],pos[s]['mid'],pos[s]['end']), (pos[s]['mid']+2*pos[s]['end'])/max(1,sum(pos[s].values())-pos[s]['END'])-pos[s]['start']/max(1,sum(pos[s].values()))))
for s in order:
    n=sum(pos[s].values())-pos[s]['END']
    if n==0: print(f'  S{s}: end-of-text state'); continue
    print(f'  S{s}: start {pos[s]["start"]/n:4.0%} mid {pos[s]["mid"]/n:4.0%} end {pos[s]["end"]/n:4.0%} | '+' '.join(x for x,_ in sgn[s].most_common(7)))
# agreement of each sign's dominant state with behaviour classes
dom={}
for s,c in sgn.items():
    for x,n in c.items():
        if x not in dom or n>dom[x][1]: dom[x]=(s,n)
common=[x for x in dom if tags[x]['behaviour_class']]
print(f'HMM state vs behaviour class, AMI = {ami([tags[x]["behaviour_class"] for x in common],[dom[x][0] for x in common]):.2f} over {len(common)} signs')
tr=h.transmat_; print('strongest state transitions:',', '.join(f'S{a}->S{b} {tr[a,b]:.0%}' for a,b in sorted(((a,b) for a in range(10) for b in range(10)),key=lambda x:-tr[x])[:6]))
# ---- 3. foreign texts with the best model ----
M=WB(home,n=3,use_cls=True); hd=np.array(heldout)
print('\nForeign texts (trigram+class), percentile vs held-out homeland:')
out=[]
for site,t in far:
    sc=np.mean(M.score(t)); out.append((site,' '.join(t),(hd<sc).mean()))
for site,t,p in sorted(out,key=lambda x:x[2]): print(f'  {p:4.0%}  {site:20s} {t}')
print(f'below homeland 10th percentile: {sum(p<0.1 for _,_,p in out)}/{len(out)}')
