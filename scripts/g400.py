import csv, collections
rows=list(csv.DictReader(open('../data/indus_decipher/data/indus_website_real_corpus.csv')))
exec(open('../scripts/objtype.py').read().split("exec(open('../scripts/motif_dedup.py')")[0])
def kind(r):
    o,_=bycisi.get(r['cisi_number'],([],'?')); return 'TAB' if 'TAB' in o else 'SEAL' if 'SEAL' in o else '?'
tab=[r for r in rows if r['site']=='Harappa' and kind(r)=='TAB']
seqs=[r['sign_sequence'].split()[::-1] for r in tab]
g=[s for s in seqs if 'G400' in s]
print('Harappa tablets',len(tab),'(incl duplicates) with G400:',len(g),'distinct texts:',len(set(map(tuple,g))))
print('G400 position:',collections.Counter(('final' if s.index('G400')==len(s)-1 else 'initial' if s.index('G400')==0 else 'medial') for s in g))
print('lengths:',collections.Counter(len(s) for s in g))
prev=collections.Counter(s[s.index('G400')-1] for s in g if s.index('G400')>0)
print('sign before G400:',prev.most_common(8))
print('most common full texts:')
for t,n in collections.Counter(' '.join(s) for s in g).most_common(12): print(f'   {n:3d}x  {t}')
motifs=collections.Counter(r['motif'] for r in tab if 'G400' in r['sign_sequence'].split())
print('motifs on G400 tablets:',motifs.most_common(8))
alltab=collections.Counter(r['motif'] for r in tab); print('motifs on all Harappa tablets:',alltab.most_common(8))
