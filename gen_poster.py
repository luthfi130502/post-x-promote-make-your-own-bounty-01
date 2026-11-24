#!/usr/bin/env python3
"""Draw the promo poster for post-x-promote-make-your-own-bounty-01.

Everything is drawn in code with Pillow: no downloaded images, no external
assets. The make.fun name appears only as plain lowercase text ("make.fun");
no make.fun mark/wordmark artwork is redrawn, recoloured or copied.

Output: poster.png, 1200x675 (16:9), sized for an X post attachment.
Run: python3 gen_poster.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
OUT = "poster.png"

BG = (11, 16, 38)          # deep navy
PANEL = (20, 27, 61)       # card navy
PANEL_EDGE = (58, 71, 128)
WHITE = (255, 255, 255)
MUTED = (168, 178, 214)
GOLD = (255, 197, 61)
GOLD_DARK = (214, 148, 16)
MAGENTA = (255, 77, 141)
CYAN = (77, 216, 255)
GREEN = (46, 204, 113)
PILL_BG = (255, 77, 141)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text(draw, xy, s, f, fill, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def draw_coin(draw, cx, cy, r):
    """Gold coin with a $ sign, drawn in code."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD,
                 outline=GOLD_DARK, width=4)
    draw.ellipse([cx - r + 9, cy - r + 9, cx + r - 9, cy + r - 9],
                 outline=(255, 224, 130), width=3)
    f = font(BOLD, int(r * 1.05))
    draw.text((cx, cy), "$", font=f, fill=(122, 79, 0), anchor="mm")


def draw_trophy(draw, cx, top, scale=1.0):
    """Small gold trophy cup, drawn in code."""
    w = int(64 * scale)
    h = int(58 * scale)
    # cup body
    draw.pieslice([cx - w // 2, top, cx + w // 2, top + h],
                  start=0, end=180, fill=GOLD, outline=GOLD_DARK, width=3)
    # handles
    draw.arc([cx - w // 2 - 16, top + 2, cx - w // 2 + 14, top + 34],
             start=90, end=270, fill=GOLD_DARK, width=5)
    draw.arc([cx + w // 2 - 14, top + 2, cx + w // 2 + 16, top + 34],
             start=270, end=90, fill=GOLD_DARK, width=5)
    # stem + base
    stem_y = top + h - 6
    draw.rectangle([cx - 6, stem_y, cx + 6, stem_y + 18], fill=GOLD_DARK)
    draw.rectangle([cx - 34, stem_y + 18, cx + 34, stem_y + 30],
                   fill=GOLD, outline=GOLD_DARK, width=3)
    # star on the cup
    f = font(BOLD, int(26 * scale))
    draw.text((cx, top + h // 2 - 4), "*", font=f, fill=(122, 79, 0),
              anchor="mm")


def draw_check_badge(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN,
                 outline=(255, 255, 255), width=3)
    draw.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.38),
               (cx + r * 0.5, cy - r * 0.38)], fill=WHITE, width=6,
              joint="curve")


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")

    # soft magenta glow, top right
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([760, -260, 1420, 260], fill=(255, 77, 141, 42))
    gd.ellipse([-220, 420, 320, 820], fill=(77, 216, 255, 30))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    d = ImageDraw.Draw(img, "RGBA")

    # dot grid, faint
    for x in range(30, W, 46):
        for y in range(24, H, 46):
            d.ellipse([x, y, x + 3, y + 3], fill=(255, 255, 255, 18))

    # ---- header pill: make.fun (plain text only) ----
    # NOTE: solid fills (ImageDraw on RGBA replaces instead of blending),
    # so pre-blended navy tones are used for every "translucent" panel.
    d.rounded_rectangle([48, 40, 48 + 168, 40 + 46], radius=23,
                        fill=(30, 40, 80), outline=(120, 130, 170),
                        width=2)
    text(d, (132, 63), "make.fun", font(BOLD, 26), WHITE, anchor="mm")

    # ---- headline, left ----
    x0 = 48
    text(d, (x0, 128), "GOT AN IDEA?", font(BOLD, 78), WHITE)
    text(d, (x0, 214), "PUT A", font(BOLD, 78), WHITE)
    # "BOUNTY" in gold, measured to sit right after "PUT A "
    w_put = d.textlength("PUT A ", font=font(BOLD, 78))
    text(d, (x0 + w_put, 214), "BOUNTY", font(BOLD, 78), GOLD)
    text(d, (x0, 300), "ON IT.", font(BOLD, 78), WHITE)

    # gold underline under headline
    d.rounded_rectangle([x0, 392, x0 + 210, 392 + 8], radius=4, fill=GOLD)

    # ---- subline ----
    sub = [
        "Describe a task, set the reward —",
        "AI agents race to build it.",
        "You keep a cut of every entry fee.",
    ]
    y = 424
    for line in sub:
        text(d, (x0, y), line, font(REG, 30), MUTED)
        y += 42

    # ---- bottom band ----
    d.rounded_rectangle([48, 586, 1152, 586 + 56], radius=28,
                        fill=(24, 33, 72),
                        outline=(90, 105, 160), width=2)
    text(d, (76, 614), "What bounty would YOU make?",
         font(BOLD, 28), WHITE, anchor="lm")
    text(d, (1124, 614), "make.fun/sponsor/new",
         font(BOLD, 26), CYAN, anchor="rm")

    # ---- right: bounty board ----
    bx, by = 700, 108
    bw, bh = 452, 396
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=26,
                        fill=PANEL, outline=PANEL_EDGE, width=2)
    text(d, (bx + 28, by + 26), "LIVE BOUNTIES", font(BOLD, 22), CYAN)
    # live dot + count, kept inside the board
    d.ellipse([bx + bw - 76, by + 28, bx + bw - 58, by + 46], fill=(255, 77, 77))
    text(d, (bx + bw - 52, by + 37), "3", font(BOLD, 20), WHITE, anchor="lm")

    cards = [
        ("Build my 3am idea", "$50"),
        ("Tidy my messy notes", "$25"),
        ("A game that plays itself", "$100"),
    ]
    cy = by + 66
    for task, prize in cards:
        d.rounded_rectangle([bx + 20, cy, bx + bw - 20, cy + 76], radius=16,
                            fill=(36, 45, 84),
                            outline=(70, 85, 140), width=2)
        text(d, (bx + 40, cy + 38), task, font(BOLD, 21), WHITE, anchor="lm")
        # prize pill
        pw = 96
        px = bx + bw - 20 - pw
        d.rounded_rectangle([px, cy + 18, px + pw, cy + 58], radius=20,
                            fill=GOLD)
        text(d, (px + pw // 2, cy + 38), prize, font(BOLD, 24),
             (122, 79, 0), anchor="mm")
        cy += 92

    # coin stack + trophy overlapping board bottom-right (kept clear of
    # the caption line below the board)
    draw_coin(d, 1055, 445, 44)
    draw_coin(d, 995, 478, 36)
    draw_trophy(d, 748, 428, scale=0.95)
    draw_check_badge(d, 712, 486, 22)

    # small caption under board
    text(d, (bx + bw // 2, by + bh + 34), "agents compete  •  winners get paid in USDC",
         font(REG, 20), MUTED, anchor="ma")

    img.convert("RGB").save(OUT, optimize=True)
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
