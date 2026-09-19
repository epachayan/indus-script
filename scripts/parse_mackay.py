# Extract seal find-spots from the OCR text of Mackay (1938), Further Excavations at
# Mohenjo-daro, vol. I. Output: outputs/findspots_mackay.csv (one row per seal mention).
# Usage: python3 parse_mackay.py [input.txt] [output.csv]
import re, sys, csv
src=sys.argv[1] if len(sys.argv)>1 else '../data/mackay1938_vol1.txt'
out=sys.argv[2] if len(sys.argv)>2 else '../outputs/findspots_mackay.csv'
txt=open(src,encoding='utf8',errors='replace').read()
txt=re.sub(r'\s+',' ',txt).replace('–','-').replace('—','-')
# Mackay's DK-area average levels (ft below datum) for door-sills/pavements, per phase
PHASES=[(-6.0,'Late I'),(-8.5,'Late II'),(-11.5,'Late III'),(-14.5,'Intermediate I'),
        (-18.0,'Intermediate II'),(-22.0,'Intermediate III'),(-99,'Early')]
SD_OFFSET=2.2   # SD bench mark is 2.2 ft above the DK datum
def phase(level_dk):
    for lim,name in PHASES:
        if level_dk>lim: return name
    return 'Early'
# context trackers: area from chapter headings, block from "Block N" headings
events=[]
for m in re.finditer(r'CHAPTER [IVXL]+ ?\.? ?([A-Z][A-Z ]*?AREA)',txt): events.append((m.start(),'area',m.group(1).split()[0]))
for m in re.finditer(r'\bBlocks? (\d+[A-Z]?)(?: and \d+[A-Z]?)? \( ?Pls?\b',txt): events.append((m.start(),'block',m.group(1)))   # section headings only
for m in re.finditer(r'\b((?:[A-Z][a-z]+ ){1,2}(?:Street|Lane))s? \( ?Pls?\b',txt): events.append((m.start(),'block',m.group(1)))   # street sections
events.sort()
SEAL=re.compile(r'\bseals?,? (?:No\s?[.:]\s?)?(\d{1,4})\b|\bNo\s?\.\s?(\d{1,4})(?= at (?:the level )?[+-]?\s?\d)',re.I)
# the printed decimal point is a middle dot, which OCR renders as "." or "-": -1-1 ft = -1.1 ft
LEVEL=re.compile(r'(?:level|at)\s*([+-])?\s?(\d+(?:\s?[.·\-]\s?\d+)?)\s?ft\s?\.?(\s?\.?\s?(below|above)\s+datum)?',re.I)
FIELD=re.compile(r'\b(SD|DK|VS|HR|L|DM|C)\s?(\d{3,5})\b')
rows=[]
for m in SEAL.finditer(txt):
    no=m.group(1) or m.group(2)
    win=txt[m.end():m.end()+160]
    nxt=SEAL.search(win)
    if nxt: win=win[:nxt.start()]           # do not borrow the next seal's level
    lv=LEVEL.search(win); fd=FIELD.search(txt[m.end():m.end()+40])
    area=block=None
    for pos,kind,val in events:
        if pos>m.start(): break
        if kind=='area': area=val; block=None
        else: block=val
    level=None; ph=None
    if lv:
        val=float(re.sub(r'\s','',lv.group(2)).replace('·','.').replace('-','.'))
        sign=-1 if (lv.group(1)=='-' or (lv.group(4) or '').lower()=='below') else 1
        level=sign*val
        dk=level+(SD_OFFSET if (fd and fd.group(1)=='SD') or area=='SD' else 0)
        ph=phase(dk)
    rows.append(dict(mackay_no=int(no),field_no=(fd.group(1)+' '+fd.group(2)) if fd else '',
        area=(fd.group(1) if fd else area) or '',block=block or '',level_ft=level if level is not None else '',
        phase_estimate=ph or '',context=txt[max(0,m.start()-60):m.end()+100].strip()))
seen=set(); uniq=[]
for r in rows:
    k=(r['mackay_no'],r['level_ft'])
    if k not in seen: seen.add(k); uniq.append(r)
with open(out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(uniq[0].keys())); w.writeheader(); w.writerows(uniq)
print(f'seal mentions: {len(rows)}; unique (number, level): {len(uniq)}; with level: {sum(r["level_ft"]!="" for r in uniq)}; with field no: {sum(bool(r["field_no"]) for r in uniq)}')
