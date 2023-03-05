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
import os
import re

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

begin_line = 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
max_char = 6000
total_char = 0
file_char = 0
cn_en_split = '\\N{\\rEN}'
style_regex = '{.*?}'
proceed_flags = ['yes', 'y', 'Y', 'YES']
input_prompt = '''Do you want to continue?
    'y/Y/yes/YES' will be accepted to approve.
> Enter a value: '''
file_suffix = '.ass'
cn_file_suffix = '-CN' + file_suffix
result_file_suffix = '-CN&EN' + file_suffix


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
        if self.Text.__contains__(cn_en_split):
            t = self.Text.split(cn_en_split)
            self.CN = t[0]
            self.EN = t[1]
        else:
            self.CN = ''
            self.EN = self.Text
        self.List = list

    def __str__(self):
        # debug
        return 'CN -> (' + self.CN + ');EN -> (' + self.EN

    def combine(self, cn, en):
        l = []
        l.extend(self.List[0:9])
        cn = cn.replace('，', ' ')
        cn = cn.replace('。', ' ')
        cn = cn.replace('、', ' ')
        cn = cn.replace('--', '-')
        cn = cn.replace('-', ' - ')
        cn = cn.replace('｛', '{')
        cn = cn.replace('｝', '}')
        l.append(''.join([cn, cn_en_split, en]))
        return ','.join(l) + '\n'

    def combine_new(self, cn):
        l = []
        l.extend(self.List[0:9])
        cn = cn.replace('，', ' ')
        cn = cn.replace('。', ' ')
        cn = cn.replace('、', ' ')
        cn = cn.replace('--', '-')
        cn = cn.replace('-', ' - ')
        cn = cn.replace('｛', '{')
        cn = cn.replace('｝', '}')
        l.append(''.join([cn, cn_en_split, self.EN]))
        return ','.join(l)


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def trans(format_list, en, file):
    query = re.sub(style_regex, '', en)
    # Build request
    payload = {
        'appid': appid,
        'q': query,
        'from': from_lang,
        'to': to_lang,
        'salt': salt,
        'sign': make_md5(appid + query + str(salt) + appkey)
    }
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    # Show response
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    q_len = len(query)
    print('len(format_list)={}; len(trans_result)={}; len(query_char)={}'.format(len(format_list), len(result['trans_result']), q_len))
    global file_char
    file_char += q_len
    # print(format_list[0],result['trans_result'][0])
    # print(format_list[len(format_list) - 1], result['trans_result'][len(result['trans_result']) - 1])
    l = []
    cn = ''
    t = ''
    for index in range(len(result['trans_result'])):
        r = result['trans_result'][index]
        l.append(format_list[index].combine_new(r['dst']))
        # t=t+r['dst']+cn_en_split+r['src']+'\n'
        cn = cn + r['dst'] + '\n'
    cn_list.append(cn)
    # l.append(t)
    file.writelines(l)


print('begin\n')

cwd = os.getcwd()
src_dir = input('dir to scan ' + file_suffix + ' file [' + cwd + ']:')
if len(src_dir.strip()) == 0:
    src_dir = cwd
try:
    os.chdir(src_dir)
    print()
    file_list = []
    for file in os.listdir(src_dir):
        if file.endswith(file_suffix):
            file_list.append(file)
            print(file)
    print('\nTotal ' + file_suffix + ' files:', len(file_list), '\n')
    is_proceed = input(input_prompt)
    if is_proceed in proceed_flags:
        for file in file_list:
            file_char = 0
            print('\ntranslating [' + file + ']...')
            src_file_path = os.path.join(src_dir, file)
            file_name = file.removesuffix(file_suffix)
            result_file_path = os.path.join(src_dir,
                                            file_name + result_file_suffix)
            # open file
            src_file = open(src_file_path, 'r', encoding='utf_8_sig')
            result_file = open(result_file_path, 'w', encoding='utf_8_sig')
            try:
                lines = src_file.readlines()
                en = ''
                en_list = []
                cn_list = []
                format_list = []
                head_line_list = []
                begin_flag = 0
                break_flag = 0
                for line in lines:
                    if begin_flag == 1:
                        if line == '\n':
                            continue
                        break_flag = break_flag + 1
                        f = Format(line.split(','))
                        # print(i,f)
                        # print(f)
                        if len(en) + len(f.EN) <= max_char:
                            en = en + f.EN
                            format_list.append(f)
                        else:
                            trans(format_list, en, result_file)
                            format_list = []
                            format_list.append(f)
                            en_list.append(en)
                            en = f.EN
                        # if break_flag == 1:
                        #     break
                    else:
                        head_line_list.append(line)
                    if line == begin_line:
                        begin_flag = 1
                        result_file.writelines(head_line_list)
                trans(format_list, en, result_file)
                en_list.append(en)
                # print(en)
                # print(len(en))
            finally:
                print('this file translated char: ', file_char)
                total_char = total_char + file_char
                src_file.close()
                result_file.close()

            # EN file
            # en_file = open(en_file_path, 'w', encoding = 'utf_8_sig')
            # en_file.writelines('\n\n\n'.join(en_list))
            # en_file.close()

            # CN file
            # cn_file = open(cn_file_path, 'w', encoding = 'utf_8_sig')
            # cn_file.writelines('\n\n\n'.join(cn_list))
            # cn_file.close()
except Exception as e:
    print('\nexception: {}'.format(repr(e)))

print('\ntotal translated char: ', total_char)
print('\nend')
