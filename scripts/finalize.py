import json,csv,numpy as np
from PIL import Image, ImageDraw
names={0:'fish',1:'comb/frame + quadruped (mixed)',2:'butterfly/hourglass',3:'leaf/arch',4:'circle/bracketed',5:'small marked + misc',
6:'human figure',7:'A-shape/spear-head',8:'diamond',9:'crescent/curve',10:'cup with attachments',11:'single/double stroke',
12:'stem with crossbar',13:'ladder/frame',14:'bracketed composite',15:'forked stem/arrow',16:'human with object',17:'jar/U-vessel',
18:'human with side loops',19:'oval with infill',20:'D-bow',21:'X/insect-like',22:'stroke groups',23:'thin curve/bead chain',
24:'mixed line groups/birds',25:'grid/multi-bar',26:'box with inner marks',27:'tall stroke + ladder/cone',28:'left bracket',
29:'NOT RENDERED (font placeholder)',30:'intersecting ovals',31:'slanted triple (rake)',32:'lens with inner marks',33:'quadruped animal',
34:'zoomorph/hatched (mixed)',35:'half-X/hourglass'}
im=np.load('imgs.npy'); d=json.load(open('tags.json')); ids=d['ids']; t=d['tags']; lab=np.load('labels.npy')
pos=json.load(open('meta.json'))['pos']
rows=[]
for i,g in enumerate(ids):
    v=t[str(g)]; p=pos.get(str(g),{}); n=sum(p.values()) or 1
    rows.append(dict(sign=f'G{g}',family=names[lab[i]],cluster=int(lab[i]),frequency=v['freq'],
      tags=';'.join(v['tags']),parts=v['ncomp'],holes=v['holes'],aspect=v['aspect'],sym_LR=v['symLR'],
      ends_text=round(p.get('first',0)/n,2),starts_text=round(p.get('last',0)/n,2)))
with open('../outputs/indus_sign_tags.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(sorted(rows,key=lambda r:-r['frequency']))
# family summary
tot=sum(r['frequency'] for r in rows); fam={}
for r in rows:
    a=fam.setdefault(r['family'],[0,0,0,0]); a[0]+=1; a[1]+=r['frequency']
    a[2]+=r['frequency']*r['starts_text']; a[3]+=r['frequency']*r['ends_text']
for k,(n,f,l,fi) in sorted(fam.items(),key=lambda x:-x[1][1])[:14]:
    print(f'{k:30s} signs={n:3d} tokens={f/tot:5.1%} starts_text={l/max(f,1):.0%} ends_text={fi/max(f,1):.0%}')
# atlas: one row per family, top 12 by frequency
order=[k for k in sorted(names,key=lambda k:-sum(r['frequency'] for r in rows if r['cluster']==k)) if k!=29]
W,C=62,12; sheet=Image.new('L',(230+C*W,len(order)*W+10),255); dr=ImageDraw.Draw(sheet)
for r_,k in enumerate(order):
    mem=sorted([i for i in range(len(ids)) if lab[i]==k],key=lambda i:-t[str(ids[i])]['freq'])
    toks=sum(t[str(ids[i])]['freq'] for i in mem)
    dr.text((6,r_*W+18),names[k],fill=0); dr.text((6,r_*W+32),f'{len(mem)} signs, {toks/tot:.1%} of text',fill=90)
    for c,i in enumerate(mem[:C]):
        sheet.paste(Image.fromarray(255-(im[i]*255).astype(np.uint8)).resize((44,44)),(230+c*W,r_*W+4))
        dr.text((232+c*W,r_*W+49),f'G{ids[i]}',fill=60)
sheet.save('../outputs/indus_sign_family_atlas.png')
print(sheet.size, 'missing glyphs:',[f'G{ids[i]}' for i in range(len(ids)) if lab[i]==29])
