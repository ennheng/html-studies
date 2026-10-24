"""生成 X / OG 分享卡（1200×630）。

用法：
    python scripts/make_og.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
THUMBS = ROOT / "thumbs"
OUT = ROOT / "og.jpg"

W, H = 1200, 630
PAPER = "#f2eee4"
INK = "#191713"
MUTED = "#5f594e"
ACCENT = "#a63a22"
FONT_CN = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_EN = r"C:\Windows\Fonts\msyh.ttc"

card_w, card_h = 344, 215
gap, margin = 12, 72


def main() -> None:
    canvas = Image.new("RGB", (W, H), PAPER)

    # 标题区
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(FONT_CN, 46)
    eyebrow_font = ImageFont.truetype(FONT_EN, 15)
    meta_font = ImageFont.truetype(FONT_EN, 15)

    draw.text((margin, 28), "C O L L E C T I O N   ·   S I N G L E - F I L E   H T M L", font=eyebrow_font, fill=ACCENT)
    draw.text((margin, 56), "20 个 HTML，一个作品集", font=title_font, fill=INK)
    draw.text((W - margin, 34), "2026", font=meta_font, fill=MUTED, anchor="ra")
    draw.text((W - margin, 58), "SELF-CONTAINED", font=meta_font, fill=MUTED, anchor="ra")

    # 2×3 缩略图墙
    picks = ["01-chromatic-orbit", "06-brutalist-radio", "09-alpine-air",
             "10-pixel-teahouse", "14-memory-arcade", "20-the-last-signal"]
    top = 126
    for index, stem in enumerate(picks):
        path = THUMBS / f"{stem}.jpg"
        if not path.exists():
            continue
        row, col = divmod(index, 3)
        with Image.open(path) as image:
            thumb = image.convert("RGB").resize((card_w, card_h), Image.LANCZOS)
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        canvas.paste(thumb, (x, y))
        draw.rectangle([x, y, x + card_w, y + card_h], outline="#d9d1bf", width=1)

    footer = "单文件 · 无 CDN · 可离线打开    ·    ennheng.github.io/html-studies"
    draw.text((margin, H - 34), footer, font=ImageFont.truetype(FONT_EN, 14), fill=MUTED)

    canvas.save(OUT, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"已生成 {OUT.name} · {W}×{H} · {OUT.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
