import re
english_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

chinese_pattern = re.compile(u'[\u4e00-\u9fff]')
_decimal_number_re = re.compile(r'([0-9]+\.[0-9]+)')
_number_re = re.compile(r'(?<!#)[0-9]+')
_comma_number_re = re.compile(r'(?<!#)([0-9][0-9\,]+[0-9])')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Licensed under WTFPL or the Unlicense or CC0.
# This uses Python 3, but it's easy to port to Python 2 by changing
# strings to u'xx'.

import itertools

def num2cn(num, big=False, simp=True, o=False, twoalt=False):
    """
    Converts numbers to Chinese representations.

    `big`   : use financial characters.
    `simp`  : use simplified characters instead of traditional characters.
    `o`     : use 〇 for zero.
    `twoalt`: use 两/兩 for two when appropriate.

    Note that `o` and `twoalt` is ignored when `big` is used, 
    and `twoalt` is ignored when `o` is used for formal representations.
    """
    # check num first
    nd = str(num)
    if abs(float(nd)) >= 1e48:
        raise ValueError('number out of range')
    elif 'e' in nd:
        raise ValueError('scientific notation is not supported')
    c_symbol = '正负点' if simp else '正負點'
    if o:  # formal
        twoalt = False
    if big:
        c_basic = '零壹贰叁肆伍陆柒捌玖' if simp else '零壹貳參肆伍陸柒捌玖'
        c_unit1 = '拾佰仟'
        c_twoalt = '贰' if simp else '貳'
    else:
        c_basic = '〇一二三四五六七八九' if o else '零一二三四五六七八九'
        c_unit1 = '十百千'
        if twoalt:
            c_twoalt = '两' if simp else '兩'
        else:
            c_twoalt = '二'
    c_unit2 = '万亿兆京垓秭穰沟涧正载' if simp else '萬億兆京垓秭穰溝澗正載'
    revuniq = lambda l: ''.join(k for k, g in itertools.groupby(reversed(l)))
    nd = str(num)
    result = []
    if nd[0] == '+':
        result.append(c_symbol[0])
    elif nd[0] == '-':
        result.append(c_symbol[1])
    if '.' in nd:
        integer, remainder = nd.lstrip('+-').split('.')
    else:
        integer, remainder = nd.lstrip('+-'), None
    if int(integer):
        splitted = [integer[max(i - 4, 0):i]
                    for i in range(len(integer), 0, -4)]
        intresult = []
        for nu, unit in enumerate(splitted):
            # special cases
            if int(unit) == 0:  # 0000
                intresult.append(c_basic[0])
                continue
            elif nu > 0 and int(unit) == 2:  # 0002
                intresult.append(c_twoalt + c_unit2[nu - 1])
                continue
            ulist = []
            unit = unit.zfill(4)
            for nc, ch in enumerate(reversed(unit)):
                if ch == '0':
                    if ulist:  # ???0
                        ulist.append(c_basic[0])
                elif nc == 0:
                    ulist.append(c_basic[int(ch)])
                elif nc == 1 and ch == '1' and unit[1] == '0':
                    # special case for tens
                    # edit the 'elif' if you don't like
                    # 十四, 三千零十四, 三千三百一十四
                    ulist.append(c_unit1[0])
                elif nc > 1 and ch == '2':
                    ulist.append(c_twoalt + c_unit1[nc - 1])
                else:
                    ulist.append(c_basic[int(ch)] + c_unit1[nc - 1])
            ustr = revuniq(ulist)
            if nu == 0:
                intresult.append(ustr)
            else:
                intresult.append(ustr + c_unit2[nu - 1])
        result.append(revuniq(intresult).strip(c_basic[0]))
    else:
        result.append(c_basic[0])
    if remainder:
        result.append(c_symbol[2])
        result.append(''.join(c_basic[int(ch)] for ch in remainder))
    return ''.join(result)

def _expand_decimal_point(m):
    return m.group(1).replace('.', '点')

def _expand_number(m):
    num = int(m.group(0))
    return num2cn(num)

def _remove_commas(m):
    return m.group(1).replace(',', '')

def normalize_numbers(text):
    text = re.sub(_comma_number_re, _remove_commas, text)
    text = re.sub(_decimal_number_re, _expand_decimal_point, text)
    text = re.sub(_number_re, _expand_number, text)
    return text


def char_is_chinese(c):
    return chinese_pattern.match(c)


def split_chinese_english(text):
    splitted_arr = []
    cnt = 0
    prev_cn = True
    start_cnt = 0
    for c in text:
        cur_cn = char_is_chinese(c)
        if cur_cn and not prev_cn:
            splitted_arr.append(text[start_cnt:cnt])
            start_cnt = cnt
        elif not cur_cn and prev_cn and cnt:
            splitted_arr.append(text[start_cnt:cnt])
            start_cnt = cnt
        prev_cn = cur_cn
        cnt += 1
    splitted_arr.append(text[start_cnt:cnt])
    return splitted_arr


def contains_chinese(text):
    return len(re.findall(u'[\u4e00-\u9fff]+', text)) > 0


def substr2cn(s):
    # special cases considered:
    # 1. dot
    # 3. %
    # 4. nian
    # 8. date
    # 2. @#&%*/-+=<>
    # 5. seperate english
    # 5. replace english to latin
    # 7. replace chinese symbol
    # 6. de5
    res_prefix = ''
    res_suffix = ''
    num_as_year = False
    #decimal_digits = 0
    if s[-1] == '%':
        res_prefix = '百分之'
        s = s[:-1]
    if s[-1] == '年':
        res_suffix = '年'
        num_as_year = True
        s = s[:-1]

    if '.' in s:
        int_dec = s.split('.')
        if len(int_dec) == 2:
            int_part = int_dec[0]
            dec_part = int_dec[1]
            s = num2cn(int(int_part))+'点'+str2cn1by1(dec_part)
        elif len(int_dec) == 3:
            s = str2cn1by1(int_dec[0])+'点' + \
                str2cn1by1(int_dec[1])+'点'+str2cn1by1(int_dec[2])
    elif num_as_year:
        s = str2cn1by1(s)
    else:
        s = num2cn(int(s))
    return res_prefix+s+res_suffix


def str2cn1by1(s):
    res = ''
    for i in s:
        res += num2cn(int(i))
    return res


def symbol2cn(s):
    s = s.replace('@', '艾特')
    #s = s.replace('#', '井')
    #s = s.replace('%', '百分号')
    s = s.replace('+', '加')
    s = s.replace('=', '等于')
    return s


def is_ascii(s):
    return all(ord(c) < 128 for c in s) or '£' in s


def is_english(s):
    return s in (english_chars + ' ')

# TODO: check whether the start space is needed


def sep_english(s):
    # not needed function
    return s
    res = ''
    for i in range(0, len(s)):
        if i != len(s)-1:
            if is_english(s[i]) and not is_english(s[i+1]) or not is_english(s[i]) and is_english(s[i+1]):
                res += (s[i]+' ')
            else:
                res += s[i]
    res += s[-1]
    return res


def replace_punc(text):
    return text.translate(text.maketrans("，。？：；！‘’“”、（）《》\"—…", ",.?:;!\'\'\'\',()\'\'\',."))

def process_num(match):
    s = match.group()
    return substr2cn(s)


def cn_convert(s):
    # num2cn
    s = re.sub(_comma_number_re, _remove_commas, s)
    s = re.sub('(?<!#)\d+\.?\d*[%年]?', process_num, s)

    return replace_punc(symbol2cn(normalize_numbers(s)))
