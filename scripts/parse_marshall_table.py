# Parse Marshall (1931) vol. II, "Mohenjo-daro: Tabulation of Seals" (printed pp. 402-405,
# PDF pages 56-59). Two columns per page. Output: outputs/marshall_seal_table.csv
# Columns as printed: plate no., size in inches, level below SURFACE (ft/in), type,
# material ticks, site and serial no. NB level is below the modern surface, not Mackay's datum.
import sys, re, csv, subprocess, glob, os
from PIL import Image
import pytesseract
src=sys.argv[1] if len(sys.argv)>1 else '../data/marshall1931_vol2.pdf'
tmp='/tmp/_mar'; os.makedirs(tmp,exist_ok=True)
AREAS=('HR','VS','DK','SD','BJ','L','C','E','B','DM','MB')
rows=[]
for pg in (56,57,58,59):
    subprocess.run(['pdftoppm','-png','-r','300','-f',str(pg),'-l',str(pg),src,f'{tmp}/p{pg}'],check=True)
    im=Image.open(glob.glob(f'{tmp}/p{pg}-*.png')[0]); w,h=im.size
    for half,(x0,x1) in (('L',(0.05,0.50)),('R',(0.50,0.97))):
        crop=im.crop((int(w*x0),int(h*0.14),int(w*x1),int(h*0.98)))
        txt=pytesseract.image_to_string(crop,config='--psm 6')
        for line in txt.split('\n'):
            l=' '.join(line.split())
            m=re.search(r'\b('+'|'.join(AREAS)+r')\.?\s*([0-9OoIlSs]{1,5})\s*$',l)
            if not m: continue
            area=m.group(1); serial=m.group(2).translate(str.maketrans('OoIlSs','001155'))
            # the foot mark is printed as a prime and comes out as ' ’ ` or °, the inch mark as " ”
            lv=re.search(r"\b([0-9Il]{1,2})\s*[’'`°]\s*([0-9OoIlqQ]{1,2})?",l)
            ft=(lv.group(1).translate(str.maketrans('Il','11')) if lv else '')
            inch=((lv.group(2) or '0').translate(str.maketrans('OoIlqQ','001100')) if lv else '')
            sur='Sur' in l or 'sur' in l
            typ=re.search(r'\b([A-G])\b\.?\s+(?:Wh|Wl|Whe|W)',l)
            # "1-85 x 1-85": the decimal point prints as a middle dot, the times sign varies
            sz=re.search(r'(\d[\d.·:\-]{0,3})\s*[xX×%>K¥\\/,\.]\s*(\d[\d.·:\-]{0,3})',l)
            # the printed plate number starts the line; OCR renders digits loosely
            pn=re.match(r'^\s*([0-9IlOoSs]{1,3})\b',l)
            num=pn.group(1).translate(str.maketrans('IlOoSs','110055')) if pn else ''
            rows.append(dict(page=pg,column=half,printed_no=num,
                size_in=(sz.group(1)+'x'+sz.group(2)).replace('·','.').replace(':','.').replace('-','.') if sz else '',
                level_ft_below_surface=('surface' if sur else (f'{ft}.{inch}' if ft else '')),
                type=typ.group(1) if typ else '', area=area, serial=serial, ocr_line=l))
print(f'rows parsed: {len(rows)}')
# use the printed number; repair it from the sequence only when it is missing or out of order
prev=0; repaired=0
for r in rows:
    n=int(r['printed_no']) if r['printed_no'].isdigit() else None
    if n is None or not (prev < n <= prev+8):
        n=prev+1; r['repaired']='yes'; repaired+=1
    else: r['repaired']=''
    r['plate_no']=n; prev=n
print(f'plate numbers: printed {sum(1 for r in rows if not r["repaired"])}, repaired {repaired}; range {rows[0]["plate_no"]}-{rows[-1]["plate_no"]}')
os.makedirs('../outputs',exist_ok=True)
hdr=['plate_no','repaired','area','serial','level_ft_below_surface','size_in','type','page','column','ocr_line']
with open('../outputs/marshall_seal_table.csv','w',newline='') as f:
    w2=csv.DictWriter(f,fieldnames=hdr,quoting=csv.QUOTE_MINIMAL); w2.writeheader()
    for r in rows: w2.writerow({k:r[k] for k in hdr})
import collections
print('by area:',collections.Counter(r['area'] for r in rows).most_common())
print('with a level:',sum(1 for r in rows if r['level_ft_below_surface']),'; with a size:',sum(1 for r in rows if r['size_in']))
print('example rows:')
for r in rows[:5]: print('  ',{k:r[k] for k in ('plate_no','area','serial','level_ft_below_surface','size_in','type')})
