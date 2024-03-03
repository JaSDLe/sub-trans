# -*- coding: utf-8 -*-

import opencc
import os
import re

converter = opencc.OpenCC('t2s.json')

skip_regex = r'[0-9:,-> \n]+'

input_prompt = '''Please input the file you want to convert.
    e.g. 'C:\\test.srt'
> Enter a value: '''
# OJC means 'Converted by Jason with OpenCC' backwards
result_file_suffix = '.CHS.[OJC]'

print('begin\n')

try:
    src_file_path = input(input_prompt)
    if os.path.isfile(src_file_path):
        src_file_tuple = os.path.split(src_file_path)
        src_dir = src_file_tuple[0]
        file = src_file_tuple[1]
        fn = file.split('.')
        file_suffix = '.' + fn[len(fn) - 1]
        file_name = file.removesuffix(file_suffix)
        result_file_path = os.path.join(
            src_dir, file_name + result_file_suffix + file_suffix)
        # open file
        src_file = open(src_file_path, 'r', encoding='utf_8_sig')
        result_file = open(result_file_path, 'w', encoding='utf_8_sig')
        print('\nconverting...')
        try:
            lines = src_file.readlines()
            for line in lines:
                if not re.fullmatch(skip_regex, line):
                    line = converter.convert(line)
                result_file.write(line)
        finally:
            src_file.close()
            result_file.close()
            print('success!')
    else:
        print('\nERROR: not a valid path or file not exist')
except Exception as e:
    print('\nexception: {}'.format(repr(e)))

print('\nend')
