import csv, collections, math, numpy as np, json
abroad={'Ur':'Mesopotamia','Kish':'Mesopotamia','Tell Umma':'Mesopotamia','Susa':'Elam','Luristan':'Iran',
 'Karzakan':'Gulf','Hajar':'Gulf',"Qala'at al-Bahrain":'Gulf','Saar':'Gulf',"Ra's al-Junayz":'Oman','Salut':'Oman',
 'Gonur Depe':'Central Asia','Altyn Depe':'Central Asia'}
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
rows=list(csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')))
def seq(r): return [s for s in r['sign_sequence'].split() if s in tags][::-1]
home=[]; seen=set()
for r in rows:
    if r['site'] in abroad or r['site'] in ('Unknown','Shortughai'): continue
    if r['sign_sequence'] in seen: continue
    seen.add(r['sign_sequence']); s=seq(r)
    if len(s)>=2: home.append(s)
far=[(r['site'],abroad[r['site']],seq(r)) for r in rows if r['site'] in abroad]
V=len(tags)+1
def train(texts):
    u=collections.Counter(); b=collections.Counter()
    for t in texts:
        t=['<s>']+t+['</s>']
        for x,y in zip(t,t[1:]): u[x]+=1; b[(x,y)]+=1
    return u,b
def score(t,u,b):   # mean log-prob per transition, add-0.1 smoothing
    t=['<s>']+t+['</s>']
    return np.mean([math.log((b[(x,y)]+0.1)/(u[x]+0.1*V)) for x,y in zip(t,t[1:])])
u,b=train(home)
# homeland baseline: leave-one-out on a sample
rng=np.random.default_rng(0); base=[]
for i in rng.choice(len(home),400,replace=False):
    t=home[i]; t2=['<s>']+t+['</s>']
    for x,y in zip(t2,t2[1:]): u[x]-=1; b[(x,y)]-=1
    base.append(score(t,u,b))
    for x,y in zip(t2,t2[1:]): u[x]+=1; b[(x,y)]+=1
base=np.array(base)
print(f'homeland texts {len(home)}; LOO score median {np.median(base):.2f}, 10th pct {np.percentile(base,10):.2f}')
bc={s:r['behaviour_class'] for s,r in tags.items()}
out=[]
for site,reg,t in far:
    if not t: continue
    sc=score(t,u,b) if len(t)>=1 else float('nan')
    pct=(base<sc).mean()
    seen_bi=sum(b[(x,y)]>0 for x,y in zip(t,t[1:])); nb=max(len(t)-1,0)
    unk=sum(tags[s]['frequency']=='0' or int(tags[s]['frequency'])<3 for s in t)
    ends=bc.get(t[-1],'') ; starts=bc.get(t[0],'')
    out.append((reg,site,' '.join(t),len(t),round(sc,2),f'{pct:.0%}',f'{seen_bi}/{nb}',unk,starts,ends))
for o in sorted(out): print(o)
sc_far=[o[4] for o in out if o[3]>=2]
print('abroad (len>=2) median score',np.median(sc_far),'n',len(sc_far),' share below homeland 10th pct:',np.mean(np.array(sc_far)<np.percentile(base,10)))
json.dump(out,open('abroad.json','w'))
