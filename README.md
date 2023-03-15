# sub-trans

## Subtitles Translation

### Python调用百度翻译API批量翻译ASS字幕文件

#### *Baidu_Text_transAPI_for_ass_batch.py* **usage:**

1. You may need to install `requests` first, run this code: `pip install requests`
2. update your own appid & appkey in code
3. run
4. input the dir you want to translate or just press Enter means this file current dir
5. console will print all the files would be translated so check
6. input one of 'y/Y/yes/YES' and press Enter will begin the translation
7. finally will generate `your-file-name-CN&EN.[BJT].ass`

#### **(Deprecated)** ~~*Baidu_Text_transAPI_for_ass.py* **usage:**~~

~~1. update your own appid/appkey~~  
~~2. update your `src_file_path`~~  
~~3. run~~  
~~4. will generate 3 files: `en`, `cn`, `result`~~

### Python利用OpenCC繁体转简体

#### *cht2chs.py* **usage:**

1. You may need to install `opencc` first, run this code: `pip install opencc`
2. run
3. input the dir and filename you want to convert
4. finally will generate `your-file-name-CHS.[OJC].srt`

### Python合并中文和英文ASS字幕文件

#### *auto_concat_cn&en_for_ass.py* **usage:**

1. run
2. input the CN dir and filename you want to concat
3. input the EN dir and filename you want to concat
4. finally will generate `your-file-name-CN&EN.[JC].srt`

## Todo

- [x] cht2chs `ref: http://www.aies.cn/`
- [x] auto concat cn&en

## Scenario

- no CHS or CHT subtitle, only ENG from resource or [Subscene](https://subscene.com)

> use Baidu_Text_transAPI_for_ass.py

- no CHS subtitle, only CHT and ENG

> use cht2chs.py

- separate CHS and ENG

> use auto_concat_cn&en_for_ass.py

---
> <http://subhd.tv/u/JaSDLe>  
> <https://zimuku.pw/u/A3FNKkhX0>
