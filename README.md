# ProjectSekaiStickerMaker
✨ 基于 PIL 的 Project Sekai 贴纸绘制工具 ✨

## 使用
### 安装环境
```
pip install Pillow numpy fonttools
```
### 调用
请先确保 `ProjectSekaiStickerMaker` 文件夹与你要调用它的文件同级

```python
# 运行目录在你调用 ProjectSekaiStickerMaker 这级
from ProjectSekaiStickerMaker import make_sticker, make_preview, make_character_list

# 运行目录在你调用 ProjectSekaiStickerMaker 更上级（一般用的都是这个吧？）
from .ProjectSekaiStickerMaker import make_sticker, make_preview, make_character_list

from PIL import Image


character_list_image: Image.Image = make_character_list()

preview_image: Image.Image = make_preview(character="Emu")
# 支持的角色请参考 nickname.py

sticker_image: Image.Image = make_sticker(
    character = "Emu", # 此处的 `character` 必须是 `nickname.py` 中存在的键
    index = "01", # 此处的 `index` 必须是 data/stickers 中存在的序号，只能是 `01`, `02` 之类的
    text = "你好吖",
    # 下面的参数是可选的
    degree = 0,
    text_zoom_ratio = 1,
    text_pos = "mu",
    line_spacing = 0,
    text_x_offset = 0,
    text_y_offset = 0,
    disable_different_font_size = False
)
```

## 感谢
[Original stickers](https://www.reddit.com/r/ProjectSekai/comments/x1h4v1/after_an_ungodly_amount_of_time_i_finally_made/)

[Cropped images](https://github.com/Modder4869)