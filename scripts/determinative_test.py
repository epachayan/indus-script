# Does the Indus script have DETERMINATIVE-like signs?
# Not a shape comparison (look-alike matching between scripts is unfalsifiable) but a
# functional one. Egyptian determinatives have a distributional fingerprint: they sit at
# the END of a word, attach to MANY different words, and are unpronounced - so they appear
# in the hieroglyphs but have no counterpart in the transliteration.
# Here that fingerprint is measured on Egyptian, then looked for in the Indus corpus.
import json, sys, csv, collections, math, unicodedata, numpy as np
path=sys.argv[1] if len(sys.argv)>1 else '../data/tla_egyptian_earlier.jsonl'
rows=[json.loads(l) for l in open(path,encoding='utf8')]
def glyphs(s): return [ch for ch in s if unicodedata.category(ch)=='Lo' and ord(ch)>=0x13000]
# build word-level data: glyph string + lemma id
WORDS=[]
for r in rows:
    hs=r['hieroglyphs'].split(); lem=r['lemmatization'].split()
    if len(hs)!=len(lem): continue
    for h,l in zip(hs,lem):
        g=glyphs(h)
        if g: WORDS.append((g,l.split('|')[0]))
print(f'Egyptian words with glyphs and lemma: {len(WORDS)}')
fin=collections.Counter(); tot=collections.Counter(); lemmas=collections.defaultdict(set)
for g,l in WORDS:
    for i,ch in enumerate(g):
        tot[ch]+=1
        if i==len(g)-1: fin[ch]+=1
        lemmas[ch].add(l)
prof=[(ch,tot[ch],fin[ch]/tot[ch],len(lemmas[ch])) for ch in tot if tot[ch]>=30]
det=[p for p in prof if p[2]>=0.8 and p[3]>=20]
print(f'glyphs with 30+ tokens: {len(prof)}; determinative-like (80%+ word-final, 20+ lemmas): {len(det)}')
print('  examples:',' '.join(f'{ch}({n},{f:.0%},{L})' for ch,n,f,L in sorted(det,key=lambda p:-p[1])[:10]))
share=sum(p[1] for p in det)/sum(tot.values())
print(f'  they are {share:.1%} of all glyph tokens')
print(f'  median final-share among ALL frequent glyphs: {np.median([p[2] for p in prof]):.0%}')

# --- same fingerprint in the Indus corpus ---
irows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']]
T=[r['signs_reading_order'].split() for r in irows]
ifin=collections.Counter(); itot=collections.Counter(); ictx=collections.defaultdict(set)
for t in T:
    for i,s in enumerate(t):
        itot[s]+=1
        if i==len(t)-1: ifin[s]+=1
        if i>0: ictx[s].add(t[i-1])
iprof=[(s,itot[s],ifin[s]/itot[s],len(ictx[s])) for s in itot if itot[s]>=30]
idet=[p for p in iprof if p[2]>=0.8 and p[3]>=20]
print(f'\nIndus signs with 30+ tokens: {len(iprof)}; matching the fingerprint: {len(idet)}')
for s,n,f,L in sorted(idet,key=lambda p:-p[1])[:10]:
    print(f'  {s:6s} {n:5d} tokens, {f:.0%} text-final, {L} different signs before it')
ishare=sum(p[1] for p in idet)/sum(itot.values())
print(f'  they are {ishare:.1%} of all Indus sign tokens')
print(f'  median final-share among ALL frequent Indus signs: {np.median([p[2] for p in iprof]):.0%}')
# near misses: strongly final but less context-diverse, or diverse but less final
near=[p for p in iprof if p not in idet and p[2]>=0.5 and p[3]>=20]
print(f'  near misses (50-80% final, 20+ contexts): {len(near)} -> '
      + ', '.join(f'{s}({f:.0%})' for s,n,f,L in sorted(near,key=lambda p:-p[1])[:8]))
