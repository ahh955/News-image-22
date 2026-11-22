#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261122.

A 1024x1024 newspaper front page summing up the world news of
Sunday 22 November 2026: 3 leads + 11 features + 14 briefs, a
UTC timeline strip, a BY THE NUMBERS box, a short DATE CHECK box,
a look-ahead cell, and a VOICES strip with illustrated figures
(a verbatim Zelenskyy quote and factual labels — no invented speech).
on Sunday 22 November 2026 in at least one time zone.

Deterministic: no randomness, no clock, no network. Running it
twice produces byte-identical output (PIL writes no timestamps
into the PNG).

Usage: python3 compose.py [output-path]   (default: entry.png)
"""

import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
CW = W - 2 * MARGIN  # 996, content width

# Palette: light paper, black ink, newspaper red.
PAPER = (248, 245, 238)
INK = (24, 24, 24)
RED = (178, 30, 42)
DARK = (28, 28, 30)
GREY = (105, 102, 94)
LINE = (203, 196, 178)
SHADOW = (214, 208, 194)
SHADOW_SOFT = (227, 222, 210)
CARD = (255, 252, 245)
WHITE = (255, 255, 255)
SLATE = (52, 64, 84)
TAG_CONFIRMED = (27, 120, 70)
TAG_OFFICIAL = (30, 90, 160)
TAG_REPORTED = (176, 106, 12)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_MAST = font("DejaVuSerif-Bold.ttf", 40)
F_MAST_DATE = font("DejaVuSans-Bold.ttf", 19)
F_MAST_SUB = font("DejaVuSans.ttf", 11)
F_BAND = font("DejaVuSans-Bold.ttf", 17)
F_CHECK_HEAD = font("DejaVuSans-Bold.ttf", 14)
F_CHECK_BODY = font("DejaVuSans.ttf", 10)
F_TIME_HEAD = font("DejaVuSans-Bold.ttf", 11)
F_TIME = font("DejaVuSans.ttf", 10)
F_KICKER = font("DejaVuSans-Bold.ttf", 11)
F_LEAD1_HEAD = font("DejaVuSerif-Bold.ttf", 25)
F_LEAD1_DECK = font("DejaVuSans.ttf", 13)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 17)
F_LEAD_DECK = font("DejaVuSans.ttf", 12)
F_SOURCE = font("DejaVuSans.ttf", 10)
F_SECTION = font("DejaVuSans-Bold.ttf", 12)
F_FEAT_KICK = font("DejaVuSans-Bold.ttf", 9)
F_FEAT_TAG = font("DejaVuSans-Bold.ttf", 8)
F_FEAT_HEAD = font("DejaVuSans-Bold.ttf", 12)
F_FEAT_DECK = font("DejaVuSans.ttf", 10)
F_BRIEF_HEAD = font("DejaVuSans-Bold.ttf", 11)
F_BRIEF_DECK = font("DejaVuSans.ttf", 10)
F_NUM_HEAD = font("DejaVuSans-Bold.ttf", 11)
F_NUM_BODY = font("DejaVuSans.ttf", 10)
F_FOOT = font("DejaVuSans.ttf", 9)
F_BUBBLE_BOLD = font("DejaVuSans-Bold.ttf", 10)
F_BUBBLE_SMALL = font("DejaVuSans-Bold.ttf", 9)

TAG_COLORS = {
    "CONFIRMED": TAG_CONFIRMED,
    "OFFICIAL": TAG_OFFICIAL,
    "REPORTED": TAG_REPORTED,
}


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_capped(draw, text, fnt, width, max_lines):
    """Wrap to at most max_lines; ellipsis on the last line if cut."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "...", font=fnt) > width:
        last = last[:-1].rstrip(" ,;:")
    lines[-1] = last + "..."
    return lines


