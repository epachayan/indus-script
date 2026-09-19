# One tidy row per inscription, ready for pandas / ML. Signs in READING order (right to left).
import csv, json
exec(open('../scripts/objtype.py').read().split("exec(open('../scripts/motif_dedup.py')")[0])
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
def kind(r):
    o,m=bycisi.get(r['cisi_number'],([],'')); return ('TAB' if 'TAB' in o else 'SEAL' if 'SEAL' in o else 'TAG' if 'TAG' in o else 'unknown'), m or 'unknown'
rows=list(csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')))
seen=set(); out=[]
for r in rows:
    t=r['sign_sequence'].split()[::-1]; ok=[s for s in t if s in tags]
    ob,mat=kind(r)
    out.append(dict(inscription_id=r['inscription_id'],cisi=r['cisi_number'],site=r['site'],object_type=ob,material=mat,
        motif=r['motif'],motif_group=('unicorn' if r['motif'].startswith('Bull1') else r['motif']),
        n_signs=len(ok),signs_reading_order=' '.join(ok),
        families=' | '.join(tags[s]['family'] for s in ok),
        behaviour=' | '.join(tags[s]['behaviour_class'] or 'rare' for s in ok),
        first_occurrence=r['sign_sequence'] not in seen))
    seen.add(r['sign_sequence'])
with open('../outputs/inscriptions_ml.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=out[0].keys()); w.writeheader(); w.writerows(out)
print(len(out),'rows;',sum(o['first_occurrence'] for o in out),'distinct texts')
