import math
import numpy as np
from PIL import Image, ImageDraw

from .config import *


font = ImageFont.truetype(font_path, font_size)
font_jp = ImageFont.truetype(font_jp_path, font_jp_size)
s_font = ImageFont.truetype(font_path, int(font_size * s_font_zoom_ratio))
s_font_jp = ImageFont.truetype(font_jp_path, int(font_jp_size * s_font_zoom_ratio))


def has_glyph(ttfont, glyph):
    for table in ttfont["cmap"].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False


def _remove_blank(image: Image.Image):
    # 打开图像并转换为 NumPy 数组
    image_array = np.array(image)

    # 将图像转换为灰度图像
    gray_image_array = image_array[:, :, 3]  # 使用 alpha 通道作为灰度值

    # 计算图像的边界
    non_blank_rows = np.where(np.any(gray_image_array != 0, axis=1))[0]
    non_blank_columns = np.where(np.any(gray_image_array != 0, axis=0))[0]

    # 切割图像
    if non_blank_rows.size > 0 and non_blank_columns.size > 0:
        left = non_blank_columns[0]
        right = non_blank_columns[-1]
        top = non_blank_rows[0]
        bottom = non_blank_rows[-1]

        image = Image.fromarray(image_array[top : bottom + 1, left : right + 1])
    else:
        # 图像全为空白，返回原图像
        image = Image.fromarray(image_array)

    return image


def _fill_transparent(image: Image.Image):
    # 确保图像具有Alpha通道
    image = image.convert("RGBA")

    # 将图像转换为NumPy数组
    np_image = np.array(image)

    # 获取Alpha通道
    alpha = np_image[:, :, 3]

    # 创建一个全白的NumPy数组
    white_image = np.ones_like(np_image) * 255

    # 将Alpha通道为0的像素保持透明
    white_image[:, :, 3] = np.where(alpha == 0, 0, 255)

    # 创建一个新的PIL图像
    new_image = Image.fromarray(white_image.astype(np.uint8))

    return new_image


def paste(background: Image.Image, overlay: Image.Image, box: tuple) -> Image.Image:
    """
    - 将 `overlay` 以 `alpha` 相加的方式粘贴到 `background` 的指定位置上

    :param background: 背景图片
    :param overlay: 需要粘贴的图片
    :param box: 粘贴图片在背景图片的左上角位置

    :return: 返回合并后的图片
    """
    paste_x, paste_y = box

    # 创建一个和 background 大小相同的透明图像作为遮罩
    mask = Image.new("L", background.size, 0)
    mask_draw = ImageDraw.Draw(mask)

    # 在遮罩上画一个矩形，矩形的左上角为 (paste_x, paste_y)
    # 矩形的右下角为 (paste_x + overlay.width, paste_y + overlay.height)
    mask_draw.rectangle(
        (paste_x, paste_y, paste_x + overlay.width, paste_y + overlay.height), fill=255
    )

    # 将 overlay 粘贴到 background 上，只在矩形区域内合并 alpha 值
    background.alpha_composite(overlay, dest=(paste_x, paste_y))

    # 返回合并后的图片
    return background


def _border_img(image: Image.Image, xy: tuple, border_width: int = 1) -> Image.Image:
    """
    绘制描边的图片

    改自 https://stackoverflow.com/questions/41556771/is-there-a-way-to-outline-text-with-a-dark-line-in-pil
    """

    x, y = xy
    points = 15
    white_image = _fill_transparent(image)
    result = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # 绘制描边
    for step in range(0, math.floor(border_width * points)):
        angle = step * 2 * math.pi / math.floor(border_width * points)
        result.paste(
            white_image,
            (
                int(x - border_width * math.cos(angle)),
                int(y - border_width * math.sin(angle)),
            ),
            white_image,
        )

    # 绘制填充文字
    result.paste(image, xy, image)

    return result


def _get_text_img(
    text: str,
    color: tuple,
    line_spacing: int = 0,
    stroke_width: int = 10,
    disable_different_font_size: bool = True,
) -> Image.Image:
    """绘制文字图像"""

    def get_y_offset(c: str, f: ImageFont.ImageFont) -> int:
        if c.isascii() and c != "a":
            # 以"a"作为ascii字符的基准
            return get_y_offset("a", f)

        std_bbox = font.getbbox("的")
        bbox = f.getbbox(c)

        std_baseline = std_bbox[3]
        baseline = bbox[3]
        y_offset = std_baseline - baseline

        return y_offset

    def get_font(chart: str) -> ImageFont.ImageFont:
        empty_glyph_bbox = font_jp.getmask(chr(35813)).getbbox()  # 仅适用于该字体
        glyph_bbox = font_jp.getmask(chart).getbbox()

        if ord(chart) % 3 != 0 or chart.isascii() or disable_different_font_size:
            return (
                font_jp
                if has_glyph(ttfont_jp, chart) and glyph_bbox != empty_glyph_bbox
                else font
            )
        else:
            # ord(chart) % 3 == 0
            return (
                s_font_jp
                if has_glyph(ttfont_jp, chart) and glyph_bbox != empty_glyph_bbox
                else s_font
            )

    texts = text.split(line_break_symbol)
    text_width, text_height = 0, 0
    for t in texts:
        t_width = 0
        t_height = 0
        for chart in t:
            c_font = get_font(chart)

            _, _, c_width, c_height = c_font.getbbox(chart)
            t_width += c_width

            if c_height > t_height:
                t_height = c_height

        if t_width > text_width:
            text_width = t_width

        text_height += t_height + stroke_width * 2 + line_spacing
    text_width += stroke_width * 2
    text_height += stroke_width * 2

    text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_image)

    x, y = stroke_width, stroke_width

    sentence_width, sentence_height = {}, {}
    for i, sentence in enumerate(texts):
        sentence_width[i] = 0
        sentence_height[i] = 0
        for chart in sentence:
            c_font = get_font(chart)

            _, _, width, height = c_font.getbbox(chart)
            sentence_width[i] += width

            if height > sentence_height[i]:
                sentence_height[i] = height

    for i, sentence in enumerate(texts):
        x = (text_width - sentence_width[i]) // 2
        for chart in sentence:
            c_font = get_font(chart)
            draw.text((x, y + get_y_offset(chart, c_font)), chart, color, c_font)
            x += c_font.getlength(chart)
        y += sentence_height[i] + line_spacing
    return text_image


def draw_text(
    text: str,
    degree: float,
    color: tuple,
    width: int,
    line_spacing: int,
    stroke_width: int,
    disable_different_font_size: bool,
) -> Image.Image:
    """
    绘制Sticker的文字

    :param text: 要绘制的文字
    :param degree: 文字倾斜角度
    :param font: 文字字体
    :param color: 文字颜色
    :param width: 输出图像宽度
    :param line_spacing: 行间距
    :param stroke_width: 文字描边厚度
    :param disable_different_font_size: 是否禁用大小字

    :return: 文字图片
    """
    text_img = _get_text_img(
        text, color, line_spacing, stroke_width, disable_different_font_size
    )

    text_img = _border_img(text_img, (0, 0), stroke_width)

    rotated_text_image = _remove_blank(
        text_img.rotate(degree, Image.Resampling.BICUBIC, expand=True)
    )
    height = int(rotated_text_image.height / rotated_text_image.width * width)

    return rotated_text_image.resize((width, height), Image.Resampling.BICUBIC)
