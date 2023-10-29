import os
import math
from PIL import Image, ImageDraw

from .utils import draw_text, paste
from .config import *


def make_sticker(
    character: str,
    index: str,
    text: str,
    degree: float = 0,
    text_zoom_ratio: float = 1,
    text_pos: str = "mu",
    line_spacing: int = 0,
    text_x_offset: int = 0,
    text_y_offset: int = 0,
    disable_different_font_size: bool = False,
) -> Image.Image:
    """
    绘制Sticker

    :param character: 角色名
    :param index: Sticker序号
    :param text: Sticker文字
    :param degree: 文字倾斜角度
    :param text_zoom_ratio: 文字缩放比
    :param text_pos: 文字位置
    :param line_spacing: 行间距
    :param text_x_offset: 文字左右偏移量
    :param text_y_offset: 文字上下偏移量
    :param disable_different_font_size: 是否禁用大小字

    关于`text_pos`, 请参照下表

    | | 左 | 中 | 右 |
    | --- | --- | --- | --- |
    | 上 | lu | mu | ru |
    | 中 | lm | mm | rm |
    | 下 | ld | md | rd |

    :return: Sticker图像
    """
    sticker = Image.open(f"./data/stickers/{character}_{index.zfill(2)}.png").convert(
        "RGBA"
    )
    if text == "":
        return sticker

    if character == "Miku" and index == "16":
        character = "Miku_16"

    text_image = draw_text(
        text,
        degree,
        sticker_colors[character],
        int(sticker.width * text_zoom_ratio),
        line_spacing,
        10,
        disable_different_font_size,
    )

    x_pos, y_pos = text_pos[0], text_pos[1]

    x_positions = {
        "l": 0,
        "m": (sticker.width - text_image.width) // 2,
        "r": sticker.width - text_image.width,
    }
    y_positions = {
        "u": 0,
        "m": (sticker.height - text_image.height) // 2,
        "d": sticker.height - text_image.height,
    }
    x, y = x_positions[x_pos], y_positions[y_pos]

    return paste(
        Image.new("RGBA", sticker.size, (0, 0, 0, 255)),
        paste(sticker, text_image, (x + text_x_offset, y + text_y_offset)),
        (0, 0),
    )


def make_character_list() -> Image.Image:
    """
    获取角色列表

    :return: 角色列表图片
    """
    sample_stickers_name = sorted(
        {
            sticker
            for sticker in os.listdir("./data/stickers")
            if sticker.endswith("_01.png")
        }
    )
    sample_stickers = [
        Image.open(os.path.join(".\\data\\stickers", sticker)).convert("RGBA")
        for sticker in sample_stickers_name
    ]
    preview_row = math.ceil(len(sample_stickers) / preview_column)

    width = (
        2 * padding
        + sum([sticker.width for sticker in sample_stickers[:preview_column]])
        + (preview_column - 1) * spacing
    )
    height = (
        2 * padding
        + sum([sticker.height for sticker in sample_stickers[:preview_row]])
        + (preview_row - 1) * spacing
    )
    bg = Image.new("RGBA", (width, height), (120, 120, 120))
    draw = ImageDraw.Draw(bg)

    x, y = padding, padding
    for idx, sticker in enumerate(sample_stickers):
        if idx % preview_column == 0 and idx != 0:
            x = padding
            y += sticker.height + spacing

        bg.paste(sticker, (x, y), sticker)
        draw.text(
            (x, y - preview_font_size),
            sample_stickers_name[idx].split("_")[0],
            (255, 255, 255),
            preview_font,
        )
        x += sticker.width + spacing
    return bg


def make_preview(character: str) -> Image.Image:
    """获取指定角色Sticker底图预览

    :param character: 角色名

    :return: 预览图
    """

    def get_lighter_color(color: tuple, color_light_value: int = -60) -> tuple:
        """获取更亮的颜色"""
        if len(color) == 3:
            r, g, b = color
        else:
            r, g, b, a = color

        if max([r, g, b]) + color_light_value > 255:
            color_light_value = 255 - max([r, g, b])
        if min([r, g, b]) + color_light_value < 0:
            color_light_value = 0 - min([r, g, b])

        if len(color) == 3:
            return (r + color_light_value, g + color_light_value, b + color_light_value)
        return (r + color_light_value, g + color_light_value, b + color_light_value, a)

    bg_color = get_lighter_color(sticker_colors[character])
    stickers_name = [
        sticker
        for sticker in os.listdir("./data/stickers")
        if sticker.startswith(character)
    ]
    stickers = [
        Image.open(os.path.join(".\\data\\stickers", sticker)).convert("RGBA")
        for sticker in stickers_name
    ]

    preview_row = math.ceil(len(stickers) / preview_column)

    width = (
        2 * padding
        + sum([sticker.width for sticker in stickers[:preview_column]])
        + (preview_column - 1) * spacing
    )
    height = (
        2 * padding
        + sum([sticker.height for sticker in stickers[:preview_row]])
        + (preview_row - 1) * spacing
    )
    bg = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(bg)

    x, y = padding, padding
    for idx, sticker in enumerate(stickers):
        if idx % preview_column == 0 and idx != 0:
            x = padding
            y += sticker.height + spacing

        bg.paste(sticker, (x, y), sticker)
        draw.text(
            (x, y - preview_font_size),
            stickers_name[idx].split(".")[0].split("_")[-1],
            (255, 255, 255),
            preview_font,
        )
        x += sticker.width + spacing
    return bg
