# Segment a Mackay plate scan: find each seal photo, read its printed number, crop the
# inscription band and estimate the number of signs.
# Usage: python3 plate_segment.py <plate.jpg> <out_dir> [min_no] [max_no]
import sys, os, json, numpy as np
from PIL import Image
from scipy import ndimage
import pytesseract
src,out=sys.argv[1],sys.argv[2]
lo=int(sys.argv[3]) if len(sys.argv)>3 else 1; hi=int(sys.argv[4]) if len(sys.argv)>4 else 9999
os.makedirs(out,exist_ok=True)
im=Image.open(src).convert('L'); W,H=im.size
a=np.array(im)
paper=np.percentile(a,80)
m=a<paper-28                                   # photos are darker than the paper
m=ndimage.binary_closing(m,np.ones((11,11)))
m=ndimage.binary_opening(m,np.ones((7,7)))
lab,n=ndimage.label(m)
boxes=[]
for sl in ndimage.find_objects(lab):
    y0,y1,x0,x1=sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
    w,h=x1-x0,y1-y0
    if w<120 or h<90 or w*h<30000: continue
    if w>W*0.9 or h>H*0.5: continue
    boxes.append([int(x0),int(y0),int(x1),int(y1)])
print(f'{os.path.basename(src)}: {len(boxes)} photo regions')
# printed numbers are small dark blobs on bare paper: find them once, then OCR each
photo=np.zeros_like(m)
for x0,y0,x1,y1 in boxes: photo[max(0,y0-12):y1+12,max(0,x0-12):x1+12]=True
txt_mask=(a<paper-40)&(~photo)
tl,tn=ndimage.label(ndimage.binary_closing(txt_mask,np.ones((9,31))))
labels=[]
for sl in ndimage.find_objects(tl):
    y0,y1,x0,x1=sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
    w,h=x1-x0,y1-y0
    if 25<h<110 and 20<w<260 and 0.25<w/h<4.0:
        crop=im.crop((x0-8,y0-8,x1+8,y1+8))
        crop=crop.resize((crop.size[0]*4,crop.size[1]*4),Image.LANCZOS)
        d=''
        for psm in ('8','7','13'):
            t=pytesseract.image_to_string(crop,config=f'--psm {psm} -c tessedit_char_whitelist=0123456789')
            d=''.join(ch for ch in t if ch.isdigit())
            if d and lo<=int(d)<=hi: break
        if not (d and lo<=int(d)<=hi):
            # split the label into single digits and read each on its own
            sub=np.array(im.crop((x0-4,y0-4,x1+4,y1+4)))
            bw=sub<np.percentile(sub,55)
            dl,dn=ndimage.label(ndimage.binary_closing(bw,np.ones((9,3))))
            parts=[]
            for s2 in ndimage.find_objects(dl):
                dh=s2[0].stop-s2[0].start; dw=s2[1].stop-s2[1].start
                if dh>0.45*(y1-y0) and dw>6: parts.append((s2[1].start,s2))
            digs=''
            for _,s2 in sorted(parts):
                c2=Image.fromarray(sub[s2]).resize(((s2[1].stop-s2[1].start)*6,(s2[0].stop-s2[0].start)*6),Image.LANCZOS)
                c3=Image.new('L',(c2.size[0]+40,c2.size[1]+40),255); c3.paste(c2,(20,20))
                t=pytesseract.image_to_string(c3,config='--psm 10 -c tessedit_char_whitelist=0123456789')
                t=''.join(ch for ch in t if ch.isdigit())
                digs+=t[:1] if t else '?'
            if digs and '?' not in digs and lo<=int(digs)<=hi: d=digs
        if d and lo<=int(d)<=hi: labels.append((int(d),(x0+x1)//2,(y0+y1)//2))
seen={}
for no,cx,cy in labels: seen.setdefault(no,[]).append((cx,cy))
labels=[(no,v[0][0],v[0][1]) for no,v in seen.items() if len(v)==1]   # drop numbers read twice
print(f'printed numbers found: {len(labels)} (unique)')
def read_label(b):
    # nearest label below-left / below-right / right of the photo
    x0,y0,x1,y1=b; best=None
    for no,cx,cy in labels:
        if cy<y0-30: continue
        dx=0 if x0-60<=cx<=x1+60 else min(abs(cx-x0),abs(cx-x1))
        dy=max(0,cy-y1)
        d=dx+dy*1.2
        if dx>320 or dy>260: continue
        if best is None or d<best[0]: best=(d,no)
    return best[1] if best else None
# one label per photo: solve it as an assignment problem on the distances
from scipy.optimize import linear_sum_assignment
BIG=1e6
C=np.full((len(boxes),len(labels)),BIG)
for i,(x0,y0,x1,y1) in enumerate(boxes):
    for j,(no,cx,cy) in enumerate(labels):
        dx=0 if x0-70<=cx<=x1+70 else min(abs(cx-x0),abs(cx-x1))
        dy=max(0,cy-y1) if cy>y1 else (max(0,y0-cy)*2.5)
        if dx>340 or dy>300: continue
        C[i,j]=dx+dy*1.2
ri,ci=linear_sum_assignment(C)
res=[dict(box=b,no=None) for b in boxes]
for i,j in zip(ri,ci):
    if C[i,j]<BIG: res[i]['no']=labels[j][0]
got=[r for r in res if r['no']]
print(f'numbers read: {len(got)}/{len(boxes)}; duplicates: {len(got)-len(set(r["no"] for r in got))}')
for r in got:
    x0,y0,x1,y1=r['box']
    im.crop((x0,y0,x1,y1)).save(f'{out}/seal_{r["no"]:03d}.png')
json.dump(res,open(f'{out}/boxes.json','w'))
