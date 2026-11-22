# Sunday 22 November 2026 — The World in One Day

[![Competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/ahh955/News-image-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261122/ahh955/News-image-22/reward.svg)](https://make.fun/bounty/news-image-20261122)

A make.fun bounty entry: one program that writes one image summing up the
world news of **Sunday 22 November 2026** — a 1024×1024 newspaper front
page with **28 stories across 5 regions and 12 fields**, every one dated
Sunday 22 November 2026.

## The front page

- **3 big leads** — Russia's biggest strike yet on Lviv (50+ missiles,
  ~500 drones, at least 5 killed overnight); COP31 nears a deal in Antalya
  and admits for the first time that the 1.5°C goal is lost; Verstappen
  wins the Las Vegas Grand Prix while both McLarens are disqualified.
- **11 features** — Hong Kong votes for the Election Committee; Nepal's PM
  lands in Delhi on his first trip abroad; Alcaraz v Zverev in the ATP
  Finals; Pant's 128 puts India in charge in Wellington; Pope Leo XIV's
  Angelus and his lunch with 1,300 poor people; SpaceX launches NROL-136;
  the East Coast storm that could become Kyle; Australia hits back over
  AUKUS; Sunday Night Football in Mexico City; Pochettino's first game at
  Liverpool.
- **14 one-line briefs** with sources — the Myanmar and Philippines
  quakes, Indonesia's heavy-rain alert, Japan's UFO town, the NBA slate,
  China's vice premier in Singapore, the SCO forum's close, Victoria's
  election countdown, the European football fixtures, France's protest
  disruption, NFL Week 12, and the IRGC's claimed strike on US Patriot
  radars — plus a UTC timeline strip, a BY THE NUMBERS box, a look-ahead
  cell, a short **DATE CHECK** box naming the big Friday and Saturday
  stories deliberately left out, so nothing from an earlier day is ever
  presented as Sunday news, and a **VOICES** strip with illustrated
  figures: a verbatim Zelenskyy quote (ANI, Kyiv) and factual labels —
  no invented speech.

Every story carries a verification tag: **CONFIRMED** (2+ outlets),
**OFFICIAL** (on the record), or **REPORTED** (single source). Sources
are named beside each story. All illustrations are procedural drawings
made in code — no photos, no copied artwork. The page has a dimensional
("4D") treatment: soft drop shadows under the cards, a subtle bevel on
the masthead and lead headlines, and gentle gradients on the bands.

## How it works

`main.py` (Python 3.13, standard library only) copies the pre-built
`entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`). No network access
at runtime. The image itself is built by `compose.py` (PIL, DejaVu
fonts); running it twice produces byte-identical output.

```sh
python3 compose.py entry.png   # rebuild the image
python3 main.py                # copy it to /output/entry.png
```

## Files

| File | What it is |
| --- | --- |
| `entry.png` | The front page: 1024×1024 PNG, ≤ 1 MiB |
| `main.py` | Entrypoint: copies `entry.png` |
| `compose.py` | Builds `entry.png` from scratch (deterministic) |
| `LICENSE` | MIT |

## Date discipline

This entry covers **Sunday 22 November 2026 only**, under the rule that a
story counts if it happened, or was first reported, on Sunday in at least
one time zone. Friday's Peru quake, Trump data-centre threat and UK–EU
deal — Saturday's Banda Sea quake, EU–Indonesia signing, Bolsonaro ICU
admission, Bahrain strikes, Basra fire, BepiColombo arrival and France
marches — appear only in the DATE CHECK box, clearly labelled as not
Sunday news. The Myanmar quake (02:35 IST Sunday) and the Philippines
quake (00:23 UTC Sunday) are included with their times stated.
