from PIL import Image, ImageDraw, ImageFont
from typing import List, Sequence


def load_font(font_file: str, font_size: int) -> ImageFont.FreeTypeFont:
    """font size is in pixels. it will be converted to points to be used in the lib"""
    font = ImageFont.truetype(font_file, int(font_size * 0.75))
    return font


def get_best_font_size(img_width: int) -> int:
    """all in pixels"""
    return int(img_width / 26)
