# Egyptian as a comparison corpus. Egyptian is a MIXED system (phonetic signs, logograms,
# determinatives) with a large sign inventory - the closest structural analogue to what the
# Indus inventory size implies. Data: Thesaurus Linguae Aegyptiae (CC-BY-SA 4.0), JSONL with
# hieroglyphs, transliteration, UPOS tags. Place as data/tla_egyptian.jsonl.
# NOTE the corpus supplied here is LATER Egyptian (-1539 to -332), so it post-dates the
# Indus cities; it is used as a script-type comparand, not a chronological one.
import json, sys, collections, math, random, unicodedata, numpy as np
random.seed(97)
path=sys.argv[1] if len(sys.argv)>1 else '../data/tla_egyptian.jsonl'
rows=[json.loads(l) for l in open(path,encoding='utf8')]
def H(s):
    c=collections.Counter(s); n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values())
def mi(p): return H([a for a,_ in p])+H([b for _,b in p])-H(p)
def excess(seqs,d=1,n=1000,draws=12,reps=25):
    S=[s for s in seqs if len(s)>=d+1]
    if len(S)<200: return None
    v=[]
    for _ in range(draws):
        X=random.sample(S,min(n,len(S)))
        p=[(s[i],s[i+d]) for s in X for i in range(len(s)-d)]
        o=mi(p); hl=H([b for _,b in p]); nl=[]
        for _ in range(reps):
            b=[y for _,y in p]; random.shuffle(b); nl.append(mi(list(zip([x for x,_ in p],b))))
        v.append((o-np.mean(nl))/hl)
    return float(np.mean(v))
def glyphs(s):
    return [ch for ch in s if unicodedata.category(ch)=='Lo' and ord(ch)>=0x13000]
# sign sequences: whole sentence, and within a single word
SENT=[glyphs(r['hieroglyphs']) for r in rows]
SENT=[s for s in SENT if len(s)>=3]
WORD=[glyphs(w) for r in rows for w in r['hieroglyphs'].split() if len(glyphs(w))>=3]
WORDSEQ=[r['transliteration'].split() for r in rows if len(r['transliteration'].split())>=3]
print(f'Egyptian: {len(SENT)} sentences as sign strings (median {int(np.median([len(s) for s in SENT]))} signs), '
      f'{len(WORD)} words of 3+ signs, {len(WORDSEQ)} sentences as word strings')
print('\n--- ending constraint and conditioning ---')
for lab,S in (('Egyptian signs in a sentence',SENT),('Egyptian signs in a word',WORD),
              ('Egyptian words in a sentence',WORDSEQ)):
    f=[s[0] for s in S]; l=[s[-1] for s in S]
    print(f'  {lab:30s} H(first)={H(f):5.2f} H(last)={H(l):5.2f} diff={H(l)-H(f):+5.2f} '
          f'commonest last {collections.Counter(l).most_common(1)[0][1]/len(l):4.0%}  '
          f'conditioning excess {excess(S):5.1%}')
print('\n--- direction ---')
for lab,S in (('Egyptian signs in a sentence',SENT),('Egyptian words in a sentence',WORDSEQ)):
    X=random.sample(S,min(1500,len(S)))
    fwd=[(s[i],s[i+1]) for s in X for i in range(len(s)-1)]
    m=mi(fwd); Hf=H([b for _,b in fwd])-m; Hb=H([a for a,_ in fwd])-m
    print(f'  {lab:30s} H(next|prev)={Hf:5.2f}  H(prev|next)={Hb:5.2f}  diff={Hb-Hf:+.2f}')
print('\n--- do our measures track grammatical category? (UPOS, where the answer is known) ---')
POS=[r['UPOS'].split() for r in rows if len(r['UPOS'].split())>=3]
f=[s[0] for s in POS]; l=[s[-1] for s in POS]
print(f'  POS tags: H(first)={H(f):.2f} H(last)={H(l):.2f} diff={H(l)-H(f):+.2f}; '
      f'conditioning excess {excess(POS):.1%}')
print(f'  commonest final POS: {collections.Counter(l).most_common(3)}')
print(f'  commonest initial POS: {collections.Counter(f).most_common(3)}')
# does sign-level conditioning survive after controlling for POS? (are they the same signal?)
print('\n--- frequency classes (as in FINDINGS 32b) ---')
cnt=collections.Counter(s for t in SENT for s in t)
pairs=[(t[i],t[i+1]) for t in SENT for i in range(len(t)-1)]
def band(s):
    n=cnt[s]; return 'frequent (50+)' if n>=50 else ('mid (10-49)' if n>=10 else 'rare (<10)')
for b in ('frequent (50+)','mid (10-49)','rare (<10)'):
    P=[p for p in pairs if band(p[0])==b]
    if len(P)<200: continue
    o=mi(P); hl=H([y for _,y in P]); nl=[]
    for _ in range(40):
        y=[q for _,q in P]; random.shuffle(y); nl.append(mi(list(zip([x for x,_ in P],y))))
    print(f'  first sign {b:16s} n={len(P):6d}  excess {(o-np.mean(nl))/hl:5.1%}')
