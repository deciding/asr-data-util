#from tqdm import tqdm
import sys
from pathlib import Path

print_size=True

# text
infile=sys.argv[1]
# wav.scp
infile2=sys.argv[2]
# sort on ratio or abs size
#outfile=sys.argv[2]

fac=3
cn2en=6
d={}

#with open('utt2textcnt') as f:
with open(infile) as f:
    for line in f:
        line=line.strip()
        if line=='':
            continue
        iid, text=line.split()
        d[iid]=text

def get_len(s):
    cnt=0
    for c in s:
        if c.isalpha():
            cnt+=1
        else:
            cnt+=cn2en
    return cnt

bad_ratio=[]
bad_abs=[]
#with open('utt2wavsize') as f:
with open(infile2) as f:
    lines=f.readlines()
    l=len(lines)
    for idx, line in enumerate(lines):
        print('PROGRESS: %.2f percent' % ((idx+1)/l*100), file=sys.stderr)
        line=line.strip()
        if line=='':
            continue

        #iid, size=line.split()
        iid, path=line.split()
        size=Path(path).stat().st_size
        #import pdb;pdb.set_trace()

        #if not size.endswith('K'):
        #    print('large file', line)
        #    continue
        #size=float(size[:-1])

        if not iid in d:
            print('not found', line)
            continue
        text=d[iid]
        #if get_len(text)*fac>size:
        #TODO
        rate=size/get_len(text)
        bad_ratio.append((iid, text, rate))
        bad_abs.append((iid, text, size))

bad_ratio.sort(key=lambda x: x[2])
bad_abs.sort(key=lambda x: x[2])
for (iid, text, rate), (iid2, text2, size) in zip(bad_ratio, bad_abs):
    if print_size:
        print(iid2, size, text)
    else:
        print(iid, text, iid2, text2)
