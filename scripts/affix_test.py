# Does the Indus corpus look like a SUFFIXING language (constrained endings) or a
# PREFIXING one (constrained beginnings)?  Method: for each corpus of short sequences,
# compare how constrained the LAST element is against the FIRST, using entropy and the
# share taken by the commonest element.  Comparison corpora, with their morphology:
#   Linear B words      = Mycenaean Greek, strongly suffixing (case/number endings)
#   Sumerian words      = heavily prefixing verbal morphology (CDLI administrative lines)
#   Sumerian seal legends = same language, same genre as the Indus seals
#   Linear A words      = unknown language (control)
#   shuffled Indus      = null (same signs, order destroyed)
import re, csv, json, collections, random, math
random.seed(5)
def H(seq):
    c=collections.Counter(seq); n=sum(c.values())
    return -sum(v/n*math.log2(v/n) for v in c.values()) if n else 0.0
def top(seq):
    c=collections.Counter(seq); n=sum(c.values())
    return c.most_common(1)[0][1]/n if n else 0.0
def report(name,seqs):
    seqs=[s for s in seqs if len(s)>=2]
    if len(seqs)<100: print(f'{name:26s} (only {len(seqs)} sequences - skipped)'); return None
    hf,hl=H([s[0] for s in seqs]),H([s[-1] for s in seqs])
    tf,tl=top([s[0] for s in seqs]),top([s[-1] for s in seqs])
    print(f'{name:26s} n={len(seqs):6d}  H(first)={hf:5.2f}  H(last)={hl:5.2f}  '
          f'H(last)-H(first)={hl-hf:+5.2f}   commonest first {tf:4.0%}  last {tl:4.0%}')
    return dict(corpus=name,n=len(seqs),h_first=round(hf,3),h_last=round(hl,3),
                diff=round(hl-hf,3),top_first=round(tf,3),top_last=round(tl,3))
out=[]
# Indus
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['signs_reading_order']]
ind=[r['signs_reading_order'].split() for r in rows]
mj=[r['signs_reading_order'].split() for r in rows if r['site']=='Mohenjo-daro']
out.append(report('Indus (all sites)',ind)); out.append(report('Indus (Mohenjo-daro)',mj))
sh=[random.sample(t,len(t)) for t in ind]
out.append(report('Indus shuffled (null)',sh))
# Aegean
def aegean_words(path,key):
    # words are syllabogram sequences joined by hyphens; strip editorial marks
    txt=open(path,encoding='utf8',errors='replace').read()
    words=[]
    for m in re.findall(r'"'+key+r'"\s*:\s*"((?:[^"\\]|\\.)*)"',txt):
        m=m.replace('\\n',' ')
        for w in re.split(r'[\s,]+',m):
            w=re.sub(r'[\[\]\(\)<>%*?!\u2026\.]','',w).strip('-')
            if '-' in w and re.match(r'^[a-z0-9\-]+$',w): words.append(w.split('-'))
    return words
for path,key,lab in (('../data/linearb.xyz/LinearBInscriptions.js','parsedInscription','Linear B words (Greek)'),
                     ('../data/lineara.xyz/LinearAInscriptions.js','parsedInscription','Linear A words (unknown)')):
    try: out.append(report(lab,aegean_words(path,key)))
    except Exception as e: print(lab,'unavailable:',e)
# Sumerian: words as sign sequences, from CDLI administrative lines
try:
    txt=open('../data/cdliatf_unblocked.atf',encoding='utf8',errors='replace').read()
    words=[]
    for line in txt.split('\n'):
        if not line.startswith(tuple('123456789')): continue
        for w in line.split()[1:]:
            w=re.sub(r'[\[\]<>#?!\(\)]','',w)
            if '-' in w and re.match(r'^[a-zA-Z0-9\-\.]+$',w): words.append(w.split('-'))
        if len(words)>60000: break
    out.append(report('Sumerian words (signs)',words))
except Exception as e: print('CDLI unavailable:',e)
with open('../outputs/affix_profile.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['corpus','n','h_first','h_last','diff','top_first','top_last'])
    w.writeheader(); w.writerows([r for r in out if r])
print('\nReading: a suffixing language constrains its ENDINGS, so H(last) < H(first) and the')
print('commonest final element takes a large share. A prefixing one shows the mirror image.')

# Unit-matched comparison: an Indus inscription is a short PHRASE, so compare it with
# phrases (word sequences), not with single words.
print()
try:
    txt=open('../data/linearb.xyz/LinearBInscriptions.js',encoding='utf8',errors='replace').read()
    phr=[]
    for m in re.findall(r'"parsedInscription"\s*:\s*"((?:[^"\\]|\\.)*)"',txt):
        for line in m.split('\\n'):
            ws=[re.sub(r'[\[\]\(\)<>%*?!\u2026\.]','',w).strip('-') for w in re.split(r'[\s,]+',line)]
            ws=[w for w in ws if w and re.match(r'^[a-z0-9\-]+$',w)]
            if len(ws)>=2: phr.append(ws)
    out.append(report('Linear B phrases (Greek)',phr))
except Exception as e: print('Linear B phrases unavailable:',e)
try:
    txt=open('../data/cdliatf_unblocked.atf',encoding='utf8',errors='replace').read()
    lines=[]
    for line in txt.split('\n'):
        if not line.startswith(tuple('123456789')): continue
        ws=[re.sub(r'[\[\]<>#?!\(\)]','',w) for w in line.split()[1:]]
        ws=[w for w in ws if w and re.match(r'^[a-zA-Z0-9\-\.]+$',w)]
        if len(ws)>=2: lines.append(ws)
        if len(lines)>40000: break
    out.append(report('Sumerian lines (words)',lines))
except Exception as e: print('CDLI lines unavailable:',e)
with open('../outputs/affix_profile.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['corpus','n','h_first','h_last','diff','top_first','top_last'])
    w.writeheader(); w.writerows([r for r in out if r])
