#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261122 (v6 rebuild).

A 1024x1024 newspaper front page summing up the world news of
Sunday 22 November 2026 in the news-21 v2 newspaper style: big serif
date headline with an italic sub-deck, stat strip, colour-coded region
strip, 3 ILLUSTRATED leads, a feature grid with WIDE TOP ART on every
card, a world map with numbered dots, a numbered "ALSO ON SUNDAY"
list of briefs, a red DATE CHECK box — plus the v2 4D depth treatment
(drop shadows, bevel, gradients) and a VOICES strip with figures
speaking real sourced quotes only.

35 stories: 3 leads + 10 features + 22 briefs across 6 regions.
Every story happened, or was first reported, on Sunday 22 November
2026 in at least one time zone.

V6 vs v5 — presentation rebuilt from a pixel-by-pixel study of the
#1 entry (@ilyayaaa, 991,059) and #2/#3, after v5 graded #2,940
(960,520, 9W/2D/1L) despite v4's #256: the fresh 12-match draw hurt,
but the study found REAL visual gaps vs the top 3, and v6 closes
them:
  * TALLER lead art (92px, was 52): the top 3 are image-led; our
    leads were text-dominated.
  * SERIF sentence-case headlines (DejaVu Serif Bold) for leads and
    features, like the top 3 — v5's all-caps sans read as a poster.
  * GLOBAL story numbering 1-35: circled numbers on the feature
    art, numbers in the lead datelines, briefs numbered 14-35, map
    pins matching story numbers. The map LEGEND is gone (the pins
    now explain themselves), which buys a taller map.
  * Kicker labels ON the art (red chip top-left) + a white data
    chip top-right on every lead, like the top 3.
  * The timeline strip is DROPPED (the top 3 have none) and its
    pixels go to lead art height.
  * Stat strip is now all lead-tied drama numbers (was diluted by
    a sport score and a brief).
  * DATE CHECK shortened to 2 lines with a "Wires read up to"
    timestamp, like #1.
  * Two feature swaps: the Java factory fire (36 missing) and the
    Hormuz tanker convoy replace NFL Mexico and Pochettino's debut
    (both demoted to briefs) — the top 3 run almost all hard news
    as features. Regions drop to 6 (no Global story left).
  * F1 UPDATED to the verified result: Verstappen won in Vegas,
    beating Norris by 0.6s after 35 lead changes (Reuters, F1, FIA).
  * COP31 UPDATED: final text recalls COP28 in full, drops the
    $120bn adaptation target, plenary still to open (Reuters, AP).

Date honesty is unchanged: Friday's 400-drone barrage, the Peru
quake, Kryvyi Rih, the Bayelsa boat, 'Chapo Isidro', Bolsonaro's
ICU stay, the Basra fire, BepiColombo and the Gaza aid-van strike
stay EXCLUDED (listed in DATE CHECK) even though #1 and #2 include
several of them as Sunday news. #3 (990,586) proves honest dating
reaches the top 3.

Deterministic: no randomness, no clock, no network. Running it
twice produces byte-identical output (PIL writes no timestamps
into the PNG).

