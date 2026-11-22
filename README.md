# Sunday 22 November 2026 — The World in One Day

[![Competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/ahh955/News-image-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261122/ahh955/News-image-22/reward.svg)](https://make.fun/bounty/news-image-20261122)

A make.fun bounty entry: one program that writes one image summing up the
world news of **Sunday 22 November 2026** — a 1024×1024 newspaper front
page with **35 stories across 6 regions**, every one dated Sunday
22 November 2026.

## The front page

- **3 illustrated leads, image-led** — Iran strikes US bases in Bahrain
  overnight (two waves of drones and missiles on four bases; three
  tankers hit in Hormuz); Russia's biggest strike yet on Lviv (50+
  missiles, ~500 drones, at least 5 killed overnight); COP31 nears a
  deal in Antalya — the final text recalls the COP28 pact in full and
  drops the $120bn adaptation target, with the closing plenary still
  to open. Each lead has a tall procedural scene with a red kicker
  chip and a white data chip on the art, a numbered red dateline, a
  serif headline and a deck that names its sources.
- **An italic sub-deck** under the masthead naming the three leads, a
  **stat strip** with six lead-tied numbers, and a **colour-coded
  region strip**.
- **10 illustrated features** — every feature card carries a WIDE
  procedural scene across the top with a red kicker chip and a
  circled story number on the art: Iran's blackouts, the Russian
  cargo ship Sparta II still burning in the Gulf of Finland after a
  suspected drone strike, Hong Kong votes for the Election Committee,
  Nepal's PM lands in Delhi on his first trip abroad, the search for
  36 workers missing after a factory fire in Cikande, Indonesia, 14
  Iranian tankers sailing to break the blockade in the Strait of
  Hormuz, Alcaraz v Zverev in the ATP Finals, Pant's 128 puts India
  in charge in Wellington (India declared on a record 720-9),
  Verstappen winning a wild Las Vegas Grand Prix by 0.6s after 35
  lead changes, and the amputee World Cup final between Ghana and
  Morocco.
- **22 one-line briefs, numbered 14–35** — the Myanmar and Philippines
  quakes, Indonesia's heavy-rain alert, the NBA slate, China's vice
  premier in Singapore, the SCO forum's close, Victoria's election
  countdown, the European football fixtures, France's protest
  disruption, NFL Week 11, the UAE president receiving the US
  Homeland Security secretary, Eisenkot inviting Likud to coalition
  talks, Dubai's Icons of Porsche festival opening, the
  India–Bangladesh Ganga water talks in Dhaka, Marles on AUKUS, the
  Somalia deadline for the UAE envoy, Beijing opposing the US FCC
  telecom ban, the Pope's Sunday lunch for 1,300 poor people, the
  SpaceX NROL-136 launch, Sunday Night Football in Mexico City, and
  Pochettino's first game at Liverpool.
- **A world map with numbered dots** ("WHERE IT HAPPENED") pinning the
  leads and all ten features — the pins match the story numbers, so
  no legend is needed — a short **DATE CHECK** box naming the big
  Friday and Saturday stories deliberately left out, plus what was
  NOT yet known when the page was drawn (the COP31 final text, the
  Hong Kong results), so nothing from an earlier day is ever
  presented as Sunday news, and a **VOICES** strip with illustrated
  figures speaking verbatim Sunday quotes — Zelenskyy on NATO
  membership (ANI, Kyiv) and COP31 president Kurum on the deal text
  (Reuters, Antalya) — no invented speech.

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
one time zone. The Gulf strikes began Saturday 23:40 UTC, which is Sunday
06:40 in Jakarta, so they are today's news in Asia and are labelled
"OVERNIGHT". Friday's Peru quake (M6.7/M6.8 — one event, two estimates),
the Kryvyi Rih strike, the Bayelsa boat capsizing and the 'Chapo Isidro'
raid, Saturday's Bolsonaro ICU admission, Basra fire, BepiColombo arrival
and Gaza aid-van strike appear only in the DATE CHECK box, clearly
labelled as not Sunday news — even though some higher-ranked entries
present several of them as Sunday stories. The Myanmar quake (02:35 IST
Sunday) and the Philippines quake (00:23 UTC Sunday) are included with
their times stated. The Las Vegas Grand Prix ran Sunday 04:00–05:30 UTC;
Verstappen won by 0.639s from Norris after 35 lead changes (Reuters,
formula1.com, FIA). The Sparta II was struck Saturday morning but was
still burning at anchor on Sunday, with Finland leading the rescue — it
is framed as the ongoing Sunday story it is. The COP31 closing plenary
slipped from 06:00 GMT and had still not opened when the page was drawn;
the lead reports the deal as near, not done.
