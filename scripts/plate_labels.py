# Extract the printed number labels from a plate scan into a grid for manual reading.
# Usage: python3 plate_labels.py <plate.jpg> <out_dir> ; writes labels.json + labels_grid.png
import sys, os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
src,out=sys.argv[1],sys.argv[2]
os.makedirs(out,exist_ok=True)
im=Image.open(src).convert('L'); W,H=im.size; a=np.array(im)
paper=np.percentile(a,80)
m=a<paper-28
m=ndimage.binary_opening(ndimage.binary_closing(m,np.ones((11,11))),np.ones((7,7)))
lab,_=ndimage.label(m)
photo=np.zeros_like(m)
for sl in ndimage.find_objects(lab):
    y0,y1,x0,x1=sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
    if (x1-x0)>120 and (y1-y0)>90 and (x1-x0)*(y1-y0)>30000: photo[max(0,y0-12):y1+12,max(0,x0-12):x1+12]=True
tm=(a<paper-40)&(~photo)
tl,_=ndimage.label(ndimage.binary_closing(tm,np.ones((9,31))))
labs=[]
for sl in ndimage.find_objects(tl):
    y0,y1,x0,x1=sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
    h,w=y1-y0,x1-x0
    if 25<h<120 and 20<w<300 and 0.2<w/h<4.5: labs.append([int(x0),int(y0),int(x1),int(y1)])
labs.sort(key=lambda b:(b[1]//220,b[0]))
json.dump(labs,open(f'{out}/labels.json','w'))
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
except Exception: f=None
cols=8; cw,ch=210,120
sheet=Image.new('L',(cols*cw,((len(labs)+cols-1)//cols)*ch),255); d=ImageDraw.Draw(sheet)
for i,b in enumerate(labs):
    c=im.crop((b[0]-6,b[1]-6,b[2]+6,b[3]+6))
    s=min(2.2,(cw-70)/max(1,c.size[0]),(ch-30)/max(1,c.size[1]))
    c=c.resize((max(1,int(c.size[0]*s)),max(1,int(c.size[1]*s))))
    x,y=(i%cols)*cw,(i//cols)*ch
    d.text((x+6,y+40),f'{i}:',fill=0,font=f)
    sheet.paste(c,(x+60,y+20))
    d.rectangle([x,y,x+cw-2,y+ch-2],outline=200)
sheet.save(f'{out}/labels_grid.png'); print(len(labs),'labels ->',f'{out}/labels_grid.png',sheet.size)
