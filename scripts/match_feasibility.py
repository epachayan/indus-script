# How far do size, shape and material narrow the Mackay <-> CISI match, before reading the plates?
import re, csv, collections, numpy as np
sql=open('../data/indus-website/population-script.sql',encoding='utf8').read()
b=sql[sql.index('INSERT INTO SEAL ('):]; b=b[:b.index(');\n')+1]
cisi=[]
for _,typ,mat,c,_,w,h in re.findall(r'\((\d+),\s*"([^"]*)",\s*"([^"]*)",\s*"([^"]*)",\s*"?([^,"]*)"?,\s*([\d.]+),\s*([\d.]+)',b):
    if c.startswith('M-') and float(w)>0 and float(h)>0: cisi.append(dict(cisi=c,typ=typ,mat=mat,w=float(w),h=float(h)))
print(f'CISI Mohenjo-daro seals with measurements: {len(cisi)}')
M=[r for r in csv.DictReader(open('../outputs/mackay_seal_table.csv')) if r['no'].isdigit()]
def dims(r):
    m=re.match(r'([\d.]+)x([\d.]+)',r['dims_in'])
    return (float(m.group(1))*25.4,float(m.group(2))*25.4) if m else None
Mm=[(r,dims(r)) for r in M]; Mm=[(r,d) for r,d in Mm if d]
print(f'Mackay seals with two dimensions: {len(Mm)}')
print('sizes (mm): Mackay median %.1f x %.1f | CISI median %.1f x %.1f'%(
    np.median([d[0] for _,d in Mm]),np.median([d[1] for _,d in Mm]),
    np.median([c['w'] for c in cisi]),np.median([c['h'] for c in cisi])))
SHAPE={'B':'square','C':'square','F':'rect','D':'rect'}
cand=[]; strict=[]
for tol in (0.5,1.0,2.0):
    n=[]
    for r,(w,h) in Mm:
        k=[c for c in cisi if abs(c['w']-w)<=tol and abs(c['h']-h)<=tol]
        n.append(len(k))
    n=np.array(n)
    print(f'tolerance +/-{tol} mm: median candidates {np.median(n):.0f}, unique match for {np.mean(n==1):.0%}, no candidate {np.mean(n==0):.0%}')
    if tol==1.0: cand=n
# material as an extra filter
mat_map={'Steatite':'Steatite','Faience':'Faience','Silver':'Silver','Paste':'Paste','Ivory':'Ivory'}
n2=[]
for r,(w,h) in Mm:
    mm=mat_map.get(r['material'].split(' (')[0])
    k=[c for c in cisi if abs(c['w']-w)<=1.0 and abs(c['h']-h)<=1.0 and (mm is None or c['mat']==mm or not c['mat'])]
    n2.append(len(k))
n2=np.array(n2)
print(f'size +/-1 mm + material: median {np.median(n2):.0f}, unique {np.mean(n2==1):.0%}, none {np.mean(n2==0):.0%}')
print('\nHow much does a text reading add? candidate counts with size +/-1mm:')
print('  distribution:',dict(collections.Counter(np.clip(cand,0,6)).most_common()))

# calibrate a systematic offset/scale between Mackay's inches and the CISI measurements
best=None
for scale in np.arange(0.97,1.09,0.005):
    for off in np.arange(-0.5,2.6,0.25):
        n=[]
        for r,(w,h) in Mm:
            W,H=w*scale+off,h*scale+off
            n.append(sum(1 for c in cisi if abs(c['w']-W)<=0.5 and abs(c['h']-H)<=0.5))
        n=np.array(n); score=np.mean(n==1)-0.5*np.mean(n==0)
        if best is None or score>best[0]: best=(score,scale,off,np.mean(n==1),np.mean(n==0),np.median(n))
print(f'\nbest calibration: scale {best[1]:.3f}, offset {best[2]:.2f} mm -> unique {best[3]:.0%}, none {best[4]:.0%}, median candidates {best[5]:.0f}')
print('Interpretation: size+shape is a filter, not an identifier; the plates are needed to decide.')
