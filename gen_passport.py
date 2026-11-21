#!/usr/bin/env python3
"""Generate entry.png: an invented passport spread for the Republic of Velmora.

A small alpine republic that does not exist. Left page: data page with a
drawn portrait, holder details and a machine-readable zone. Right page:
arrival/departure stamps from three neighbouring (invented) countries, a
visa-condition stamp and a mountain-rescue fee stamp. All stamp dates fall
after the passport's issue date (12 JUN 2025).

Deterministic: fixed seed, fixed fonts, fixed layout. Run:
    python3 gen_passport.py   -> writes entry.png (1024x1024) next to this file.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

random.seed(20261121)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

NAVY = (28, 42, 74)
NAVY_SOFT = (52, 68, 104)
INK = (32, 32, 34)
GREY = (104, 104, 100)
PAPER = (244, 238, 224)
PAPER_L = (233, 226, 208)
GOLD = (150, 112, 44)
BLUE_INK = (28, 74, 140)
RED_INK = (168, 44, 44)
PURPLE_INK = (96, 52, 128)
GREEN_INK = (34, 110, 74)


def font(path, size):
    return ImageFont.truetype(path, size)


def text(d, xy, s, f, fill, anchor="la"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def mrz_check(s):
    """ICAO 9303 check digit: weights 7,3,1; A=10..Z=35, '<'=0."""
    vals = {c: i for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
    total = 0
    for i, ch in enumerate(s):
        v = 0 if ch == "<" else vals[ch]
        total += v * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    # Line 1: document type, issuing state, name (44 chars).
    name = "VOSS<<MARA<ELENA"
    line1 = ("P<VLM" + name).ljust(44, "<")
    # Line 2: passport no + check, nationality, DOB + check, sex,
    # expiry + check, personal number + check (44 chars).
    doc = "VM4839201"
    dob = "940314"
    exp = "350612"
    personal = "<" * 14
    core = (
        doc + mrz_check(doc)
        + "VLM"
        + dob + mrz_check(dob)
        + "F"
        + exp + mrz_check(exp)
        + personal + mrz_check(personal)
    )
    # Position 44 is the composite check digit over the checked fields.
    line2 = core + mrz_check(core)
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


def draw_portrait(size=(176, 196)):
    """Stylised head-and-shoulders portrait of Mara Elena Voss, a Velmoran
    woman in her early thirties, dark hair, folk-pattern scarf."""
    w, h = size
    img = Image.new("RGB", size, (176, 196, 214))
    d = ImageDraw.Draw(img, "RGBA")
    # soft background gradient + faint guilloche arcs
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)],
               fill=(int(176 - 30 * t), int(196 - 34 * t), int(214 - 30 * t)))
    for r in range(30, 260, 18):
        d.arc([w // 2 - r, -20 - r // 3, w // 2 + r, 120 + r // 3],
              200, 340, fill=(255, 255, 255, 26))
    cx = w // 2
    # shoulders / jacket
    d.pieslice([cx - 88, h - 78, cx + 88, h + 60], 180, 360, fill=(58, 64, 84))
    d.polygon([(cx - 88, h), (cx - 52, h - 66), (cx - 30, h - 52),
               (cx - 30, h), ], fill=(58, 64, 84))
    d.polygon([(cx + 88, h), (cx + 52, h - 66), (cx + 30, h - 52),
               (cx + 30, h), ], fill=(58, 64, 84))
    # folk-pattern scarf (deep red with gold diamonds)
    d.polygon([(cx - 46, h - 58), (cx + 46, h - 58), (cx + 58, h - 34),
               (cx - 58, h - 34)], fill=(122, 34, 40))
    for sx in range(cx - 44, cx + 45, 16):
        d.polygon([(sx, h - 52), (sx + 6, h - 46), (sx, h - 40),
                   (sx - 6, h - 46)], fill=(212, 168, 84))
    # shirt collar
    d.polygon([(cx - 16, h - 58), (cx + 16, h - 58), (cx, h - 34)],
              fill=(238, 232, 216))
    # neck
    d.rectangle([cx - 13, h - 118, cx + 13, h - 52], fill=(214, 172, 138))
    d.polygon([(cx - 13, h - 74), (cx + 13, h - 74), (cx + 13, h - 58),
               (cx - 13, h - 58)], fill=(188, 142, 110))
    # head
    d.ellipse([cx - 34, h - 178, cx + 34, h - 96], fill=(222, 180, 146))
    # ears
    d.ellipse([cx - 40, h - 148, cx - 30, h - 128], fill=(222, 180, 146))
    d.ellipse([cx + 30, h - 148, cx + 40, h - 128], fill=(222, 180, 146))
    # hair: dark brown bob framing the face
    d.pieslice([cx - 40, h - 186, cx + 40, h - 108], 180, 360,
               fill=(62, 42, 30))
    d.polygon([(cx - 40, h - 150), (cx - 34, h - 92), (cx - 22, h - 96),
               (cx - 26, h - 146)], fill=(62, 42, 30))
    d.polygon([(cx + 40, h - 150), (cx + 34, h - 92), (cx + 22, h - 96),
               (cx + 26, h - 146)], fill=(62, 42, 30))
    d.ellipse([cx - 36, h - 184, cx + 36, h - 138], fill=(62, 42, 30))
    # fringe
    d.pieslice([cx - 34, h - 178, cx + 34, h - 138], 180, 360,
               fill=(62, 42, 30))
    d.ellipse([cx - 34, h - 178, cx + 34, h - 146], fill=(62, 42, 30))
    # eyebrows
    d.arc([cx - 24, h - 142, cx - 6, h - 130], 200, 340, fill=(52, 36, 26),
          width=2)
    d.arc([cx + 6, h - 142, cx + 24, h - 130], 200, 340, fill=(52, 36, 26),
          width=2)
    # eyes
    d.ellipse([cx - 21, h - 136, cx - 9, h - 128], fill=(255, 255, 255))
    d.ellipse([cx + 9, h - 136, cx + 21, h - 128], fill=(255, 255, 255))
    d.ellipse([cx - 18, h - 135, cx - 12, h - 129], fill=(52, 38, 28))
    d.ellipse([cx + 12, h - 135, cx + 18, h - 129], fill=(52, 38, 28))
    # nose + mouth
    d.line([(cx, h - 130), (cx - 2, h - 116), (cx + 3, h - 114)],
           fill=(190, 146, 116), width=2)
    d.arc([cx - 9, h - 110, cx + 9, h - 100], 20, 160, fill=(150, 84, 78),
          width=2)
    # cheeks
    d.ellipse([cx - 30, h - 122, cx - 18, h - 112], fill=(226, 158, 132))
    d.ellipse([cx + 18, h - 122, cx + 30, h - 112], fill=(226, 158, 132))
    return img


def draw_emblem(d, cx, cy, s):
    """Velmora's arms: a shield with three peaks under a star."""
    w, h = int(s * 0.72), s
    x0, y0 = cx - w // 2, cy - h // 2
    d.polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + int(h * 0.62)),
               (cx, y0 + h), (x0, y0 + int(h * 0.62))],
              outline=GOLD, width=3)
    d.polygon([(x0 + 4, y0 + 4), (x0 + w - 4, y0 + 4),
               (x0 + w - 4, y0 + int(h * 0.60)), (cx, y0 + h - 5),
               (x0 + 4, y0 + int(h * 0.60))], fill=(38, 66, 110))
    # three peaks
    d.polygon([(x0 + 8, y0 + int(h * 0.66)), (x0 + int(w * 0.30), y0 + int(h * 0.34)),
               (x0 + int(w * 0.46), y0 + int(h * 0.66))], fill=(240, 238, 230))
    d.polygon([(x0 + int(w * 0.38), y0 + int(h * 0.66)),
               (cx, y0 + int(h * 0.26)),
               (x0 + int(w * 0.66), y0 + int(h * 0.66))], fill=(240, 238, 230))
    d.polygon([(x0 + int(w * 0.58), y0 + int(h * 0.66)),
               (x0 + int(w * 0.78), y0 + int(h * 0.40)),
               (x0 + w - 8, y0 + int(h * 0.66))], fill=(240, 238, 230))
    # star above the peaks
    sx, sy, r = cx, y0 + int(h * 0.20), 5
    pts = []
    for i in range(10):
        ang = -90 + i * 36
        rr = r if i % 2 == 0 else r * 0.42
        import math
        pts.append((sx + rr * math.cos(math.radians(ang)),
                    sy + rr * math.sin(math.radians(ang))))
    d.polygon(pts, fill=(212, 168, 84))