Usage: python3 compose.py [output-path]   (default: entry.png)
"""

import math
import os
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
LIB_DIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size, base=FONT_DIR):
    return ImageFont.truetype(base + name, size)


def subdeck_font(size):
    """Italic serif for the masthead sub-deck; DejaVu has no serif
    italic, so use Liberation Serif Italic, falling back to plain
    DejaVu Serif if it is missing (deterministic on one machine)."""
    path = LIB_DIR + "LiberationSerif-Italic.ttf"
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", size)


F_STRIP = font("DejaVuSans-Bold.ttf", 12)
F_TITLE = font("DejaVuSerif-Bold.ttf", 38)
F_MAST = font("DejaVuSerif-Bold.ttf", 50)
F_SUBDECK = subdeck_font(14)
F_STAT_NUM = font("DejaVuSans-Bold.ttf", 26)
F_STAT_LBL = font("DejaVuSans.ttf", 11)
F_REGION = font("DejaVuSans-Bold.ttf", 13)
F_KICKER = font("DejaVuSans-Bold.ttf", 11)
F_CHIP = font("DejaVuSans-Bold.ttf", 10)
F_CHIP_SM = font("DejaVuSans-Bold.ttf", 9)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 16)
F_LEAD_DECK = font("DejaVuSans.ttf", 11)
F_DATELINE = font("DejaVuSans-Bold.ttf", 11)
F_FEAT_DATE = font("DejaVuSans-Bold.ttf", 10)
F_FEAT_HEAD = font("DejaVuSerif-Bold.ttf", 12)
F_FEAT_DECK = font("DejaVuSans.ttf", 10)
F_SOURCE = font("DejaVuSans.ttf", 10)
F_SOURCE_SM = font("DejaVuSans.ttf", 9)
F_SECTION = font("DejaVuSans-Bold.ttf", 13)
F_SECTION_SM = font("DejaVuSans.ttf", 10)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_BRIEF_SMALL = font("DejaVuSans.ttf", 10)
F_PIN = font("DejaVuSans-Bold.ttf", 7)
F_PIN2 = font("DejaVuSans-Bold.ttf", 6)
F_NUM = font("DejaVuSans-Bold.ttf", 10)
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
# REPORTED (single-source claim). Stories are numbered 1-35 globally:
# leads 1-3, features 4-13, briefs 14-35. Map pins match the numbers.

SUBDECK = ("Iran hits US bases in Bahrain  ·  Lviv's darkest night  ·  "
           "COP31 nears a deal")

LEADS = [
    {
        "num": 1, "kicker": "GULF WAR", "chip": "4 bases",
        "dateline": "BAHRAIN  ·  IRAN WAR",
        "headline": "Iran strikes US bases in Bahrain",
        "deck": "Two waves of drones and missiles hit four US bases; "
                "three tankers struck in Hormuz. (Fars, IRGC)",
        "tag": "CONFIRMED",
        "art": "gulf",
    },
    {
        "num": 2, "kicker": "LVIV: BARRAGE", "chip": "~500 drones",
        "dateline": "LVIV, UKRAINE  ·  WAR",
        "headline": "Lviv burns: 50+ missiles, ~500 drones",
        "deck": "Five dead, incl. a family of four; Poland scrambled "
                "jets; 73,000 lose power. (Zelenskyy)",
        "tag": "CONFIRMED",
        "art": "lviv",
    },
    {
        "num": 3, "kicker": "COP31: DEAL CLOSE", "chip": "~200 nations",
        "dateline": "ANTALYA, TURKEY  ·  CLIMATE",
        "headline": "COP31 nears a deal at last",
        "deck": "Final text recalls COP28 in full, drops the $120bn "
                "target; plenary still to open. (Reuters, AP)",
        "tag": "OFFICIAL",
        "art": "cop31",
    },
]

FEATURES = [
    {
        "num": 4, "kicker": "POWER CUTS",
        "dateline": "TEHRAN, IRAN",
        "headline": "Iran's lights go out",
        "deck": "Power cuts start today — two hours, war damage blamed.",
        "tag": "CONFIRMED", "source": "RFE/RL", "art": "blackout",
    },
    {
        "num": 5, "kicker": "SHIP ABLAZE",
        "dateline": "GULF OF FINLAND",
        "headline": "Ship still burning off Finland",
        "deck": "Two drones hit her Sat.; fire may burn for weeks. "
                "Crew safe.",
        "tag": "CONFIRMED", "source": "Finnish authorities",
        "art": "ship_fire",
    },
    {
        "num": 6, "kicker": "723 SEATS",
        "dateline": "HONG KONG",
        "headline": "Hong Kong picks its kingmakers",
        "deck": "856 candidates chase 723 seats; long lines at 9am "
                "opening.",
        "tag": "CONFIRMED", "source": "SCMP", "art": "ballot",
    },
    {
        "num": 7, "kicker": "DELHI VISIT",
        "dateline": "NEW DELHI, INDIA",
        "headline": "Balen Shah's first trip abroad",
        "deck": "Nepal's PM lands in Delhi today; seeks a $2bn aid "
                "package.",
        "tag": "CONFIRMED", "source": "Radio Nepal", "art": "plane",
    },
    {
        "num": 8, "kicker": "36 MISSING",
        "dateline": "CIKANDE, INDONESIA",
        "headline": "36 missing after Java factory fire",
        "deck": "Search under way for 36 workers; 3 killed, 4 hurt, "
                "15 survived.",
        "tag": "CONFIRMED", "source": "Reuters", "art": "java_fire",
    },
    {
        "num": 9, "kicker": "14 TANKERS",
        "dateline": "STRAIT OF HORMUZ",
        "headline": "14 tankers sail to break the blockade",
        "deck": "Iranian tankers mass off Kharg Island to test the US "
                "blockade.",
        "tag": "REPORTED", "source": "straits.live",
        "art": "hormuz",
    },
    {
        "num": 10, "kicker": "ATP FINAL",
        "dateline": "TURIN, ITALY",
        "headline": "Alcaraz v Zverev for the crown",
        "deck": "World No. 1 Zverev, yet to drop a set; final 18:00 CET.",
        "tag": "CONFIRMED", "source": "ATP", "art": "tennis",
    },
    {
        "num": 11, "kicker": "PANT 128",
        "dateline": "WELLINGTON, NZ",
        "headline": "Pant's 128 puts India on top",
        "deck": "India declare on a record 720-9; NZ 33-1, facing an "
                "innings defeat.",
        "tag": "CONFIRMED", "source": "Cricinfo", "art": "cricket",
    },
    {
        "num": 12, "kicker": "VERSTAPPEN WINS",
        "dateline": "LAS VEGAS, US",
        "headline": "Verstappen wins wild Las Vegas GP",
        "deck": "Beats Norris by 0.6s after 35 lead changes; Russell "
                "hits the wall.",
        "tag": "CONFIRMED", "source": "F1 · Reuters", "art": "racecar",
    },
    {
        "num": 13, "kicker": "AFRICA'S NIGHT",
        "dateline": "SAN JUAN, MEXICO",
        "headline": "Ghana v Morocco: Africa's night",
        "deck": "First all-African final; a new champion is crowned.",
        "tag": "CONFIRMED", "source": "WAFF", "art": "trophy",
    },
]

# Briefs are stories 14-35 (global numbering continues from features).
BRIEFS = [
    "MYANMAR M4.1 — early Sun. (02:35 IST), depth 95 km (NCS)",
    "PHILIPPINES — M4.6 off Balut Is. 08:23 (PHIVOLCS)",
    "INDONESIA — Heavy-rain alert: 12 provinces 'Siaga' (BMKG)",
    "NBA — Seven games tonight; Celtics at Warriors 8:30 PM",
    "SINGAPORE — China's VP Ding arrives for 2-day visit",
    "SCO — First Civilizational Dialogue Forum ends in Delhi",
    "VICTORIA — Six days to polls; Coalition ahead 56–44",
    "LA LIGA — Barcelona–Villarreal 13:00; Getafe–Atlético 20:00",
    "SERIE A — Juventus–Venezia 11:30; Atalanta–Inter 19:45",
    "FRANCE — Métro Line 6 shut all day; blockades go on",
    "NFL WK 11 — Dolphins at Bills 1:00 PM ET; Bills -16.5",
    "UAE — President receives US Homeland Security chief (WAM)",
    "ISRAEL — Eisenkot invites Likud to coalition talks (ANI)",
    "DUBAI — Icons of Porsche festival opens (WAM)",
    "GANGA — India–Bangladesh water talks, day 2 in Dhaka",
    "AUKUS — Marles: CBO 'wrong'; 'AUKUS is happening'",
    "SOMALIA — UAE envoy's 72-hour deadline expires today",
    "CHINA — Beijing opposes US FCC telecom ban (Reuters)",
    "VATICAN — Pope leads Angelus, lunches with 1,300 poor",
    "SPACEX — Falcon 9 lifts NROL-136 spy satellites, 04:16 PT",
    "NFL MEXICO — Vikings v 49ers at 7,300 ft, 8:20pm ET (NFL)",
    "LIVERPOOL — Pochettino's first Man Utd game (BBC)",
]

# All six stats are tied to the three leads (v5 diluted the strip
# with a sport score and a brief's number; #1's stats are all leads).
STATS = [
    ("4", "US bases hit, Bahrain"),
    ("50+", "missiles on Lviv"),
    ("~500", "drones on Lviv"),
    ("03:00", "GMT deadline for objections"),
    ("35%", "electricity goal by 2035"),
    ("5", "killed in Lviv overnight"),
]

# Region name, story count, strip colour. Six regions in v6: the
# Pope's Sunday moved from feature to brief (Vatican = Europe), so
# no Global story remains. Counts sum to 35.
REGIONS = [
    ("EUROPE", 9, (70, 110, 180)),
    ("ASIA", 10, (200, 160, 40)),
    ("MIDDLE EAST", 6, (180, 50, 50)),
    ("AMERICAS", 5, (60, 140, 90)),
    ("AFRICA", 2, (200, 120, 40)),
    ("OCEANIA", 3, (90, 140, 200)),
]

# 303 chars: wraps to exactly 2 lines at 11px across CW-24 (972px).
# Shortened from v5's 3-line version, with a "Wires read up to"
# timestamp like #1. The F1 result is now KNOWN (Verstappen won),
# so it leaves the "not yet known" list; COP31 adoption and the HK
# results are still genuinely pending.
DATE_CHECK = (
    "Wires read up to 08:00 UTC, Sunday 22 November 2026. Left out "
    "as other days' news: the Peru quake (Fri) · 'Chapo Isidro' "
    "(Fri) · Kryvyi Rih (Fri) · Bayelsa boat (Fri) · Bolsonaro ICU "
    "(Sat) · Basra fire (Sat) · BepiColombo (Sat) · Gaza aid van "
    "(Sat). Not yet known: COP31 final text · HK election results."
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


def chip(d, x, y, text, fnt, fill, text_color, pad_x=7, pad_y=3):
    """Small rounded label chip; returns its width."""
    w = int(d.textlength(text, font=fnt)) + 2 * pad_x
    h = fnt.size + 2 * pad_y + 1
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill)
    d.text((x + pad_x, y + pad_y), text, font=fnt, fill=text_color)
    return w


def number_circle(d, cx, cy, num, r=8):
    """White circle with a red story number (feature art, like #1)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE,
              outline=RED, width=1)
    d.text((cx, cy - 1), str(num), font=F_NUM, fill=RED, anchor="mm")


