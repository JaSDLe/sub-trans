# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5
from urllib.parse import urlencode

src_file_path = "C:/Users/jasonzli/Desktop/a.ass"
en_file_path = "C:/Users/jasonzli/Desktop/en.ass"
cn_file_path = "C:/Users/jasonzli/Desktop/cn.ass"
result_file_path = "C:/Users/jasonzli/Desktop/r.ass"

# Set your own appid/appkey.
appid = '77202003010998900390764'
appkey = '1gc77cZI1_C89DcfZ_1DbvM99Vw'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'auto'
to_lang = 'zh'
endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
salt = random.randint(32768, 65536)
max_char = 6000

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

print("begin")
begin_line = 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
begin_flag = 0
cn_en_split = '\\N{\\rEN}'

class Format:
    def __init__(self, list):
        self.Layer = list[0]
        self.Start = list[1]
        self.End = list[2]
        self.Style = list[3]
        self.Name = list[4]
        self.MarginL = list[5]
        self.MarginR = list[6]
        self.MarginV = list[7]
        self.Effect = list[8]
        self.Text = ','.join(list[9:])
        t = self.Text.split(cn_en_split)
        self.CN = t[0]
        self.EN = t[1]
        self.List = list
    def __str__(self):
        # debug
        return 'CN -> (' + self.CN + ');EN -> ('+self.EN
    def combine(self,cn,en):
        l=[]
        l.extend(self.List[0:8])
        cn=cn.replace('，',' ')
        cn=cn.replace('。',' ')
        cn=cn.replace('、',' ')
        cn=cn.replace('--','-')
        cn=cn.replace('-',' - ')
        l.append(''.join([cn,cn_en_split,en]))
        return ','.join(l) + '\n'

def trans(format_list,en):
    query = en
    # Build request
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': make_md5(appid + query + str(salt) + appkey)}
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    # Show response
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    # print('len(format_list)=',len(format_list),';len(trans_result)=',len(result['trans_result']))
    # print(format_list[0],result['trans_result'][0])
    print(format_list[len(format_list)-1],result['trans_result'][len(result['trans_result'])-1])
    l=[]
    cn=''
    t=''
    for index in range(len(result['trans_result'])):
        r=result['trans_result'][index]
        l.append(format_list[index].combine(r['dst'],r['src']))
        # t=t+r['dst']+cn_en_split+r['src']+'\n'
        cn=cn+r['dst']+'\n'
    cn_list.append(cn)
    # l.append(t)
    result_file.writelines(l)

src_file = open(src_file_path, 'r', encoding = 'utf_8_sig')
result_file = open(result_file_path, 'w', encoding = 'utf_8_sig')
try:
    lines = src_file.readlines()
    en = ''
    en_list = []
    cn_list=[]
    format_list = []
    break_flag = 0
    for line in lines:
        if begin_flag == 1:
            break_flag = break_flag + 1
            f = Format(line.split(','))
            # print(i,f)
            # print(f)
            if len(en)+len(f.EN) <= max_char:
                en = en + f.EN
                format_list.append(f)
            else:
                trans(format_list,en)
                format_list = []
                format_list.append(f)
                en_list.append(en)
                en = f.EN
            # if break_flag == 1:
            #     break
        if line == begin_line:
            begin_flag = 1
    trans(format_list,en)
    en_list.append(en)
    # print(en)
    # print(len(en))
finally:
    src_file.close()

# EN file
en_file = open(en_file_path, 'w', encoding = 'utf_8_sig')
en_file.writelines('\n\n\n'.join(en_list))
en_file.close()

# CN file
cn_file = open(cn_file_path, 'w', encoding = 'utf_8_sig')
cn_file.writelines('\n\n\n'.join(cn_list))
cn_file.close()
result_file.close()

print("end")
