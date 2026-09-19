# Merge the hand-transcribed pages of Mackay (1938) "Tabulation of Seals" into one CSV
# and run consistency checks. Transcriptions: transcriptions/mackay1938_seal_table/pNN.csv (first file has the header).
import csv, glob, re, collections
HDR=['no','type','dims_in','material','block','house','room','street','level_ft','field_no','pdf_page']
OUT=HDR+['area','level_dk_ft','phase_estimate']
files=sorted(glob.glob('../transcriptions/mackay1938_seal_table/p*.csv'))
rows=[]
for f in files:
    for r in csv.reader(open(f)):
        if not r or r[0]=='no': continue
        rows.append(dict(zip(HDR,r)))
main=[r for r in rows if r['no'].isdigit()]          # 378A-D etc. are addenda repeating earlier seals
addenda=[r['no'] for r in rows if not r['no'].isdigit()]
nums=[int(r['no']) for r in main]
dups=[n for n,c in collections.Counter(nums).items() if c>1]
gaps=[n for n in range(1,max(nums)+1) if n not in set(nums)]
out_of_order=[b for a,b in zip(nums,nums[1:]) if b<=a]
def lv(r):
    try: return float(r['level_ft'])
    except ValueError: return None
jumps=[]
for a,b in zip(main,main[1:]):
    la,lb=lv(a),lv(b)
    if la is not None and lb is not None and abs(la-lb)>1.0 and a['field_no'][:2]==b['field_no'][:2]: jumps.append((a['no'],la,b['no'],lb))
fields=collections.Counter(r['field_no'] for r in main); dupf=[k for k,v in fields.items() if v>1]
print(f'rows {len(rows)} ({len(addenda)} addenda: {addenda}), numbers 1-{max(nums)}; not in table: {gaps}')
print(f'duplicate numbers {dups}; out of order {out_of_order}; level jumps >1 ft {jumps}')
print(f'field numbers used twice (check against scan): {dupf}')
# derived: excavation area, level on the DK datum (SD bench mark is 2.2 ft higher), phase estimate
PHASES=[(-6.0,'Late I'),(-8.5,'Late II'),(-11.5,'Late III'),(-14.5,'Intermediate I'),(-18.0,'Intermediate II'),(-22.0,'Intermediate III')]
for r in rows:
    r['area']=r['field_no'].split()[0].replace('DK.H.','DK-H') if r['field_no'] else ''
    l=lv(r)
    if l is None: r['level_dk_ft']=''; r['phase_estimate']='surface' if r['level_ft']=='surface' else ''; continue
    d=l+(2.2 if r['area']=='SD' else 0); r['level_dk_ft']=round(d,1)
    r['phase_estimate']=next((n for lim,n in PHASES if d>lim),'Early')
with open('../outputs/mackay_seal_table.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=OUT); w.writeheader(); w.writerows(rows)
print('areas:',dict(collections.Counter(r['area'] for r in rows)))
print('phases:',dict(collections.Counter(r['phase_estimate'] for r in rows)))
print('materials printed:',dict(collections.Counter(r['material'] for r in rows)))
print('types:',dict(collections.Counter(r['type'] for r in rows)))
