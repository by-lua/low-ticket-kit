"""Gera PNG 720x1280 transparente com texto estilo story do Instagram (caixa branca por linha)."""
import sys
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1]
lines = sys.argv[2:]  # cada linha; emoji no fim marcado com |EMOJI
W, H = 720, 1280
SIZE = 38
font = ImageFont.truetype("~/.local/share/fonts/minhaempresa/Inter.ttf", SIZE)
try:
    font.set_variation_by_axes([700])
except Exception:
    pass
emo_font = ImageFont.truetype("/usr/share/fonts/noto/NotoColorEmoji.ttf", 109)

def emoji_img(ch, h):
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=emo_font, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
y = int(__import__("os").environ.get("STORY_Y", "70"))
PADX, PADY, GAP, R = 18, 10, 0, 12
for raw in lines:
    text, _, emo = raw.partition("|")
    tw = d.textlength(text, font=font)
    ei = emoji_img(emo, int(SIZE * 1.05)) if emo else None
    total = tw + ((ei.width + 10) if ei else 0)
    asc, desc = font.getmetrics()
    bh = asc + desc + PADY * 2
    x0 = (W - total) / 2 - PADX
    d.rounded_rectangle([x0, y, x0 + total + PADX * 2, y + bh], R, fill=(255, 255, 255, 255))
    d.text((x0 + PADX, y + PADY), text, font=font, fill=(0, 0, 0, 255))
    if ei:
        img.alpha_composite(ei, (int(x0 + PADX + tw + 10), int(y + (bh - ei.height) / 2)))
    y += bh + GAP
img.save(out)
print(out)
