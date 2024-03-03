# -*- coding: utf-8 -*-

import os

input_prompt = '''\nPlease input the {} file you want to concat.
    e.g. 'C:\\test.ass'
> Enter a value: '''
# JC means 'Concatenated by Jason' backwards
result_file_suffix = '.CN&EN.[JC]'
begin_line = 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
default_style_str = ',Default,,'
cn_style_str = ',CN,,'
en_style_str = ',EN,,'
default_layer_str = 'Dialogue: 0,'
en_layer_str = 'Dialogue: 1,'

print('begin\n')

try:
    cn_file_path = input(input_prompt.format('CN'))
    cn_file_path = cn_file_path.removeprefix('& \'')
    cn_file_path = cn_file_path.removesuffix('\'')
    en_file_path = input(input_prompt.format('EN'))
    en_file_path = en_file_path.removeprefix('& \'')
    en_file_path = en_file_path.removesuffix('\'')
    if os.path.isfile(cn_file_path) and os.path.isfile(en_file_path):
        cn_file_tuple = os.path.split(cn_file_path)
        cn_dir = cn_file_tuple[0]
        file = cn_file_tuple[1]
        fn = file.split('.')
        file_suffix = '.' + fn[len(fn) - 1]
        file_name = file.removesuffix(file_suffix)
        result_file_path = os.path.join(
            cn_dir, file_name + result_file_suffix + file_suffix)
        # open file
        cn_file = open(cn_file_path, 'r', encoding='utf_8_sig')
        en_file = open(en_file_path, 'r', encoding='utf_8_sig')
        result_file = open(result_file_path, 'w', encoding='utf_8_sig')
        print('\nconcat-ing...')
        try:
            # CN
            lines = cn_file.readlines()
            head_line_list = []
            begin_flag = 0
            for line in lines:
                if begin_flag == 1:
                    result_file.write(
                        line.replace(default_style_str, cn_style_str))
                else:
                    head_line_list.append(line)
                if line == begin_line:
                    begin_flag = 1
                    result_file.writelines(head_line_list)
            # EN
            lines = en_file.readlines()
            begin_flag = 0
            for line in lines:
                if begin_flag == 1:
                    result_file.write(
                        line.replace(default_style_str, en_style_str).replace(
                            default_layer_str, en_layer_str))
                if line == begin_line:
                    begin_flag = 1
        finally:
            cn_file.close()
            en_file.close()
            result_file.close()
            print('success!')
    else:
        print('\nERROR: not a valid path or file not exist')
except Exception as e:
    print('\nexception: {}'.format(repr(e)))

print('\nend')
