# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()
import datetime
import os
import time

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}
trackers_str = ''
backup_dir = './trackers'
backup_filename = 'trackers-{}.txt'.format(
    datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
url1 = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best_ip.txt'
url2 = 'https://dns.icoa.cn/tracker/'

print('begin\n')

try:
    print('calling url1...')
    start = time.time()
    r1 = requests.get(url1, headers=headers, verify=False)
    end = time.time()
    print('call url1 done({}s)'.format(end - start))

    print('calling url2...')
    start = time.time()
    r2 = requests.get(url2, headers=headers, verify=False)
    end = time.time()
    print('call url2 done({}s)'.format(end - start))
    # print(r2.text)
    soup = BeautifulSoup(r2.text, 'lxml')
    # soup=BeautifulSoup(result,'lxml')
    textarea = soup.select_one('#box_shadow > textarea')
    # print(textarea.get_text())

    trackers_str_raw = '\n'.join([r1.text, textarea.get_text()])
    trackers_list_raw = trackers_str_raw.splitlines()
    trackers_set = set()
    trackers_list = []
    for line in trackers_list_raw:
        if line != '' and line not in trackers_set:
            trackers_set.add(line)
            trackers_list.append(line)
    trackers_str = '\n'.join(trackers_list)
    result_file = open('./trackers.txt', 'w', encoding='utf_8_sig')
    result_file.write(trackers_str)
    result_file.close()
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    result_backup_file = open(os.path.join(backup_dir, backup_filename),
                              'w',
                              encoding='utf_8_sig')
    result_backup_file.write(trackers_str)
    result_backup_file.close()
except Exception as e:
    print('\nexception: {}'.format(repr(e)))

# print(trackers_str)
print('\nend')
