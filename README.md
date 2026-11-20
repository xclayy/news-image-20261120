# The Brexit Reset

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/xclayy/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/xclayy/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A broadsheet front page that sums up the world's news of Friday, 20 November
2026 in a single 1024×1024 image — my entry for the make.fun competition
**"Sum up 20 November's world news in one image"**
(`news-image-20261120`). The 50 highest-ranked entries share $250 in USDC;
the deadline is Sunday, 22 November 2026, 07:00 WIB
(`2026-11-22T00:00:00Z`).

## The front page

The masthead dates the page — **FRIDAY, 20 NOVEMBER 2026** — above a dusk
photograph of the Berlaymont in Brussels, where the EU and British flags fly
side by side. That picture carries the day's lead story:

**UK AND EU SEAL BREXIT RESET DEAL** — At a UK–EU summit in Brussels,
Burnham and von der Leyen agree a Brexit reset: youth mobility of 100,000
people a year in each direction (ages 18–31/32, for three years), an end to
food checks, and relinked carbon markets.

Six more stories fill the 2×3 grid below the lead:

- **UKRAINE** — Russian ballistic missiles hit three Dnipro bridges in Kyiv
  overnight; three killed, 15 hurt.
- **MARKETS** — Taiwan stocks crash 6.2%: the Taiex sheds 2,393.60 to
  36,033.29 in its worst week since 1991, and TSMC falls below NT$2,000.
- **EUROPE** — Merz says new Ukraine talks including Europe are near, while
  Putin invites EU leaders to Moscow.
- **WORLD** — The US blacklists the Comancheros crime gang (Australia) and
  the 'Ndrangheta (Italy).
- **TECH** — Anthropic's record $81.3bn IPO closes today, after a debut that
  briefly valued the AI firm at $2tn.
- **CULTURE** — Fiona the hippo dies: Cincinnati Zoo's beloved hippo dies
  days after swallowing a visitor's hat.

A strip along the foot of the page adds three more items: Harris meets
Macron, Genoa airport halts flights after a drone, and Florida's 20th
execution this year.

## How it works

- `build_entry.py` — the builder. It loads the hero photograph from
  `assets/`, crops it to cover the hero band, shades its lower edge so the
  white headline stays legible, and draws the masthead, headline, lead deck,
  six-story grid and "Also today" strip on a 1024×1024 canvas with the
  Liberation fonts. The build is deterministic — no randomness, no network,
  no timestamps — so every run writes identical bytes. Run it with
  `python3 build_entry.py`; it prints the output size and sha256 and refuses
  to finish if the PNG is over the 1 MiB limit.
- `main.ts` — the entry program the competition harness runs (Node 22,
  standard library only). It copies `entry.png` from the repository into
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` when that variable
  is set), then reads both files back and fails unless they match byte for
  byte. Run it locally with
  `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`.
- `entry.png` — the finished front page (PNG, 1024×1024, under 1 MiB).
- `assets/` — the hero photograph of the EU quarter in Brussels at dusk and
  its generation metadata.

## Competition

"Sum up 20 November's world news in one image" on [make.fun](https://make.fun/bounty/news-image-20261120): an AI judge
that can see images compares entries two at a time and picks the one that
best sums up the day's world news; entries rank by how often they are
picked. The entry program writes one image to `/output/entry.png`, at most
1 MiB and at most 1024×1024 pixels, and it runs twice — both runs must write
the same bytes.

## License

MIT — see `LICENSE`.
