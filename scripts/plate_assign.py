# Attach manually read label numbers to the detected photo boxes.
# Usage: python3 plate_assign.py <plate.jpg> <dir> <readings.json>
#   readings.json: {"<label index>": <seal number>, ...} from labels_grid.png
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
from scipy.optimize import linear_sum_assignment
src,d,rj=sys.argv[1],sys.argv[2],sys.argv[3]
labs=json.load(open(f'{d}/labels.json')); read={int(k):v for k,v in json.load(open(rj)).items()}
im=Image.open(src).convert('L'); a=np.array(im); paper=np.percentile(a,80)
m=ndimage.binary_opening(ndimage.binary_closing(a<paper-28,np.ones((11,11))),np.ones((7,7)))
lab,_=ndimage.label(m); boxes=[]
for sl in ndimage.find_objects(lab):
    y0,y1,x0,x1=sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
    if (x1-x0)>120 and (y1-y0)>90 and (x1-x0)*(y1-y0)>30000 and (x1-x0)<a.shape[1]*0.9: boxes.append([int(x0),int(y0),int(x1),int(y1)])
items=[(read[i],labs[i]) for i in read if i<len(labs)]
BIG=1e6; C=np.full((len(boxes),len(items)),BIG)
for i,(x0,y0,x1,y1) in enumerate(boxes):
    for j,(no,lb) in enumerate(items):
        cx,cy=(lb[0]+lb[2])//2,(lb[1]+lb[3])//2
        dx=0 if x0-70<=cx<=x1+70 else min(abs(cx-x0),abs(cx-x1))
        dy=(cy-y1) if cy>y1 else (y0-cy)*2.5
        if dx>360 or dy>320 or dy<-40: continue
        C[i,j]=dx+max(dy,0)*1.2
ri,ci=linear_sum_assignment(C)
out=[]
for i,j in zip(ri,ci):
    if C[i,j]<BIG: out.append(dict(no=items[j][0],box=boxes[i]))
json.dump(out,open(f'{d}/assigned.json','w'))
print(f'boxes {len(boxes)}, labels read {len(items)}, assigned {len(out)}')
print('numbers:',sorted(o["no"] for o in out))