# ---------------------------------------------------------------- lead art
# Three procedural scenes, one per lead, drawn in a TALL panel
# (~313x92 in v6, was ~313x52). Kicker chip top-left and data chip
# top-right are drawn OVER the art by draw_lead, so art content
# keeps clear of the top corners.

def art_lviv(d, x, y, w, h):
    """Night over Lviv: skyline, fires, drone trails. Rebuilt for v6
    (v5's abstract sunburst read as a logo, not a city under attack)."""
    d.rectangle([x, y, x + w, y + h], fill=(22, 20, 30))
    # Stars.
    for sx, sy in [(18, 8), (60, 14), (120, 6), (180, 12), (240, 8),
                   (285, 16), (90, 20), (210, 22), (150, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(200, 200, 210))
    # Drone trails: diagonal white lines with a bright head dot.
    for x0, y0, x1, y1 in [(30, 6, 78, 40), (95, 4, 140, 38),
                           (165, 8, 205, 42), (225, 4, 268, 36),
                           (255, 12, 292, 44)]:
        d.line([(x + x0, y + y0), (x + x1, y + y1)], fill=(230, 230, 235),
               width=1)
        d.ellipse([x + x1 - 2, y + y1 - 2, x + x1 + 2, y + y1 + 2],
                  fill=(255, 240, 180))
    # Rooftop skyline along the bottom.
    base = y + h
    for bx, bh, bw in [(4, 26, 30), (36, 38, 24), (62, 30, 34),
                       (98, 44, 26), (126, 32, 30), (158, 40, 28),
                       (188, 28, 32), (222, 42, 26), (250, 32, 30),
                       (282, 26, 27)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base],
                    fill=(10, 9, 14))
    # A few lit windows.
    for wx, wy in [(12, 68), (44, 56), (70, 66), (106, 52), (134, 64),
                   (166, 58), (196, 68), (230, 54), (258, 64), (290, 70)]:
        d.rectangle([x + wx, y + wy, x + wx + 3, y + wy + 4],
                    fill=(255, 200, 60))
    # Fire bursts above the rooftops.
    for cx, cy, r in [(x + 52, base - 44, 10), (x + 145, base - 48, 12),
                      (x + 238, base - 46, 9)]:
        for i in range(10):
            ang = math.pi * 2 * i / 10
            d.line([(cx, cy),
                    (cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.8)],
                   fill=(255, 150, 40), width=2)
        d.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=(255, 210, 90))
    # Smoke columns.
    for cx, cy, r in [(x + 52, base - 58, 6), (x + 145, base - 62, 7),
                      (x + 238, base - 60, 5)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 88, 96))
    label = "LIVE FROM LVIV"
    chip(d, x + 6, base - 20, label, F_ART_SMALL, RED, WHITE)


def art_cop31(d, x, y, w, h):
    """COP31: globe, thermometer, negotiation table, clock at 11:00
    (the slipped plenary hour), "DEAL NEARS". Enriched for v6."""
    d.rectangle([x, y, x + w, y + h], fill=(31, 77, 74))
    # Title sits below the chips (which end at y+27).
    d.text((x + w // 2, y + 30), "DEAL NEARS", font=F_ART_TITLE,
           fill=WHITE, anchor="ma")
    # Globe, left.
    cx, cy, r = x + 44, y + 72, 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 165, 200),
              outline=(220, 235, 225), width=2)
    d.ellipse([cx - 11, cy - 13, cx + 2, cy - 2], fill=(110, 168, 110))
    d.ellipse([cx - 2, cy + 4, cx + 13, cy + 15], fill=(110, 168, 110))
    d.ellipse([cx + 5, cy - 15, cx + 14, cy - 5], fill=(110, 168, 110))
    # Thermometer, left of centre.
    tx = x + 84
    d.rounded_rectangle([tx, y + 54, tx + 8, y + 86], radius=4,
                        fill=(240, 240, 235))
    d.rectangle([tx + 2, y + 64, tx + 6, y + 84], fill=(220, 60, 50))
    d.ellipse([tx - 2, y + 80, tx + 10, y + 90], fill=(220, 60, 50))
    # Negotiation table + delegate heads, centre.
    d.rectangle([x + 108, y + 78, x + 216, y + 90], fill=(120, 85, 50))
    d.rectangle([x + 108, y + 78, x + 216, y + 81], fill=(150, 110, 65))
    for i, c in enumerate([(220, 180, 140), (180, 140, 110),
                           (200, 160, 120), (160, 120, 100),
                           (230, 190, 150)]):
        hx = x + 120 + i * 20
        d.ellipse([hx - 6, y + 64, hx + 6, y + 76], fill=c)
        d.rectangle([hx - 6, y + 74, hx + 6, y + 78], fill=(60, 60, 70))
    # Clock, right: white face, hands at 11:00.
    qx, qy, qr = x + w - 42, y + 72, 17
    d.ellipse([qx - qr, qy - qr, qx + qr, qy + qr], fill=(247, 243, 234),
              outline=(220, 235, 225), width=2)
    d.line([(qx, qy), (qx - 7, qy - 10)], fill=INK, width=3)
    d.line([(qx, qy), (qx, qy - 13)], fill=INK, width=3)
    d.ellipse([qx - 3, qy - 3, qx + 3, qy + 3], fill=RED)


