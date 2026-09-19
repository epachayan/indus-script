# Exp 3: numbers inside titles and number/item order in Sumerian & Akkadian administrative lines (CDLI).
import re, collections, numpy as np
txt=open('../data/cdliatf_unblocked.atf',encoding='utf8',errors='replace').read()
NUM=re.compile(r'^\d+(/\d+)?\((disz|u|gesz2|asz|ban2|barig|bur3|esze3|iku|gur|sila3|gin2|ma-na|n\d+|N\d+)[^)]*\)$',re.I)
lines=collections.Counter(); first=collections.Counter(); titled=collections.Counter(); after=collections.Counter()
TITLE=re.compile(r'^(ugula|nu-banda3|nu-banda|sza13-dub-ba|kurusda|GAL|gal|ugula-gesz2-da)$')
for b in re.split(r'\n(?=&P\d+)',txt):
    m=re.search(r'#atf:\s*lang\s*(\w+)',b); lang=m.group(1) if m else '?'
    if lang not in('sux','akk'): continue
    seal=False
    for l in b.split('\n'):
        if l.startswith('@'): seal=l.startswith('@seal'); continue
        mm=re.match(r"^\d+'?\.\s*(.*)",l)
        if not mm or seal: continue
        w=[x for x in re.sub(r'[\[\]#?!]','',mm.group(1)).split() if x not in('...','x')]
        if len(w)<2: continue
        nums=[i for i,x in enumerate(w) if NUM.match(x)]
        if not nums: continue
        lines[lang]+=1
        first[(lang,'number first' if nums[0]==0 else 'number later')]+=1
        for i in range(len(w)-1):
            if TITLE.match(w[i]) and NUM.match(w[i+1]): titled[(w[i],w[i+1])]+=1; after[' '.join(w[i+2:i+3])]+=1
        for i in range(1,len(w)):
            if w[i-1] in('ugula','nu-banda3') and w[i]=='gesz2-da': titled[(w[i-1],'gesz2-da (=60)')]+=1
print('administrative lines with numbers:',dict(lines))
for lang in('sux','akk'):
    a=first[(lang,'number first')]; b=first[(lang,'number later')]
    print(f'  {lang}: number comes first in {a/(a+b):.0%} of numbered lines')
print('\ntitle followed directly by a number (numbered ranks / group leaders):')
for (t,n),c in titled.most_common(10): print(f'  {c:5d}  {t} {n}')
print('  word after "title + number":',after.most_common(6))

# explicit "overseer of 10 / 60" forms (hyphenated or spaced)
for pat,lab in ((r'ugula[- ]gesz2-da','ugula gesz2-da (overseer of 60)'),(r'ugula[- ]1\(gesz2\)','ugula 1(gesz2) (overseer of 60)'),(r'ugula[- ]1\(u\)','ugula 1(u) (overseer of 10)')):
    print(f'  {len(re.findall(pat,txt)):5d}  {lab}')
# compare: value distribution of Indus count signs inside text cores
import csv
VAL={'G1':1,'G3':3,'G4':4,'G5':5,'G7':7,'G16':6,'G17':7,'G18':8,'G19':9,'G31':1,'G32':2,'G33':3,'G35':5}
rows=list(csv.DictReader(open('../outputs/inscriptions_ml.csv')))
v=collections.Counter(VAL[s] for r in rows if r['first_occurrence']=='True' for s in r['signs_reading_order'].split() if s in VAL)
tot=sum(v.values())
print('\nIndus count values:',{k:f'{c/tot:.0%}' for k,c in sorted(v.items())},'| round 10/60 not attested as single signs')
