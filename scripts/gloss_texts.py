# Render Mohenjo-daro texts in plain English SHAPE names (not meanings), using the visual
# families from outputs/indus_sign_tags.csv plus hand labels for the commonest signs.
import csv, collections
tags={r['sign']:r for r in csv.DictReader(open('../outputs/indus_sign_tags.csv'))}
NAME={ # hand labels for the commonest signs, from the rendered glyphs
 'G740':'JAR','G741':'jar-variant','G742':'jar-variant-2','G760':'stacked-jar','G520':'ARROW',
 'G220':'fish','G231':'fish-with-line','G235':'fish-with-roof','G240':'fish-crossed',
 'G2':'two-strokes','G1':'one-stroke','G3':'three-strokes','G32':'two-long-strokes',
 'G33':'three-long-strokes','G16':'six-strokes','G17':'seven-strokes',
 'G820':'circled-cross','G817':'circled-cross-2','G861':'diamond','G692':'lens',
 'G390':'forked-stem','G391':'forked-stem-2','G405':'forked-stem-3','G407':'forked-stem-4',
 'G176':'comb','G100':'cup','G90':'closing-stroke','G400':'double-hook','G60':'joined-strokes',
 'G233':'fish-plain','G705':'U-vessel','G706':'U-vessel-2','G803':'grid','G920':'man-figure',
 'G151':'jar-like-ending','G550':'crossed-oval','G927':'plant'}
def gloss(s):
    if s in NAME: return NAME[s]
    f=tags.get(s,{}).get('family','')
    return (f.replace('/',' or ') if f and f!='(mixed)' else s)
rows=[r for r in csv.DictReader(open('../outputs/inscriptions_ml.csv'))
      if r['site']=='Mohenjo-daro' and r['signs_reading_order']]
c=collections.Counter(r['signs_reading_order'] for r in rows)
print('The 15 commonest Mohenjo-daro texts, read right to left as the script runs:\n')
for t,n in c.most_common(15):
    sg=t.split()
    print(f'  x{n:<3d} {" | ".join(gloss(s) for s in sg)}')
print('\nThe same texts as they appear on the object, left to right:\n')
for t,n in c.most_common(6):
    sg=t.split()[::-1]
    print(f'  x{n:<3d} {" | ".join(gloss(s) for s in sg)}')
print('\nA few longer texts:\n')
longer=[t for t in c if len(t.split())>=8]
for t in longer[:6]:
    print(f'  {" | ".join(gloss(s) for s in t.split())}')
