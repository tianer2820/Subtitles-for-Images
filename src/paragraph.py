import PIL
from PIL.Image import Image
from PIL.ImageColor import getrgb
from PIL.ImageFont import FreeTypeFont
from PIL.ImageDraw import ImageDraw
from typing import Union, Sequence, Tuple


__all__ = ['TextBlock', 'Paragraph']


class TextBlock:
    def __init__(self, text: str, font: FreeTypeFont = None, color: Union[str, Sequence] = (0, 0, 0)):
        self.text = text
        self.font = font
        if type(color) is str:
            self.color = getrgb(color)
        else:
            self.color = color

    def get_size(self, start=None, end=None) -> Tuple[int, int]:
        """
        get the rendered size
        :param start: int, index of the string
        :param end: int, index of the string
        :return: (width, height)
        """
        if start is None:
            start = 0
        if end is None:
            end = len(self.text)
        s = self.text[start:end]
        return self.font.getsize(s)

    def draw(self, img, xy, start=None, end=None):
        """

        :param img: image to be painted on
        :param xy: (x, y)
        :param start: int, index of the string
        :param end: int, index of the string
        """
        if len(self.text) == 0:
            return
        if start is None:
            start = 0
        if end is None:
            end = len(self.text)
        s = self.text[start:end]
        draw = ImageDraw(img)
        draw.text(xy, s, fill=self.color, font=self.font)


class Paragraph:
    def __init__(self, width: int = 100):
        """

        :param width: width of the paragraph. Can be modified later
        """
        self._block_list = []
        self.width = width

    def add_text_block(self, block: TextBlock):
        self._block_list.append(block)

    def draw(self, img: Image, xy: Sequence[int]):
        """
        Paint the paragraph on an image.
        :param img: the image to be painted on
        :param xy: (x, y), upperleft corner in pixels
        """
        draw = ImageDraw(img)
        y_offset = 0

        line_width = 0
        line_height = 0

        i_block = 0
        i = 0
        line_start = [0, 0]
        while True:
            block = self._block_list[i_block]
            block: TextBlock
            if len(block.text) == 0:
                w, h = 0, 0
            elif i_block == line_start[0]:
                # this may be an incomplete block
                w, h = block.get_size(line_start[1], i + 1)
            else:
                w, h = block.get_size(0, i + 1)
            if line_width + w > self.width or len(block.text) == 0:
                # need new line
                line_height = max(line_height, h)
                # draw this line
                if line_start[0] == i_block:
                    # the whole line is one block
                    block.draw(img, (xy[0], xy[1] + y_offset), start=line_start[1], end=i)
                else:
                    # several block is in this line
                    x_offset = 0
                    for b in range(line_start[0], i_block+1):  # draw each block
                        bw = self._block_list[b]
                        bw: TextBlock
                        if b == line_start[0]:
                            # first block
                            size = bw.get_size(line_start[1])
                            bw.draw(img, (xy[0] + x_offset, xy[1] + y_offset + line_height - size[1]), line_start[1])
                            x_offset += size[0]
                        elif b == i_block:
                            size = bw.get_size(0, i)
                            bw.draw(img, (xy[0] + x_offset, xy[1] + y_offset + line_height - size[1]), 0, i)
                            x_offset += size[0]
                        else:
                            size = bw.get_size()
                            bw.draw(img, (xy[0] + x_offset, xy[1] + y_offset + line_height - size[1]))
                            x_offset += size[0]
                # prepare for new line
                y_offset += line_height
                line_height = 0
                line_width = 0
                line_start = i_block, i
                if len(block.text) == 0:
                    i = 0
                    i_block += 1
                    if i_block >= len(self._block_list):
                        # finished
                        break
                continue
            else:
                # do not need new line
                i += 1
                if i >= len(block.text):
                    # this block is finished
                    line_height = max(line_height, h)
                    line_width += w
                    i_block += 1
                    i = 0
                    if i_block >= len(self._block_list):
                        # all blocks are done
                        # paint the remaining
                        if line_start[0] == i_block:
                            # the whole line is one block
                            block.draw(img, (xy[0], xy[1] + y_offset), start=line_start[1], end=i)
                        else:
                            # several block is in this line
                            x_offset = 0
                            for b in range(line_start[0], i_block):  # draw each block
                                bw = self._block_list[b]
                                bw: TextBlock
                                if b == line_start[0]:
                                    # first block
                                    size = bw.get_size(line_start[1])
                                    bw.draw(img, (xy[0] + x_offset, xy[1] + y_offset + line_height - size[1]), line_start[1])
                                    x_offset += size[0]
                                elif b == i_block:
                                    size = bw.get_size(0, i)
                                    bw.draw(img, (xy[0] + x_offset, xy[1] + y_offset + line_height - size[1]), 0, i)
                                    x_offset += size[0]
                                else:
                                    size = bw.get_size()
                                    bw.draw(img, (xy[0] + x_offset, xy[1] + y_offset + line_height - size[1]))
                                    x_offset += size[0]
                        break

    def get_size(self):
        height = 0

        line_width = 0
        line_height = 0

        i_block = 0
        i = 0
        line_start = [0, 0]
        while True:
            block = self._block_list[i_block]
            block: TextBlock
            if len(block.text) == 0:
                w, h = 0, 0
            elif i_block == line_start[0]:
                # this may be an incomplete block
                w, h = block.get_size(line_start[1], i + 1)
            else:
                w, h = block.get_size(0, i + 1)
            if line_width + w > self.width or len(block.text) == 0:
                # need new line
                line_height = max(line_height, h)
                height += line_height
                line_height = 0
                line_width = 0
                line_start = i_block, i
                if len(block.text) == 0:
                    i_block += 1
                    i = 0
                    if i_block >= len(self._block_list):
                        break
                continue
            else:
                # do not need new line
                i += 1
                if i >= len(block.text):
                    # this block is finished
                    line_height = max(line_height, h)
                    line_width += w
                    i_block += 1
                    i = 0
                    if i_block >= len(self._block_list):
                        # all blocks are done
                        height += line_height
                        break
        return self.width, height


if __name__ == '__main__':
    par = Paragraph(500)
    t = '一只敏捷的灰棕狐狸跳过一堵墙。'
    for i in range(30):
        index = i * 5
        index %= len(t)
        color = [0, 0, 0]
        color[i % 3] = 255
        font = FreeTypeFont(font='fonts/FZY3JW.TTF', size=30 + 10*(i%3))
        tb = TextBlock(t[index:index+5], color=tuple(color), font=font)

        par.add_text_block(tb)
        if i == 15:
            print('15')
            par.add_text_block(TextBlock('', font))

    size = par.get_size()
    print(size)

    img = PIL.Image.new('RGB', size)
    par.draw(img, (0, 0))
    img.save('./partest.png')
    img.show()