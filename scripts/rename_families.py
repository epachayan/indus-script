import json, csv
rf={int(k):tuple(v) for k,v in json.load(open("refine.json")).items()}
NAMES={(1,0):"comb/frame + strokes (mixed)",(1,1):"quadruped animal",(5,0):"marked stroke numeral",(5,1):"stem/half-disc (small set)",
(5,2):"bird-like figure",(5,3):"anthropomorph (rare)",(24,0):"line groups/fringed (mixed)",(24,1):"bird",(34,0):"creature (insect/animal)",
(34,1):"angular/zigzag (mixed)",(34,2):"hatched creature",(14,0):"bracketed composite (mixed)",(14,1):"bracketed figure"}
p="../outputs/indus_sign_tags.csv"; rows=list(csv.DictReader(open(p)))
for r in rows:
    k=rf.get(int(r["sign"][1:]))
    if k: r["family"]=NAMES[k]
with open(p,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print("families renamed; still mixed:",sum("(mixed)" in r["family"] for r in rows))
