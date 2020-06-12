"""
根据文件夹内的图片自动生成台词文件的分页符
"""
import typing
from typing import List, Tuple
import os
import re


def is_split_page(line: str) -> bool:
    line = line.strip('\n ')
    if line.startswith('---') and line.endswith('---'):
        return True
    return False


if __name__ == "__main__":
    from settings_loader import load_settings
    from main import try_get
    join = os.path.join

    settings = load_settings(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../settings.txt'))

    working_folder = try_get(settings, 'working_folder', '../working folder/')
    source_folder = try_get(settings, 'source_folder', 'imgs')
    text_file = try_get(settings, 'text_file', 'subtitle.txt')

    current_dir = os.path.abspath(join(os.path.dirname(__file__), working_folder))
    print('working folder is: "{}"'.format(current_dir))

    print('-----')
    answer = input('settings are shown above, continue? [y/n]:\n')
    if answer.lower() != 'y':
        exit(0)

    source_list = os.listdir(join(current_dir, source_folder))
    source_list.sort()

    file_names = []
    for source in source_list:
        file_names.append(os.path.splitext(source)[0])

    text_file_dir = join(current_dir, text_file)
    with open(text_file_dir, 'rt', encoding='utf8') as f:
        lines = f.readlines()

    line_num = 0
    page_num = 0
    out_text = ''
    while True:
        if line_num >= len(lines) or page_num >= len(file_names):
            break
        line = lines[line_num].strip(' \n')
        if not is_split_page(line):
            out_text += line + '\n'
            line_num += 1
            continue
        file_name = file_names[page_num]
        if line.strip(' -') != file_name:
            # new image or deleted image
            if line in file_names[page_num+1:]:
                # this line if found in later images, line deleted or new image
                # this image is new, so adds new page split line
                out_text += "-----" + file_name + "-----\n"
                page_num += 1
                continue
            else:
                # this line is not found later, image deleted or line added
                # this line is use less so delete it
                line_num += 1
                out_text += '# ' + line + '\n'
                while line_num < len(lines) and not is_split_page(lines[line_num]):
                    line = lines[line_num].strip(' \n')
                    if line != '':
                        out_text += '# ' + line + '\n'
                    else:
                        out_text += '\n'
                    line_num += 1 # jump to next splitline
                continue
        else:
            # the subtitle and the file is in synchronize
            page_num += 1
            out_text += line + '\n'
            line_num += 1
            while line_num < len(lines) and not is_split_page(lines[line_num]):
                line = lines[line_num].strip(' \n')
                out_text += line + '\n'
                line_num += 1
            continue
    while line_num < len(lines):
        out_text += '# ' + lines[line_num].strip(' \n') + '\n'
        line_num += 1

    while page_num < len(file_names):
        file_name = file_names[page_num]
        out_text += "-----" + file_name + "-----\n"
        page_num += 1

    with open(text_file_dir, 'wt', encoding='utf8') as f:
        f.write(out_text)
