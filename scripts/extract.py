import re, json, collections, csv
sql=open('../data/indus-website/population-script.sql',encoding='utf8').read()
g=sql[sql.index('INSERT INTO GLYPH (GLYPHID'):]; g=g[:g.index(");\n")]
glyph={int(a):b for a,b in re.findall(r'\((\d+),\s*"([^"]*)"\)',g)}
cp={k:int(re.search(r'#x([0-9A-Fa-f]+)',v).group(1),16) for k,v in glyph.items() if '#x' in v}
s=sql[sql.index('INSERT INTO GLYPHSIMILARITY'):]; s=s[:s.index(");\n")]
sim=[tuple(map(int,p)) for p in re.findall(r'\((\d+),\s*(\d+)\)',s)]
freq=collections.Counter(); pos=collections.defaultdict(collections.Counter)
for r in csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')):
    seq=[int(x[1:]) for x in r['sign_sequence'].split() if x.startswith('G')]
    for i,x in enumerate(seq):
        freq[x]+=1
        pos[x]['first' if i==0 else 'last' if i==len(seq)-1 else 'mid']+=1
json.dump(dict(cp=cp,sim=sim,freq=freq,pos={k:dict(v) for k,v in pos.items()}),open('meta.json','w'))
print(len(glyph),len(cp),len(sim),'used signs',len(freq),'tokens',sum(freq.values()))
print(freq.most_common(10))
