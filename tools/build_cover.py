from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONTS = Path("C:/Windows/Fonts")
PAPER = (249, 249, 247)
INK = (26, 26, 29)
RED = (190, 37, 50)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def build():
    canvas = Image.new("RGB", (1440, 600), PAPER)
    avatar = Image.open(ROOT / "assets/chihiro-avatar.png").convert("RGB")
    avatar = avatar.resize((650, 650), Image.Resampling.LANCZOS)
    canvas.paste(avatar, (790, -18))
    draw = ImageDraw.Draw(canvas)

    # A slanted paper edge leaves the original portrait unobstructed.
    draw.polygon([(0, 0), (847, 0), (755, 600), (0, 600)], fill=PAPER)
    draw.line((847, 0, 755, 600), fill=INK, width=2)
    draw.rectangle((0, 0, 1440, 7), fill=RED)
    draw.text((62, 48), "WANGSHEN233", font=font("arialbd.ttf", 25), fill=RED)
    draw.text((63, 87), "A SMALL CORNER OF MY WORLD", font=font("arial.ttf", 15), fill=INK)
    draw.text((51, 132), "千寻", font=font("msyhbd.ttc", 166), fill=INK)
    draw.text((66, 349), "C H I H I R O", font=font("arialbd.ttf", 43), fill=RED)
    draw.line((66, 424, 130, 424), fill=RED, width=3)
    draw.text((66, 450), "保持好奇，继续向前。", font=font("msyh.ttc", 27), fill=INK)
    draw.text((66, 503), "CODE  /  CURIOSITY  /  LITTLE ADVENTURES", font=font("arial.ttf", 14), fill=(95, 95, 98))
    draw.text((66, 561), "日天  /  @wangshen233", font=font("msyh.ttc", 15), fill=INK)
    draw.rectangle((1329, 31, 1399, 96), fill=RED)
    draw.text((1343, 42), "01", font=font("arialbd.ttf", 34), fill=PAPER)
    canvas.save(ROOT / "assets/chihiro-cover.png", optimize=True)

    # A shared palette keeps the portrait stable while the red accent moves.
    palette = canvas.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    frames = []
    for index in range(40):
        frame = canvas.copy()
        pen = ImageDraw.Draw(frame)
        offset = int(index / 39 * 610)
        pen.line((66, 539, 716, 539), fill=(225, 222, 221), width=2)
        pen.line((66 + offset, 539, min(716, 106 + offset), 539), fill=RED, width=3)
        if index < 25:
            pen.rectangle((349, 566, 356, 579), fill=RED)
        frames.append(frame.quantize(palette=palette, dither=Image.Dither.NONE))
    frames[0].save(
        ROOT / "assets/chihiro-cover.gif",
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        optimize=True,
        disposal=1,
    )


if __name__ == "__main__":
    build()
