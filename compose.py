#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261122 (v7 rebuild).

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

V7 vs v6 — v6 graded #1,213 (975,354, 11W/1D/0L); the one draw cost
dearly, but the live top 10 (22 Nov ~10:30 UTC) also shows REAL
content gaps, and v7 closes them:
  * UKRAINE NUMBERS CORRECTED: v6's "~500 drones / 50+ missiles"
    came from a single weak aggregator quoting Zelenskyy. The
    Ukrainian Air Force's own morning report says 186 drones were
    launched overnight and 161 were shot down or suppressed, with
    strikes at 18 sites — and the current #1, #7 and #15 all use
    186. V7 leads with the Air Force figures (stat strip, lead
    chip, sub-deck) and keeps the 5 Lviv dead (family of four)
    as a Zelenskyy-attributed deck line.
  * NEW FEATURE — DYMER: a Russian drone collapsed part of a
    5-storey apartment block in Dymer, Kyiv region, on Sunday
    morning; 14 feared trapped, 9 evacuated (Reuters, Zelenskyy).
    It replaces the Hormuz tanker convoy as a feature (single
    source, REPORTED) — the tankers drop to a brief.
  * FRESH SUNDAY STORIES the top entries carry and v6 lacks:
    the IRGC's claim of a 4th US drone downed in 24 hours over
    Hormuz, Odesa still without power/heat/water with classes
    online to 27 Nov, the UAE condemning Iran's Bahrain attack.
  * CRICKET UPDATED to stumps: NZ 119-2, trail by 233 (v6 had the
    tea score). HONG KONG UPDATED: turnout 97% by 4pm, a record
    (v6 had the 9am queues). GHANA-MOROCCO framed as tonight's
    final, 19:30 local (v6 read as if already played).
  * COP31: final text recalls COP28, drops the $120bn target and
    admits 1.5C will be breached; the plenary slipped to 11:00
    Antalya and adoption is still NOT confirmed — DATE CHECK
    lists it under "not yet known".
  * DATE CHECK now explicitly excludes Friday's 400-drone barrage
    by name (the #1 entry presents it as Sunday news) and the
    Shenzhen summit (Thu).
  * BOTTOM STRIP added ("THE WORLD IN ONE DAY — SUNDAY 22
    NOVEMBER 2026 · ONE PAGE"), as on the #1 entry; the footer
    drops to two lines to pay for it.
  * ATP deck fixed: v6's "World No. 1 Zverev" mislabelled Zverev
    — Alcaraz is the world No. 1.

Date honesty is unchanged: Friday's 400-drone barrage, the Peru
quake, Kryvyi Rih, the Bayelsa boat, 'Chapo Isidro', Bolsonaro's
ICU stay, the Basra fire and the Gaza aid-van strike stay EXCLUDED
(listed in DATE CHECK) even though the #1 entry presents several
of them as Sunday news. The France police-immunity law is Friday
and the sixth-weekend marches are Saturday — neither is presented
as Sunday news; the France brief keeps only Sunday's Metro Line 6
closure (verified: shut all day for works, RATP).

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
F_BOTTOM = font("DejaVuSans-Bold.ttf", 9)

TAG_COLORS = {
    "CONFIRMED": TAG_CONFIRMED,
    "OFFICIAL": TAG_OFFICIAL,
    "REPORTED": TAG_REPORTED,
}

# Truncation warnings collected while drawing; printed at the end so a
# build that silently cuts text is never mistaken for a clean one.
WARNINGS = []


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


# ---------------------------------------------------------------- stories
# Tags: CONFIRMED (2+ outlets), OFFICIAL (on the record),
# REPORTED (single-source claim). Stories are numbered 1-35 globally:
# leads 1-3, features 4-13, briefs 14-35. Map pins match the numbers.

SUBDECK = ("Iran hits US bases in Bahrain  ·  186 drones over Ukraine  ·  "
           "COP31 nears a deal")

LEADS = [
    {
        "num": 1, "kicker": "GULF WAR", "chip": "2 radars",
        "dateline": "BAHRAIN  ·  IRAN WAR",
        "headline": "Iran strikes US bases in Bahrain",
        "deck": "IRGC claims two Patriot radars hit; Bahrain: "
                "industrial site burned, no injuries. (IRGC, Fars)",
        "tag": "CONFIRMED",
        "art": "gulf",
    },
    {
        "num": 2, "kicker": "LVIV: BARRAGE", "chip": "186 drones",
        "dateline": "LVIV, UKRAINE  ·  WAR",
        "headline": "186 drones in one night over Ukraine",
        "deck": "186 launched, 161 downed; 18 sites hit. Five dead "
                "in Lviv, incl. a family of four. (Air Force)",
        "tag": "CONFIRMED",
        "art": "lviv",
    },
    {
        "num": 3, "kicker": "COP31: DEAL CLOSE", "chip": "~200 nations",
        "dateline": "ANTALYA, TURKEY  ·  CLIMATE",
        "headline": "COP31 nears a deal at last",
        "deck": "Final text recalls COP28, drops $120bn target, "
                "admits 1.5°C will be breached. (Reuters, AP)",
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
        "deck": "856 chase 723 seats; turnout 97% by 4pm — a record.",
        "tag": "CONFIRMED", "source": "SCMP · China Daily",
        "art": "ballot",
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
        "num": 9, "kicker": "14 TRAPPED",
        "dateline": "DYMER, UKRAINE",
        "headline": "Drone flattens Kyiv apartment block",
        "deck": "5-storey block collapses; 14 feared trapped, "
                "9 evacuated.",
        "tag": "CONFIRMED", "source": "Reuters", "art": "rubble",
    },
    {
        "num": 10, "kicker": "ATP FINAL",
        "dateline": "TURIN, ITALY",
        "headline": "Alcaraz v Zverev for the crown",
        "deck": "World No. 1 Alcaraz meets Zverev tonight, 18:00 CET.",
        "tag": "CONFIRMED", "source": "ATP", "art": "tennis",
    },
    {
        "num": 11, "kicker": "PANT 128",
        "dateline": "WELLINGTON, NZ",
        "headline": "Pant's 128 puts India on top",
        "deck": "India declare on a record 720-9; NZ 119-2 at stumps, "
                "trail by 233.",
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
        "deck": "First all-African final tonight, 19:30 local.",
        "tag": "CONFIRMED", "source": "WAFF", "art": "trophy",
    },
]

# Briefs are stories 14-35 (global numbering continues from features).
# Each must fit one line at 10-11px across 329px; the build warns on
# any truncation, so over-long lines surface instead of clipping.
BRIEFS = [
    "MYANMAR M4.1 — early Sun. (02:35 IST), depth 95 km (NCS)",
    "PHILIPPINES — M4.6 off Balut Is. 08:23 (PHIVOLCS)",
    "INDONESIA — Heavy-rain alert: 12 provinces 'Siaga' (BMKG)",
    "GULF — IRGC claims 4th US drone downed in 24 hours (IRGC)",
    "SINGAPORE — China's VP Ding arrives for 2-day visit",
    "ODESA — Power, heat, water out; classes online to 27 Nov",
    "VICTORIA — Six days to polls; Coalition ahead 56–44",
    "LA LIGA — Barcelona–Villarreal 13:00; Getafe–Atlético 20:00",
    "SERIE A — Juventus–Venezia 11:30; Atalanta–Inter 19:45",
    "FRANCE — Métro Line 6 shut all day; blockades end (RATP)",
    "NFL WK 11 — Dolphins at Bills 1:00 PM ET; Bills -16.5",
    "UAE — Condemns Bahrain attack; hosts US security chief",
    "ISRAEL — Eisenkot invites Likud to coalition talks (ANI)",
    "HORMUZ — 14 tankers sail to break blockade (REPORTED)",
    "GANGA — India–Bangladesh water talks, day 2 in Dhaka",
    "AUKUS — Marles: CBO 'wrong'; 'AUKUS is happening'",
    "SOMALIA — UAE envoy's 72-hour deadline expires today",
    "CHINA — Beijing opposes US FCC telecom ban (Reuters)",
    "VATICAN — Pope leads Angelus, lunches with 1,300 poor",
    "SPACEX — Falcon 9 lifts NROL-136 spy satellites, 04:16 PT",
    "NFL MEXICO — Vikings v 49ers at 7,300 ft, 8:20pm ET (NFL)",
    "LIVERPOOL — Pochettino's Man Utd debut at Anfield (BBC)",
]

# All six stats are tied to the three leads plus the biggest brief
# (the Java fire) — v6's "~500 drones / 50+ missiles" pair is
# replaced by the Air Force's verified 186/161 and the IRGC's
# 2-radar claim.
STATS = [
    ("186", "drones fired at Ukraine"),
    ("2", "Patriot radars claimed hit"),
    ("03:00", "GMT deadline for objections"),
    ("35%", "electricity goal by 2035"),
    ("5", "killed in Lviv overnight"),
    ("36", "missing in Java factory fire"),
]

# Region name, story count, strip colour. Counts sum to 35:
# EUROPE 11 (Lviv, COP31, Sparta II, Dymer, Turin, Odesa, La Liga,
# Serie A, France, Vatican, Liverpool); ASIA 9 (Hong Kong, Delhi,
# Cikande, Myanmar, Philippines, Indonesia, Singapore, Ganga,
# China); MIDDLE EAST 6 (Bahrain, Tehran, Gulf drone, UAE, Israel,
# Hormuz tankers); AMERICAS 4 (Las Vegas, NFL, SpaceX, NFL Mexico);
# AFRICA 2 (Ghana–Morocco, Somalia); OCEANIA 3 (Wellington,
# Victoria, AUKUS).
REGIONS = [
    ("EUROPE", 11, (70, 110, 180)),
    ("ASIA", 9, (200, 160, 40)),
    ("MIDDLE EAST", 6, (180, 50, 50)),
    ("AMERICAS", 4, (60, 140, 90)),
    ("AFRICA", 2, (200, 120, 40)),
    ("OCEANIA", 3, (90, 140, 200)),
]

# ~300 chars: wraps to exactly 2 lines at 11px across CW-24 (972px).
# New in v7: Friday's 400-drone barrage is excluded BY NAME (the #1
# entry presents it as Sunday news) and the Shenzhen summit (Thu) is
# listed too. "Not yet known" is now COP31 adoption (the plenary
# slipped to 11:00 Antalya and no adoption was confirmed by wires
# time) and the HK results.
DATE_CHECK = (
    "Wires read up to 10:30 UTC, Sunday 22 November 2026. Left out "
    "as other days' news: the Peru quake (Fri) · the 400-drone "
    "barrage (Fri) · 'Chapo Isidro' (Fri) · Kryvyi Rih (Fri) · "
    "Bayelsa boat (Fri) · Bolsonaro ICU (Sat) · Basra fire (Sat) · "
    "Shenzhen summit (Thu). Not yet known: COP31 adoption · "
    "HK results."
)

# Two lines in v7 (was three): the "every story happened..." line is
# dropped — the top strip and DATE CHECK already state the day —
# and its 12px pay for the new bottom strip.
FOOTER = [
    "Sources: Reuters · AP · Fars · IRGC · RFE/RL · Vatican · SpaceX · SCMP · Radio Nepal · ATP · Cricinfo · NFL · BBC · F1 · WAFF · ANI · WAM · Finland · China Daily — make.fun news-image-20261122",
    "Tags: CONFIRMED = verified by 2+ outlets  ·  OFFICIAL = on the record  ·  REPORTED = single-source claim.",
]


# ---------------------------------------------------------------- lead art
# Each lead art panel is (w-12) x 92 px. Like the current #1, each
# carries a small caption label bottom-left naming the image's
# source context ("BAHRAIN GOVT", "OFFICIALS' COUNT",
# "SUMMIT PRESIDENT") — small white text on a dark bar.


def art_caption(d, x, y, w, h, text):
    """Small caption label bottom-left on lead art (like the #1)."""
    tw = int(d.textlength(text, font=F_ART_SMALL)) + 10
    th = 13
    d.rectangle([x + 4, y + h - th - 4, x + 4 + tw, y + h - 4],
                fill=(15, 15, 15))
    d.text((x + 9, y + h - th - 2), text, font=F_ART_SMALL, fill=WHITE)


def art_gulf(d, x, y, w, h):
    """Night air base under attack: radar dishes, hangars, missile
    trails arcing in, a fire burning at a building, smoke."""
    vgrad(d, [x, y, x + w, y + h], (8, 12, 30), (30, 26, 40))
    # Stars.
    for sx, sy in [(20, 8), (60, 14), (120, 6), (180, 12), (240, 8),
                   (290, 16), (90, 20), (210, 22), (150, 10), (30, 26)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(220, 220, 220))
    # Moon.
    d.ellipse([x + w - 40, y + 6, x + w - 24, y + 22], fill=(235, 230, 200))
    d.ellipse([x + w - 36, y + 8, x + w - 26, y + 18], fill=(40, 36, 50))
    # Missile trails arcing in from the top-left.
    for (tx0, ty0, tx1, ty1) in [(40, 0, 90, 46), (80, 0, 150, 52),
                                (140, 0, 220, 44)]:
        d.line([(x + tx0, y + ty0), (x + tx1, y + ty1)],
               fill=(255, 180, 60), width=2)
        d.ellipse([x + tx1 - 3, y + ty1 - 3, x + tx1 + 3, y + ty1 + 3],
                  fill=(255, 220, 120))
    # Radar dish, left.
    d.line([(x + 34, y + 78), (x + 34, y + 52)], fill=(150, 150, 150),
           width=3)
    d.pieslice([x + 18, y + 38, x + 50, y + 62], start=200, end=340,
               fill=(190, 190, 190))
    # Hangars.
    for hx in (70, 130):
        d.pieslice([x + hx, y + 56, x + hx + 56, y + 92], start=180,
                   end=360, fill=(60, 60, 70))
        d.rectangle([x + hx, y + 74, x + hx + 56, y + 92],
                    fill=(50, 50, 58))
    # Building on fire, right.
    d.rectangle([x + 210, y + 52, x + 260, y + 92], fill=(70, 60, 55))
    d.polygon([(x + 222, y + 52), (x + 232, y + 30), (x + 240, y + 46),
               (x + 248, y + 32), (x + 252, y + 52)],
              fill=(255, 120, 20))
    d.polygon([(x + 228, y + 52), (x + 236, y + 38), (x + 244, y + 52)],
              fill=(255, 200, 60))
    # Smoke column.
    for i, (sx, sy, sr) in enumerate([(236, 22, 8), (242, 14, 6),
                                      (248, 8, 5)]):
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(90, 90, 95))
    # Ground line + runway lights.
    d.rectangle([x, y + 88, x + w, y + h], fill=(20, 18, 24))
    for lx in range(8, w, 24):
        d.ellipse([x + lx - 1, y + 90, x + lx + 1, y + 92],
                  fill=(255, 200, 60))
    art_caption(d, x, y, w, h, "BAHRAIN GOVT")


def art_lviv(d, x, y, w, h):
    """Night city under a drone barrage: skyline, explosions,
    searchlight beams, drone silhouettes with red lights."""
    vgrad(d, [x, y, x + w, y + h], (6, 10, 28), (40, 30, 45))
    # Stars.
    for sx, sy in [(14, 10), (48, 6), (90, 12), (140, 8), (200, 6),
                   (260, 10), (300, 14), (170, 16), (110, 20)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(210, 210, 210))
    # Searchlight beams from the ground.
    for (bx0, bx1) in [(60, 120), (220, 160)]:
        d.polygon([(x + bx0, y + 88), (x + bx0 + 6, y + 88),
                   (x + bx1 + 14, y + 6), (x + bx1, y + 6)],
                  fill=(200, 200, 180))
    # Skyline silhouette with lit windows.
    d.rectangle([x, y + 60, x + w, y + h], fill=(15, 15, 20))
    for (bx, bw, bh) in [(0, 34, 30), (36, 26, 42), (64, 40, 24),
                         (106, 30, 48), (138, 44, 32), (184, 28, 40),
                         (214, 36, 26), (252, 30, 44), (284, 29, 30)]:
        d.rectangle([x + bx, y + 88 - bh, x + bx + bw, y + 88],
                    fill=(25, 25, 32))
        for wy in range(y + 92 - bh, y + 86, 8):
            for wx in range(x + bx + 4, x + bx + bw - 3, 8):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4],
                                fill=(255, 200, 80))
    # Explosions over the skyline.
    for (ex, ey, er) in [(120, 52, 14), (232, 48, 11), (60, 58, 8)]:
        d.ellipse([x + ex - er, y + ey - er, x + ex + er, y + ey + er],
                  fill=(255, 140, 30))
        d.ellipse([x + ex - er // 2, y + ey - er // 2,
                   x + ex + er // 2, y + ey + er // 2],
                  fill=(255, 220, 100))
    # Drones: small X silhouettes with red lights.
    for (dx, dy) in [(90, 22), (190, 14), (260, 26), (30, 30)]:
        d.line([(x + dx - 5, y + dy - 3), (x + dx + 5, y + dy + 3)],
               fill=(10, 10, 10), width=2)
        d.line([(x + dx - 5, y + dy + 3), (x + dx + 5, y + dy - 3)],
               fill=(10, 10, 10), width=2)
        d.ellipse([x + dx - 2, y + dy - 2, x + dx + 2, y + dy + 2],
                  fill=(255, 40, 40))
    art_caption(d, x, y, w, h, "OFFICIALS' COUNT")


def art_cop31(d, x, y, w, h):
    """Summit hall: flags row, podium with a globe, a "FINAL TEXT"
    document panel, delegate rows below."""
    vgrad(d, [x, y, x + w, y + h], (20, 60, 90), (12, 40, 60))
    # Flags row along the top.
    flag_colors = [(200, 40, 40), (40, 120, 200), (40, 160, 80),
                   (220, 180, 40), (150, 60, 180), (40, 180, 180),
                   (230, 120, 40), (100, 100, 200)]
    for i, fc in enumerate(flag_colors):
        fx = x + 10 + i * 38
        d.line([(fx, y + 4), (fx, y + 26)], fill=(200, 200, 200), width=1)
        d.rectangle([fx, y + 4, fx + 26, y + 18], fill=fc)
    # Podium + globe, left.
    d.rectangle([x + 20, y + 56, x + 90, y + 88], fill=(90, 60, 30))
    d.rectangle([x + 16, y + 52, x + 94, y + 58], fill=(120, 80, 40))
    d.ellipse([x + 36, y + 28, x + 74, y + 56], fill=(60, 140, 200),
              outline=(255, 255, 255), width=1)
    d.ellipse([x + 44, y + 34, x + 56, y + 44], fill=(80, 180, 90))
    d.ellipse([x + 58, y + 42, x + 68, y + 52], fill=(80, 180, 90))
    # "FINAL TEXT" document panel, centre-right.
    d.rectangle([x + 120, y + 24, x + 236, y + 82], fill=(250, 248, 240),
                outline=(180, 170, 150), width=1)
    d.rectangle([x + 120, y + 24, x + 236, y + 36], fill=RED)
    d.text((x + 128, y + 27), "FINAL TEXT", font=F_ART_SMALL,
           fill=WHITE)
    for i, ln in enumerate(["COP28 recalled in full",
                            "$120bn target dropped",
                            "1.5°C breach admitted"]):
        d.text((x + 128, y + 42 + i * 13), ln,
               font=font("DejaVuSans.ttf", 9), fill=INK)
    # Delegate rows, bottom.
    for i in range(9):
        px = x + 252 + (i % 3) * 20
        py = y + 40 + (i // 3) * 16
        d.ellipse([px, py, px + 10, py + 10], fill=(220, 180, 140))
        d.rectangle([px - 2, py + 10, px + 12, py + 16],
                    fill=(50, 70, 100))
    art_caption(d, x, y, w, h, "SUMMIT PRESIDENT")


ART = {"gulf": art_gulf, "lviv": art_lviv, "cop31": art_cop31}


# ---------------------------------------------------------------- feature art
# Each feature art panel is (w-2) x 48 px (192x48). Wide top art with
# a red kicker chip top-left and a circled story number top-right,
# both drawn by draw_feature on top of the art.


def art_blackout(d, x, y, w, h):
    """City skyline at night, most windows dark, a few lit."""
    vgrad(d, [x, y, x + w, y + h], (10, 14, 34), (25, 22, 35))
    d.ellipse([x + w - 30, y + 4, x + w - 16, y + 18],
              fill=(235, 230, 200))
    for (bx, bw, bh) in [(0, 30, 26), (32, 24, 36), (58, 34, 20),
                         (94, 26, 40), (122, 30, 28), (154, 38, 34)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                    fill=(20, 20, 28))
        for wy in range(y + h - bh + 4, y + h - 3, 7):
            for wx in range(x + bx + 4, x + bx + bw - 3, 7):
                if (wx * 7 + wy * 3) % 11 == 0:
                    d.rectangle([wx, wy, wx + 2, wy + 3],
                                fill=(255, 200, 80))
    # One dark block with a single candle-lit window.
    d.rectangle([x + 70, y + h - 18, x + 78, y + h - 10],
                fill=(255, 180, 60))


def art_ship_fire(d, x, y, w, h):
    """Cargo ship on a grey sea, fire and smoke amidships."""
    vgrad(d, [x, y, x + w, y + h], (120, 130, 145), (170, 175, 185))
    d.rectangle([x, y + 30, x + w, y + h], fill=(60, 90, 120))
    for wx in range(4, w, 18):
        d.line([(x + wx, y + 36), (x + wx + 10, y + 36)],
               fill=(140, 180, 210), width=1)
        d.line([(x + wx + 6, y + 43), (x + wx + 16, y + 43)],
               fill=(140, 180, 210), width=1)
    # Hull + containers.
    d.polygon([(x + 20, y + 30), (x + 172, y + 30), (x + 164, y + 42),
               (x + 28, y + 42)], fill=(40, 50, 60))
    for i, cc in enumerate([(200, 60, 50), (60, 140, 90), (220, 170, 50),
                            (70, 110, 180), (200, 120, 40)]):
        d.rectangle([x + 30 + i * 22, y + 18, x + 50 + i * 22, y + 30],
                    fill=cc)
    # Bridge tower.
    d.rectangle([x + 148, y + 8, x + 164, y + 30], fill=(220, 220, 220))
    d.rectangle([x + 150, y + 12, x + 162, y + 16], fill=(30, 60, 90))
    # Fire amidships + smoke.
    d.polygon([(x + 84, y + 18), (x + 92, y + 2), (x + 98, y + 12),
               (x + 104, y + 4), (x + 108, y + 18)],
              fill=(255, 120, 20))
    d.polygon([(x + 90, y + 18), (x + 96, y + 8), (x + 102, y + 18)],
              fill=(255, 200, 60))
    for (sx, sy, sr) in [(100, 2, 6), (108, -2, 5)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(100, 100, 105))


def art_ballot(d, x, y, w, h):
    """Ballot box with a voting slip going in, red seal."""
    vgrad(d, [x, y, x + w, y + h], (240, 235, 220), (215, 205, 185))
    # Ballot box.
    d.rectangle([x + 60, y + 18, x + 132, y + 44], fill=(200, 200, 200),
                outline=(120, 120, 120), width=1)
    d.rectangle([x + 60, y + 18, x + 132, y + 24], fill=(179, 32, 44))
    d.rectangle([x + 88, y + 18, x + 104, y + 22], fill=(40, 40, 40))
    d.text((x + 96, y + 28), "723", font=F_ART_TITLE, fill=INK,
           anchor="ma")
    # Slip going in.
    d.polygon([(x + 84, y + 20), (x + 108, y + 20), (x + 104, y + 2),
               (x + 88, y + 2)], fill=(255, 255, 255),
              outline=(150, 150, 150))
    d.line([(x + 92, y + 8), (x + 100, y + 16)], fill=RED, width=2)
    d.line([(x + 100, y + 16), (x + 104, y + 5)], fill=RED, width=2)
    # Queue of voters, right.
    for i in range(3):
        px = x + 148 + i * 14
        d.ellipse([px, y + 26, px + 9, y + 35], fill=(220, 180, 140))
        d.rectangle([px - 2, y + 35, px + 11, y + 44],
                    fill=(60, 90, 130))


def art_plane(d, x, y, w, h):
    """Airliner descending over a runway, Delhi dusk."""
    vgrad(d, [x, y, x + w, y + h], (250, 200, 130), (220, 140, 90))
    d.ellipse([x + w - 34, y + 4, x + w - 14, y + 24],
              fill=(255, 240, 200))
    # Runway.
    d.rectangle([x, y + 40, x + w, y + h], fill=(70, 70, 75))
    for lx in range(6, w, 20):
        d.line([(x + lx, y + 44), (x + lx + 10, y + 44)],
               fill=(255, 255, 255), width=2)
    # Plane silhouette.
    px, py = x + 60, y + 16
    d.ellipse([px, py, px + 70, py + 10], fill=(250, 250, 250))
    d.polygon([(px + 24, py + 8), (px + 44, py + 20), (px + 52, py + 20),
               (px + 46, py + 8)], fill=(230, 230, 230))
    d.polygon([(px + 56, py + 2), (px + 66, py - 6), (px + 70, py - 6),
               (px + 68, py + 4)], fill=(179, 32, 44))
    d.rectangle([px + 58, py + 2, px + 68, py + 8], fill=(179, 32, 44))
    for wx in range(px + 8, px + 56, 8):
        d.rectangle([wx, py + 3, wx + 4, py + 6], fill=(40, 80, 120))
    # Control tower.
    d.rectangle([x + 160, y + 14, x + 168, y + 40], fill=(120, 120, 125))
    d.rectangle([x + 154, y + 8, x + 174, y + 16], fill=(90, 130, 170))


def art_java_fire(d, x, y, w, h):
    """Factory building with flames and a fire crew's water jet."""
    vgrad(d, [x, y, x + w, y + h], (45, 35, 40), (90, 70, 60))
    # Factory shed.
    d.rectangle([x + 20, y + 18, x + 130, y + 44], fill=(120, 115, 110))
    d.polygon([(x + 16, y + 18), (x + 75, y + 6), (x + 134, y + 18)],
              fill=(90, 85, 80))
    d.rectangle([x + 30, y + 28, x + 48, y + 44], fill=(60, 55, 50))
    d.rectangle([x + 100, y + 28, x + 120, y + 36], fill=(60, 55, 50))
    # Flames from the roof.
    d.polygon([(x + 60, y + 8), (x + 70, y - 6), (x + 76, y + 4),
               (x + 84, y - 4), (x + 90, y + 8)],
              fill=(255, 120, 20))
    d.polygon([(x + 66, y + 8), (x + 74, y - 2), (x + 82, y + 8)],
              fill=(255, 200, 60))
    # Smoke.
    for (sx, sy, sr) in [(78, -4, 7), (88, -8, 6), (98, -10, 5)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(110, 110, 115))
    # Firefighter with a water jet.
    d.ellipse([x + 152, y + 26, x + 160, y + 34], fill=(255, 200, 40))
    d.rectangle([x + 150, y + 34, x + 162, y + 44], fill=(200, 60, 40))
    for i in range(6):
        d.ellipse([x + 146 - i * 8, y + 26 - i * 2,
                   x + 150 - i * 8, y + 30 - i * 2],
                  fill=(150, 200, 255))


def art_rubble(d, x, y, w, h):
    """Collapsed apartment block at dawn: a half-standing slab,
    a rubble mound, a crane, rescue lights in the dust."""
    vgrad(d, [x, y, x + w, y + h], (70, 80, 100), (150, 140, 125))
    # Standing half of the block, left, broken top edge.
    d.polygon([(x + 8, y + 44), (x + 8, y + 10), (x + 34, y + 4),
               (x + 52, y + 12), (x + 58, y + 8), (x + 66, y + 16),
               (x + 66, y + 44)], fill=(150, 145, 135))
    for wy in range(y + 14, y + 42, 8):
        for wx in range(x + 12, x + 62, 12):
            d.rectangle([wx, wy, wx + 6, wy + 5], fill=(60, 60, 65))
    # Rubble mound, centre-right.
    d.polygon([(x + 66, y + 44), (x + 96, y + 22), (x + 130, y + 28),
               (x + 150, y + 44)], fill=(120, 112, 100))
    d.polygon([(x + 84, y + 40), (x + 100, y + 30), (x + 112, y + 40)],
              fill=(140, 132, 118))
    d.polygon([(x + 108, y + 42), (x + 122, y + 32), (x + 134, y + 42)],
              fill=(100, 94, 84))
    # Leaning concrete slab.
    d.polygon([(x + 118, y + 30), (x + 142, y + 12), (x + 148, y + 16),
               (x + 126, y + 36)], fill=(165, 160, 150))
    # Crane arm.
    d.line([(x + 168, y + 44), (x + 168, y + 6)], fill=(200, 160, 40),
           width=3)
    d.line([(x + 168, y + 6), (x + 186, y + 6)], fill=(200, 160, 40),
           width=2)
    d.line([(x + 186, y + 6), (x + 186, y + 18)], fill=(60, 60, 60),
           width=1)
    d.rectangle([x + 182, y + 18, x + 190, y + 24], fill=(60, 60, 60))
    # Rescue lights in the dust.
    for (lx, ly) in [(92, 38), (120, 40), (150, 40)]:
        d.ellipse([x + lx - 3, y + ly - 3, x + lx + 3, y + ly + 3],
                  fill=(255, 220, 80))
    # Dust haze.
    for (dx, dy, dr) in [(80, 18, 9), (110, 12, 7), (140, 20, 8)]:
        d.ellipse([x + dx - dr, y + dy - dr, x + dx + dr, y + dy + dr],
                  fill=(175, 168, 152))


def art_tennis(d, x, y, w, h):
    """Indoor court at night: net, ball in play, crowd dots."""
    vgrad(d, [x, y, x + w, y + h], (30, 50, 90), (20, 35, 70))
    # Crowd dots.
    for i in range(24):
        cx = 8 + (i % 12) * 16
        cy = 4 + (i // 12) * 6
        d.ellipse([x + cx, y + cy, x + cx + 4, y + cy + 4],
                  fill=(180, 180, 190) if i % 3 else (220, 200, 120))
    # Court.
    d.rectangle([x, y + 22, x + w, y + h], fill=(40, 110, 70))
    d.line([(x + 10, y + 28), (x + w - 10, y + 28)], fill=(255, 255, 255),
           width=1)
    d.line([(x + 10, y + 44), (x + w - 10, y + 44)], fill=(255, 255, 255),
           width=1)
    d.line([(x + w // 2, y + 28), (x + w // 2, y + 44)],
           fill=(255, 255, 255), width=1)
    # Net.
    d.line([(x + w // 2, y + 22), (x + w // 2, y + 34)],
           fill=(20, 20, 20), width=2)
    # Players (small figures) + ball.
    for (px, pc) in [(40, (255, 255, 255)), (150, (255, 80, 80))]:
        d.ellipse([x + px, y + 30, x + px + 7, y + 37], fill=(220, 180, 140))
        d.rectangle([x + px - 1, y + 37, x + px + 8, y + 44], fill=pc)
    d.ellipse([x + 118, y + 14, x + 126, y + 22], fill=(220, 230, 60))


def art_cricket(d, x, y, w, h):
    """Day four at the Basin: batsman, stumps, green outfield."""
    vgrad(d, [x, y, x + w, y + h], (140, 190, 230), (200, 225, 240))
    d.ellipse([x + w - 30, y + 4, x + w - 14, y + 20],
              fill=(255, 245, 180))
    d.rectangle([x, y + 30, x + w, y + h], fill=(70, 150, 80))
    # Pitch strip.
    d.rectangle([x + 70, y + 30, x + 122, y + h], fill=(200, 180, 140))
    # Stumps.
    for sx in (88, 94, 100):
        d.rectangle([x + sx, y + 26, x + sx + 2, y + 34],
                    fill=(255, 220, 120))
    # Batsman.
    d.ellipse([x + 108, y + 18, x + 116, y + 26], fill=(40, 40, 40))
    d.rectangle([x + 106, y + 26, x + 118, y + 40], fill=(255, 255, 255))
    d.line([(x + 112, y + 36), (x + 104, y + 46)], fill=(200, 160, 100),
           width=3)
    # Ball + score bug.
    d.ellipse([x + 60, y + 22, x + 66, y + 28], fill=(200, 40, 40))
    d.rectangle([x + 6, y + 4, x + 62, y + 18], fill=(20, 20, 20))
    d.text((x + 10, y + 6), "720-9 dec", font=F_ART_SMALL, fill=WHITE)


def art_racecar(d, x, y, w, h):
    """Night street circuit: chequered flag, speed lines, F1 car."""
    vgrad(d, [x, y, x + w, y + h], (10, 10, 30), (40, 30, 70))
    # Chequered flag, top-left.
    for r in range(2):
        for c in range(6):
            fill = DARK if (r + c) % 2 == 0 else WHITE
            d.rectangle([x + 4 + c * 8, y + 3 + r * 4,
                         x + 12 + c * 8, y + 7 + r * 4], fill=fill)
    # Speed lines behind the car.
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
    """Gold cup on green, ball at the foot, confetti."""
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
    "java_fire": art_java_fire, "rubble": art_rubble,
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
# order 1-13 (the pins ARE the legend — no legend list is needed).
# Nudges (pins are 11px wide; neighbours need >=12px of separation):
# pin 1 (Bahrain) west and pin 4 (Tehran) north-east so they clear
# each other; pin 5 (Sparta II) north-east of Loviisa; pin 9 (Dymer,
# true lon ~30.3E) nudged EAST to 40E — at its true position it
# would sit ~6px from pin 2 (Lviv) and overlap it; pin 10 (Turin)
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
    (9, 50.8, 40.0),    # Dymer, Kyiv region (nudged east)
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
    """Lead card: TALL art (92px) with a red kicker chip top-left, a
    white data chip top-right and a tag chip bottom-right, all ON the
    art; then a numbered red dateline, a serif headline and a deck
    that carries its source in parens (no separate source line, like
    the top 3). The art itself carries a small caption label
    bottom-left (see art_caption).
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
    """Feature card: wide art panel with a red kicker chip top-left
    and a circled story number top-right, both ON the art; then a
    red dateline, a serif headline, a 2-line deck and a tag + source
    line at the bottom.
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
    # list is needed — the map is taller instead (130px).
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


def bottom_strip(d, y):
    """Thin dark strip closing the page (like the #1 entry):
    the paper's name on the left, the day + 'ONE PAGE' on the right."""
    h = 14
    d.rectangle([MARGIN, y, MARGIN + CW, y + h], fill=INK)
    d.text((MARGIN + 8, y + 3), "THE WORLD IN ONE DAY",
           font=F_BOTTOM, fill=WHITE)
    right = "SUNDAY 22 NOVEMBER 2026 · ONE PAGE"
    rw = d.textlength(right, font=F_BOTTOM)
    d.text((MARGIN + CW - 8 - rw, y + 3), right, font=F_BOTTOM,
           fill=(255, 200, 60))
    return y + h


# ---------------------------------------------------------------- assembly
# Budget (px): title 150, stat 44+4, region 18+6, leads 178+3,
# features 266+2, voices 34+2, lower 209+2, date check 58+2,
# footer 25, bottom strip 14 = 1,017 of 1,024 (7 px slack).
# The build raises on overflow, so any miscount surfaces instead
# of clipping.

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
    y = bottom_strip(d, y)
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
