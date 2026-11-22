#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261122 (v4 rebuild).

A 1024x1024 newspaper front page summing up the world news of
Sunday 22 November 2026 in the news-21 v2 newspaper style: big serif
date headline, stat strip, 3 ILLUSTRATED leads, an "hour by hour"
timeline strip, a feature grid with ILLUSTRATED cards (a small
procedural scene on every card), a world map with numbered dots, a
numbered "ALSO ON SUNDAY" list of briefs, a red DATE CHECK box —
plus the v2 4D depth treatment (drop shadows, bevel, gradients) and
a VOICES strip with figures speaking real sourced quotes only.

34 stories: 3 leads + 12 features + 19 briefs across 7 regions.
Every story happened, or was first reported, on Sunday 22 November
2026 in at least one time zone. V4 fixes v3's one factual error (the
F1 lead was a 2025 story) and leads with the day's dominant story:
the Gulf war overnight.

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
F_TIMELINE_HEAD = font("DejaVuSans-Bold.ttf", 10)

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
        "kicker": "THE GULF WAR  ·  OVERNIGHT",
        "headline": "IRAN STRIKES U.S. BASES IN BAHRAIN",
        "deck": "Two waves of drones and missiles hit four US bases; "
                "three tankers struck in Hormuz.",
        "tag": "CONFIRMED",
        "source": "Fars · IRGC · UKMTO · Bahrain",
        "art": "gulf",
    },
    {
        "kicker": "WAR IN UKRAINE  ·  OVERNIGHT",
        "headline": "LVIV BURNS: 50+ MISSILES, ~500 DRONES",
        "deck": "Five dead, incl. a family of four; Poland scrambled "
                "jets; 73,000 lose power.",
        "tag": "CONFIRMED",
        "source": "Zelenskyy · Reuters",
        "art": "lviv",
    },
    {
        "kicker": "CLIMATE  ·  COP31, ANTALYA",
        "headline": "COP31: THE DEAL THAT ADMITS 1.5°C IS LOST",
        "deck": "Delegates vote at 06:00 GMT on a text with no "
                "fossil-fuel language; $120bn pledged.",
        "tag": "OFFICIAL",
        "source": "UNFCCC · UN News",
        "art": "cop31",
    },
]

