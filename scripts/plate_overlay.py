# Draw the detected photo boxes with an index on a plate scan, for manual number mapping.
# Usage: python3 plate_overlay.py <plate.jpg> <boxes.json> <out.png> [scale]
import sys, json
from PIL import Image, ImageDraw
src,bj,out=sys.argv[1],sys.argv[2],sys.argv[3]
sc=float(sys.argv[4]) if len(sys.argv)>4 else 0.34
im=Image.open(src).convert('RGB')
res=json.load(open(bj))
im=im.resize((int(im.size[0]*sc),int(im.size[1]*sc)))
d=ImageDraw.Draw(im)
for i,r in enumerate(res):
    x0,y0,x1,y1=[int(v*sc) for v in r['box']]
    d.rectangle([x0,y0,x1,y1],outline=(255,0,0),width=2)
    d.text((x0+3,y0+3),str(i),fill=(255,0,0))
im.save(out); print(out, im.size, len(res),'boxes')
