import typing
from typing import List, Tuple


def load_subtitle(filename: str) -> List[Tuple[List[str], List[str]]]:
    f = open(filename, 'rt', encoding='utf8')
    text = f.read()
    lines = text.splitlines(keepends=False)

    names = []
    words = []
    pages = []

    line_counter = 0
    for line in lines:
        if line.strip() == '' or line.strip()[0] == '#':
            continue

        if '---' in line:
            page_split = True
            for c in line:
                if not c in '-. !@#$%^&*(){}[];:<>,/?`~' and not c.isdigit():
                    page_split = False
                    break
        else:
            page_split = False

        if page_split:
            if len(names) == len(words) == len(pages) == 0:
                continue
            if len(names) == 1 and len(words) == 0:
                # speak aside
                words.append(names[0])
                names[0] = ''
            pages.append((names, words))
            names = []
            words = []
            line_counter = 0
            continue


        if line_counter % 2 == 0:
            names.append(line.strip(':：'))
        else:
            words.append(line)
        line_counter += 1
    if len(names) == 1 and len(words) == 0:
        # speak aside
        words.append(names[0])
        names[0] = ''
    if len(names) != 0 and len(words) != 0:
        pages.append((names, words))

    return pages


if __name__ == '__main__':
    pages = load_subtitle('subtitle.txt')

    for page in pages:
        print('--------------')
        names, words = page
        for i in range(len(names)):
            print(names[i] + ': ' + words[i])