def vgrad(draw, box, c_top, c_bot):
    """Vertical gradient fill of box from c_top to c_bot (deterministic)."""
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / (h - 1) if h > 1 else 0
        c = tuple(int(c_top[k] + (c_bot[k] - c_top[k]) * t)
                  for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def emboss_text(draw, xy, text, fnt, fill, hi, dx=0, dy=1):
    """Text with a 1px offset underlay for a raised (4D) look."""
    draw.text((xy[0] + dx, xy[1] + dy), text, font=fnt, fill=hi)
    draw.text(xy, text, font=fnt, fill=fill)


def card_shadow(draw, box):
    """Soft two-layer drop shadow behind a card (draw before the card)."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0 + 3, y0 + 4, x1 + 3, y1 + 4], fill=SHADOW_SOFT)
    draw.rectangle([x0 + 2, y0 + 3, x1 + 2, y1 + 3], fill=SHADOW)


# ---------------------------------------------------------------- stories
# Tags: CONFIRMED (2+ outlets), OFFICIAL (on the record),
# REPORTED (single-source claim).

LEAD1 = {
    "kicker": "WAR IN UKRAINE  ·  OVERNIGHT",
    "headline": "Russia's biggest strike yet on Lviv: 50+ missiles, ~500 drones",
    "deck": "At least five killed — a family of four, including a 15-year-old "
            "girl, in Lapaivka, and a woman in Zaporizhzhia; about ten injured. "
            "Parts of Lviv are without power in likely the largest attack on "
            "the city of the war. Poland scrambled jets and Dutch F-35s "
            "responded; no Polish airspace violated in this attack.",
    "tag": "CONFIRMED",
    "source": "Reuters · AP",
}

LEADS23 = [
    {
        "kicker": "CLIMATE  ·  COP31, ANTALYA",
        "headline": "COP31 nears a deal — and admits 1.5°C is lost",
        "deck": "Talks ran past the deadline into early Sunday. President "
                "Kurum put a new package to a late-night plenary; objections "
                "by 03:00 GMT, approval 06:00 GMT. The Accords admit for the "
                "first time that 1.5°C is missed.",
        "tag": "CONFIRMED",
        "source": "Reuters",
        "icon": "globe",
    },
    {
        "kicker": "FORMULA 1  ·  LAS VEGAS GP",
        "headline": "Verstappen wins in Vegas — both McLarens thrown out",
        "deck": "Verstappen won under the lights. Norris and Piastri were "
                "disqualified for excessive skid-block wear — a dramatic "
                "title twist. The race began 20:00 local Saturday — 04:00 "
                "UTC Sunday.",
        "tag": "CONFIRMED",
        "source": "Sky Sports",
        "icon": "flag",
    },
]

FEATURES = [
    {
        "kicker": "CHINA · HONG KONG", "color": (30, 70, 140),
        "headline": "Hong Kong votes for the committee that picks its leader",
        "deck": "Polls 9am–6pm. 5,700 voters elect the 1,500-member committee "
                "picking the chief executive and legislators.",
        "tag": "OFFICIAL", "source": "info.gov.hk",
    },
    {
        "kicker": "INDIA · NEPAL", "color": (176, 106, 12),
        "headline": "Nepal's PM lands in Delhi on first trip abroad",
        "deck": "Balendra Shah begins a two-day state visit, his first to India "
                "since taking office in March. Talks with Modi on Monday.",
        "tag": "CONFIRMED", "source": "IANS · MEA",
    },
    {
        "kicker": "TENNIS · ATP FINALS, TURIN", "color": (27, 120, 70),
        "headline": "Alcaraz v Zverev for the ATP Finals crown today",
        "deck": "Singles final 18:00 CET; doubles final (Arevalo/Pavic v "
                "Arribage/Olivetti) 15:00 CET. Sinner withdrew, knee injury.",
        "tag": "CONFIRMED", "source": "ATP",
    },
    {
        "kicker": "CRICKET · WELLINGTON TEST", "color": (140, 40, 40),
        "headline": "Pant's 128 puts India in charge",
        "deck": "Pant's ninth Test century powered India to 629-6 at lunch on "
                "day four — the highest Test tally in New Zealand.",
        "tag": "CONFIRMED", "source": "Reuters",
    },
    {
        "kicker": "VATICAN · ROME", "color": (110, 70, 150),
        "headline": "Pope Leo XIV: Angelus for Christ the King",
        "deck": "At noon CET the Pope leads the Angelus for the Solemnity of "
                "Christ the King and the 41st World Youth Day.",
        "tag": "OFFICIAL", "source": "Vatican",
    },
    {
        "kicker": "VATICAN · WORLD DAY OF THE POOR", "color": (15, 118, 110),
        "headline": "Pope has lunch with 1,300 poor people",
        "deck": "Guests from 20+ Rome charities are served by Red Cross "
                "volunteers in the Paul VI Hall.",
        "tag": "OFFICIAL", "source": "Vatican",
    },
    {
        "kicker": "SPACE · NROL-136", "color": (40, 60, 120),
        "headline": "SpaceX launches spy satellites today",
        "deck": "Falcon 9 lifts off with the 15th batch of the NRO "
                "constellation. Booster B1097 flies a 14th time.",
        "tag": "CONFIRMED", "source": "SpaceX · VSFB",
    },
    {
        "kicker": "WEATHER · US EAST COAST", "color": (60, 100, 140),
        "headline": "Storm bearing down on East Coast — could become 'Kyle'",
        "deck": "A low off Florida tracks up the coast into Monday. The NHC "
                "gives it a 60% chance of becoming Storm Kyle; not yet named.",
        "tag": "OFFICIAL", "source": "NHC",
    },
    {
        "kicker": "AUSTRALIA · DEFENCE", "color": (110, 110, 40),
        "headline": "Australia hits back at US report on AUKUS subs",
        "deck": "Defence Minister Marles criticised the US Budget Office over "
                "a report saying AUKUS would cut US Navy submarines.",
        "tag": "CONFIRMED", "source": "Reuters",
    },
    {
        "kicker": "NFL · MEXICO CITY", "color": (150, 40, 40),
        "headline": "Sunday Night Football comes to Mexico City",
        "deck": "Vikings (7-2) v 49ers (8-1) — NFC seeding on the line. San "
                "Francisco favoured by 3 to 3.5; total 46.5.",
        "tag": "CONFIRMED", "source": "CBS Sports",
    },
    {
        "kicker": "FOOTBALL · PREMIER LEAGUE", "color": (178, 30, 42),
        "headline": "Pochettino's first game: Man Utd at Liverpool",
        "deck": "Mauricio Pochettino takes charge of Manchester United for the "
                "first time at Anfield. Hull City host Brighton at 14:00 GMT.",
        "tag": "CONFIRMED", "source": "Sportradar",
    },
]

BRIEFS = [
    ("MYANMAR QUAKE M4.1",
     "Early Sunday (02:35 IST), depth 95 km, near 24.4°N 94.6°E. — NCS"),
    ("PHILIPPINES QUAKES",
     "M4.6 at 08:23 AM off Balut Island, depth 10 km; felt in Kiamba, "
     "General Santos. M2.0 followed. — PHIVOLCS"),
    ("INDONESIA: HEAVY-RAIN ALERT",
     "BMKG alert in force today: 12 provinces 'Siaga', West Kalimantan "
     "'Awas'; strong winds Aceh, West Java."),
    ("JAPAN'S UFO TOWN CASHES IN",
     "As Tokyo heightens UAP alerts, Iino — 'UFO Village' — turns alien "
     "tourism into business. — ABC feature"),
    ("NBA: SEVEN GAMES TONIGHT",
     "Pistons at Hawks (3:30 PM ET) first up; Thunder at Heat 6 PM; "
     "Celtics at Warriors 8:30 PM the late show."),
    ("CHINA'S VICE PREMIER IN SINGAPORE",
     "Ding Xuexiang arrives today for a two-day visit, co-chairing the "
     "22nd Joint Council for Bilateral Cooperation."),
    ("SCO DIALOGUE FORUM ENDS",
     "The first SCO Civilizational Dialogue Forum concludes in New Delhi "
     "today after three days (20–22 Nov)."),
    ("VICTORIA: SIX DAYS TO THE POLLS",
     "Saturday's state election is six days away; polling puts the "
     "Coalition ahead 56–44 after preferences."),
    ("LA LIGA SUNDAY",
     "Barcelona–Villarreal 13:00; Racing Santander–Real Sociedad 15:15; "
     "Osasuna–Málaga 17:30; Getafe–Atlético 20:00."),
    ("SERIE A SUNDAY",
     "Juventus–Venezia 11:30; Bologna–Udinese, Sassuolo–Genoa 14:00; "
     "Milan–Frosinone 17:00; Atalanta–Inter 19:45."),
    ("GERMANY & FRANCE",
     "Bundesliga: Augsburg–Mainz, Werder–Hamburg. Ligue 1: Paris "
     "FC–Angers, Lorient–Rennes, Marseille–Le Mans."),
    ("FRANCE: PROTEST DISRUPTION CONTINUES",
     "Paris Métro Line 6 closed all day; highway blockades continue; US, "
     "UK, Canada, Australia advisories in force."),
    ("NFL WEEK 12: ELEVEN GAMES SUNDAY",
     "Before the Mexico City night game: Dolphins at Bills 1:00 PM ET "
     "headlines the early slate."),
    ("IRGC CLAIMS STRIKE ON US PATRIOT RADARS",
     "Iran's Revolutionary Guard claims a missile and drone operation "
     "hit two US Patriot air defence radars. — ANI"),
]

NUMBERS = (
    "5 killed in Lviv · ~500 drones · 629-6 India · 1,300 at Pope's lunch · "
    "856 HK candidates · 723 seats · 60% Kyle · 15th NROL · 7 NBA games"
)

LOOK_AHEAD = (
    "Mon: Nepal PM meets Modi. Tue: year's biggest supermoon. Sun 29 Nov: "
    "France v South Africa final."
)

VERIFIED = (
    "All stories checked and dated to Sunday 22 Nov 2026. Tags: CONFIRMED "
    "2+ · OFFICIAL record · REPORTED 2."
)

TIMELINE_LINES = [
    "OVERNIGHT Lviv strike · 00:23 PH quake M4.6 · 03:00 COP31 deadline · "
    "04:00 F1 Las Vegas · 06:00 COP31 approval",
    "09:00 HK polls open · 11:00 Pope Angelus · 12:16 SpaceX NROL-136 · "
    "15:00 ATP doubles · 16:30 Liverpool–Man Utd · 17:00 ATP final · 01:20 "
    "NFL Mexico City",
]

DATE_CHECK = (
    "Every story here happened, or was first reported, on Sunday 22 November "
    "2026. Deliberately NOT included — they happened earlier: Peru quake "
    "M6.7 (Fri) · Banda Sea quake M6.8 (Sat) · EU–Indonesia deal signed "
    "(Sat) · 'Chapo Isidro' raid (Fri) · Bolsonaro in ICU (Sat) · Iran "
    "strikes on Bahrain (Sat night) · Basra power fire (Sat) · BepiColombo "
    "at Mercury (Sat) · Lviv station strike (Fri — a different attack)"
)

FOOTER = (
    "Sources: Reuters · AP · Sky Sports · PHIVOLCS · NCS · BMKG · NHC · "
    "Vatican · SpaceX · IANS · MEA · info.gov.hk · CBS Sports · ANI — make.fun "
    "news-image-20261122"
)


# ---------------------------------------------------------------- drawing

def draw_tag(draw, x, y, tag):
    """Small coloured verification tag, right-aligned at x."""
    color = TAG_COLORS[tag]
    w = draw.textlength(tag, font=F_FEAT_TAG)
    draw.text((x - w, y), tag, font=F_FEAT_TAG, fill=color)
    return w


def draw_starburst(draw, box):
    """Procedural explosion graphic for the Lviv lead."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 6
    draw.rectangle(box, fill=(38, 34, 40))
    # rays
    import math
    for i in range(12):
        ang = math.pi * 2 * i / 12
        r1, r2 = 14, 52
        x_a = cx + r1 * math.cos(ang)
        y_a = cy + r1 * math.sin(ang) * 0.8
        x_b = cx + r2 * math.cos(ang)
        y_b = cy + r2 * math.sin(ang) * 0.8
        draw.line([(x_a, y_a), (x_b, y_b)], fill=(255, 170, 40), width=3)
    draw.ellipse([cx - 20, cy - 16, cx + 20, cy + 16], fill=(255, 200, 60))
    draw.ellipse([cx - 11, cy - 9, cx + 11, cy + 9], fill=(255, 240, 180))
    # smoke dots
    for dx, dy, r in [(-38, -22, 7), (40, -18, 6), (-42, 18, 6), (36, 22, 8)]:
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=(120, 116, 110))
    # drone dots
    for dx, dy in [(-52, -30), (52, -32), (-55, 8), (55, 2)]:
        draw.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2],
                     fill=(255, 255, 255))
    # reporter figure + LIVE label bubble, bottom-left of the panel
    fx, fy = x0 + 8, y1 - 34
    draw_person(draw, fx, fy, 26, 30, skin=(224, 184, 150),
                hair=(60, 45, 35), suit=(50, 55, 60),
                helmet=(90, 110, 150))
    label = "LIVE FROM LVIV"
    bw = int(draw.textlength(label, font=F_BUBBLE_SMALL)) + 14
    bx, by = x0 + 38, y1 - 58
    draw_bubble(draw, bx, by, bw, 18, (fx + 20, fy + 8),
                fill=RED, outline=(120, 16, 26))
    draw.text((bx + 7, by + 4), label, font=F_BUBBLE_SMALL, fill=WHITE)


