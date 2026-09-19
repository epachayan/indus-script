import re, collections
sql=open('../data/indus-website/population-script.sql',encoding='utf8').read()
def block(name):
    b=sql[sql.index(f'INSERT INTO {name}'):]; return b[:b.index(');\n')+1]
feat={int(a):b for a,b in re.findall(r'\((\d+),\s*"([^"]*)"\)',block('FEATURE ('))}
sealcisi={int(a):(mat,c) for a,s_,mat,c in re.findall(r'\((\d+),\s*"([^"]*)",\s*"([^"]*)",\s*"([^"]*)"',block('SEAL ('))}
obj=collections.defaultdict(set)
for a,q in re.findall(r'\((\d+),\s*(\d+)\)',block('ICONOGRAPHYFEATURES')):
    f=feat.get(int(q),'')
    obj[int(a)].add(f.split(':')[0])
bycisi={c:(sorted(obj[i]),m) for i,(m,c) in sealcisi.items()}
exec(open('../scripts/motif_dedup.py').read().split("print('inscriptions'")[0])
has=[('G400' in s) for s in S]
for st in ['Harappa','Mohenjo-daro']:
    t=collections.Counter(); g=collections.Counter()
    for i,r in enumerate(rs):
        if r['site']!=st: continue
        o,mat=bycisi.get(r['cisi_number'],([],'?'))
        k=('TAB' if 'TAB' in o else 'SEAL' if 'SEAL' in o else '/'.join(o) or '?')+(' unicorn' if M[i]=='unicorn' else ' other-animal')
        t[k]+=1; g[k]+=has[i]
    print(st); [print(f'   {k:22s} {g[k]:2d}/{n:3d} {100*g[k]/n:3.0f}%') for k,n in sorted(t.items())]
