# -*- coding: utf-8 -*-

import os


input_prompt = '''Please input the dir you want to batch rename.
    e.g. 'C:\\'
> Enter a value: '''
subtitle_suffix=('.ass','.srt')
video_suffix=('.mp4','.mkv')

print('begin\n')

try:
    src_file_path = input(input_prompt)
    if os.path.isdir(src_file_path):
        subtitle_list = []
        video_list = []
        for file in os.listdir(src_file_path):
            if file.endswith(subtitle_suffix):
                subtitle_list.append(file)
            elif file.endswith(video_suffix):
                video_list.append(file)
        print(subtitle_list)
        print()
        print(video_list)
        print()
        for video_name in video_list:
            for index in range(len(video_list)+1):
                episode='e{:0>2}'.format(index)
                episode_cap='E{:0>2}'.format(index)
                if episode in video_name or episode_cap in video_name:
                    print('{} or {}'.format(episode,episode_cap))
                    for subtitle_name in subtitle_list:
                        if episode in subtitle_name or episode_cap in subtitle_name:
                            new_name=''
                            for v_suffix in video_suffix:
                                if video_name.endswith(v_suffix):
                                    new_name= video_name.removesuffix(v_suffix)
                                    break
                            for s_suffix in subtitle_suffix:
                                if video_name.endswith(v_suffix):
                                    old_name=subtitle_name.removesuffix(s_suffix)
                                    print('rename \n{} \nto \n{}\n'.format(subtitle_name,new_name+s_suffix))
                                    print(os.path.join(src_file_path,subtitle_name))
                                    os.rename(os.path.join(src_file_path,subtitle_name),os.path.join(src_file_path,new_name+s_suffix))
                                    break
                    break
    else:
        print('\nERROR: not a valid path or not exist')
except Exception as e:
    print('\nexception: {}'.format(repr(e)))

print('\nend')
