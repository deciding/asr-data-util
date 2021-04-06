import string
import sys
from cn_convert import cn_convert
en_punc=string.punctuation
cn_punc="！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
with open('text.txt', 'w') as outf:
    with open(sys.argv[1]) as f:
        for line in f.readlines()[1:]:
            line=line.strip()
            if line=='':
                continue
            iid, text=line.split(',', 1)
            try:
                newiid='zhaoli%04d%03d' % (int(iid.split('-')[0]), int(iid.split('-')[1]))
            except:
                import pdb;pdb.set_trace()
                print(iid)
            for c in en_punc:
                text=text.replace(c, '')
            for c in cn_punc:
                text=text.replace(c, '')
            text=cn_convert(text)
            outf.write(f'{newiid} {text}\n')