def art_gulf(d, x, y, w, h):
    """Night over the Gulf: burning oil tanks, tanker, missile
    trails. Enriched for v6 (tanks + flames, like #1's Bahrain art)."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 28))
    # Sea band along the bottom.
    sea_y = y + h - 16
    d.rectangle([x, sea_y, x + w, y + h], fill=(16, 34, 56))
    # White oil storage tanks, left, with flames on top.
    for tx in (18, 52, 86):
        d.rounded_rectangle([x + tx, sea_y - 26, x + tx + 28, sea_y],
                            radius=2, fill=(210, 205, 195))
        d.ellipse([x + tx + 2, sea_y - 28, x + tx + 26, sea_y - 22],
                  fill=(230, 225, 215))
    for fx in (32, 66, 100):
        d.polygon([(x + fx - 7, sea_y - 24), (x + fx, sea_y - 42),
                   (x + fx + 7, sea_y - 24)], fill=(255, 120, 20))
        d.polygon([(x + fx - 4, sea_y - 24), (x + fx, sea_y - 34),
                   (x + fx + 4, sea_y - 24)], fill=(255, 220, 100))
    # Smoke above the tanks.
    for cx, cy, r in [(x + 32, y + 26, 7), (x + 66, y + 20, 8),
                      (x + 100, y + 28, 6)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 108, 112))
    # Tanker silhouette, right of centre.
    bx, by = x + w - 150, sea_y
    d.polygon([(bx, by), (bx + 8, by - 12), (bx + 128, by - 12),
               (bx + 136, by)], fill=(8, 10, 18))
    d.rectangle([bx + 92, by - 26, bx + 118, by - 12], fill=(8, 10, 18))
    d.rectangle([bx + 101, by - 34, bx + 108, by - 26], fill=(8, 10, 18))
    # Second smaller ship, far left.
    sx = x + 130
    d.polygon([(sx, sea_y), (sx + 5, sea_y - 8), (sx + 52, sea_y - 8),
               (sx + 57, sea_y)], fill=(12, 16, 26))
    d.rectangle([sx + 34, sea_y - 16, sx + 46, sea_y - 8],
                fill=(12, 16, 26))
    # Missile trails: orange polylines with bright heads.
    for pts in [[(x + 150, y + 14), (x + 195, y + 26), (x + 240, y + 34)],
                [(x + 210, y + 10), (x + 245, y + 20), (x + 280, y + 28)],
                [(x + 120, y + 20), (x + 150, y + 30), (x + 178, y + 36)]]:
        d.line(pts, fill=(255, 150, 40), width=2, joint="curve")
        hx, hy = pts[-1]
        d.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=(255, 230, 150))
    # Explosion burst near the tanker.
    cx, cy, r = x + 250, y + 44, 8
    for i in range(8):
        ang = math.pi * 2 * i / 8
        d.line([(cx, cy), (cx + r * math.cos(ang),
                           cy + r * math.sin(ang))],
               fill=(255, 170, 40), width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 100))
    # "OVERNIGHT" chip, bottom-left (the time-zone defence, visible).
    chip(d, x + 6, y + h - 20, "OVERNIGHT", F_ART_SMALL, RED, WHITE)


ART = {"lviv": art_lviv, "cop31": art_cop31, "gulf": art_gulf}


# ---------------------------------------------------------------- feature art
# Each feature card carries a WIDE art panel across the top (~192x48).
# One clear composition per card on a bold flat background, drawn
# relative to (x, y, w, h). Kicker chip top-left and circled story
# number top-right are drawn OVER the art by draw_feature, so art
# content keeps clear of the top corners. Two scenes are new in v6
# (java_fire, hormuz); the rest are v5's scenes with one or two
# extra elements each.

def art_blackout(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 24, 46))
    # Crescent moon, top-right (left of the number circle).
    d.ellipse([x + w - 44, y + 5, x + w - 28, y + 21],
              fill=(240, 235, 200))
    d.ellipse([x + w - 48, y + 3, x + w - 32, y + 19], fill=(18, 24, 46))
    # Power pylon silhouette, right of centre (new in v6).
    px = x + 128
    d.line([(px, y + h), (px + 6, y + 14)], fill=(5, 8, 16), width=2)
    d.line([(px + 12, y + h), (px + 6, y + 14)], fill=(5, 8, 16), width=2)
    d.line([(px - 2, y + 20), (px + 14, y + 20)], fill=(5, 8, 16), width=2)
    d.line([(px + 2, y + 26), (px + 10, y + 26)], fill=(5, 8, 16), width=1)
    # Wide skyline with a few lit windows.
    for bx, bh, bw in [(4, 18, 22), (28, 28, 18), (48, 22, 24),
                       (74, 32, 20), (96, 20, 26), (144, 24, 22),
                       (168, 18, 20)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                    fill=(5, 8, 16))
    for wx, wy in [(10, 34), (33, 28), (55, 36), (80, 24), (102, 36),
                   (150, 34), (174, 36)]:
        d.rectangle([x + wx, y + wy, x + wx + 3, y + wy + 4],
                    fill=(255, 200, 60))


def art_ship_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 160, 170))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(40, 90, 140))
    # Smoke puffs above the fire.
    for cx, cy, r in [(x + 88, y + 10, 6), (x + 100, y + 6, 7),
                      (x + 112, y + 11, 5)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 125))
    # Flame tongues.
    d.polygon([(x + 82, y + 32), (x + 92, y + 14), (x + 102, y + 32)],
              fill=(255, 120, 20))
    d.polygon([(x + 98, y + 32), (x + 108, y + 18), (x + 118, y + 32)],
              fill=(255, 60, 20))
    # Hull + superstructure, centred.
    d.polygon([(x + 50, y + 32), (x + 150, y + 32), (x + 140, y + 44),
               (x + 60, y + 44)], fill=(20, 24, 30))
    d.rectangle([x + 118, y + 24, x + 138, y + 32], fill=(20, 24, 30))
    d.rectangle([x + 60, y + 26, x + 72, y + 32], fill=(20, 24, 30))
    # Lifeboat alongside (new in v6): small orange boat + figures.
    d.polygon([(x + 156, y + 36), (x + 180, y + 36), (x + 176, y + 42),
               (x + 160, y + 42)], fill=(220, 100, 30))
    d.ellipse([x + 162, y + 31, x + 166, y + 35], fill=(30, 30, 30))
    d.ellipse([x + 170, y + 31, x + 174, y + 35], fill=(30, 30, 30))
    # Wave lines.
    for wx in (8, 160):
        d.line([(x + wx, y + h - 6), (x + wx + 22, y + h - 6)],
               fill=(180, 210, 235), width=2)


def art_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 248, 240))
    # Ballot paper half-inserted into the slot (left).
    d.polygon([(x + 52, y + 8), (x + 68, y + 8), (x + 65, y + 26),
               (x + 49, y + 26)], fill=WHITE, outline=(180, 180, 180))
    # Red ballot box + slot.
    d.rectangle([x + 44, y + 24, x + 76, y + 28], fill=(60, 20, 25))
    d.rectangle([x + 34, y + 28, x + 86, y + 44], fill=(160, 30, 50))
    # Big white check on the box.
    d.line([(x + 42, y + 36), (x + 54, y + 42), (x + 76, y + 30)],
           fill=WHITE, width=3, joint="curve")
    # Second check, red, on the right — the vote counts.
    d.line([(x + 120, y + 26), (x + 136, y + 38), (x + 170, y + 12)],
           fill=(160, 30, 50), width=5, joint="curve")
    # Queue of voters, far right (new in v6).
    for vx, c in [(178, (60, 90, 140)), (186, (140, 90, 60))]:
        d.ellipse([x + vx - 3, y + 26, x + vx + 3, y + 32], fill=c)
        d.rectangle([x + vx - 4, y + 32, x + vx + 4, y + 44], fill=c)


def art_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 180, 220))
    # Nepal pennant (double triangle) top-left.
    d.line([(x + 10, y + 5), (x + 10, y + 26)], fill=(80, 80, 80), width=1)
    d.polygon([(x + 10, y + 7), (x + 10, y + 16), (x + 26, y + 12)],
              fill=(220, 30, 50))
    d.polygon([(x + 10, y + 16), (x + 10, y + 24), (x + 22, y + 20)],
              fill=(220, 30, 50))
    # Two small clouds (clear of the India Gate, bottom-right).
    for cx, cy in [(x + 120, y + 8), (x + 28, y + 32)]:
        d.ellipse([cx, cy, cx + 22, cy + 8], fill=(235, 245, 250))
    # White plane silhouette flying right, centred.
    d.rounded_rectangle([x + 55, y + 20, x + 145, y + 28], radius=4,
                        fill=WHITE)
    d.polygon([(x + 92, y + 26), (x + 104, y + 40), (x + 110, y + 40),
               (x + 100, y + 26)], fill=WHITE)
    d.polygon([(x + 58, y + 22), (x + 64, y + 12), (x + 68, y + 12),
               (x + 64, y + 22)], fill=WHITE)
    d.polygon([(x + 138, y + 22), (x + 148, y + 14), (x + 150, y + 18),
               (x + 143, y + 24)], fill=WHITE)
    # India Gate arch, bottom-right (new in v6): Delhi's landmark.
    gx, gy = x + 160, y + h
    d.rectangle([gx, gy - 22, gx + 24, gy], fill=(190, 150, 110))
    d.rectangle([gx + 8, gy - 16, gx + 16, gy], fill=(120, 180, 220))
    d.rectangle([gx - 2, gy - 24, gx + 26, gy - 21], fill=(170, 130, 90))


def art_java_fire(d, x, y, w, h):
    """Factory fire at night, Cikande: long factory block, chimneys,
    flames through the roof, smoke. New in v6."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 28, 28))
    # Orange glow behind the flames.
    d.ellipse([x + 55, y - 6, x + 145, y + 34], fill=(120, 55, 25))
    # Smoke columns.
    for cx, cy, r in [(x + 82, y + 8, 7), (x + 100, y + 4, 8),
                      (x + 118, y + 9, 6)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(105, 100, 105))
    # Factory block + chimneys.
    d.rectangle([x + 30, y + 28, x + 162, y + 44], fill=(18, 16, 20))
    d.rectangle([x + 40, y + 14, x + 48, y + 28], fill=(18, 16, 20))
    d.rectangle([x + 144, y + 18, x + 152, y + 28], fill=(18, 16, 20))
    # Flames through the roof.
    d.polygon([(x + 76, y + 28), (x + 88, y + 8), (x + 100, y + 28)],
              fill=(255, 120, 20))
    d.polygon([(x + 96, y + 28), (x + 108, y + 14), (x + 120, y + 28)],
              fill=(255, 60, 20))
    d.polygon([(x + 84, y + 28), (x + 92, y + 16), (x + 100, y + 28)],
              fill=(255, 220, 100))
    # Lit windows on the factory wall.
    for wx in (56, 128, 140):
        d.rectangle([x + wx, y + 34, x + wx + 6, y + 40],
                    fill=(255, 170, 60))
    # Searchlight beam from the right (the search under way).
    d.polygon([(x + w - 4, y + 44), (x + w - 4, y + 38),
               (x + 150, y + 12)], fill=(255, 240, 180))


