from color_reader import load_colors, str2color
from paragraph import Paragraph, TextBlock
from settings_loader import load_settings
from subtitle_reader import load_subtitle
from utilities import get_best_font_size, load_font

import os
import PIL
from PIL.Image import Image


def try_get(dictionary: dict, key, default_value, quiet=False):
    if key in dictionary.keys():
        value = dictionary[key]
        if not quiet:
            print('{}: {}'.format(key, value))
        return value
    if not quiet:
        print('can\'t find setting {}, defaulting to {}'.format(key, default_value))
    return default_value


if __name__ == "__main__":
    settings = load_settings('../settings.txt')

    working_folder = try_get(settings, 'working_folder', '../working folder/')
    source_folder = try_get(settings, 'source_folder', 'imgs')
    out_folder = try_get(settings, 'out_folder', 'products')
    text_file = try_get(settings, 'text_file', 'subtitle.txt')
    name_color_dict = try_get(settings, 'color_file', 'color_index.txt')
    print('-----')

    default_text_color = str2color(try_get(settings, 'default_text_color', 'white'))
    bg_color = str2color(try_get(settings, 'bg_color', '(50,50,50)'))

    print('-----')
    border_width = int(try_get(settings, 'border_width', '15'))
    name_scale_factor = float(try_get(settings, 'name_scale_factor', '0.7'))

    print('-----')
    try_get(settings, 'name_font', 'fonts/FZY3JW.TTF')
    try_get(settings, 'word_font', 'fonts/FZY3JW.TTF')

    join = os.path.join

    current_dir = os.path.abspath(join(os.path.dirname(__file__), working_folder))
    name_color_dict = load_colors(join(current_dir, name_color_dict))
    print('-----')
    print('working folder is: "{}"'.format(current_dir))

    print('-----')
    answer = input('settings are shown above, continue? [y/n]:\n')
    if answer.lower() != 'y':
        exit(0)

    #######################################


    out_dir = join(current_dir, out_folder)
    if not os.path.isdir(out_dir):
        if os.path.exists(out_dir):
            print('out dir cannot be created, exiting.')
            exit(1)
        os.mkdir(out_dir)
    elif len(os.listdir(out_dir)) > 0:
        answer = input('there are files in the our dir, this operation may overwrite them, continue? [y/n]:\n')
        if answer.lower() != 'y':
            exit(0)

    img_dir = join(current_dir, source_folder)
    img_list = os.listdir(img_dir)
    img_list.sort()

    pages_texts = load_subtitle(join(current_dir, text_file))

    if len(pages_texts) != len(img_list):
        answer = input('the length of text does not match the number of images, some will be ignored, continue? [y/n]:\n')
        if answer.lower() != 'y':
            exit(0)
    page_num = min(len(pages_texts), len(img_list))

    for page in range(page_num):
        print('making page {}...'.format(page))

        names, words = pages_texts[page]
        assert len(names) == len(words)
        length = len(names)

        img = PIL.Image.open(join(img_dir, img_list[page]))
        print('image loaded')
        img: Image
        width = img.width
        name_font = load_font(join(current_dir, try_get(settings, 'name_font', 'fonts/FZY3JW.TTF', quiet=True)),
                              int(get_best_font_size(width) * name_scale_factor))
        word_font = load_font(join(current_dir, try_get(settings, 'word_font', 'fonts/FZY3JW.TTF', quiet=True)),
                              int(get_best_font_size(width)))
        paragraph = Paragraph(width - border_width * 2)
        for i in range(length):
            name = names[i]
            word = words[i]
            name_color = try_get(name_color_dict, name, default_text_color, quiet=True)
            name_block = TextBlock(name+':', name_font, name_color)
            paragraph.add_text_block(name_block)

            word_block = TextBlock(word, word_font, name_color)
            paragraph.add_text_block(word_block)
            paragraph.add_text_block(TextBlock('', word_font))
        additional_height = paragraph.get_size()[1]
        new_img = PIL.Image.new('RGB', (img.width, img.height + additional_height + border_width * 2), bg_color)
        new_img.paste(img)
        paragraph.draw(new_img, (border_width, img.height + border_width))
        print('editing done!')
        file_name = '{:0>4}.png'.format(page)
        print('saving to {}...'.format(join(out_dir, file_name)))
        new_img.save(join(out_dir, file_name))
        print('saving done!\n')