FEATURES = [
    {
        "strip": "IRAN BLACKOUTS", "color": (30, 40, 80),
        "headline": "IRAN'S LIGHTS GO OUT",
        "deck": "Power cuts start today — two hours, war damage blamed.",
        "tag": "CONFIRMED", "source": "RFE/RL", "art": "blackout",
    },
    {
        "strip": "SPARTA II STILL BURNING", "color": (120, 30, 30),
        "headline": "SHIP STILL BURNING OFF FINLAND",
        "deck": "Two drones hit her Sat.; fire may burn for weeks. "
                "Crew safe.",
        "tag": "CONFIRMED", "source": "Finnish authorities",
        "art": "ship_fire",
    },
    {
        "strip": "HONG KONG VOTES", "color": (160, 30, 50),
        "headline": "HONG KONG PICKS ITS KINGMAKERS",
        "deck": "856 candidates chase 723 seats; long lines at 9am "
                "opening.",
        "tag": "CONFIRMED", "source": "SCMP", "art": "ballot",
    },
    {
        "strip": "NEPAL PM IN DELHI", "color": (180, 60, 30),
        "headline": "BALEN SHAH'S FIRST TRIP ABROAD",
        "deck": "Nepal's PM lands in Delhi today; seeks a $2bn aid "
                "package.",
        "tag": "CONFIRMED", "source": "Radio Nepal", "art": "plane",
    },
    {
        "strip": "ATP FINALS, TURIN", "color": (40, 100, 60),
        "headline": "ALCARAZ v ZVEREV FOR THE CROWN",
        "deck": "World No. 1 Zverev, yet to drop a set; final 18:00 CET.",
        "tag": "CONFIRMED", "source": "ATP", "art": "tennis",
    },
    {
        "strip": "PANT 128, WELLINGTON", "color": (30, 90, 140),
        "headline": "PANT'S 128 PUTS INDIA ON TOP",
        "deck": "India declare 720-9 v NZ; Pant first keeper with SENA "
                "tons.",
        "tag": "CONFIRMED", "source": "Cricinfo", "art": "cricket",
    },
    {
        "strip": "A POPE'S SUNDAY", "color": (150, 120, 40),
        "headline": "ANGELUS, THEN LUNCH FOR 1,300",
        "deck": "Leo XIV leads the Angelus, then dines with 1,300 poor.",
        "tag": "CONFIRMED", "source": "Vatican", "art": "pope",
    },
    {
        "strip": "SPACEX NROL-136", "color": (40, 40, 90),
        "headline": "SPY SATELLITES LIFT OFF TODAY",
        "deck": "Falcon 9 lifts the 15th NRO batch at 04:16 PT.",
        "tag": "CONFIRMED", "source": "SpaceX", "art": "rocket",
    },
    {
        "strip": "NFL IN MEXICO CITY", "color": (120, 30, 80),
        "headline": "VIKINGS v 49ERS AT 7,300 FEET",
        "deck": "NFC seeding on the line at Estadio Banorte, 8:20pm ET.",
        "tag": "CONFIRMED", "source": "NFL", "art": "football",
    },
    {
        "strip": "POCHETTINO'S DEBUT", "color": (140, 30, 30),
        "headline": "POCH'S UNITED BOW AT ANFIELD",
        "deck": "New boss takes charge of 18th-placed United at "
                "Liverpool.",
        "tag": "CONFIRMED", "source": "BBC", "art": "soccer",
    },
    {
        "strip": "F1 — LAS VEGAS GP", "color": (200, 30, 30),
        "headline": "VERSTAPPEN ON POLE IN VEGAS",
        "deck": "Antonelli fastest but penalised; race tonight, 04:00 "
                "GMT.",
        "tag": "CONFIRMED", "source": "F1", "art": "racecar",
    },
    {
        "strip": "AMPUTEE WORLD CUP", "color": (30, 120, 60),
        "headline": "GHANA v MOROCCO: AFRICA'S NIGHT",
        "deck": "First all-African final; a new champion is crowned.",
        "tag": "CONFIRMED", "source": "WAFF", "art": "trophy",
    },
]

BRIEFS = [
    "MYANMAR M4.1 — early Sun. (02:35 IST), depth 95 km (NCS)",
    "PHILIPPINES — M4.6 off Balut Is. 08:23; M2.0 after (PHIVOLCS)",
    "INDONESIA — Heavy-rain alert: 12 provinces 'Siaga' (BMKG)",
    "NBA — Seven games tonight; Celtics at Warriors 8:30 PM",
    "SINGAPORE — China's VP Ding arrives for 2-day visit",
    "SCO — First Civilizational Dialogue Forum ends in Delhi",
    "VICTORIA — Six days to polls; Coalition ahead 56–44",
    "LA LIGA — Barcelona–Villarreal 13:00; Getafe–Atlético 20:00",
    "SERIE A — Juventus–Venezia 11:30; Atalanta–Inter 19:45",
    "FRANCE — Métro Line 6 shut all day; blockades go on",
    "NFL WK 11 — Dolphins at Bills 1:00 PM ET; Bills -16.5",
    "HORMUZ — 14 Iranian tankers sail to break the blockade",
    "UAE — President receives US Homeland Security chief (WAM)",
    "ISRAEL — Eisenkot invites Likud to coalition talks (ANI)",
    "DUBAI — Icons of Porsche festival opens (WAM)",
    "GANGA — India–Bangladesh water talks, day 2 in Dhaka",
    "KYLE? — East Coast storm may briefly become 'Kyle'",
    "AUKUS — Marles: CBO 'wrong'; 'AUKUS is happening'",
    "SOMALIA — UAE envoy's 72-hour deadline expires today",
]

STATS = [
    ("4", "US bases hit, Bahrain"),
    ("50+", "missiles on Lviv"),
    ("06:00", "COP31 vote GMT"),
    ("720-9", "India declared"),
    ("1,300", "at Pope's lunch"),
    ("34", "stories, all today"),
]

