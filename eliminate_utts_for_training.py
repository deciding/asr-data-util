import sys
import re
import os
from enum import Enum
import string
#from tqdm import tqdm
# eliminate shape, or just at the begining the utt.list
EngElim = Enum('EngElim', 'all any')

eliminate_shape=False
engelim=EngElim.all

badutt=[]
badspk=[]

def contains_english(line):
    line=line.strip()
    return any(c in string.ascii_letters for c in line)

def contains_chinese(line):
    line=line.strip()
    return re.findall(r'[\u4e00-\u9fff]+', line)

if os.path.exists('badutt.txt'):
    with open('badutt.txt') as f:
        for line in f:
            line=line.strip()
            badutt.append(line)

if os.path.exists('badspk.txt'):
    with open('badspk.txt') as f:
        for line in f:
            line=line.strip()
            badspk.append(line)

if eliminate_shape:
    shapefile1='exp/asr_stats_raw_zh_char_sp/train/speech_shape'
    shapefile2='exp/asr_stats_raw_zh_char_sp/valid/speech_shape'
    shapefile3='exp/asr_stats_raw_zh_char_sp/train/text_shape.char'
    shapefile4='exp/asr_stats_raw_zh_char_sp/valid/text_shape.char'
    text_file=''
    #shapefiles=[shapefile1, shapefile2, shapefile3, shapefile4]
    target_files=[shapefile3, shapefile4]
else:
    uttlist1='/workspace/espnet/egs2/aishell/asr1/data_zhaoli/local/test/utt.list'
    target_files=[uttlist1]
    text_file='/workspace/espnet/egs2/aishell/asr1/data_zhaoli/test/text'

def bad_line(line):
    for utt in badutt:
        if utt in line:
            return True
    for spk in badspk:
        if spk in line:
            return True
    return False

def eliminate_english(line):
    if engelim == EngElim.all:
        return not contains_chinese(line)
    else:
        return any([l.isalpha() for l in line])

text_d={}
with open(text_file) as f:
    lines=f.readlines()
    l=len(lines)
    for idx, line in enumerate(lines):
        print('DICT PROGRESS: %.2f percent' % ((idx+1)/l*100), file=sys.stderr)
        iid, text=line.split()
        text_d[iid]=text

cnt=0
for sf in target_files:
    with open(sf) as f:
        with open(f'{sf}_new', 'w') as outf:
            lines=f.readlines()
            l=len(lines)
            for idx, line in enumerate(lines):
                print('PROGRESS: %.2f percent' % ((idx+1)/l*100), file=sys.stderr)
                if bad_line(line):
                    cnt+=1
                elif eliminate_english(text_d[line.strip()]):
                    cnt+=1
                else:
                    outf.write(line)
    print(f'{cnt} eliminated')
    cnt=0

