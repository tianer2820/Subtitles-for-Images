from color_reader import load_colors, str2color
from settings_loader import load_settings
from subtitle_reader import load_subtitle
from main import try_get

import os
import argparse


settings = load_settings(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../settings.txt'))

working_folder = try_get(settings, 'working_folder', '../working folder/')
text_file = try_get(settings, 'text_file', 'subtitle.txt')
name_color_file_name = try_get(settings, 'color_file', 'color_index.txt')

default_text_color = try_get(settings, 'default_text_color', 'white')

join = os.path.join

current_dir = os.path.abspath(join(os.path.dirname(__file__), working_folder))
name_color = join(current_dir, name_color_file_name)

print('-----')
print('working folder is: "{}"'.format(current_dir))
answer = input('writing to {}, continue?[y/n]:\n'.format(name_color))
if answer.lower() != 'y':
    exit(0)

pages = load_subtitle(join(current_dir, text_file))
names = set()
for page in pages:
    n = page[0]
    for name in n:
        names.add(name)

print(names)

if os.path.isfile(name_color):
    # file exists, append
    colors = load_colors(name_color)
    for name in colors.keys():
        if name in names:
            names.remove(name)

answer = input('adding these names to the file:\n{}\ncontinue?[y/n]\n'.format(names))
if answer.lower() != 'y':
    exit(0)

with open(name_color, 'at', encoding='utf8') as f:
    for name in names:
        f.write('{} = {}\n'.format(name, default_text_color))
