# ProjectSekaiStickerMaker
✨ 基于 PIL 的 Project Sekai 贴纸绘制工具 ✨

## 使用
### 安装环境
```
pip install Pillow numpy fonttools
```
### 调用
请先确保 `ProjectSekaiStickerMaker` 文件夹与你要调用它的文件同级。如果不是，请自行解决导入问题

```python
# 运行目录在你调用 ProjectSekaiStickerMaker 这级
from ProjectSekaiStickerMaker import make_sticker, make_preview, make_character_list

# 运行目录在你调用 ProjectSekaiStickerMaker 更上级
from .ProjectSekaiStickerMaker import make_sticker, make_preview, make_character_list

from PIL import Image


character_list_image: Image.Image = make_character_list()

preview_image: Image.Image = make_preview(character="Emu")
# 支持的角色请参考 config.py 中的 sticker_colors 的键

sticker_image: Image.Image = make_sticker(
    character = "Emu",
    index = "01",
    text = "你好吖",
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