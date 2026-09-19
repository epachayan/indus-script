# Genre-matched comparison: Egyptian TITLE+NAME label texts vs Indus seal texts.
# Data: TLA Earlier Egyptian (CC-BY-SA 4.0), -3350 to -1539, i.e. contemporary with the
# mature Indus phase. Label texts are rows whose glossing contains only titles, personal
# names, divine/royal/place names and bare nouns - the closest Egyptian parallel to a seal
# legend, in the way Sumerian seal legends were used in FINDINGS 12-13.
import json, sys, csv, collections, math, random, unicodedata, numpy as np
random.seed(101)
path=sys.argv[1] if len(sys.argv)>1 else '../data/tla_egyptian_earlier.jsonl'
rows=[json.loads(l) for l in open(path,encoding='utf8')]
def H(s):
    c=collections.Counter(s); n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
def mi(p): return H([a for a,_ in p])+H([b for _,b in p])-H(p)
def excess(seqs,n=1000,draws=12,reps=25):
    S=[s for s in seqs if len(s)>=2]
    if len(S)<200: return float('nan')
    v=[]
    for _ in range(draws):
        X=random.sample(S,min(n,len(S)))
        p=[(s[i],s[i+1]) for s in X for i in range(len(s)-1)]
        o=mi(p); hl=H([b for _,b in p]); nl=[]
        for _ in range(reps):
            b=[y for _,y in p]; random.shuffle(b); nl.append(mi(list(zip([x for x,_ in p],b))))
        v.append((o-np.mean(nl))/hl)
    return float(np.mean(v))
def glyphs(s): return [ch for ch in s if unicodedata.category(ch)=='Lo' and ord(ch)>=0x13000]
LABELSET={'TITL','PERSN','ROYLN','DIVN','TOPN','N.m','N.f','N','N.m:stc','N.f:sg'}
lab=[r for r in rows if r['glossing'] and set(r['glossing'].split())<=LABELSET]
oth=[r for r in rows if r not in lab]
print(f'Earlier Egyptian: {len(rows)} rows, {len(lab)} label texts (title/name only), dates '
      f"{min(int(r['dateNotBefore']) for r in rows)} to {max(int(r['dateNotAfter']) for r in rows)}")
LABSIGN=[glyphs(r['hieroglyphs']) for r in lab]; LABSIGN=[s for s in LABSIGN if len(s)>=3]
LABWORD=[r['transliteration'].split() for r in lab if len(r['transliteration'].split())>=2]
RUNSIGN=[glyphs(r['hieroglyphs']) for r in oth]; RUNSIGN=[s for s in RUNSIGN if len(s)>=3]
# Indus, for the same table
irows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']]
IND=[r['signs_reading_order'].split() for r in irows if r['site']=='Mohenjo-daro']
IND=[t for t in IND if len(t)>=3]
print(f'\n{"corpus":38s}{"n":>6s}{"len":>6s}{"H(first)":>10s}{"H(last)":>9s}{"diff":>7s}{"top last":>10s}{"cond":>8s}{"unique":>8s}')
for name,S in (('Indus seal texts (signs)',IND),
               ('Egyptian label texts (signs)',LABSIGN),
               ('Egyptian label texts (words)',LABWORD),
               ('Egyptian running text (signs)',RUNSIGN)):
    f=[s[0] for s in S]; l=[s[-1] for s in S]
    uniq=len({tuple(s) for s in S})/len(S)
    print(f'{name:38s}{len(S):6d}{np.mean([len(s) for s in S]):6.1f}{H(f):10.2f}{H(l):9.2f}'
          f'{H(l)-H(f):+7.2f}{collections.Counter(l).most_common(1)[0][1]/len(l):9.0%}{excess(S):8.1%}{uniq:8.0%}')
print('\n--- how a title/name label is built (Egyptian, word level) ---')
gl=collections.Counter(r['glossing'].strip() for r in lab)
print('  commonest glossing patterns:',[(k,v) for k,v in gl.most_common(6)])
first=collections.Counter(r['glossing'].split()[0] for r in lab if r['glossing'].split())
last=collections.Counter(r['glossing'].split()[-1] for r in lab if r['glossing'].split())
print('  first element:',first.most_common(4))
print('  last element: ',last.most_common(4))
print('\n--- repetition: do labels reuse a small stock? ---')
for name,S in (('Indus seal texts',IND),('Egyptian label texts',LABWORD)):
    c=collections.Counter(tuple(s) for s in S)
    print(f'  {name:22s} {len(S):5d} texts, {len(c):5d} distinct, {sum(1 for v in c.values() if v==1)/len(c):4.0%} occur once, '
          f'commonest {max(c.values())} copies')
