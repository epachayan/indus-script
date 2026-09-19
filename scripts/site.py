import collections, numpy as np
exec(open('../scripts/motif_dedup.py').read().split("print('inscriptions'")[0])
site=[r['site'] for r in rs]; has=[('G400' in s) for s in S]
print(collections.Counter(site).most_common(8))
# motif x site counts
for st in ['Mohenjo-daro','Harappa']:
    idx=[i for i in range(len(rs)) if site[i]==st]
    c=collections.Counter(M[i] for i in idx); g=collections.Counter(M[i] for i in idx if has[i])
    print(st, len(idx), 'G400 overall %.0f%%'%(100*sum(has[i] for i in idx)/max(1,len(idx))))
    for m,n in c.most_common(): print(f'   {m:13s} {g[m]:2d}/{n:3d} {100*g[m]/n:4.0f}%')
print('other sites:',collections.Counter((site[i],M[i]) for i in range(len(rs)) if has[i] and site[i] not in ('Mohenjo-daro','Harappa')))