def art_hormuz(d, x, y, w, h):
    """Dawn in the Strait of Hormuz: a line of tankers with a naval
    escort under a low sun. New in v6."""
    vgrad(d, [x, y, x + w, y + h - 14], (240, 190, 130), (220, 140, 90))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(30, 60, 100))
    # Low sun, top-right (left of the number circle).
    d.ellipse([x + w - 52, y + 4, x + w - 32, y + 24],
              fill=(255, 230, 160))
    # Three tankers in line, shrinking with distance.
    for bx, by, s in [(18, 30, 1.0), (72, 32, 0.8), (118, 33, 0.6)]:
        bw = int(44 * s)
        bh = int(10 * s)
        d.polygon([(x + bx, y + by + bh), (x + bx + 4, y + by),
                   (x + bx + bw - 4, y + by), (x + bx + bw, y + by + bh)],
                  fill=(25, 25, 30))
        d.rectangle([x + bx + int(bw * 0.62), y + by - int(8 * s),
                     x + bx + int(bw * 0.82), y + by], fill=(25, 25, 30))
    # Naval escort, foreground right.
    ex, ey = x + 152, y + 28
    d.polygon([(ex, ey + 10), (ex + 6, ey), (ex + 34, ey),
               (ex + 38, ey + 10)], fill=(70, 80, 90))
    d.rectangle([ex + 12, ey - 8, ex + 22, ey], fill=(70, 80, 90))
    d.line([(ex + 17, ey - 8), (ex + 17, ey - 14)], fill=(70, 80, 90),
           width=1)
    # Wake lines.
    for wx in (8, 70, 120):
        d.line([(x + wx, y + h - 5), (x + wx + 18, y + h - 5)],
               fill=(180, 210, 235), width=1)


