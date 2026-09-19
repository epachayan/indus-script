# Candidate finder for matching a photographed Mackay seal to a CISI text.
# Usage: python3 plate_candidates.py <mackay_no> <n_signs> [tol_mm]
# Filters CISI Mohenjo-daro texts by seal size (calibrated) and sign count, and renders
# each candidate's signs to work/cand_<no>.png for visual comparison with the plate.
import sys, re, csv, json, numpy as np
from PIL import Image, ImageDraw
no=sys.argv[1]; nsign=int(sys.argv[2]); tol=float(sys.argv[3]) if len(sys.argv)>3 else 1.5
SCALE,OFF=1.015,-0.5      # calibration from match_feasibility.py
row=[r for r in csv.DictReader(open('../outputs/mackay_seal_table.csv')) if r['no']==no][0]
m=re.match(r'([\d.]+)x([\d.]+)',row['dims_in'])
W,H=(float(m.group(1))*25.4*SCALE+OFF,float(m.group(2))*25.4*SCALE+OFF) if m else (None,None)
print(f"Mackay {no}: type {row['type']}, {row['dims_in']} in -> {W:.1f} x {H:.1f} mm, level {row['level_ft']} ft, {row['area']}")
sql=open('../data/indus-website/population-script.sql',encoding='utf8').read()
b=sql[sql.index('INSERT INTO SEAL ('):]; b=b[:b.index(');\n')+1]
size={}
for _,typ,mat,c,_,w,h in re.findall(r'\((\d+),\s*"([^"]*)",\s*"([^"]*)",\s*"([^"]*)",\s*"?([^,"]*)"?,\s*([\d.]+),\s*([\d.]+)',b):
    if float(w)>0: size[c.strip().upper().replace(' ','')]=(float(w),float(h),typ,mat)
texts={r['cisi'].upper().replace(' ',''):r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv')) if r['site']=='Mohenjo-daro'}
cand=[]
for cid,r in texts.items():
    t=r['signs_reading_order'].split()
    if len(t)!=nsign: continue
    s=size.get(cid)
    ok_size = s is None or W is None or (abs(s[0]-W)<=tol and abs(s[1]-H)<=tol)
    if ok_size: cand.append((cid,t,s))
print(f'candidates with {nsign} signs and size within +/-{tol} mm: {len(cand)}')
im=np.load('imgs.npy'); ids=json.load(open('tags.json'))['ids']; ix={f'G{g}':i for i,g in enumerate(ids)}
rowh=64; sheet=Image.new('L',(210+nsign*58,max(1,len(cand))*rowh+10),255); d=ImageDraw.Draw(sheet)
for i,(cid,t,s) in enumerate(cand):
    d.text((6,i*rowh+18),f'{cid}',fill=0)
    d.text((6,i*rowh+32),(f'{s[0]:.1f}x{s[1]:.1f}mm' if s else 'no size'),fill=90)
    for j,g in enumerate(t[::-1]):                # drawn left-to-right as the impression looks
        if g in ix: sheet.paste(Image.fromarray(255-(im[ix[g]]*255).astype(np.uint8)).resize((46,46)),(210+j*58,i*rowh+6))
        d.text((212+j*58,i*rowh+52),g,fill=60)
sheet.save(f'cand_{no}.png')
for cid,t,s in cand[:12]: print(' ',cid,' '.join(t),(f'{s[0]:.1f}x{s[1]:.1f}' if s else ''))
