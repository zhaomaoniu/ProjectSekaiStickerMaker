from PIL import ImageFont
from fontTools.ttLib import TTFont

font_path = "./data/fonts/ShangShouFangTangTi.ttf"
font_jp_path = "./data/fonts/YurukaStd.woff2"
font_size = 100
font_jp_size = 80
s_font_zoom_ratio = 0.8

ttfont_jp = TTFont(font_jp_path)

line_break_symbol = "/"

preview_column = 4
preview_font_size = 32
preview_font = ImageFont.truetype(font_path, preview_font_size)
padding = 64
spacing = 32 + preview_font_size

sticker_colors = {
    "Airi": (251, 138, 172),
    "Akito": (255, 199, 34),
    "An": (0, 186, 220),
    "Emu": (255, 102, 187),
    "Ena": (177, 143, 108),
    "Haruka": (100, 149, 240),
    "Honami": (248, 102, 102),
    "Ichika": (51, 170, 238),
    "KAITO": (51, 102, 204),
    "Kanade": (187, 102, 136),
    "Kohane": (255, 102, 153),
    "Len": (211, 189, 0),
    "Luka": (248, 140, 167),
    "Mafuyu": (113, 113, 175),
    "Meiko": (228, 72, 95),
    "Miku": (51, 204, 187),
    "Miku_16": (176, 172, 173),
    "Minori": (243, 158, 125),
    "Mizuki": (202, 141, 182),
    "Nene": (25, 205, 148),
    "Rin": (232, 165, 5),
    "Rui": (187, 136, 238),
    "Saki": (245, 179, 3),
    "Shiho": (160, 193, 11),
    "Shizuku": (92, 208, 185),
    "Touya": (0, 119, 221),
    "Tsukasa": (240, 154, 4),
}