def draw_globe_icon(draw, x, y, s):
    """Small globe: blue disc, green blobs, orbit ring."""
    draw.ellipse([x, y, x + s, y + s], fill=(70, 130, 200),
                 outline=(30, 70, 140), width=2)
    draw.ellipse([x + s * 0.2, y + s * 0.15, x + s * 0.5, y + s * 0.4],
                 fill=(90, 180, 110))
    draw.ellipse([x + s * 0.45, y + s * 0.55, x + s * 0.8, y + s * 0.85],
                 fill=(90, 180, 110))
    draw.arc([x - 4, y + s * 0.2, x + s + 4, y + s * 0.8], start=200,
             end=340, fill=(178, 30, 42), width=2)


def draw_flag_icon(draw, x, y, s):
    """Small chequered flag."""
    n = 4
    cell = s // n
    for r in range(n):
        for c in range(n):
            fill = DARK if (r + c) % 2 == 0 else WHITE
            draw.rectangle([x + c * cell, y + r * cell,
                            x + (c + 1) * cell, y + (r + 1) * cell],
                           fill=fill)
    draw.rectangle([x, y, x + s, y + s], outline=DARK, width=2)
    draw.line([(x, y), (x, y + s + 8)], fill=DARK, width=2)


def draw_person(draw, x, y, w, h, skin, hair, suit, helmet=None, tie=None):
    """Small stylized head-and-shoulders figure in an (x, y, w, h) box."""
    d = min(w - 6, 18)  # head diameter
    cx = x + w // 2
    hy = y + 1
    draw.rounded_rectangle([x, y + h - 14, x + w, y + h], radius=4,
                           fill=suit)
    draw.rectangle([cx - 3, hy + d - 3, cx + 3, hy + d + 2], fill=skin)
    draw.ellipse([cx - d // 2, hy, cx + d // 2, hy + d], fill=skin)
    top = helmet if helmet else hair
    draw.pieslice([cx - d // 2, hy, cx + d // 2, hy + d], start=180,
                  end=360, fill=top)
    if helmet:
        draw.rectangle([cx - d // 2 - 2, hy + d // 2 - 1,
                        cx + d // 2 + 2, hy + d // 2 + 2], fill=helmet)
    ex = d // 4
    ey = hy + d // 2 + 1
    draw.ellipse([cx - ex - 1, ey, cx - ex + 1, ey + 2], fill=INK)
    draw.ellipse([cx + ex - 1, ey, cx + ex + 1, ey + 2], fill=INK)
    if tie:
        draw.polygon([(cx - 3, y + h - 13), (cx + 3, y + h - 13),
                      (cx, y + h - 3)], fill=tie)


def draw_bubble(draw, x, y, w, h, tail_to, fill=WHITE, outline=INK):
    """Speech bubble: rounded rect + tail pointing at tail_to."""
    tx, ty = tail_to
    draw.polygon([(x + 8, y + h - 7), (x + 3, y + h - 2), (tx, ty)],
                 fill=fill)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=fill,
                           outline=outline, width=1)
    draw.line([(x + 8, y + h - 7), (tx, ty)], fill=outline, width=1)
    draw.line([(x + 3, y + h - 2), (tx, ty)], fill=outline, width=1)


def masthead(draw):
    vgrad(draw, [0, 0, W, 64], (44, 44, 48), (18, 18, 20))
    emboss_text(draw, (MARGIN, 6), "THE WORLD TODAY", F_MAST, WHITE,
                (0, 0, 0))
    d1 = "SUNDAY"
    d2 = "22 NOVEMBER 2026"
    w1 = draw.textlength(d1, font=F_MAST_DATE)
    w2 = draw.textlength(d2, font=F_MAST_DATE)
    rx = W - MARGIN
    draw.text((rx - w1, 6), d1, font=F_MAST_DATE, fill=(255, 120, 110))
    draw.text((rx - w2, 27), d2, font=F_MAST_DATE, fill=WHITE)
    draw.text((MARGIN, 50), "ONE DAY  ·  28 STORIES  ·  EVERY ONE VERIFIED",
              font=F_MAST_SUB, fill=(190, 186, 176))
    sub = "make.fun news-image-20261122"
    w = draw.textlength(sub, font=F_MAST_SUB)
    draw.text((rx - w, 50), sub, font=F_MAST_SUB, fill=(190, 186, 176))


def date_band(draw, y):
    vgrad(draw, [0, y, W, y + 22], (198, 45, 56), (156, 22, 34))
    text = "★  SUNDAY, 22 NOVEMBER 2026  ★  —  EVERY STORY ON THIS PAGE IS TODAY'S NEWS"
    w = draw.textlength(text, font=F_BAND)
    emboss_text(draw, ((W - w) / 2, y + 2), text, F_BAND, WHITE,
                (120, 16, 26))
    draw.rectangle([0, y + 22, W, y + 24], fill=(120, 16, 26))
    return y + 24


def date_check(draw, y):
    lines = wrap(draw, DATE_CHECK, F_CHECK_BODY, CW - 24)
    box_h = 8 + 16 + 2 + len(lines) * 12 + 6
    card_shadow(draw, [MARGIN, y, MARGIN + CW, y + box_h])
    draw.rectangle([MARGIN, y, MARGIN + CW, y + box_h], fill=CARD,
                   outline=RED, width=3)
    draw.text((MARGIN + 12, y + 6), "✓  DATE CHECK", font=F_CHECK_HEAD,
              fill=RED)
    head2 = "— Sunday, 22 November 2026 only"
    draw.text((MARGIN + 12 + draw.textlength("✓  DATE CHECK  ", font=F_CHECK_HEAD),
               y + 6), head2, font=F_CHECK_HEAD, fill=INK)
    ty = y + 6 + 16 + 2
    for line in lines:
        draw.text((MARGIN + 12, ty), line, font=F_CHECK_BODY, fill=INK)
        ty += 12
    return y + box_h


def timeline(draw, y):
    lines = TIMELINE_LINES
    box_h = 4 + len(lines) * 12 + 4
    card_shadow(draw, [MARGIN, y, MARGIN + CW, y + box_h])
    vgrad(draw, [MARGIN, y, MARGIN + CW, y + box_h], (64, 78, 100),
          (42, 52, 70))
    draw.text((MARGIN + 12, y + 4), "TODAY IN UTC", font=F_TIME_HEAD,
              fill=(255, 200, 60))
    ty = y + 4
    for line in lines:
        draw.text((MARGIN + 12 + 110, ty), line, font=F_TIME, fill=WHITE)
        ty += 12
    return y + box_h


def lead1(draw, y):
    text_w = CW - 170
    head_lines = wrap(draw, LEAD1["headline"], F_LEAD1_HEAD, text_w)
    deck_lines = wrap(draw, LEAD1["deck"], F_LEAD1_DECK, text_w)
    block_h = 4 + 14 + len(head_lines) * 29 + 4 + len(deck_lines) * 14 + 13 + 6
    card_shadow(draw, [MARGIN, y, MARGIN + CW, y + block_h])
    draw.rectangle([MARGIN, y, MARGIN + CW, y + block_h], fill=CARD,
                   outline=LINE, width=1)
    draw.rectangle([MARGIN, y, MARGIN + CW, y + 4], fill=RED)
    tx = MARGIN + 12
    ty = y + 9
    draw.text((tx, ty), LEAD1["kicker"], font=F_KICKER, fill=RED)
    draw_tag(draw, MARGIN + text_w + 4, ty + 2, LEAD1["tag"])
    ty += 14
    for line in head_lines:
        emboss_text(draw, (tx, ty), line, F_LEAD1_HEAD, INK, WHITE)
        ty += 29
    ty += 4
    for line in deck_lines:
        draw.text((tx, ty), line, font=F_LEAD1_DECK, fill=INK)
        ty += 14
    draw.text((tx, ty + 1), "Source: " + LEAD1["source"], font=F_SOURCE,
              fill=GREY)
    ax0 = MARGIN + CW - 158
    draw_starburst(draw, (ax0, y + 10, MARGIN + CW - 12, y + block_h - 10))
    return y + block_h


def leads23(draw, y):
    col_w = (CW - 10) // 2
    heights = []
    wrapped = []
    for lead in LEADS23:
        tw = col_w - 24
        hl = wrap(draw, lead["headline"], F_LEAD_HEAD, tw)
        dl = wrap(draw, lead["deck"], F_LEAD_DECK, tw)
        wrapped.append((hl, dl))
        heights.append(4 + 13 + len(hl) * 19 + 3 + len(dl) * 13 + 13 + 6)
    block_h = max(heights)
    for i, lead in enumerate(LEADS23):
        x0 = MARGIN + i * (col_w + 10)
        card_shadow(draw, [x0, y, x0 + col_w, y + block_h])
        draw.rectangle([x0, y, x0 + col_w, y + block_h], fill=CARD,
                       outline=LINE, width=1)
        draw.rectangle([x0, y, x0 + col_w, y + 4],
                       fill=(30, 90, 160) if i == 0 else (178, 30, 42))
        tx = x0 + 12
        ty = y + 9
        draw.text((tx, ty), lead["kicker"], font=F_KICKER,
                  fill=(30, 90, 160) if i == 0 else RED)
        draw_tag(draw, x0 + col_w - 12, ty + 2, lead["tag"])
        if lead["icon"] == "globe":
            draw_globe_icon(draw, x0 + col_w - 40, y + block_h - 38, 26)
        else:
            draw_flag_icon(draw, x0 + col_w - 40, y + block_h - 40, 26)
        ty += 13
        hl, dl = wrapped[i]
        for line in hl:
            emboss_text(draw, (tx, ty), line, F_LEAD_HEAD, INK, WHITE)
            ty += 19
        ty += 3
        for line in dl:
            draw.text((tx, ty), line, font=F_LEAD_DECK, fill=INK)
            ty += 13
        draw.text((tx, ty + 1), "Source: " + lead["source"], font=F_SOURCE,
                  fill=GREY)
    return y + block_h


def section_header(draw, y, text):
    draw.text((MARGIN, y), text, font=F_SECTION, fill=INK)
    tw = draw.textlength(text, font=F_SECTION)
    draw.line([(MARGIN + tw + 10, y + 8), (MARGIN + CW, y + 8)], fill=RED,
              width=2)
    return y + 13


def features_grid(draw, y):
    cols = 3
    gap = 9
    cell_w = (CW - gap * (cols - 1)) // cols
    cell_h = 63
    row_gap = 3
    # 11 features + 1 numbers box = 12 cells in 4 rows
    cells = list(FEATURES) + [{"numbers": True}]
    for idx, cell in enumerate(cells):
        r, c = divmod(idx, cols)
        x0 = MARGIN + c * (cell_w + gap)
        y0 = y + r * (cell_h + row_gap)
        card_shadow(draw, [x0, y0, x0 + cell_w, y0 + cell_h])
        draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], fill=CARD,
                       outline=LINE, width=1)
        draw.line([(x0 + 1, y0 + 1), (x0 + cell_w - 1, y0 + 1)], fill=WHITE)
        tx = x0 + 8
        tw = cell_w - 16
        if "numbers" in cell:
            draw.text((tx, y0 + 5), "BY THE NUMBERS", font=F_NUM_HEAD,
                      fill=RED)
            lines = wrap_capped(draw, NUMBERS, F_NUM_BODY, tw, 3)
            ty = y0 + 5 + 14
            for line in lines:
                draw.text((tx, ty), line, font=F_NUM_BODY, fill=INK)
                ty += 12
            continue
        draw.text((tx, y0 + 5), cell["kicker"], font=F_FEAT_KICK,
                  fill=cell["color"])
        draw_tag(draw, x0 + cell_w - 8, y0 + 6, cell["tag"])
        head_lines = wrap_capped(draw, cell["headline"], F_FEAT_HEAD, tw, 2)
        ty = y0 + 5 + 12
        for line in head_lines:
            draw.text((tx, ty), line, font=F_FEAT_HEAD, fill=INK)
            ty += 13
        deck_lines = wrap_capped(draw, cell["deck"], F_FEAT_DECK, tw, 2)
        for line in deck_lines:
            draw.text((tx, ty), line, font=F_FEAT_DECK, fill=(60, 60, 60))
            ty += 10
    return y + 4 * cell_h + 3 * row_gap


def briefs_grid(draw, y):
    cols = 3
    gap = 9
    cell_w = (CW - gap * (cols - 1)) // cols
    cell_h = 37
    row_gap = 2
    # 14 briefs + look-ahead + verified = 16 cells in 6 rows
    cells = [("brief", h, d) for h, d in BRIEFS]
    cells.append(("look", "COMING UP", LOOK_AHEAD))
    cells.append(("verified", "✓ VERIFIED", VERIFIED))
    for idx, cell in enumerate(cells):
        r, c = divmod(idx, cols)
        x0 = MARGIN + c * (cell_w + gap)
        y0 = y + r * (cell_h + row_gap)
        kind = cell[0]
        card_shadow(draw, [x0, y0, x0 + cell_w, y0 + cell_h])
        if kind == "verified":
            draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h],
                           fill=(232, 244, 232), outline=LINE, width=1)
        elif kind == "look":
            draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h],
                           fill=(235, 240, 248), outline=LINE, width=1)
        else:
            draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], fill=CARD,
                           outline=LINE, width=1)
        draw.line([(x0 + 1, y0 + 1), (x0 + cell_w - 1, y0 + 1)], fill=WHITE)
        tx = x0 + 8
        tw = cell_w - 16
        head_lines = wrap_capped(draw, cell[1], F_BRIEF_HEAD, tw, 1)
        draw.text((tx, y0 + 4), head_lines[0], font=F_BRIEF_HEAD,
                  fill=RED if kind == "brief" else INK)
        deck_lines = wrap_capped(draw, cell[2], F_BRIEF_DECK, tw, 2)
        ty = y0 + 4 + 13
        for line in deck_lines:
            draw.text((tx, ty), line, font=F_BRIEF_DECK, fill=(60, 60, 60))
            ty += 10
    # VOICES strip: row 6, columns 2-3 (row 6 col 1 is the verified
    # cell). Two figures with speech bubbles. The Zelenskyy quote is
    # verbatim from ANI's Kyiv report of 22 Nov 2026; the COP31 label is
    # a factual time from the timeline. No invented speech anywhere.
    vx0 = MARGIN + (cell_w + gap)
    vx1 = MARGIN + CW
    vy0 = y + 5 * (cell_h + row_gap)
    vy1 = vy0 + cell_h
    card_shadow(draw, [vx0, vy0, vx1, vy1])
    draw.rectangle([vx0, vy0, vx1, vy1], fill=CARD, outline=LINE, width=1)
    draw.line([(vx0 + 1, vy0 + 1), (vx1 - 1, vy0 + 1)], fill=WHITE)
    draw.text((vx0 + 8, vy0 + 14), "VOICES", font=F_FEAT_TAG, fill=RED)
    zx = vx0 + 48
    draw_person(draw, zx, vy0 + 2, 30, 33, skin=(224, 184, 150),
                hair=(60, 45, 35), suit=(74, 86, 60))
    quote = ("\u201cNATO membership remains the clearest security "
             "guarantee\u201d")
    zbw = int(draw.textlength(quote, font=F_BRIEF_DECK)) + 16
    zbx = zx + 34
    draw_bubble(draw, zbx, vy0 + 4, zbw, 29, (zx + 24, vy0 + 12))
    draw.text((zbx + 8, vy0 + 7), quote, font=F_BRIEF_DECK, fill=INK)
    draw.text((zbx + 8, vy0 + 19), "\u2014 Zelenskyy, Kyiv \u00b7 ANI",
              font=F_FEAT_TAG, fill=GREY)
    cx = zbx + zbw + 10
    draw_person(draw, cx, vy0 + 2, 26, 33, skin=(200, 160, 130),
                hair=(120, 120, 125), suit=(40, 60, 110),
                tie=(178, 30, 42))
    label2 = "COP31: APPROVAL 06:00 GMT"
    cbw = int(draw.textlength(label2, font=F_BUBBLE_BOLD)) + 16
    cbx = cx + 30
    draw_bubble(draw, cbx, vy0 + 7, cbw, 23, (cx + 20, vy0 + 12))
    draw.text((cbx + 8, vy0 + 12), label2, font=F_BUBBLE_BOLD, fill=INK)
    return y + 6 * cell_h + 5 * row_gap


def footer(draw, y):
    lines = wrap(draw, FOOTER, F_FOOT, CW)
    ty = y + 1
    for line in lines:
        w = draw.textlength(line, font=F_FOOT)
        draw.text(((W - w) / 2, ty), line, font=F_FOOT, fill=GREY)
        ty += 11
    return ty


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    y = 64
    y = date_band(draw, y)
    y += 2
    y = date_check(draw, y)
    y += 3
    y = timeline(draw, y)
    y += 3
    y = lead1(draw, y)
    y += 3
    y = leads23(draw, y)
    y += 3
    y = section_header(draw, y, "FEATURES — THE DAY IN DEPTH")
    y += 1
    y = features_grid(draw, y)
    y += 3
    y = section_header(draw, y, "IN BRIEF")
    y += 1
    y = briefs_grid(draw, y)
    y += 1
    y = footer(draw, y)
    if y > H:
        raise SystemExit("layout overflow: used %d px of %d" % (y, H))
    img.save(path, format="PNG")
    print("wrote %s (%d px used)" % (path, y))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