REGIONS = [
    ("EUROPE", 8), ("ASIA", 8), ("MIDDLE EAST", 6),
    ("AMERICAS", 6), ("AFRICA", 2), ("OCEANIA", 3), ("GLOBAL", 1),
]

DATE_CHECK = (
    "Deliberately NOT included — they happened earlier: Peru quake "
    "(Fri) · Banda Sea quake (Sat) · EU–Indonesia deal (Sat) · "
    "'Chapo Isidro' raid (Fri) · Bolsonaro ICU (Sat) · Basra fire "
    "(Sat) · BepiColombo (Sat) · Lviv station strike (Fri) · Gaza "
    "tents appeal (15 Nov) · Hormuz talks (Fri–Sat). Gulf strikes: "
    "Sat 23:40 UTC = Sun 06:40 Jakarta — today's news in Asia."
)

FOOTER = [
    "Every story happened, or was first reported, on Sunday 22 November 2026 in at least one time zone.",
    "Sources: Reuters · AP · Fars · IRGC · UKMTO · RFE/RL · Vatican · SpaceX · SCMP · Radio Nepal · ATP · Cricinfo · NFL · BBC · F1 · WAFF · ANI · WAM · Finland — make.fun news-image-20261122",
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


def art_gulf(d, x, y, w, h):
    """Night over the Gulf: tanker silhouettes, missile trails, bursts."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 28))
    # Sea band along the bottom.
    sea_y = y + h - 12
    d.rectangle([x, sea_y, x + w, y + h], fill=(16, 34, 56))
    # Tanker silhouette, right of centre: dark hull + superstructure.
    bx, by = x + w - 130, sea_y
    d.polygon([(bx, by), (bx + 8, by - 10), (bx + 108, by - 10),
               (bx + 116, by)], fill=(8, 10, 18))
    d.rectangle([bx + 78, by - 22, bx + 100, by - 10], fill=(8, 10, 18))
    d.rectangle([bx + 86, by - 28, bx + 92, by - 22], fill=(8, 10, 18))
    # Second smaller ship, far left.
    sx = x + 18
    d.polygon([(sx, sea_y), (sx + 5, sea_y - 7), (sx + 58, sea_y - 7),
               (sx + 63, sea_y)], fill=(12, 16, 26))
    d.rectangle([sx + 40, sea_y - 14, sx + 52, sea_y - 7],
                fill=(12, 16, 26))
    # Missile trails: orange polylines with bright heads.
    for pts in [[(x + 40, y + 8), (x + 85, y + 22), (x + 130, y + 30)],
                [(x + 150, y + 6), (x + 185, y + 16), (x + 220, y + 26)],
                [(x + 235, y + 10), (x + 262, y + 18), (x + 290, y + 24)]]:
        d.line(pts, fill=(255, 150, 40), width=2, joint="curve")
        hx, hy = pts[-1]
        d.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=(255, 230, 150))
    # Explosion bursts (small starbursts).
    for cx, cy, r in [(x + 70, y + 20, 8), (x + 250, y + 14, 6)]:
        for i in range(8):
            ang = math.pi * 2 * i / 8
            d.line([(cx, cy), (cx + r * math.cos(ang),
                               cy + r * math.sin(ang))],
                   fill=(255, 170, 40), width=2)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 100))
    # "OVERNIGHT" chip, bottom-left.
    label = "OVERNIGHT"
    lw = int(d.textlength(label, font=F_ART_SMALL)) + 12
    base = y + h
    d.rounded_rectangle([x + 6, base - 20, x + 6 + lw, base - 6], radius=3,
                        fill=RED)
    d.text((x + 12, base - 18), label, font=F_ART_SMALL, fill=WHITE)


ART = {"lviv": art_lviv, "cop31": art_cop31, "gulf": art_gulf}


# ---------------------------------------------------------------- feature art
# New in v4: one small procedural scene per feature card, drawn in a
# 56x86 panel on the card's left. Each scene is ONE clear shape on a
# bold flat background — at 300px page scale a card is ~71x26px, so
# the art reads as a coloured block with one recognisable shape.

def art_blackout(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 24, 46))
    # Crescent moon, top-right.
    d.ellipse([x + w - 20, y + 6, x + w - 6, y + 20],
              fill=(240, 235, 200))
    d.ellipse([x + w - 23, y + 4, x + w - 9, y + 18], fill=(18, 24, 46))
    # Black skyline with a few lit windows.
    for bx, bh, bw in [(2, 30, 10), (14, 42, 12), (28, 26, 10),
                       (40, 36, 12)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                    fill=(5, 8, 16))
    for wx, wy in [(6, 62), (17, 52), (31, 66), (43, 58)]:
        d.rectangle([x + wx, y + wy, x + wx + 2, y + wy + 3],
                    fill=(255, 200, 60))


def art_ship_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 160, 170))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(40, 90, 140))
    # Smoke puffs above the fire.
    for cx, cy, r in [(x + 22, y + 22, 4), (x + 30, y + 16, 5),
                      (x + 26, y + 10, 3)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 125))
    # Flame tongues.
    d.polygon([(x + 16, y + 48), (x + 22, y + 28), (x + 28, y + 48)],
              fill=(255, 120, 20))
    d.polygon([(x + 26, y + 48), (x + 32, y + 32), (x + 38, y + 48)],
              fill=(255, 60, 20))
    # Hull + superstructure.
    d.polygon([(x + 6, y + 48), (x + 50, y + 48), (x + 44, y + 60),
               (x + 12, y + 60)], fill=(20, 24, 30))
    d.rectangle([x + 30, y + 40, x + 42, y + 48], fill=(20, 24, 30))


def art_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 248, 240))
    # Ballot paper half-inserted into the slot.
    d.polygon([(x + 22, y + 22), (x + 34, y + 22), (x + 32, y + 42),
               (x + 20, y + 42)], fill=WHITE, outline=(180, 180, 180))
    # Red ballot box + slot.
    d.rectangle([x + 18, y + 40, x + 38, y + 44], fill=(60, 20, 25))
    d.rectangle([x + 10, y + 44, x + 46, y + 76], fill=(160, 30, 50))
    # White check on the box.
    d.line([(x + 16, y + 58), (x + 24, y + 66), (x + 38, y + 50)],
           fill=WHITE, width=3, joint="curve")


def art_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 180, 220))
    # Nepal pennant (double triangle) top-left.
    d.line([(x + 6, y + 6), (x + 6, y + 32)], fill=(80, 80, 80), width=1)
    d.polygon([(x + 6, y + 8), (x + 6, y + 20), (x + 18, y + 14)],
              fill=(220, 30, 50))
    d.polygon([(x + 6, y + 20), (x + 6, y + 30), (x + 15, y + 25)],
              fill=(220, 30, 50))
    # White plane silhouette flying right.
    d.rounded_rectangle([x + 8, y + 38, x + 48, y + 46], radius=4,
                        fill=WHITE)
    d.polygon([(x + 24, y + 44), (x + 32, y + 58), (x + 36, y + 58),
               (x + 30, y + 44)], fill=WHITE)
    d.polygon([(x + 10, y + 40), (x + 14, y + 30), (x + 17, y + 30),
               (x + 15, y + 40)], fill=WHITE)


def art_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 140, 80))
    d.line([(x + 4, y + 62), (x + w - 4, y + 62)], fill=WHITE, width=2)
    d.line([(x + w // 2, y + 62), (x + w // 2, y + 72)], fill=WHITE,
           width=2)
    cx, cy, r = x + 28, y + 34, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 230, 60))
    d.arc([cx - r, cy - r, cx + r, cy + r], start=300, end=60,
          fill=WHITE, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=120, end=240,
          fill=WHITE, width=2)


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(50, 130, 70))
    # Stumps + bails, bottom-right.
    for sx in (38, 43, 48):
        d.rectangle([x + sx, y + 58, x + sx + 3, y + 74],
                    fill=(255, 220, 80))
    d.rectangle([x + 38, y + 56, x + 51, y + 58], fill=(255, 220, 80))
    # Angled bat.
    d.polygon([(x + 10, y + 24), (x + 18, y + 18), (x + 34, y + 58),
               (x + 26, y + 64)], fill=(220, 180, 130))
    # Red ball.
    d.ellipse([x + 35, y + 25, x + 45, y + 35], fill=(200, 40, 40))


def art_pope(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 205))
    # Cross on top of the dome.
    d.line([(x + 28, y + 8), (x + 28, y + 18)], fill=(120, 100, 60),
           width=2)
    d.line([(x + 24, y + 12), (x + 32, y + 12)], fill=(120, 100, 60),
           width=2)
    # Dome + drum.
    d.pieslice([x + 10, y + 18, x + 46, y + 54], start=180, end=360,
               fill=(200, 180, 140))
    d.rectangle([x + 10, y + 44, x + 46, y + 58], fill=(210, 195, 160))
    # Columns + lunch table.
    d.rectangle([x + 14, y + 58, x + 17, y + 72], fill=(190, 175, 140))
    d.rectangle([x + 39, y + 58, x + 42, y + 72], fill=(190, 175, 140))
    d.rectangle([x + 18, y + 66, x + 38, y + 76], fill=WHITE,
                outline=(180, 175, 160))


def art_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 50))
    for sx, sy in [(8, 10), (44, 16), (12, 30), (48, 36), (20, 8)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    # Nose cone, body, fins.
    d.polygon([(x + 22, y + 24), (x + 34, y + 24), (x + 28, y + 10)],
              fill=WHITE)
    d.rounded_rectangle([x + 22, y + 22, x + 34, y + 58], radius=4,
                        fill=WHITE)
    d.ellipse([x + 25, y + 31, x + 31, y + 37], fill=(80, 140, 200))
    d.polygon([(x + 22, y + 52), (x + 16, y + 62), (x + 22, y + 62)],
              fill=(200, 60, 60))
    d.polygon([(x + 34, y + 52), (x + 40, y + 62), (x + 34, y + 62)],
              fill=(200, 60, 60))
    # Flame.
    d.polygon([(x + 24, y + 62), (x + 32, y + 62), (x + 28, y + 76)],
              fill=(255, 140, 30))
    d.polygon([(x + 26, y + 62), (x + 30, y + 62), (x + 28, y + 70)],
              fill=(255, 220, 80))


def art_football(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 120, 60))
    # Yellow goalpost.
    d.rectangle([x + 10, y + 8, x + 12, y + 30], fill=(255, 220, 60))
    d.rectangle([x + 44, y + 8, x + 46, y + 30], fill=(255, 220, 60))
    d.rectangle([x + 10, y + 28, x + 46, y + 30], fill=(255, 220, 60))
    d.rectangle([x + 27, y + 30, x + 29, y + 40], fill=(255, 220, 60))
    # Brown football, rotated ~30 degrees (ellipse as a polygon).
    cx, cy = x + 28, y + 58
    pts = []
    for t in range(0, 360, 15):
        a = math.radians(t)
        px = cx + 16 * math.cos(a) * 0.866 - 9 * math.sin(a) * 0.5
        py = cy + 16 * math.cos(a) * 0.5 + 9 * math.sin(a) * 0.866
        pts.append((px, py))
    d.polygon(pts, fill=(150, 90, 50))
    # White laces.
    d.line([(x + 21, y + 54), (x + 35, y + 62)], fill=WHITE, width=2)
    for p0, p1 in [((x + 25, y + 54), (x + 23, y + 57)),
                   ((x + 29, y + 56), (x + 27, y + 60)),
                   ((x + 33, y + 59), (x + 31, y + 62))]:
        d.line([p0, p1], fill=WHITE, width=1)


def art_soccer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(50, 130, 70))
    # Soccer ball with black spots.
    cx, cy, r = x + 28, y + 40, 16
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    for px, py, pr in [(28, 40, 3), (20, 32, 2), (36, 32, 2),
                       (22, 48, 2), (34, 48, 2)]:
        d.ellipse([x + px - pr, y + py - pr, x + px + pr, y + py + pr],
                  fill=(30, 30, 30))
    # Corner flag.
    d.line([(x + 8, y + 58), (x + 8, y + 76)], fill=WHITE, width=2)
    d.polygon([(x + 8, y + 58), (x + 18, y + 61), (x + 8, y + 64)],
              fill=(255, 220, 60))


def art_racecar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
    # Chequered strip at the top.
    for r in range(2):
        for c in range(12):
            fill = DARK if (r + c) % 2 == 0 else WHITE
            d.rectangle([x + 4 + c * 4, y + 4 + r * 4,
                         x + 8 + c * 4, y + 8 + r * 4], fill=fill)
    # Race car (navy body, yellow wing accents), scaled-down F1 shapes.
    d.rectangle([x + 4, y + 38, x + 14, y + 40], fill=(255, 200, 60))
    d.rectangle([x + 6, y + 40, x + 12, y + 48], fill=(255, 200, 60))
    d.rounded_rectangle([x + 6, y + 48, x + 50, y + 58], radius=3,
                        fill=(30, 50, 130))
    d.rounded_rectangle([x + 24, y + 42, x + 34, y + 48], radius=3,
                        fill=(30, 50, 130))
    d.rectangle([x + 46, y + 54, x + 52, y + 57], fill=(255, 200, 60))
    for wx in (14, 40):
        d.ellipse([x + wx - 5, y + 56, x + wx + 5, y + 66],
                  fill=(10, 10, 12))
        d.ellipse([x + wx - 2, y + 59, x + wx + 2, y + 63],
                  fill=(160, 160, 160))
    d.text((x + 28, y + 70), "VEGAS", font=F_ART_SMALL,
           fill=(255, 200, 60), anchor="ma")


def art_trophy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 90, 50))
    # Gold cup: rim, bowl, handles, stem, base.
    d.rectangle([x + 16, y + 12, x + 40, y + 16], fill=(220, 180, 60))
    d.polygon([(x + 18, y + 16), (x + 38, y + 16), (x + 35, y + 32),
               (x + 21, y + 32)], fill=(220, 180, 60))
    d.ellipse([x + 10, y + 16, x + 20, y + 30], outline=(220, 180, 60),
              width=2)
    d.ellipse([x + 36, y + 16, x + 46, y + 30], outline=(220, 180, 60),
              width=2)
    d.rectangle([x + 25, y + 32, x + 31, y + 46], fill=(220, 180, 60))
    d.rectangle([x + 18, y + 46, x + 38, y + 52], fill=(180, 140, 40))
    d.rectangle([x + 15, y + 52, x + 41, y + 56], fill=(140, 110, 30))
    # Small ball at the foot.
    d.ellipse([x + 37, y + 57, x + 47, y + 67], fill=WHITE)
    d.ellipse([x + 41, y + 60, x + 44, y + 63], fill=(30, 30, 30))


FEAT_ART = {
    "blackout": art_blackout, "ship_fire": art_ship_fire,
    "ballot": art_ballot, "plane": art_plane,
    "tennis": art_tennis, "cricket": art_cricket,
    "pope": art_pope, "rocket": art_rocket,
    "football": art_football, "soccer": art_soccer,
    "racecar": art_racecar, "trophy": art_trophy,
}


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

# Numbered pins for the leads + most features, numbered by story order.
# Pin 4 (Tehran) is nudged north-east so it clears pin 1 (Bahrain);
# pin 5 (Sparta II) is nudged north-east of Loviisa as in v3. No pin
# for 8 (ATP final, Turin — would collide with pin 10, Rome) or 11
# (SpaceX, Vandenberg — would collide with pin 14, Las Vegas); the
# legend says so. Pin 15 sits on Accra, Ghana — the amputee final's
# venue (San Juan de los Lagos) would collide with pin 12.
PINS = [
    (1, 26.0, 50.6),    # Gulf war, Bahrain
    (2, 49.8, 24.0),    # Lviv strike
    (3, 36.9, 30.7),    # COP31, Antalya
    (4, 40.0, 58.0),    # Iran blackouts (nudged)
    (5, 63.5, 30.0),    # Sparta II, Gulf of Finland (nudged)
    (6, 22.3, 114.2),   # Hong Kong votes
    (7, 28.6, 77.2),    # Nepal PM in Delhi
    (9, -41.3, 174.8),  # Pant 128, Wellington
    (10, 41.9, 12.5),   # Vatican, Rome
    (12, 19.4, -99.1),  # NFL, Mexico City
    (13, 53.4, -3.0),   # Man Utd at Liverpool
    (14, 36.1, -115.2), # F1, Las Vegas
    (15, 5.6, -0.2),    # Amputee final, Accra
]

LEGEND_COLS = [
    ["1 Gulf war, Bahrain", "2 Lviv strike", "3 COP31, Antalya",
     "4 Iran blackouts", "5 Sparta II ablaze"],
    ["6 HK votes", "7 Delhi visit", "9 Pant 128, NZ",
     "10 Vatican, Rome", "12 NFL, Mexico City"],
    ["13 Man Utd, Anfield", "14 F1, Las Vegas",
     "15 Amputee final"],
]
LEGEND_NOTE = "8 ATP final (Turin) · 11 SpaceX launch — no pin"


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
    text = ("34 STORIES  ·  7 REGIONS  ·  3 LEADS  ·  12 FEATURES  ·  "
            "19 IN BRIEF  ·  EVERY ONE DATED — SUNDAY 22 NOVEMBER 2026")
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
    sh = 50
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
    vgrad(d, [MARGIN, y, W - MARGIN, y + 20], (52, 52, 56), (26, 26, 28))
    region_text = "   ·   ".join("%s %d" % (name, n) for name, n in REGIONS)
    d.text((W // 2, y + 3), region_text, font=F_REGION, fill=WHITE,
           anchor="ma")
    return y + 20


def draw_lead(d, x, y, w, h, lead):
    card_shadow(d, [x, y, x + w, y + h])
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.line([(x + 1, y + 1), (x + w - 1, y + 1)], fill=WHITE)
    ART[lead["art"]](d, x + 6, y + 6, w - 12, 50)
    tx = x + 12
    tw = w - 24
    ty = y + 60
    d.text((tx, ty), lead["kicker"], font=F_KICKER, fill=RED)
    draw_tag(d, x + w - 12, ty + 2, lead["tag"])
    ty += 14
    for line in cap_lines(d, wrap(d, lead["headline"], F_LEAD_HEAD, tw),
                          2, F_LEAD_HEAD, tw, lead["kicker"]):
        emboss_text(d, (tx, ty), line, F_LEAD_HEAD, INK, WHITE)
        ty += 18
    ty += 2
    for line in cap_lines(d, wrap(d, lead["deck"], F_LEAD_DECK, tw),
                          2, F_LEAD_DECK, tw, lead["kicker"]):
        d.text((tx, ty), line, font=F_LEAD_DECK, fill=(60, 60, 60))
        ty += 13
    d.text((tx, y + h - 13), "Source: " + lead["source"], font=F_SOURCE,
           fill=GREY)


def leads_row(d, y):
    lh = 150
    lead_w, lead_gap = 325, 10
    for i, lead in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + lead_gap)
        draw_lead(d, lx, y, lead_w, lh, lead)
    return y + lh


def draw_feature(d, x, y, w, h, feat):
    """Feature card with a 56px illustrated art panel on the left.

    V4 change: the v3 coloured header strip is gone; each card now
    carries a small procedural scene (one clear shape, readable even
    at 300px page scale). The strip label becomes a kicker line in
    the feature's colour at the top of the text area.
    """
    card_shadow(d, [x, y, x + w, y + h])
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.line([(x + 1, y + 1), (x + w - 1, y + 1)], fill=WHITE)
    FEAT_ART[feat["art"]](d, x + 1, y + 1, 56, h - 2)
    d.line([(x + 57, y + 1), (x + 57, y + h - 1)], fill=LINE)
    tx = x + 70
    tw = w - 77
    ty = y + 5
    kicker, kfnt = fit_one_line(d, feat["strip"], F_FEAT_STRIP, F_KICKER,
                                tw, feat["strip"])
    d.text((tx, ty), kicker, font=kfnt, fill=feat["color"])
    ty += 15
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


def timeline_strip(d, y):
    """New in v4: a dark band with the day's key hours, one line.

    Each event keeps its own zone label — no conversion to one zone.
    The font shrinks (11px -> 10px head + 9px events) if the line
    would not fit; the choice is deterministic.
    """
    h = 24
    vgrad(d, [MARGIN, y, W - MARGIN, y + h], (52, 52, 56), (26, 26, 28))
    head = "THE DAY, HOUR BY HOUR"
    sep = "  —  "
    events = ("04:30 GMT · Lviv blackout · 06:00 GMT · COP31 vote · "
              "09:00 HKT · HK polls open · 12:16 UTC · NROL-136 · "
              "12:30 CET · Pope's lunch · 18:00 CET · ATP final")
    for hf, ef in ((F_KICKER, F_STAT_LBL), (F_TIMELINE_HEAD, F_FOOT)):
        total = (d.textlength(head, font=hf)
                 + d.textlength(sep, font=ef)
                 + d.textlength(events, font=ef))
        if total <= CW - 16:
            break
    tx = (W - total) / 2
    d.text((tx, y + 6), head, font=hf, fill=(255, 200, 60))
    tx += d.textlength(head, font=hf)
    d.text((tx, y + 6), sep, font=ef, fill=WHITE)
    tx += d.textlength(sep, font=ef)
    d.text((tx, y + 6), events, font=ef, fill=WHITE)
    return y + h


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
    h = 36
    x0, x1 = MARGIN, MARGIN + CW
    card_shadow(d, [x0, y, x1, y + h])
    d.rectangle([x0, y, x1, y + h], fill=CARD, outline=LINE, width=1)
    d.line([(x0 + 1, y + 1), (x1 - 1, y + 1)], fill=WHITE)
    d.text((x0 + 8, y + 13), "VOICES", font=F_VOICES, fill=RED)
    zx = x0 + 52
    draw_person(d, zx, y + 2, 30, 32, skin=(224, 184, 150),
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
    draw_person(d, cx, y + 2, 26, 32, skin=(200, 160, 130),
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
    d.text((336, y), "ALSO ON SUNDAY — 19 MORE STORIES", font=F_SECTION,
           fill=INK)
    d.line([(MARGIN, y + 18), (326, y + 18)], fill=INK, width=1)
    d.line([(336, y + 18), (W - MARGIN, y + 18)], fill=INK, width=1)
    cy = y + 22
    # Map + legend (left).
    draw_map(d, MARGIN, cy, 312, 100)
    ly = cy + 104
    for col, items in enumerate(LEGEND_COLS):
        lx = MARGIN + col * 104
        for i, item in enumerate(items):
            d.text((lx, ly + i * 10), item, font=F_LEGEND,
                   fill=(60, 60, 60))
    d.text((MARGIN, ly + 52), LEGEND_NOTE, font=F_LEGEND, fill=GREY)
    map_end = ly + 52 + 10
    # Briefs: 2 columns of 10 (right). Only 19 briefs, so the last
    # slot stays empty — guard the index.
    col_w = 329
    for col in range(2):
        bx = 336 + col * (col_w + 16)
        for row in range(10):
            idx = col * 10 + row
            if idx >= len(BRIEFS):
                continue
            brief = BRIEFS[idx]
            text, fnt = fit_one_line(d, "%d. %s" % (idx + 1, brief),
                                     F_BRIEF, F_BRIEF_SMALL, col_w,
                                     "brief %d" % (idx + 1))
            d.text((bx, cy + row * 17), text, font=fnt, fill=INK)
    briefs_end = cy + 10 * 17
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
    y += 3
    y = timeline_strip(d, y)
    y += 3
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
