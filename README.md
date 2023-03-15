# sub-trans

**Subtitles Translation**


Python 调用百度翻译 API 批量翻译 ASS 字幕文件

_Baidu_Text_transAPI_for_ass_batch.py_ **usage:**

1.  You may need to install `requests` first, run this code: `pip install requests`
2.  update your own appid & appkey in code
3.  run
4.  input the dir you want to translate or just press Enter means this file current dir
5.  console will print all the files would be translated so check
6.  input one of 'y/Y/yes/YES' and press Enter will begin the translation
7.  finally will generate `your-file-name-CN&EN.[BJT].ass`


Python 利用 OpenCC 繁体转简体

_cht2chs.py_ **usage:**

1.  You may need to install `opencc` first, run this code: `pip install opencc`
2.  run
3.  input the dir and filename you want to convert
4.  finally will generate `your-file-name-CHS.[OJC].srt`


**(Deprecated)** ~~_Baidu_Text_transAPI_for_ass.py_ **usage:**~~

~~1. update your own appid/appkey~~

~~2. update your `src_file_path`~~

~~3. run~~

~~4. will generate 3 files: `en`, `cn`, `result`~~

## Todo:

- [x] cht2chs `ref: http://www.aies.cn/`
- [ ] auto concat cn&en

> http://subhd.tv/u/JaSDLe