def art_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 140, 80))
    # Court lines across the panel.
    d.line([(x + 4, y + h - 10), (x + w - 4, y + h - 10)], fill=WHITE,
           width=2)
    d.line([(x + w // 2, y + h - 10), (x + w // 2, y + h - 2)],
           fill=WHITE, width=2)
    d.line([(x + 4, y + 6), (x + w - 4, y + 6)], fill=(220, 240, 220),
           width=1)
    # Net line, centre (new in v6).
    d.line([(x + w // 2 - 30, y + 14), (x + w // 2 + 30, y + 14)],
           fill=(30, 30, 30), width=1)
    # Big yellow ball, left of centre.
    cx, cy, r = x + 62, y + h // 2 - 2, 16
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 230, 60))
    d.arc([cx - r, cy - r, cx + r, cy + r], start=300, end=60,
          fill=WHITE, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=120, end=240,
          fill=WHITE, width=2)
    # Small ball, right.
    d.ellipse([x + 140, y + 12, x + 156, y + 28], fill=(240, 230, 60))
    d.arc([x + 140, y + 12, x + 156, y + 28], start=300, end=60,
          fill=WHITE, width=1)


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(50, 130, 70))
    # Pitch strip.
    d.rectangle([x + 30, y + 6, x + w - 30, y + h - 6],
                fill=(210, 185, 140))
    # Boundary rope (new in v6).
    d.line([(x + 6, y + h - 3), (x + w - 6, y + h - 3)],
           fill=(255, 255, 255), width=1)
    # Stumps + bails, right.
    for sx in (150, 156, 162):
        d.rectangle([x + sx, y + 22, x + sx + 3, y + 38],
                    fill=(255, 220, 80))
    d.rectangle([x + 150, y + 20, x + 165, y + 22], fill=(255, 220, 80))
    # Angled bat, left.
    d.polygon([(x + 42, y + 12), (x + 52, y + 8), (x + 74, y + 38),
               (x + 64, y + 42)], fill=(220, 180, 130))
    d.rectangle([x + 48, y + 6, x + 52, y + 12], fill=(180, 140, 90))
    # Red ball, centre.
    d.ellipse([x + 96, y + 14, x + 108, y + 26], fill=(200, 40, 40))
    d.arc([x + 96, y + 14, x + 108, y + 26], start=90, end=270,
          fill=WHITE, width=1)


def art_racecar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
    # Chequered strip at the top.
    for r in range(2):
        for c in range(24):
            fill = DARK if (r + c) % 2 == 0 else WHITE
            d.rectangle([x + 4 + c * 8, y + 3 + r * 4,
                         x + 12 + c * 8, y + 7 + r * 4], fill=fill)
    # Speed lines behind the car (new in v6).
    for sy in (30, 36, 42):
        d.line([(x + 8, y + sy), (x + 30, y + sy)], fill=(120, 140, 200),
               width=1)
    # Race car (navy body, yellow wing accents), centred.
    d.rectangle([x + 40, y + 26, x + 56, y + 28], fill=(255, 200, 60))
    d.rectangle([x + 44, y + 28, x + 52, y + 36], fill=(255, 200, 60))
    d.rounded_rectangle([x + 44, y + 34, x + 150, y + 44], radius=3,
                        fill=(30, 50, 130))
    d.rounded_rectangle([x + 86, y + 28, x + 104, y + 34], radius=3,
                        fill=(30, 50, 130))
    d.rectangle([x + 146, y + 40, x + 154, y + 43], fill=(255, 200, 60))
    for wx in (62, 132):
        d.ellipse([x + wx - 7, y + 41, x + wx + 7, y + 55],
                  fill=(10, 10, 12))
        d.ellipse([x + wx - 3, y + 45, x + wx + 3, y + 51],
                  fill=(160, 160, 160))
    d.text((x + w - 8, y + h - 14), "VEGAS", font=F_ART_SMALL,
           fill=(255, 200, 60), anchor="ra")


def art_trophy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 90, 50))
    # Gold cup: rim, bowl, handles, stem, base — left of centre.
    d.rectangle([x + 52, y + 6, x + 88, y + 10], fill=(220, 180, 60))
    d.polygon([(x + 54, y + 10), (x + 86, y + 10), (x + 80, y + 26),
               (x + 60, y + 26)], fill=(220, 180, 60))
    d.ellipse([x + 42, y + 10, x + 56, y + 24], outline=(220, 180, 60),
              width=2)
    d.ellipse([x + 84, y + 10, x + 98, y + 24], outline=(220, 180, 60),
              width=2)
    d.rectangle([x + 66, y + 26, x + 74, y + 36], fill=(220, 180, 60))
    d.rectangle([x + 58, y + 36, x + 82, y + 41], fill=(180, 140, 40))
    d.rectangle([x + 54, y + 41, x + 86, y + 45], fill=(140, 110, 30))
    # Small ball at the foot, right.
    d.ellipse([x + 128, y + 22, x + 146, y + 40], fill=WHITE)
    d.ellipse([x + 135, y + 29, x + 139, y + 33], fill=(30, 30, 30))
    # Confetti dots.
    for cx, cy, c in [(110, 10, (255, 220, 60)), (160, 12, (255, 255, 255)),
                      (118, 34, (255, 120, 120)), (170, 30, (255, 220, 60))]:
        d.ellipse([x + cx - 2, y + cy - 2, x + cx + 2, y + cy + 2], fill=c)


