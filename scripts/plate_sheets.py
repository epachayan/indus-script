# Build coding sheets: each assigned seal photo, cropped and enlarged, with its number.
# Usage: python3 plate_sheets.py <plate.jpg> <dir> <sheet_size> [start_index]
import sys, json
from PIL import Image, ImageDraw, ImageFont
src,d=sys.argv[1],sys.argv[2]; n=int(sys.argv[3]); start=int(sys.argv[4]) if len(sys.argv)>4 else 0
A=sorted(json.load(open(f'{d}/assigned.json')),key=lambda r:r['no'])[start:start+n]
im=Image.open(src).convert('L')
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
except Exception: f=None
cols=4; cw,ch=430,300
sh=Image.new('L',(cols*cw,((len(A)+cols-1)//cols)*ch),255); dr=ImageDraw.Draw(sh)
for i,r in enumerate(A):
    x0,y0,x1,y1=r['box']
    c=im.crop((x0,y0,x1,y1)); s=min((cw-70)/c.size[0],(ch-20)/c.size[1],3.0)
    c=c.resize((max(1,int(c.size[0]*s)),max(1,int(c.size[1]*s))))
    x,y=(i%cols)*cw,(i//cols)*ch
    dr.text((x+6,y+ch//2-14),str(r['no']),fill=0,font=f)
    sh.paste(c,(x+64,y+8)); dr.rectangle([x,y,x+cw-2,y+ch-2],outline=210)
sh.save(f'{d}/sheet_{start}.png'); print(f'{d}/sheet_{start}.png',sh.size,[r['no'] for r in A])
