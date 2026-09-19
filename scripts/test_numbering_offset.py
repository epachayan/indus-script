# Is CISI's M-numbering just Mackay's sequence shifted? Test by size agreement across offsets.
import re, csv, numpy as np
sql=open('../data/indus-website/population-script.sql',encoding='utf8').read()
b=sql[sql.index('INSERT INTO SEAL ('):]; b=b[:b.index(');\n')+1]
cisi={}
for _,typ,mat,c,_,w,h in re.findall(r'\((\d+),\s*"([^"]*)",\s*"([^"]*)",\s*"([^"]*)",\s*"?([^,"]*)"?,\s*([\d.]+),\s*([\d.]+)',b):
    m=re.fullmatch(r'M-(\d+)([A-Za-z]?)',c.strip())
    if m and float(w)>0: cisi[int(m.group(1))]=(float(w),float(h))
M={}
for r in csv.DictReader(open('../outputs/mackay_seal_table.csv')):
    if not r['no'].isdigit(): continue
    d=re.match(r'([\d.]+)x([\d.]+)',r['dims_in'])
    if d: M[int(r['no'])]=(float(d.group(1))*25.4,float(d.group(2))*25.4)
print(f'CISI M-numbers with size: {len(cisi)} (range {min(cisi)}-{max(cisi)}); Mackay seals with size: {len(M)}')
best=[]
for off in range(-50,1400):
    pairs=[(M[n],cisi[n+off]) for n in M if n+off in cisi]
    if len(pairs)<50: continue
    d=np.array([abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in pairs])
    best.append((np.mean(d<1.5),off,len(pairs),np.median(d)))
best.sort(reverse=True)
print('best offsets by share of size matches within 1.5 mm:')
for s,off,n,med in best[:5]: print(f'  offset {off:5d}: {s:.1%} of {n} pairs match, median diff {med:.1f} mm')
rand=np.mean([abs(a[0]-b[0])+abs(a[1]-b[1])<1.5 for a in list(M.values())[:300] for b in list(cisi.values())[:300]])
print(f'chance level for a random pairing: {rand:.1%}')