def field(d, x, y, label, value, label_f, value_f, vfill=INK, width=250):
    text(d, (x, y), label, label_f, GREY)
    text(d, (x, y + 15), value, value_f, vfill)


def stamp(img, box, angle, colour, lines, small_lines=(), star=True):
    """Draw a rotated rectangular border stamp onto img (RGBA overlay)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    sd.rectangle([20, 20, 20 + w, 20 + h], outline=colour + (235,), width=3)
    sd.rectangle([24, 24, 20 + w - 4, 20 + h - 4], outline=colour + (200,),
                 width=1)
    cx = 20 + w // 2
    cy = 20 + 14
    if star:
        import math
        pts = []
        for i in range(10):
            ang = -90 + i * 36
            rr = 8 if i % 2 == 0 else 3.4
            pts.append((cx + rr * math.cos(math.radians(ang)),
                        cy + rr * math.sin(math.radians(ang))))
        sd.polygon(pts, fill=colour + (220,))
    y = 20 + 30
    for i, ln in enumerate(lines):
        f = font(SANS_B, 17) if i == 0 else font(SANS_B, 15)
        sd.text((cx, y), ln, font=f, fill=colour + (235,), anchor="ma")
        y += 20 if i == 0 else 19
    for ln in small_lines:
        sd.text((cx, y), ln, font=font(SANS, 11),
                fill=colour + (220,), anchor="ma")
        y += 14
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.paste(layer, (x0 - 20, y0 - 20), layer)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # paper grain
    for _ in range(2600):
        x, y = random.randrange(W), random.randrange(H)
        v = random.choice([(0, 0, 0, 7), (255, 255, 255, 9)])
        d.point((x, y), fill=v)

    # faint watermark: mountain range across the whole spread
    wm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wm)
    wd.polygon([(0, 1024), (120, 700), (260, 880), (420, 620), (580, 900),
                (760, 640), (900, 860), (1024, 720), (1024, 1024)],
               fill=(38, 66, 110, 14))
    img.paste(wm, (0, 0), wm)
    d = ImageDraw.Draw(img, "RGBA")

    # outer frame + gutter
    d.rectangle([10, 10, 1013, 1013], outline=NAVY, width=3)
    d.rectangle([16, 16, 1007, 1007], outline=NAVY, width=1)
    d.rectangle([508, 10, 516, 1013], fill=(200, 192, 172))
    d.line([512, 10, 512, 1013], fill=NAVY, width=1)

    # ================= LEFT PAGE: data page =================
    LX, LW = 32, 448          # left page content x, width
    CX = LX + LW // 2         # centre of left page

    text(d, (CX, 30), "REPUBLIC OF VELMORA", font(SERIF_B, 27), NAVY,
         anchor="ma")
    text(d, (CX, 62), "REPUBLIKA VELMORA  ·  PASSPORT  ·  PASPOORT",
         font(SANS, 11), NAVY_SOFT, anchor="ma")
    d.line([LX + 40, 84, LX + LW - 40, 84], fill=GOLD, width=2)
    draw_emblem(d, CX, 118, 52)

    # type / code / number row
    y = 152
    for x, lab, val in ((LX, "TYPE / TIP", "P"),
                        (LX + 150, "CODE / KOD", "VLM"),
                        (LX + 300, "No. / No.", "VM 4839201")):
        text(d, (x, y), lab, font(SANS, 10), GREY)
        text(d, (x, y + 13), val, font(SANS_B, 16), INK)
    d.line([LX, 186, LX + LW, 186], fill=NAVY_SOFT, width=1)

    # portrait
    portrait = draw_portrait((176, 196))
    img.paste(portrait, (LX + 6, 200))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([LX + 6, 200, LX + 182, 396], outline=NAVY, width=2)
    d.rectangle([LX + 10, 204, LX + 178, 392], outline=(255, 255, 255, 90),
                width=1)
    text(d, (LX + 94, 402), "PHOTO  ·  FOTO", font(SANS, 9), GREY,
         anchor="ma")

    # fields right of portrait
    fx = LX + 198
    field(d, fx, 200, "SURNAME / FAMILIJENAM", "VOSS",
          font(SANS, 10), font(SANS_B, 17))
    field(d, fx, 244, "GIVEN NAMES / VORNAAM", "MARA ELENA",
          font(SANS, 10), font(SANS_B, 17))
    field(d, fx, 288, "NATIONALITY / NASIONALITEIT", "VELMORAN",
          font(SANS, 10), font(SANS_B, 17))
    field(d, fx, 332, "DATE OF BIRTH / GEBOORTEDATUM", "14 MAR 1994",
          font(SANS, 10), font(SANS_B, 17))
    field(d, fx, 376, "SEX / GESLAG", "F",
          font(SANS, 10), font(SANS_B, 17))

    # lower fields, two columns
    y = 440
    field(d, LX, y, "PLACE OF BIRTH / GEBOORTEPLEK", "ALDHAVEN, VELMORA",
          font(SANS, 10), font(SANS_B, 16))
    field(d, LX + 250, y, "PLACE OF ISSUE / UITGIFPLEK", "ALDHAVEN",
          font(SANS, 10), font(SANS_B, 16))
    y = 484
    field(d, LX, y, "DATE OF ISSUE / UITGIFDATUM", "12 JUN 2025",
          font(SANS, 10), font(SANS_B, 16))
    field(d, LX + 250, y, "DATE OF EXPIRY / VERVALDATUM", "12 JUN 2035",
          font(SANS, 10), font(SANS_B, 16))
    y = 528
    field(d, LX, y, "AUTHORITY / OUTORITEIT",
          "MINISTRY OF THE INTERIOR", font(SANS, 10), font(SANS_B, 15))
    # signature
    y = 580
    text(d, (LX, y), "HOLDER'S SIGNATURE / HANDTEKENING", font(SANS, 10),
         GREY)
    d.line([LX, y + 40, LX + 250, y + 40], fill=INK, width=1)
    text(d, (LX + 4, y + 14), "Mara Elena Voss",
         font(SERIF, 22), (52, 52, 60))
    # small note under signature
    text(d, (LX + 268, y + 8), "HEIGHT  168 cm\nEYES  BROWN\nHAIR  DARK BROWN",
         font(SANS, 11), INK)

    # machine-readable zone
    d.line([LX, 660, LX + LW, 660], fill=NAVY_SOFT, width=1)
    text(d, (LX, 672), "MACHINE-READABLE ZONE", font(SANS, 10), GREY)
    l1, l2 = mrz_lines()
    text(d, (LX, 692), l1, font(MONO, 15), INK)
    text(d, (LX, 714), l2, font(MONO, 15), INK)
    # MRZ background band
    d.rectangle([LX - 4, 688, LX + LW + 4, 736], outline=(180, 172, 150),
                width=1)
    # passport number repeated, bottom of data page
    text(d, (LX, 760), "PASSPORT No. VM 4839201  ·  ISSUED AT ALDHAVEN",
         font(SANS, 10), NAVY_SOFT)
    text(d, (LX, 778), "VALID FOR ALL COUNTRIES EXCEPT WHERE ENDORSED",
         font(SANS, 10), NAVY_SOFT)
    # guilloche strip at bottom of left page
    for i in range(0, LW, 12):
        d.arc([LX + i - 14, 800, LX + i + 14, 828], 0, 180,
              fill=(38, 66, 110, 60))
    text(d, (CX, 852), "—  THIS PASSPORT REMAINS THE PROPERTY OF THE "
         "REPUBLIC OF VELMORA  —", font(SANS, 9), GREY, anchor="ma")

    # ================= RIGHT PAGE: visas & stamps =================
    RX, RW = 540, 448
    RCX = RX + RW // 2
    text(d, (RCX, 30), "VISAS", font(SERIF_B, 27), NAVY, anchor="ma")
    text(d, (RCX, 62), "VISUMS  ·  PAGE 12", font(SANS, 11), NAVY_SOFT,
         anchor="ma")
    d.line([RX + 40, 84, RX + RW - 40, 84], fill=GOLD, width=2)

    # four border stamps, 2 x 2 grid, dates all after issue 12 JUN 2025
    stamp(img, (RX + 6, 104, RX + 212, 214), -3, BLUE_INK,
          ["KESSARIN", "ARRIVAL", "28 AUG 2025"],
          ["Port of Venn  ·  Border Post 4"])
    stamp(img, (RX + 236, 104, RX + 442, 214), 2, RED_INK,
          ["KESSARIN", "DEPARTURE", "03 SEP 2025"],
          ["Port of Venn  ·  Border Post 4"])
    stamp(img, (RX + 6, 238, RX + 212, 348), 3, GREEN_INK,
          ["VALDRIS", "ARRIVAL", "17 JAN 2026"],
          ["Valdris Intl Airport  ·  Gate 2"])
    stamp(img, (RX + 236, 238, RX + 442, 348), -2, BLUE_INK,
          ["DRAVENHOLD", "ARRIVAL", "02 APR 2026"],
          ["High Pass  ·  Border Post 9"])
    d = ImageDraw.Draw(img, "RGBA")

    # visa-condition box: the telling paperwork detail
    d.rectangle([RX, 380, RX + RW, 540], outline=PURPLE_INK, width=3)
    d.rectangle([RX + 4, 384, RX + RW - 4, 536], outline=PURPLE_INK, width=1)
    text(d, (RCX, 392), "CONDITION OF STAY — VELMORA",
         font(SANS_B, 15), PURPLE_INK, anchor="ma")
    cond = ("The holder must register with the Mountain Warden\n"
            "within 7 days of arrival. No paid work in the high\n"
            "pastures without a herding permit. Straying beyond\n"
            "the marked trails is at the holder's own risk.")
    text(d, (RX + 16, 418), cond, font(SANS, 13), PURPLE_INK)
    text(d, (RCX, 512), "—  MINISTRY OF THE INTERIOR, ALDHAVEN  —",
         font(SANS, 10), PURPLE_INK, anchor="ma")

    # fee stamp, rotated, clear of the observations text at left
    stamp(img, (RX + 268, 588, RX + 442, 674), -7, RED_INK,
          ["FEE PAID", "40 VELMAR"],
          ["Mountain Rescue Levy"], star=False)
    d = ImageDraw.Draw(img, "RGBA")
    # small observation note, handwritten style (serif italic feel)
    text(d, (RX + 6, 566), "Observations / Opmerkings:", font(SANS_B, 12),
         INK)
    text(d, (RX + 6, 588),
         "Holder is a registered\nmountain guide. Carries a\nherding permit, class II.",
         font(SERIF, 14), (52, 52, 60))
    d.line([RX, 690, RX + RW, 690], fill=NAVY_SOFT, width=1)
    text(d, (RX, 702), "PREVIOUS JOURNEYS", font(SANS_B, 12), NAVY)
    text(d, (RX, 722),
         "2024  Kessarin — summer crossing, High Pass\n"
         "2023  Valdris — winter school, Lake Tarn",
         font(SANS, 12), INK)
    d.line([RX, 770, RX + RW, 770], fill=NAVY_SOFT, width=1)
    text(d, (RCX, 788), "VELMORA  ·  ALDHAVEN  ·  EST. 1847",
         font(SANS, 11), NAVY_SOFT, anchor="ma")
    text(d, (RCX, 810), "One people, three peaks, one road home.",
         font(SERIF, 13), NAVY_SOFT, anchor="ma")
    # small emblem, bottom right page
    draw_emblem(d, RCX, 872, 46)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
