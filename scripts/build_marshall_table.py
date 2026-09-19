# Merge the hand-transcribed pages of Marshall (1931) vol. II "Tabulation of Seals"
# (transcriptions/marshall1931_seal_table/*.csv) and run consistency checks.
# NB: levels are below the modern SURFACE (not Mackay's datum) and the locus is only the
# excavation area, so these are not directly comparable with outputs/mackay_seal_table.csv.
import csv, glob, collections, os, numpy as np
HDR=['plate_no','size_in','level_ft','level_in','type','material','area','serial']
rows=[]
for f in sorted(glob.glob('../transcriptions/marshall1931_seal_table/p*.csv')):
    for r in csv.reader(open(f)):
        if not r or r[0]=='plate_no': continue
        d=dict(zip(HDR,r+['']*(len(HDR)-len(r)))); d['source_page']=os.path.basename(f); rows.append(d)
nums=[int(r['plate_no']) for r in rows if r['plate_no'].isdigit()]
suffixed=[r['plate_no'] for r in rows if not r['plate_no'].isdigit()]
dups=[n for n,c in collections.Counter(nums).items() if c>1]
gaps=[n for n in range(min(nums),max(nums)+1) if n not in set(nums)]
def depth(r):
    # "Sur." = surface; "B.P." is Marshall's bathing-pavement datum, not a depth
    if r['level_ft']=='surface': return 0.0
    try: return float(r['level_ft'])+float(r['level_in'] or 0)/12
    except ValueError: return None
d=[depth(r) for r in rows]; dd=[x for x in d if x is not None]
print(f'rows {len(rows)}; plate numbers {min(nums)}-{max(nums)} (+{len(suffixed)} suffixed: {suffixed}); duplicates {dups}; missing {gaps}')
print(f'with a level: {len(dd)}; median {np.median(dd):.1f} ft below surface; range {min(dd):.1f}-{max(dd):.1f}')
print('areas:',dict(collections.Counter(r['area'] for r in rows)))
print('types:',dict(collections.Counter(r['type'] for r in rows)))
for r,x in zip(rows,d): r['depth_ft']=('' if x is None else round(x,2))
with open('../outputs/marshall_seal_table_transcribed.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=HDR+['depth_ft','source_page'],quoting=csv.QUOTE_MINIMAL)
    w.writeheader(); w.writerows(rows)
