import json, csv, numpy as np
from PIL import Image, ImageDraw
names={3:'Text-final markers',0:'Pre-final signs',8:'Text openers',5:'Fish core (medial)',4:'Strict medial connectors',
6:'Short-stroke numerals',7:'Stroke groups (medial)',1:'Opening-medial (A)',9:'Opening-medial (B)',2:'Core medial (varied)'}
f=json.load(open('func.json')); V=f['V']; lab=f['lab']; P=np.array(f['P']); fr=f['freq']
cls={s:(names[l],P[i]/P[i].sum()) for i,(s,l) in enumerate(zip(V,lab))}
path='../outputs/indus_sign_tags.csv'
rows=list(csv.DictReader(open(path)))
for r in rows:
    c=cls.get(r['sign']); r['behaviour_class']=c[0] if c else ''
    for k,j in (('reading_initial',0),('reading_medial',1),('reading_final',2)):
        r[k]=round(float(c[1][j]),2) if c else ''
    r.pop('ends_text',None); r.pop('starts_text',None)
with open(path,'w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
im=np.load('imgs.npy'); ids=json.load(open('tags.json'))['ids']; ix={f'G{g}':i for i,g in enumerate(ids)}
order=[3,0,8,5,4,6,7,1,9,2]; W,C=62,12; tot=sum(fr[s] for s in V)
sh=Image.new('L',(230+C*W,len(order)*W+8),255); dr=ImageDraw.Draw(sh)
for r_,k in enumerate(order):
    mem=sorted([s for s,l in zip(V,lab) if l==k],key=lambda s:-fr[s]); p=P[[V.index(s) for s in mem]].sum(0); p=p/p.sum()
    dr.text((6,r_*W+12),names[k],fill=0)
    dr.text((6,r_*W+26),f'{len(mem)} signs, {sum(fr[s] for s in mem)/tot:.0%} of use',fill=90)
    dr.text((6,r_*W+40),f'start {p[0]:.0%}  mid {p[1]:.0%}  end {p[2]:.0%}',fill=90)
    for c,s in enumerate(mem[:C]):
        sh.paste(Image.fromarray(255-(im[ix[s]]*255).astype(np.uint8)).resize((44,44)),(230+c*W,r_*W+4))
        dr.text((232+c*W,r_*W+49),s,fill=60)
sh.save('../outputs/indus_behaviour_atlas.png'); print(sh.size, list(rows[0].keys()))
