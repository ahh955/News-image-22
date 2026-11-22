#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261122 (v3 rebuild).

A 1024x1024 newspaper front page summing up the world news of
Sunday 22 November 2026 in the news-21 v2 newspaper style: big serif
date headline, stat strip, 3 ILLUSTRATED leads, a feature grid with
coloured header strips, a world map with numbered dots, a numbered
"ALSO ON SUNDAY" list of briefs, a red DATE CHECK box — plus the v2
4D depth treatment (drop shadows, bevel, gradients) and a VOICES
strip with figures speaking real sourced quotes only.

33 stories: 3 leads + 12 features + 18 briefs. Every story happened,
or was first reported, on Sunday 22 November 2026 in at least one
time zone.

Deterministic: no randomness, no clock, no network. Running it
twice produces byte-identical output (PIL writes no timestamps
into the PNG).

Usage: python3 compose.py [output-path]   (default: entry.png)
"""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
CW = W - 2 * MARGIN  # 996, content width

# Palette: light paper, black ink, newspaper red.
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (179, 32, 44)
DARK = (31, 31, 31)
GREY = (110, 108, 100)
LINE = (200, 192, 172)
CARD = (255, 252, 244)
MAP_BG = (239, 231, 211)
MAP_LAND = (183, 167, 126)
WHITE = (255, 255, 255)
SHADOW = (214, 208, 194)
SHADOW_SOFT = (227, 222, 210)
TAG_CONFIRMED = (27, 120, 70)
TAG_OFFICIAL = (30, 90, 160)
TAG_REPORTED = (176, 106, 12)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_STRIP = font("DejaVuSans-Bold.ttf", 12)
F_TITLE = font("DejaVuSerif-Bold.ttf", 38)
F_MAST = font("DejaVuSerif-Bold.ttf", 50)
F_STAT_NUM = font("DejaVuSans-Bold.ttf", 26)
F_STAT_LBL = font("DejaVuSans.ttf", 11)
F_REGION = font("DejaVuSans-Bold.ttf", 13)
F_KICKER = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 17)
F_LEAD_DECK = font("DejaVuSans.ttf", 12)
F_FEAT_STRIP = font("DejaVuSans-Bold.ttf", 12)
F_FEAT_HEAD = font("DejaVuSans-Bold.ttf", 12)
F_FEAT_DECK = font("DejaVuSans.ttf", 10)
F_SOURCE = font("DejaVuSans.ttf", 10)
F_SOURCE_SM = font("DejaVuSans.ttf", 9)
F_SECTION = font("DejaVuSans-Bold.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_BRIEF_SMALL = font("DejaVuSans.ttf", 10)
F_LEGEND = font("DejaVuSans.ttf", 9)
F_PIN = font("DejaVuSans-Bold.ttf", 7)
F_PIN2 = font("DejaVuSans-Bold.ttf", 6)
F_DATE_HEAD = font("DejaVuSans-Bold.ttf", 14)
F_DATE_BODY = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 9)
F_BUBBLE = font("DejaVuSans.ttf", 10)
F_BUBBLE_SM = font("DejaVuSans-Bold.ttf", 8)
F_VOICES = font("DejaVuSans-Bold.ttf", 9)
F_ART_SMALL = font("DejaVuSans-Bold.ttf", 8)
F_ART_TITLE = font("DejaVuSans-Bold.ttf", 20)

TAG_COLORS = {
    "CONFIRMED": TAG_CONFIRMED,
    "OFFICIAL": TAG_OFFICIAL,
    "REPORTED": TAG_REPORTED,
}

# Truncation warnings collected while drawing; printed at the end so a
# build that silently cuts text is never mistaken for a clean one.
WARNINGS = []


# ---------------------------------------------------------------- stories
# Tags: CONFIRMED (2+ outlets), OFFICIAL (on the record),
# REPORTED (single-source claim).

LEADS = [
    {
        "kicker": "WAR IN UKRAINE  ·  OVERNIGHT",
        "headline": "Biggest strike yet on Lviv: 50+ missiles, ~500 drones",
        "deck": "Five killed, incl. a family of four in Lapaivka; parts of "
                "Lviv dark. Poland scrambled jets.",
        "tag": "CONFIRMED",
        "source": "Reuters · AP",
        "art": "lviv",
    },
    {
        "kicker": "CLIMATE  ·  COP31, ANTALYA",
        "headline": "COP31 nears a deal — and admits 1.5°C is lost",
        "deck": "New package to a late-night plenary; objections by 03:00 "
                "GMT, approval 06:00 GMT.",
        "tag": "CONFIRMED",
        "source": "Reuters",
        "art": "cop31",
    },
    {
        "kicker": "FORMULA 1  ·  LAS VEGAS GP",
        "headline": "Verstappen wins in Vegas — both McLarens thrown out",
        "deck": "Norris and Piastri disqualified for skid-block wear — a "
                "dramatic title twist.",
        "tag": "CONFIRMED",
        "source": "Sky Sports",
        "art": "f1",
    },
]

FEATURES = [
    {
        "strip": "STILL BURNING", "color": (140, 47, 47),
        "headline": "Sparta II ablaze in the Gulf of Finland",
        "deck": "Hit by two suspected drones Sat.; still burning Sun. off "
                "Loviisa. 16 crew evacuated.",
        "tag": "CONFIRMED", "source": "ANI · Reuters",
    },
    {
        "strip": "5,700 VOTERS", "color": (30, 70, 140),
        "headline": "Hong Kong votes for the committee that picks its leader",
        "deck": "Polls 9am–6pm. 5,700 voters elect the 1,500-member "
                "committee picking the leader.",
        "tag": "OFFICIAL", "source": "info.gov.hk",
    },
    {
        "strip": "FIRST TRIP ABROAD", "color": (176, 106, 12),
        "headline": "Nepal's PM lands in Delhi on first trip abroad",
        "deck": "Balendra Shah begins a two-day state visit; talks with "
                "Modi on Monday.",
        "tag": "CONFIRMED", "source": "IANS · MEA",
    },
    {
        "strip": "FINAL TODAY 18:00", "color": (27, 120, 70),
        "headline": "Alcaraz v Zverev for the ATP Finals crown",
        "deck": "Singles final 18:00 CET; doubles 15:00 CET. Sinner "
                "withdrew, knee injury.",
        "tag": "CONFIRMED", "source": "ATP",
    },
    {
        "strip": "629-6 · DAY FOUR", "color": (140, 40, 40),
        "headline": "Pant's 128 puts India in charge",
        "deck": "Pant's ninth Test century powered India to 629-6 at "
                "lunch on day four.",
        "tag": "CONFIRMED", "source": "Reuters",
    },
    {
        "strip": "CHRIST THE KING", "color": (110, 70, 150),
        "headline": "Pope Leo XIV: Angelus for Christ the King",
        "deck": "At noon CET the Pope leads the Angelus for Christ the "
                "King and World Youth Day.",
        "tag": "OFFICIAL", "source": "Vatican",
    },
    {
        "strip": "1,300 GUESTS", "color": (15, 118, 110),
        "headline": "Pope has lunch with 1,300 poor people",
        "deck": "Guests from 20+ Rome charities served by Red Cross "
                "volunteers in Paul VI Hall.",
        "tag": "OFFICIAL", "source": "Vatican",
    },
    {
        "strip": "15TH BATCH", "color": (40, 60, 120),
        "headline": "SpaceX launches spy satellites today",
        "deck": "Falcon 9 lifts off with the 15th NRO batch. Booster "
                "B1097 flies a 14th time.",
        "tag": "CONFIRMED", "source": "SpaceX · VSFB",
    },
    {
        "strip": "60% CHANCE", "color": (60, 100, 140),
        "headline": "Storm bearing down on East Coast — could become 'Kyle'",
        "deck": "A low off Florida tracks up the coast; NHC gives it a "
                "60% chance of naming.",
        "tag": "OFFICIAL", "source": "NHC",
    },
    {
        "strip": "SUBS ROW", "color": (110, 110, 40),
        "headline": "Australia hits back at US report on AUKUS subs",
        "deck": "Defence Minister Marles criticised the US Budget Office "
                "over its subs report.",
        "tag": "CONFIRMED", "source": "Reuters",
    },
    {
        "strip": "SUNDAY NIGHT", "color": (150, 40, 40),
        "headline": "Sunday Night Football comes to Mexico City",
        "deck": "Vikings (7-2) v 49ers (8-1) — NFC seeding on the line. "
                "49ers favoured by 3.",
        "tag": "CONFIRMED", "source": "CBS Sports",
    },
    {
        "strip": "POCHETTINO DEBUT", "color": (178, 30, 42),
        "headline": "Pochettino's first game: Man Utd at Liverpool",
        "deck": "Pochettino takes charge of Man Utd for the first time "
                "at Anfield.",
        "tag": "CONFIRMED", "source": "Sportradar",
    },
]

BRIEFS = [
    "MYANMAR M4.1 — early Sun. (02:35 IST), depth 95 km (NCS)",
    "PHILIPPINES — M4.6 off Balut Is. 08:23; M2.0 after (PHIVOLCS)",
    "INDONESIA — Heavy-rain alert: 12 provinces 'Siaga' (BMKG)",
    "JAPAN — 'UFO Village' Iino cashes in on alien tourism (ABC)",
    "NBA — Seven games tonight; Celtics at Warriors 8:30 PM",
    "SINGAPORE — China's VP Ding arrives for 2-day visit",
    "SCO — First Civilizational Dialogue Forum ends in Delhi",
    "VICTORIA — Six days to polls; Coalition ahead 56–44",
    "LA LIGA — Barcelona–Villarreal 13:00; Getafe–Atlético 20:00",
    "SERIE A — Juventus–Venezia 11:30; Atalanta–Inter 19:45",
    "GERMANY & FRANCE — Augsburg–Mainz; Marseille–Le Mans",
    "FRANCE — Métro Line 6 shut all day; blockades go on",
    "NFL WK 12 — Eleven games; Dolphins at Bills 1:00 PM ET",
    "IRGC CLAIMS IT HIT 2 US PATRIOT RADARS (REPORTED, ANI)",
    "UAE — President receives US Homeland Security chief (WAM)",
    "ISRAEL — Eisenkot invites Likud to coalition talks (ANI)",
    "DUBAI — Icons of Porsche festival opens (WAM)",
    "GANGA — India–Bangladesh water talks, day 2 in Dhaka",
]

STATS = [
    ("50+", "missiles on Lviv"),
    ("~500", "drones overnight"),
    ("06:00", "COP31 approval GMT"),
    ("629-6", "India, day four"),
    ("1,300", "at Pope's lunch"),
    ("33", "stories, all today"),
]

REGIONS = [
    ("EUROPE", 11), ("ASIA", 9), ("MIDDLE EAST", 4),
    ("AMERICAS", 6), ("OCEANIA", 3),
]

DATE_CHECK = (
    "Every story here happened, or was first reported, on Sunday 22 November "
    "2026. Deliberately NOT included — they happened earlier: Peru quake "
    "M6.7/M6.8 (Fri) · Banda Sea quake M6.8 (Sat) · EU–Indonesia deal signed "
    "(Sat) · 'Chapo Isidro' raid (Fri) · Bolsonaro in ICU (Sat) · Iran "
    "strikes on Bahrain (Sat night) · Basra power fire (Sat) · BepiColombo "
    "at Mercury (Sat) · Lviv station strike (Fri — a different attack)"
)

FOOTER = [
    "Every story happened, or was first reported, on Sunday 22 November 2026 in at least one time zone.",
    "Sources: Reuters · AP · Sky Sports · PHIVOLCS · NCS · BMKG · NHC · Vatican · SpaceX · IANS · MEA · info.gov.hk · CBS Sports · ANI · WAM · Finnish Border Guard — make.fun news-image-20261122",
    "Tags: CONFIRMED = verified by 2+ outlets  ·  OFFICIAL = on the record  ·  REPORTED = single-source claim.",
]


# ---------------------------------------------------------------- helpers

def wrap(d, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def cap_lines(d, lines, max_n, fnt, max_w, where=""):
    """Cap wrapped lines at max_n, truncating the last with an ellipsis."""
    if len(lines) <= max_n:
        return lines
    WARNINGS.append("TRUNCATED (%s): %r" % (where, " ".join(lines)))
    lines = lines[:max_n]
    last = lines[-1]
    while last and d.textlength(last + "…", font=fnt) > max_w:
        last = last[:-1]
    lines[-1] = last + "…"
    return lines


def fit_one_line(d, text, fnt, small_fnt, max_w, where=""):
    """Return (text, font) that fits max_w: shrink once, then truncate."""
    if d.textlength(text, font=fnt) <= max_w:
        return text, fnt
    if d.textlength(text, font=small_fnt) <= max_w:
        return text, small_fnt
    WARNINGS.append("TRUNCATED (%s): %r" % (where, text))
    ell = "…"
    while text and d.textlength(text + ell, font=small_fnt) > max_w:
        text = text[:-1]
    return text + ell, small_fnt


def vgrad(d, box, c_top, c_bot):
    """Vertical gradient fill of box from c_top to c_bot (deterministic)."""
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / (h - 1) if h > 1 else 0
        c = tuple(int(c_top[k] + (c_bot[k] - c_top[k]) * t)
                  for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def emboss_text(d, xy, text, fnt, fill, hi, dx=0, dy=1):
    """Text with a 1px offset underlay for a raised (4D) look."""
    d.text((xy[0] + dx, xy[1] + dy), text, font=fnt, fill=hi)
    d.text(xy, text, font=fnt, fill=fill)


def card_shadow(d, box):
    """Soft two-layer drop shadow behind a card (draw before the card)."""
    x0, y0, x1, y1 = box
    d.rectangle([x0 + 3, y0 + 4, x1 + 3, y1 + 4], fill=SHADOW_SOFT)
    d.rectangle([x0 + 2, y0 + 3, x1 + 2, y1 + 3], fill=SHADOW)


def draw_tag(d, x, y, tag):
    """Small coloured verification tag, right-aligned at x."""
    color = TAG_COLORS[tag]
    w = d.textlength(tag, font=F_BUBBLE_SM)
    d.text((x - w, y), tag, font=F_BUBBLE_SM, fill=color)


# ---------------------------------------------------------------- lead art
# Three small procedural scenes, one per lead. All shapes are drawn in code.

def art_lviv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 34, 40))
    cx, cy = x + w // 2, y + h // 2 - 2
    for i in range(10):
        ang = math.pi * 2 * i / 10
        r1, r2 = 9, 27
        d.line([(cx + r1 * math.cos(ang), cy + r1 * math.sin(ang) * 0.8),
                (cx + r2 * math.cos(ang), cy + r2 * math.sin(ang) * 0.8)],
               fill=(255, 170, 40), width=3)
    d.ellipse([cx - 17, cy - 12, cx + 17, cy + 12], fill=(255, 200, 60))
    d.ellipse([cx - 9, cy - 7, cx + 9, cy + 7], fill=(255, 240, 180))
    for dx, dy, r in [(-110, -14, 6), (112, -12, 6), (-118, 12, 5),
                      (118, 14, 7)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                  fill=(120, 116, 110))
    for dx, dy in [(-88, -18), (88, -20), (-96, 6), (96, 2)]:
        d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2],
                  fill=WHITE)
    # Rooftop silhouettes along the bottom.
    base = y + h
    for tx, th, tw in [(6, 10, 26), (36, 14, 20), (240, 12, 24),
                       (268, 16, 22)]:
        d.rectangle([x + tx, base - th, x + tx + tw, base], fill=(18, 16, 20))
    label = "LIVE FROM LVIV"
    lw = int(d.textlength(label, font=F_ART_SMALL)) + 12
    d.rounded_rectangle([x + 6, base - 20, x + 6 + lw, base - 6], radius=3,
                        fill=RED)
    d.text((x + 12, base - 18), label, font=F_ART_SMALL, fill=WHITE)


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 77, 74))
    # Globe: blue disc with green blobs.
    cx, cy, r = x + 52, y + h // 2 + 2, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 165, 200),
              outline=(220, 235, 225), width=2)
    d.ellipse([cx - 14, cy - 16, cx + 2, cy - 2], fill=(110, 168, 110))
    d.ellipse([cx - 2, cy + 4, cx + 16, cy + 18], fill=(110, 168, 110))
    d.ellipse([cx + 6, cy - 18, cx + 18, cy - 6], fill=(110, 168, 110))
    # Clock: white face, hands at 06:00 — the approval hour.
    qx, qy, qr = x + w - 52, y + h // 2 + 2, 22
    d.ellipse([qx - qr, qy - qr, qx + qr, qy + qr], fill=(247, 243, 234),
              outline=(220, 235, 225), width=2)
    d.line([(qx, qy), (qx, qy - 15)], fill=INK, width=3)
    d.line([(qx, qy), (qx, qy + 12)], fill=INK, width=3)
    d.ellipse([qx - 3, qy - 3, qx + 3, qy + 3], fill=RED)
    d.text((x + w // 2, y + 10), "DEAL NEARS", font=F_ART_TITLE, fill=WHITE,
           anchor="ma")
    d.text((x + w // 2, y + 38), "APPROVAL 06:00 GMT", font=F_KICKER,
           fill=(255, 190, 190), anchor="ma")


def art_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
    for sx, sy in [(30, 8), (70, 14), (240, 8), (280, 16), (200, 6)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    # Chequered flag, top left.
    d.line([(x + 10, y + 4), (x + 10, y + 34)], fill=(200, 200, 200), width=2)
    for r in range(3):
        for c in range(4):
            fill = DARK if (r + c) % 2 == 0 else WHITE
            d.rectangle([x + 12 + c * 8, y + 5 + r * 8,
                         x + 20 + c * 8, y + 13 + r * 8], fill=fill)
    # Speed lines.
    for ly, lx0, lx1 in [(22, 52, 96), (30, 44, 96), (38, 56, 96)]:
        d.line([(x + lx0, y + ly), (x + lx1, y + ly)],
               fill=(255, 200, 60), width=2)
    # Race car silhouette (navy, yellow wing accents).
    bx, by = x + 104, y + 30
    d.rectangle([bx, by - 12, bx + 6, by + 2], fill=(255, 200, 60))
    d.rectangle([bx - 6, by - 14, bx + 12, by - 10], fill=(255, 200, 60))
    d.rounded_rectangle([bx, by - 2, bx + 116, by + 8], radius=4,
                        fill=(30, 50, 130))
    d.rounded_rectangle([bx + 44, by - 10, bx + 66, by - 2], radius=3,
                        fill=(30, 50, 130))
    d.rectangle([bx + 112, by + 4, bx + 126, by + 7], fill=(255, 200, 60))
    for wx in (bx + 24, bx + 88):
        d.ellipse([wx - 8, by + 2, wx + 8, by + 18], fill=(10, 10, 12))
        d.ellipse([wx - 3, by + 7, wx + 3, by + 13], fill=(160, 160, 160))
    d.text((x + w - 8, y + 38), "04:00 UTC SUN", font=F_ART_SMALL,
           fill=(255, 200, 60), anchor="ra")
    d.text((x + w - 8, y + 8), "VEGAS", font=F_KICKER, fill=WHITE,
           anchor="ra")


ART = {"lviv": art_lviv, "cop31": art_cop31, "f1": art_f1}


# ---------------------------------------------------------------- figures

def draw_person(d, x, y, w, h, skin, hair, suit, helmet=None, tie=None):
    """Small stylized head-and-shoulders figure in an (x, y, w, h) box."""
    dd = min(w - 6, 18)  # head diameter
    cx = x + w // 2
    hy = y + 1
    d.rounded_rectangle([x, y + h - 14, x + w, y + h], radius=4, fill=suit)
    d.rectangle([cx - 3, hy + dd - 3, cx + 3, hy + dd + 2], fill=skin)
    d.ellipse([cx - dd // 2, hy, cx + dd // 2, hy + dd], fill=skin)
    top = helmet if helmet else hair
    d.pieslice([cx - dd // 2, hy, cx + dd // 2, hy + dd], start=180,
               end=360, fill=top)
    if helmet:
        d.rectangle([cx - dd // 2 - 2, hy + dd // 2 - 1,
                     cx + dd // 2 + 2, hy + dd // 2 + 2], fill=helmet)
    ex = dd // 4
    ey = hy + dd // 2 + 1
    d.ellipse([cx - ex - 1, ey, cx - ex + 1, ey + 2], fill=INK)
    d.ellipse([cx + ex - 1, ey, cx + ex + 1, ey + 2], fill=INK)
    if tie:
        d.polygon([(cx - 3, y + h - 13), (cx + 3, y + h - 13),
                   (cx, y + h - 3)], fill=tie)


def draw_bubble(d, x, y, w, h, tail_to, fill=WHITE, outline=INK):
    """Speech bubble: rounded rect + tail pointing at tail_to."""
    tx, ty = tail_to
    d.polygon([(x + 8, y + h - 7), (x + 3, y + h - 2), (tx, ty)], fill=fill)
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=fill,
                        outline=outline, width=1)
    d.line([(x + 8, y + h - 7), (tx, ty)], fill=outline, width=1)
    d.line([(x + 3, y + h - 2), (tx, ty)], fill=outline, width=1)


# ---------------------------------------------------------------- world map
# Coarse equirectangular land mask: 60 columns of 6 degrees of longitude,
# 30 rows of 5 degrees of latitude (90N down to 60S). Each row lists the
# inclusive column ranges that hold land. Drawn as a dotted halftone map.

LAND = [
    [],
    [(15, 16), (22, 25)],
    [(10, 16), (20, 26), (31, 34), (37, 39), (45, 47)],
    [(2, 6), (9, 16), (20, 23), (40, 59)],
    [(2, 6), (7, 20), (32, 59)],
    [(2, 6), (7, 20), (26, 26), (30, 59)],
    [(4, 20), (29, 59)],
    [(9, 20), (28, 53), (56, 56)],
    [(9, 19), (29, 53)],
    [(9, 18), (29, 51), (53, 53)],
    [(9, 17), (28, 53)],
    [(10, 16), (28, 53)],
    [(11, 16), (27, 39), (41, 44), (46, 50)],
    [(11, 15), (27, 39), (41, 49)],
    [(12, 15), (27, 35), (37, 39), (42, 43), (45, 48), (50, 50)],
    [(14, 16), (27, 32), (35, 37), (42, 43), (46, 48), (50, 51)],
    [(15, 21), (27, 32), (35, 37), (46, 49), (51, 54)],
    [(17, 21), (31, 37), (45, 49), (51, 54)],
    [(16, 22), (31, 36), (46, 49), (51, 54)],
    [(16, 24), (32, 36), (47, 49), (52, 54)],
    [(17, 23), (32, 36), (51, 54)],
    [(18, 23), (32, 36), (37, 38), (50, 54)],
    [(18, 22), (32, 35), (37, 37), (49, 55)],
    [(18, 22), (32, 35), (49, 55)],
    [(18, 21), (33, 34), (49, 55), (57, 59)],
    [(17, 20), (53, 54), (57, 59)],
    [(17, 19), (57, 58)],
    [(17, 19)],
    [(17, 18)],
    [(18, 18)],
]

# Numbered pins for the leads + most features. Pin 4 (Sparta II) is nudged
# north-east of Loviisa so it clears pin 1 (Lviv). No pin for 7 (ATP
# final, Turin — would collide with pin 9, Rome) or 11 (SpaceX,
# Vandenberg — would collide with pin 3, Las Vegas); the legend says so.
PINS = [
    (1, 49.8, 24.0),    # Lviv strike
    (2, 36.9, 30.7),    # COP31, Antalya
    (3, 36.1, -115.2),  # F1, Las Vegas
    (4, 63.5, 30.0),    # Sparta II, Gulf of Finland (nudged)
    (5, 22.3, 114.2),   # Hong Kong votes
    (6, 28.6, 77.2),    # Nepal PM in Delhi
    (8, -41.3, 174.8),  # Pant 128, Wellington
    (9, 41.9, 12.5),    # Vatican, Rome (stories 9-10)
    (12, 28.0, -80.0),  # Storm Kyle, off Florida
    (13, -35.3, 149.1), # AUKUS, Canberra
    (14, 19.4, -99.1),  # NFL, Mexico City
    (15, 53.4, -3.0),   # Man Utd at Liverpool
]

LEGEND_COLS = [
    ["1 Lviv strike", "2 COP31, Antalya", "3 F1, Las Vegas",
     "4 Sparta II ablaze"],
    ["5 HK votes", "6 Delhi visit", "8 Pant 128, NZ",
     "9–10 Vatican, Rome"],
    ["12 Storm Kyle", "13 AUKUS, Canberra", "14 NFL, Mexico City",
     "15 Man Utd, Anfield"],
]
LEGEND_NOTE = "7 ATP final (Turin) · 11 SpaceX launch — no pin"


def draw_map(d, x0, y0, w, h):
    card_shadow(d, [x0, y0, x0 + w, y0 + h])
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG, outline=LINE, width=1)
    for r, ranges in enumerate(LAND):
        cy = y0 + (r + 0.5) / 30 * h
        for c0, c1 in ranges:
            for c in range(c0, c1 + 1):
                cx = x0 + (c + 0.5) / 60 * w
                d.ellipse([cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7],
                          fill=MAP_LAND)
    for num, lat, lon in PINS:
        px = x0 + (lon + 180) / 360 * w
        py = y0 + (90 - lat) / 150 * h
        r = 5.5
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=WHITE, width=1)
        fnt = F_PIN if num < 10 else F_PIN2
        d.text((px, py - 1), str(num), font=fnt, fill=WHITE, anchor="mm")


# ---------------------------------------------------------------- sections

def top_strip(d):
    text = ("33 STORIES  ·  5 REGIONS  ·  3 LEADS  ·  12 FEATURES  ·  "
            "18 IN BRIEF  ·  EVERY ONE DATED — SUNDAY 22 NOVEMBER 2026")
    d.text((W // 2, 8), text, font=F_STRIP, fill=GREY, anchor="ma")
    d.line([(MARGIN, 28), (W - MARGIN, 28)], fill=LINE, width=1)


def title_block(d):
    d.text((W // 2, 34), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK,
           anchor="ma")
    title = "Sunday 22 November 2026"
    tw = d.textlength(title, font=F_MAST)
    emboss_text(d, ((W - tw) / 2, 76), title, F_MAST, INK, WHITE)
    d.line([(MARGIN, 132), (W - MARGIN, 132)], fill=RED, width=3)


def stat_strip(d, y):
    sh = 54
    cell_w = CW // 6
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + i * cell_w
        card_shadow(d, [cx, y, cx + cell_w - 1, y + sh])
        d.rectangle([cx, y, cx + cell_w - 1, y + sh], fill=CARD,
                    outline=LINE, width=1)
        d.line([(cx + 1, y + 1), (cx + cell_w - 2, y + 1)], fill=WHITE)
        d.text((cx + cell_w // 2, y + 3), num, font=F_STAT_NUM, fill=RED,
               anchor="ma")
        d.text((cx + cell_w // 2, y + 34), label, font=F_STAT_LBL,
               fill=(60, 60, 60), anchor="ma")
    return y + sh


def region_strip(d, y):
    vgrad(d, [MARGIN, y, W - MARGIN, y + 22], (52, 52, 56), (26, 26, 28))
    region_text = "   ·   ".join("%s %d" % (name, n) for name, n in REGIONS)
    d.text((W // 2, y + 4), region_text, font=F_REGION, fill=WHITE,
           anchor="ma")
    return y + 22


def draw_lead(d, x, y, w, h, lead):
    card_shadow(d, [x, y, x + w, y + h])
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.line([(x + 1, y + 1), (x + w - 1, y + 1)], fill=WHITE)
    ART[lead["art"]](d, x + 6, y + 6, w - 12, 56)
    tx = x + 12
    tw = w - 24
    ty = y + 66
    d.text((tx, ty), lead["kicker"], font=F_KICKER, fill=RED)
    draw_tag(d, x + w - 12, ty + 2, lead["tag"])
    ty += 14
    for line in cap_lines(d, wrap(d, lead["headline"], F_LEAD_HEAD, tw),
                          2, F_LEAD_HEAD, tw, lead["kicker"]):
        emboss_text(d, (tx, ty), line, F_LEAD_HEAD, INK, WHITE)
        ty += 19
    ty += 2
    for line in cap_lines(d, wrap(d, lead["deck"], F_LEAD_DECK, tw),
                          2, F_LEAD_DECK, tw, lead["kicker"]):
        d.text((tx, ty), line, font=F_LEAD_DECK, fill=(60, 60, 60))
        ty += 13
    d.text((tx, y + h - 13), "Source: " + lead["source"], font=F_SOURCE,
           fill=GREY)


def leads_row(d, y):
    lh = 158
    lead_w, lead_gap = 325, 10
    for i, lead in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + lead_gap)
        draw_lead(d, lx, y, lead_w, lh, lead)
    return y + lh


def draw_feature(d, x, y, w, h, feat):
    card_shadow(d, [x, y, x + w, y + h])
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.line([(x + 1, y + 1), (x + w - 1, y + 1)], fill=WHITE)
    strip_h = 22
    d.rectangle([x, y, x + w, y + strip_h], fill=feat["color"])
    d.text((x + w // 2, y + 4), feat["strip"], font=F_FEAT_STRIP,
           fill=WHITE, anchor="ma")
    tx = x + 7
    tw = w - 14
    ty = y + strip_h + 4
    for line in cap_lines(d, wrap(d, feat["headline"], F_FEAT_HEAD, tw),
                          2, F_FEAT_HEAD, tw, feat["strip"]):
        d.text((tx, ty), line, font=F_FEAT_HEAD, fill=INK)
        ty += 14
    ty += 1
    for line in cap_lines(d, wrap(d, feat["deck"], F_FEAT_DECK, tw),
                          2, F_FEAT_DECK, tw, feat["strip"]):
        d.text((tx, ty), line, font=F_FEAT_DECK, fill=(60, 60, 60))
        ty += 11
    d.text((tx, y + h - 12), "%s · %s" % (feat["tag"], feat["source"]),
           font=F_SOURCE_SM, fill=GREY)


def features_grid(d, y):
    cols = 4
    gap = 7
    cell_w = (CW - gap * (cols - 1)) // cols  # 243
    cell_h = 88
    row_gap = 6
    for idx, feat in enumerate(FEATURES):
        r, c = divmod(idx, cols)
        x0 = MARGIN + c * (cell_w + gap)
        y0 = y + r * (cell_h + row_gap)
        draw_feature(d, x0, y0, cell_w, cell_h, feat)
    return y + 3 * cell_h + 2 * row_gap


def voices_strip(d, y):
    # Two figures with speech bubbles. Both quotes are verbatim from
    # Sunday-dated wires: Zelenskyy via ANI (Kyiv), Kurum via Reuters
    # (Antalya). No invented speech anywhere.
    h = 38
    x0, x1 = MARGIN, MARGIN + CW
    card_shadow(d, [x0, y, x1, y + h])
    d.rectangle([x0, y, x1, y + h], fill=CARD, outline=LINE, width=1)
    d.line([(x0 + 1, y + 1), (x1 - 1, y + 1)], fill=WHITE)
    d.text((x0 + 8, y + 13), "VOICES", font=F_VOICES, fill=RED)
    zx = x0 + 52
    draw_person(d, zx, y + 2, 30, 34, skin=(224, 184, 150),
                hair=(60, 45, 35), suit=(74, 86, 60))
    quote = ("\u201cNATO membership remains the clearest security "
             "guarantee\u201d")
    zbw = int(d.textlength(quote, font=F_BUBBLE)) + 16
    zbx = zx + 34
    draw_bubble(d, zbx, y + 4, zbw, 30, (zx + 24, y + 12))
    d.text((zbx + 8, y + 7), quote, font=F_BUBBLE, fill=INK)
    d.text((zbx + 8, y + 19), "\u2014 Zelenskyy, Kyiv \u00b7 ANI",
           font=F_BUBBLE_SM, fill=GREY)
    cx = zbx + zbw + 8
    draw_person(d, cx, y + 2, 26, 34, skin=(200, 160, 130),
                hair=(120, 120, 125), suit=(40, 60, 110), tie=(179, 32, 44))
    quote2 = ("\u201cWe believe that we have put forward a text which all "
              "the parties can agree upon.\u201d")
    cbw = int(d.textlength(quote2, font=F_BUBBLE)) + 16
    cbx = cx + 30
    draw_bubble(d, cbx, y + 4, cbw, 30, (cx + 20, y + 12))
    d.text((cbx + 8, y + 7), quote2, font=F_BUBBLE, fill=INK)
    d.text((cbx + 8, y + 19),
           "\u2014 Kurum, COP31 president \u00b7 approval 06:00 GMT",
           font=F_BUBBLE_SM, fill=GREY)
    return y + h


def lower_band(d, y):
    # Headers.
    d.text((MARGIN, y), "WHERE IT HAPPENED", font=F_SECTION, fill=INK)
    d.text((336, y), "ALSO ON SUNDAY — 18 MORE STORIES", font=F_SECTION,
           fill=INK)
    d.line([(MARGIN, y + 18), (326, y + 18)], fill=INK, width=1)
    d.line([(336, y + 18), (W - MARGIN, y + 18)], fill=INK, width=1)
    cy = y + 22
    # Map + legend (left).
    draw_map(d, MARGIN, cy, 312, 120)
    ly = cy + 124
    for col, items in enumerate(LEGEND_COLS):
        lx = MARGIN + col * 104
        for i, item in enumerate(items):
            d.text((lx, ly + i * 10), item, font=F_LEGEND,
                   fill=(60, 60, 60))
    d.text((MARGIN, ly + 42), LEGEND_NOTE, font=F_LEGEND, fill=GREY)
    map_end = ly + 42 + 10
    # Briefs: 2 columns of 9 (right).
    col_w = 329
    for col in range(2):
        bx = 336 + col * (col_w + 16)
        for row in range(9):
            brief = BRIEFS[col * 9 + row]
            text, fnt = fit_one_line(d, "%d. %s" % (col * 9 + row + 1, brief),
                                     F_BRIEF, F_BRIEF_SMALL, col_w,
                                     "brief %d" % (col * 9 + row + 1))
            d.text((bx, cy + row * 19), text, font=fnt, fill=INK)
    briefs_end = cy + 9 * 19
    return max(map_end, briefs_end)


def date_check(d, y):
    lines = wrap(d, DATE_CHECK, F_DATE_BODY, CW - 24)
    box_h = 8 + 16 + 2 + len(lines) * 13 + 6
    card_shadow(d, [MARGIN, y, MARGIN + CW, y + box_h])
    d.rectangle([MARGIN, y, MARGIN + CW, y + box_h], fill=CARD,
                outline=RED, width=3)
    d.text((MARGIN + 12, y + 6), "✓  DATE CHECK", font=F_DATE_HEAD,
           fill=RED)
    head2 = "— Sunday, 22 November 2026 only"
    d.text((MARGIN + 12 + d.textlength("✓  DATE CHECK  ", font=F_DATE_HEAD),
            y + 6), head2, font=F_DATE_HEAD, fill=INK)
    ty = y + 6 + 16 + 2
    for line in lines:
        d.text((MARGIN + 12, ty), line, font=F_DATE_BODY, fill=INK)
        ty += 13
    return y + box_h


def footer(d, y):
    ty = y + 1
    for line in FOOTER:
        w = d.textlength(line, font=F_FOOT)
        d.text(((W - w) / 2, ty), line, font=F_FOOT, fill=GREY)
        ty += 12
    return ty


# ---------------------------------------------------------------- assembly

def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    top_strip(d)
    title_block(d)
    y = 138
    y = stat_strip(d, y)
    y += 4
    y = region_strip(d, y)
    y += 6
    y = leads_row(d, y)
    y += 4
    y = features_grid(d, y)
    y += 4
    y = voices_strip(d, y)
    y += 4
    y = lower_band(d, y)
    y += 4
    y = date_check(d, y)
    y += 2
    y = footer(d, y)
    if y > H:
        raise SystemExit("layout overflow: used %d px of %d" % (y, H))
    img.save(path, format="PNG", optimize=True)
    print("wrote %s (%d px used)" % (path, y))
    if WARNINGS:
        print("WARNINGS (%d):" % len(WARNINGS))
        for w in WARNINGS:
            print("  " + w)
    else:
        print("no truncation warnings")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
