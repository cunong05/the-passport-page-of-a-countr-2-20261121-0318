#!/usr/bin/env python3
"""Draw 'The Passport Page of a Country That Isn't There' — an invented
passport spread for the Republic of Talveria. Renders 1024x1024 PNG.
Run: python3 draw.py  (writes entry.png next to this script)
Deterministic: same input -> same bytes (no timestamps, no randomness).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# ---------- fonts ----------
def font(name, size):
    paths = {
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serif_i": "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "mono_b": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    }
    return ImageFont.truetype(paths[name], size)

# ---------- palette ----------
INK = (31, 42, 68)          # dark navy
INK_SOFT = (58, 66, 92)
GREY = (110, 108, 96)
PAPER = (246, 241, 227)
PAPER_EDGE = (232, 224, 204)
DESK1 = (43, 52, 66)
DESK2 = (30, 37, 50)
GOLD = (176, 141, 63)
BLUE_STAMP = (43, 74, 143)
RED_STAMP = (163, 51, 39)
GREEN_STAMP = (46, 107, 69)

# ---------- MRZ check digits ----------
VALS = {c: i for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
VALS["<"] = 0

def check_digit(s):
    w = (7, 3, 1)
    return str(sum(VALS[c] * w[i % 3] for i, c in enumerate(s)) % 10)

def mrz_lines():
    line1 = "P<TALMERIDIAN<<ELENA<MARA"
    line1 = line1 + "<" * (44 - len(line1))
    doc = "TAL004821"
    dob = "880314"
    exp = "340601"
    pers = "<" * 14
    l2 = (doc + check_digit(doc) + "TAL" + dob + check_digit(dob) + "F"
          + exp + check_digit(exp) + pers + check_digit(pers))
    comp = (doc + check_digit(doc) + "TAL" + dob + check_digit(dob) + "F"
            + exp + check_digit(exp) + pers + check_digit(pers))
    l2 += check_digit(comp)
    assert len(line1) == 44 and len(l2) == 44, (len(line1), len(l2))
    return line1, l2

# ---------- helpers ----------
def guilloche(d, box, color, amp=3, step=7, wavelength=46):
    x0, y0, x1, y1 = box
    for yy in range(y0, y1, step):
        pts = []
        for x in range(x0, x1 + 1, 4):
            pts.append((x, yy + amp * math.sin((x - x0) / wavelength * 2 * math.pi)))
        d.line(pts, fill=color, width=1)

def stamp(d, cx, cy, w, h, angle, color, lines, title_size=17, line_size=15):
    """Rectangular double-border stamp, rotated, semi-transparent ink."""
    sw, sh = w + 40, h + 40
    layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    sd.rectangle([4, 4, sw - 5, sh - 5], outline=color + (235,), width=3)
    sd.rectangle([10, 10, sw - 11, sh - 11], outline=color + (200,), width=1)
    f_t = font("sans_b", title_size)
    f_l = font("sans", line_size)
    y = 16
    for i, txt in enumerate(lines):
        f = f_t if i == 0 else f_l
        tw = sd.textlength(txt, font=f)
        sd.text(((sw - tw) / 2, y), txt, font=f, fill=color + (225,))
        y += title_size + 4 if i == 0 else line_size + 5
    layer = layer.rotate(angle, expand=False, resample=Image.BICUBIC)
    return layer, (int(cx - sw / 2), int(cy - sh / 2))

def paste_stamp(base_img, layer, pos):
    base_img.alpha_composite(layer, pos)

def coat_of_arms(d, cx, cy, s):
    """Small shield: navy shield, gold star above waves."""
    # shield
    shield = [(cx - 0.42 * s, cy - 0.30 * s), (cx + 0.42 * s, cy - 0.30 * s),
              (cx + 0.42 * s, cy + 0.10 * s), (cx, cy + 0.48 * s),
              (cx - 0.42 * s, cy + 0.10 * s)]
    d.polygon(shield, fill=(255, 255, 255, 0), outline=INK, width=3)
    d.polygon(shield, fill=(31, 42, 68, 255))
    # gold star
    sx, sy, r = cx, cy - 0.08 * s, 0.16 * s
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        star.append((sx + rr * math.cos(ang), sy + rr * math.sin(ang)))
    d.polygon(star, fill=GOLD)
    # waves
    for k, yy in enumerate((0.14, 0.24)):
        pts = []
        for x in range(int(cx - 0.34 * s), int(cx + 0.35 * s), 3):
            pts.append((x, cy + yy * s + 3 * math.sin((x - cx) / 9)))
        d.line(pts, fill=(240, 238, 225), width=2)

def portrait(img, d, box):
    x0, y0, x1, y1 = box
    # draw on a layer so nothing bleeds outside the photo frame
    layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    p = ImageDraw.Draw(layer)
    Wl, Hl = x1 - x0, y1 - y0
    # photo background: pale blue-grey, plain (a printed photo, not a target)
    p.rectangle([0, 0, Wl, Hl], fill=(214, 222, 228, 255))
    # shoulders
    p.pieslice([-30, Hl - 95, Wl + 30, Hl + 60], start=180, end=360, fill=INK + (255,))
    p.rectangle([-30, Hl - 55, Wl + 30, Hl], fill=INK + (255,))
    # neck
    p.rectangle([78, Hl - 128, 118, Hl - 60], fill=INK + (255,))
    # head profile facing left: forehead, nose, lips, chin, jaw
    head = [(96, 16), (74, 28), (64, 48), (58, 64), (44, 86), (56, 94),
            (54, 102), (58, 108), (66, 118), (86, 128),
            (112, 128), (120, 110), (126, 60), (116, 24)]
    p.polygon(head, fill=INK + (255,))
    # hair: cap over the back/top of the head + bun
    p.ellipse([102, 8, 136, 42], fill=INK + (255,))
    p.pieslice([80, 2, 132, 68], start=270, end=90, fill=INK + (255,))
    p.ellipse([112, 32, 138, 58], fill=INK + (255,))
    # paste clipped to the box, then frame
    img.alpha_composite(layer, (x0, y0))
    d.rectangle(box, outline=INK, width=2)
    d.rectangle([x0 - 4, y0 - 4, x1 + 4, y1 + 4], outline=INK, width=1)

# ---------- build ----------
img = Image.new("RGBA", (W, H), DESK2 + (255,))
d = ImageDraw.Draw(img, "RGBA")
# desk gradient
for yy in range(H):
    t = yy / H
    c = tuple(int(DESK1[i] + (DESK2[i] - DESK1[i]) * t) for i in range(3))
    d.line([(0, yy), (W, yy)], fill=c)

# spread shadow
d.rectangle([28, 118, 996, 908], fill=(0, 0, 0, 90))
# pages
LX0, LY0, LX1, LY1 = 34, 122, 502, 902
RX0, RY0, RX1, RY1 = 522, 122, 990, 902
d.rectangle([LX0, LY0, LX1, LY1], fill=PAPER)
d.rectangle([RX0, RY0, RX1, RY1], fill=PAPER)
# page edges
d.rectangle([LX0, LY0, LX1, LY1], outline=PAPER_EDGE, width=2)
d.rectangle([RX0, RY0, RX1, RY1], outline=PAPER_EDGE, width=2)
# gutter shadow
for i in range(14):
    a = 55 - i * 4
    d.line([(512 - i, LY0), (512 - i, LY1)], fill=(90, 80, 60, a), width=1)
    d.line([(512 + i, RY0), (512 + i, RY1)], fill=(90, 80, 60, a), width=1)

# guilloche inside pages
guilloche(d, (LX0 + 6, LY0 + 6, LX1 - 6, LY1 - 6), (196, 198, 184, 50))
guilloche(d, (RX0 + 6, RY0 + 6, RX1 - 6, RY1 - 6), (196, 198, 184, 50))

# faint watermark compass on right page
cx, cy = 756, 420
for r in (120, 90, 60):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(31, 42, 68, 16), width=2)
for ang in range(0, 360, 45):
    a = math.radians(ang)
    d.line([(cx, cy), (cx + 118 * math.cos(a), cy + 118 * math.sin(a))],
           fill=(31, 42, 68, 13), width=1)

# ================= LEFT PAGE =================
# header
coat_of_arms(d, 268, 168, 46)
f_c = font("serif_b", 25)
t = "REPUBLIC OF TALVERIA"
tw = d.textlength(t, font=f_c)
d.text(((LX0 + LX1 - tw) / 2, 196), t, font=f_c, fill=INK)
f_s = font("sans", 13)
t = "RÉPUBLIQUE DE TALVERIA"
tw = d.textlength(t, font=f_s)
d.text(((LX0 + LX1 - tw) / 2, 228), t, font=f_s, fill=GREY)
f_p = font("serif_b", 30)
t = "PASSPORT"
tw = d.textlength(t, font=f_p)
d.text(((LX0 + LX1 - tw) / 2, 250), t, font=f_p, fill=INK)
f_s2 = font("sans", 12)
t = "PASSEPORT  ·  PASAPORTE"
tw = d.textlength(t, font=f_s2)
d.text(((LX0 + LX1 - tw) / 2, 286), t, font=f_s2, fill=GREY)
d.line([(LX0 + 24, 312), (LX1 - 24, 312)], fill=INK, width=2)
d.line([(LX0 + 24, 316), (LX1 - 24, 316)], fill=INK, width=1)

# portrait
portrait(img, d, (58, 336, 218, 526))
f_cap = font("sans", 11)
t = "PHOTOGRAPH"
tw = d.textlength(t, font=f_cap)
d.text(((58 + 218 - tw) / 2, 532), t, font=f_cap, fill=GREY)

# data fields: explicit columns inside the 240..490 strip
FX = 240
f_lab = font("sans", 11)
f_val = font("sans_b", 17)
rows = [
    [(0, "Type / Type", "P"), (68, "Code / Code", "TAL"), (128, "No. / Nº", "TAL 0048217")],
    [(0, "Surname / Nom", "MERIDIAN")],
    [(0, "Given names / Prénoms", "ELENA MARA")],
    [(0, "Nationality / Nationalité", "TALVERIAN")],
    [(0, "Date of birth / Né(e) le", "14 MAR 1988")],
    [(0, "Place of birth / Lieu de naissance", "PORT MERIDIAN")],
    [(0, "Sex / Sexe", "F"), (68, "Date of issue / Délivré le", "02 JUN 2024")],
    [(0, "Date of expiry / Expire le", "01 JUN 2034")],
    [(0, "Authority / Autorité", "MINISTRY OF THE SEA")],
]
y = 336
for row in rows:
    for dx, label, value in row:
        d.text((FX + dx, y), label, font=f_lab, fill=GREY)
        d.text((FX + dx, y + 14), value, font=f_val, fill=INK)
    y += 38
# signature (last row value ends ~672)
d.line([(FX, 706), (FX + 220, 706)], fill=INK, width=1)
f_sig = font("serif_i", 22)
d.text((FX, 676), "Elena Mara Meridian", font=f_sig, fill=INK_SOFT)
d.text((FX, 712), "Holder's signature / Signature du titulaire", font=f_lab, fill=GREY)

# MRZ band
d.rectangle([LX0 + 14, 748, LX1 - 14, 828], fill=(238, 234, 220))
l1, l2 = mrz_lines()
f_m = font("mono_b", 16)
d.text((LX0 + 28, 760), l1, font=f_m, fill=INK)
d.text((LX0 + 28, 790), l2, font=f_m, fill=INK)
# page number left
d.text((LX0 + 22, LY1 - 30), "1", font=font("sans", 12), fill=GREY)

# ================= RIGHT PAGE =================
f_h = font("serif_b", 24)
t = "VISAS"
tw = d.textlength(t, font=f_h)
d.text(((RX0 + RX1 - tw) / 2, 140), t, font=f_h, fill=INK)
f_s2 = font("sans", 12)
t = "VISA  ·  VISAS"
tw = d.textlength(t, font=f_s2)
d.text(((RX0 + RX1 - tw) / 2, 172), t, font=f_s2, fill=GREY)
d.line([(RX0 + 24, 196), (RX1 - 24, 196)], fill=INK, width=2)
d.line([(RX0 + 24, 200), (RX1 - 24, 200)], fill=INK, width=1)

# stamps
for args in [
    (640, 282, 230, 84, -6, BLUE_STAMP,
     ["MARSEILLE — FRANCE", "ENTRY  ·  12 SEP 2024", "Nº 4417"]),
    (865, 298, 200, 84, 5, RED_STAMP,
     ["TUNIS — TUNISIA", "ENTRY  ·  03 NOV 2024", "Nº 0912"]),
    (640, 470, 250, 84, 4, GREEN_STAMP,
     ["VALLETTA — MALTA", "ENTRY  ·  19 JAN 2025", "Nº 2208"]),
]:
    layer, pos = stamp(d, *args)
    paste_stamp(img, layer, pos)

# visa sticker
vx0, vy0, vx1, vy1 = 778, 400, 968, 556
d.rectangle([vx0, vy0, vx1, vy1], fill=(226, 232, 240))
d.rectangle([vx0, vy0, vx1, vy1], outline=INK_SOFT, width=2)
d.rectangle([vx0 + 5, vy0 + 5, vx1 - 5, vy1 - 5], outline=INK_SOFT, width=1)
f_vt = font("sans_b", 14)
f_vl = font("sans", 12)
d.text((vx0 + 12, vy0 + 12), "VISA", font=f_vt, fill=INK)
d.text((vx0 + 12, vy0 + 34), "REPUBLIC OF CALDONIA", font=f_vl, fill=INK_SOFT)
d.text((vx0 + 12, vy0 + 56), "Single entry", font=f_vl, fill=INK_SOFT)
d.text((vx0 + 12, vy0 + 76), "Valid 01 – 30 MAR 2025", font=f_vl, fill=INK_SOFT)
d.text((vx0 + 12, vy0 + 96), "Nº KV-7731", font=f_vl, fill=INK_SOFT)
d.text((vx0 + 12, vy0 + 122), "Port Meridian consul.", font=f_vl, fill=GREY)

# condition of issue box
bx0, by0, bx1, by1 = RX0 + 24, 600, RX1 - 24, 800
d.rectangle([bx0, by0, bx1, by1], fill=(250, 246, 236))
d.rectangle([bx0, by0, bx1, by1], outline=INK, width=2)
f_bt = font("sans_b", 16)
d.text((bx0 + 14, by0 + 12), "CONDITION OF ISSUE", font=f_bt, fill=INK)
f_b = font("sans", 16)
lines = [
    "This passport is valid for travel by sea only.",
    "Talveria has no airport. A harbour tax of",
    "12 shells is payable on arrival.",
    "",
    "Issued in Talverian and English.",
    "Délivré en talvérien et en anglais.",
]
yy = by0 + 40
for ln in lines:
    d.text((bx0 + 14, yy), ln, font=f_b, fill=INK_SOFT)
    yy += 22

# fee stamp overlapping the box's bottom-right corner, mostly below it
layer, pos = stamp(d, bx1 - 95, by1 + 12, 190, 56, -10, RED_STAMP,
                   ["HARBOUR TAX PAID", "12 SHELLS"], title_size=14, line_size=12)
paste_stamp(img, layer, pos)

# page number right
d.text((RX1 - 34, RY1 - 30), "2", font=font("sans", 12), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png")
