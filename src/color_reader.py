import re
from typing import Tuple
from PIL.ImageColor import getrgb


def str2color(string: str) -> Tuple[int]:
    color = string
    if re.fullmatch('\\((\\d+), *(\\d+), *(\\d+)\\)', color):
        # rgb color
        result = re.fullmatch('\\((\\d+), *(\\d+), *(\\d+)\\)', color)
        c = []
        for i in range(1, 4):
            c.append(int(result.group(i)))
        return tuple(c)
    elif re.fullmatch('#([0-9a-fA-F]+)', color):
        # Hex color
        result = re.fullmatch('#([0-9a-fA-F]+)', color)
        h = '{:0>6}'.format(result.group(1))
        c = []
        for i in range(3):
            a = h[i * 2:i * 2 + 2]
            c.append(int(a, 16))
        return tuple(c)
    else:
        # name color
        return getrgb(color)


def load_colors(filename: str) -> dict:
    with open(filename, 'rt', encoding='utf8') as f:
        text = f.read()
    lines = text.splitlines(keepends=False)

    colors = {}
    for line in lines:
        if line.strip() == '':
            continue
        if line.startswith('#'):
            continue

        pair = line.split('=', 1)
        name = pair[0].strip()
        color = pair[1].strip()

        colors[name] = str2color(color)

    return colors

if __name__ == '__main__':
    d = load_colors('color_index.txt')
    for pair in d.items():
        print(pair)