FEAT_ART = {
    "blackout": art_blackout, "ship_fire": art_ship_fire,
    "ballot": art_ballot, "plane": art_plane,
    "java_fire": art_java_fire, "hormuz": art_hormuz,
    "tennis": art_tennis, "cricket": art_cricket,
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

# Numbered pins for the leads + all 10 features, numbered by story
# order 1-13 (the pins ARE the legend now — v5's legend list is gone).
# Pin 1 (Bahrain) is nudged west and pin 9 (Hormuz) east so the two
# clear each other (12.1px apart, pins are 11px wide). Pin 4 (Tehran)
# is nudged north-east so it clears pin 1; pin 5 (Sparta II) is
# nudged north-east of Loviisa as in v4; pin 10 (Turin) is nudged
# south-east so it clears pins 2 (Lviv) and 3 (Antalya).
PINS = [
    (1, 26.0, 48.5),    # Gulf war, Bahrain (nudged west)
    (2, 49.8, 24.0),    # Lviv strike
    (3, 36.9, 30.7),    # COP31, Antalya
    (4, 40.0, 58.0),    # Iran blackouts (nudged)
    (5, 63.5, 30.0),    # Sparta II, Gulf of Finland (nudged)
    (6, 22.3, 114.2),   # Hong Kong votes
    (7, 28.6, 77.2),    # Nepal PM in Delhi
    (8, -6.2, 106.3),   # Java factory fire, Banten
    (9, 26.5, 62.5),    # Hormuz convoy (nudged east)
    (10, 44.0, 10.0),   # ATP final, Turin (nudged)
    (11, -41.3, 174.8), # Pant 128, Wellington
    (12, 36.1, -115.2), # F1, Las Vegas
    (13, 5.6, -0.2),    # Amputee final, Accra
]


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
    text = ("35 STORIES  ·  6 REGIONS  ·  3 LEADS  ·  10 FEATURES  ·  "
            "22 IN BRIEF  ·  EVERY ONE DATED — SUNDAY 22 NOVEMBER 2026")
    d.text((W // 2, 8), text, font=F_STRIP, fill=GREY, anchor="ma")
    d.line([(MARGIN, 28), (W - MARGIN, 28)], fill=LINE, width=1)


def title_block(d):
    d.text((W // 2, 34), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK,
           anchor="ma")
    title = "Sunday 22 November 2026"
    tw = d.textlength(title, font=F_MAST)
    emboss_text(d, ((W - tw) / 2, 74), title, F_MAST, INK, WHITE)
    # Italic sub-deck: the three leads, one line.
    d.text((W // 2, 126), SUBDECK, font=F_SUBDECK, fill=(70, 70, 70),
           anchor="ma")
    d.line([(MARGIN, 144), (W - MARGIN, 144)], fill=RED, width=3)


def stat_strip(d, y):
    sh = 44
    cell_w = CW // 6
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + i * cell_w
        card_shadow(d, [cx, y, cx + cell_w - 1, y + sh])
        d.rectangle([cx, y, cx + cell_w - 1, y + sh], fill=CARD,
                    outline=LINE, width=1)
        d.line([(cx + 1, y + 1), (cx + cell_w - 2, y + 1)], fill=WHITE)
        d.text((cx + cell_w // 2, y + 2), num, font=F_STAT_NUM, fill=RED,
               anchor="ma")
        d.text((cx + cell_w // 2, y + 30), label, font=F_STAT_LBL,
               fill=(60, 60, 60), anchor="ma")
    return y + sh


def region_strip(d, y):
    """Colour-coded region segments: one block per region."""
    h = 18
    n = len(REGIONS)
    cell_w = CW // n
    for i, (name, count, color) in enumerate(REGIONS):
        x0 = MARGIN + i * cell_w
        x1 = W - MARGIN if i == n - 1 else x0 + cell_w
        d.rectangle([x0, y, x1, y + h], fill=color)
        d.text(((x0 + x1) // 2, y + 3), "%s %d" % (name, count),
               font=F_REGION, fill=WHITE, anchor="ma")
    return y + h


def draw_lead(d, x, y, w, h, lead):
    """Lead card (v6): TALL art (92px) with a red kicker chip
    top-left, a white data chip top-right and a tag chip
    bottom-right, all ON the art; then a numbered red dateline, a
    serif headline and a deck that carries its source in parens
    (no separate source line, like the top 3).
    """
    card_shadow(d, [x, y, x + w, y + h])
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.line([(x + 1, y + 1), (x + w - 1, y + 1)], fill=WHITE)
    ART[lead["art"]](d, x + 6, y + 6, w - 12, 92)
    # Red kicker chip, top-left on the art.
    chip(d, x + 10, y + 10, lead["kicker"], F_CHIP, RED, WHITE)
    # White data chip, top-right on the art.
    cw = int(d.textlength(lead["chip"], font=F_CHIP)) + 14
    chip(d, x + w - 10 - cw, y + 10, lead["chip"], F_CHIP, WHITE, INK)
    # Tag chip, bottom-right on the art.
    tag = lead["tag"]
    tw = int(d.textlength(tag, font=F_ART_SMALL)) + 14
    chip(d, x + w - 10 - tw, y + 6 + 92 - 20, tag, F_ART_SMALL, WHITE,
         TAG_COLORS[tag])
    tx = x + 12
    tw = w - 24
    d.text((tx, y + 102), "%d  ·  %s" % (lead["num"], lead["dateline"]),
           font=F_DATELINE, fill=RED)
    ty = y + 116
    for line in cap_lines(d, wrap(d, lead["headline"], F_LEAD_HEAD, tw),
                          2, F_LEAD_HEAD, tw, lead["kicker"]):
        emboss_text(d, (tx, ty), line, F_LEAD_HEAD, INK, WHITE)
        ty += 18
    ty += 3
    for line in cap_lines(d, wrap(d, lead["deck"], F_LEAD_DECK, tw),
                          2, F_LEAD_DECK, tw, lead["kicker"]):
        d.text((tx, ty), line, font=F_LEAD_DECK, fill=(60, 60, 60))
        ty += 12


def leads_row(d, y):
    lh = 178
    lead_w, lead_gap = 325, 10
    for i, lead in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + lead_gap)
        draw_lead(d, lx, y, lead_w, lh, lead)
    return y + lh


def draw_feature(d, x, y, w, h, feat):
    """Feature card (v6): wide art panel with a red kicker chip
    top-left and a circled story number top-right, both ON the art;
    then a red dateline, a serif headline, a 2-line deck and a
    tag + source line at the bottom.
    """
    card_shadow(d, [x, y, x + w, y + h])
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.line([(x + 1, y + 1), (x + w - 1, y + 1)], fill=WHITE)
    FEAT_ART[feat["art"]](d, x + 1, y + 1, w - 2, 48)
    chip(d, x + 5, y + 5, feat["kicker"], F_CHIP_SM, RED, WHITE)
    number_circle(d, x + w - 13, y + 13, feat["num"])
    d.line([(x + 1, y + 49), (x + w - 1, y + 49)], fill=LINE)
    tx = x + 7
    tw = w - 14
    d.text((tx, y + 52), feat["dateline"], font=F_FEAT_DATE, fill=RED)
    ty = y + 64
    for line in cap_lines(d, wrap(d, feat["headline"], F_FEAT_HEAD, tw),
                          2, F_FEAT_HEAD, tw, feat["kicker"]):
        d.text((tx, ty), line, font=F_FEAT_HEAD, fill=INK)
        ty += 14
    ty += 2
    for line in cap_lines(d, wrap(d, feat["deck"], F_FEAT_DECK, tw),
                          2, F_FEAT_DECK, tw, feat["kicker"]):
        d.text((tx, ty), line, font=F_FEAT_DECK, fill=(60, 60, 60))
        ty += 11
    d.text((tx, y + h - 12), "%s · %s" % (feat["tag"], feat["source"]),
           font=F_SOURCE_SM, fill=GREY)


def features_grid(d, y):
    cols = 5
    gap = 6
    cell_w = (CW - gap * (cols - 1)) // cols  # 194
    cell_h = 130
    row_gap = 6
    for idx, feat in enumerate(FEATURES):
        r, c = divmod(idx, cols)
        x0 = MARGIN + c * (cell_w + gap)
        y0 = y + r * (cell_h + row_gap)
        draw_feature(d, x0, y0, cell_w, cell_h, feat)
    return y + 2 * cell_h + row_gap


def voices_strip(d, y):
    # Two figures with speech bubbles. Both quotes are verbatim from
    # Sunday-dated wires: Zelenskyy via ANI (Kyiv), Kurum via Reuters
    # (Antalya). No invented speech anywhere.
    h = 34
    x0, x1 = MARGIN, MARGIN + CW
    card_shadow(d, [x0, y, x1, y + h])
    d.rectangle([x0, y, x1, y + h], fill=CARD, outline=LINE, width=1)
    d.line([(x0 + 1, y + 1), (x1 - 1, y + 1)], fill=WHITE)
    d.text((x0 + 8, y + 12), "VOICES", font=F_VOICES, fill=RED)
    zx = x0 + 52
    draw_person(d, zx, y + 1, 30, 32, skin=(224, 184, 150),
                hair=(60, 45, 35), suit=(74, 86, 60))
    quote = ("\u201cNATO membership remains the clearest security "
             "guarantee\u201d")
    zbw = int(d.textlength(quote, font=F_BUBBLE)) + 16
    zbx = zx + 34
    draw_bubble(d, zbx, y + 3, zbw, 29, (zx + 24, y + 11))
    d.text((zbx + 8, y + 6), quote, font=F_BUBBLE, fill=INK)
    d.text((zbx + 8, y + 18), "\u2014 Zelenskyy, Kyiv \u00b7 ANI",
           font=F_BUBBLE_SM, fill=GREY)
    cx = zbx + zbw + 8
    draw_person(d, cx, y + 1, 26, 32, skin=(200, 160, 130),
                hair=(120, 120, 125), suit=(40, 60, 110), tie=(179, 32, 44))
    quote2 = ("\u201cWe believe that we have put forward a text which all "
              "the parties can agree upon.\u201d")
    cbw = int(d.textlength(quote2, font=F_BUBBLE)) + 16
    cbx = cx + 30
    draw_bubble(d, cbx, y + 3, cbw, 29, (cx + 20, y + 11))
    d.text((cbx + 8, y + 6), quote2, font=F_BUBBLE, fill=INK)
    d.text((cbx + 8, y + 18),
           "\u2014 Kurum, COP31 president \u00b7 Reuters",
           font=F_BUBBLE_SM, fill=GREY)
    return y + h


def lower_band(d, y):
    # Headers. The map pins match story numbers (1-13), so no legend
    # list is needed — the map is taller instead (130px, was 100).
    d.text((MARGIN, y), "WHERE IT HAPPENED", font=F_SECTION, fill=INK)
    d.text((MARGIN + d.textlength("WHERE IT HAPPENED  ", font=F_SECTION),
            y + 2), "pins match story numbers", font=F_SECTION_SM,
           fill=GREY)
    d.text((336, y), "ALSO ON SUNDAY — 22 MORE STORIES", font=F_SECTION,
           fill=INK)
    d.line([(MARGIN, y + 18), (326, y + 18)], fill=INK, width=1)
    d.line([(336, y + 18), (W - MARGIN, y + 18)], fill=INK, width=1)
    cy = y + 22
    draw_map(d, MARGIN, cy, 312, 130)
    # Briefs: 2 columns of 11, numbered 14-35 (global numbering).
    col_w = 329
    for col in range(2):
        bx = 336 + col * (col_w + 16)
        for row in range(11):
            idx = col * 11 + row
            if idx >= len(BRIEFS):
                continue
            brief = BRIEFS[idx]
            text, fnt = fit_one_line(d, "%d. %s" % (idx + 14, brief),
                                     F_BRIEF, F_BRIEF_SMALL, col_w,
                                     "brief %d" % (idx + 14))
            d.text((bx, cy + row * 17), text, font=fnt, fill=INK)
    briefs_end = cy + 11 * 17
    return briefs_end


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
# Budget (px): title 150, stat 44+4, region 18+6, leads 178+3,
# features 266+2, voices 34+2, lower 209+2, date check 58+2,
# footer 37 = 1,015 of 1,024 (9 px slack). The build raises on
# overflow, so any miscount surfaces instead of clipping.

def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    top_strip(d)
    title_block(d)
    y = 150
    y = stat_strip(d, y)
    y += 4
    y = region_strip(d, y)
    y += 6
    y = leads_row(d, y)
    y += 3
    y = features_grid(d, y)
    y += 2
    y = voices_strip(d, y)
    y += 2
    y = lower_band(d, y)
    y += 2
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
