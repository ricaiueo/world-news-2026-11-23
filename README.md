# world-news-2026-11-23

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ricaiueo/world-news-2026-11-23/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ricaiueo/world-news-2026-11-23/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A broadsheet news poster summarising the world news of Monday 23 November 2026.

`main.py` writes `entry.png` to the output directory. The image is rendered
ahead of time and committed here, so the run uses only the standard library,
touches no network, and writes the same bytes every time. Before writing, the
program checks the committed file is a whole PNG within the bounty's size caps.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```

## The stories

Every headline, figure and location is taken from a report published on
23 November 2026. Where sources gave different figures for a still-developing
toll, the figure is attributed to the source that published it.

| # | Desk | Story | Source |
| --- | --- | --- | --- |
| 1 | War | Russian strikes kill at least 15 in the Kyiv region | France 24 |
| 2 | Energy | Houthis hit Saudi refinery as Hormuz attacks widen | CNBC |
| 3 | Markets | AI-bubble fears drag Asian stocks lower | Al Jazeera |
| 4 | Technology | US widens Nvidia chip inquiry to Megaspeed | CNBC |
| 5 | Climate | Britain digs new reservoirs against drought | France 24 |
| 6 | Disaster | Factory fire toll climbs as search goes on | Al Jazeera |
| 7 | Sport | New Zealand battle to 239-5 to draw first Test | France 24 |

The three figures across the poster are 15 killed in the Kyiv region
(France 24), Brent crude at $92.35 in early Asia trading (CNBC), and a 350%
rise in attacks on medics in the occupied West Bank (Al Jazeera). The pull
quote is the WHO on fighting near an Ebola-zone hospital in DR Congo
(Al Jazeera).

## Design

Portrait broadsheet at 723x1024 — the bounty caps entries at 1024x1024 px, so
the poster keeps 1200:1700 proportions at a legal size. It is drawn at 2x and
downsampled so the type stays crisp. Newsprint paper, near-black ink and a
single vermilion spot colour; Franklin Gothic Condensed for headlines and
Georgia for body. The world map is a hand-encoded 5-degree land mask rendered
as halftone dots, with numbered markers matching the numbered stories.

## Rebuilding the image

`tools/render_poster.py` regenerates `entry.png`, with the land mask in
`tools/worldmap.py`. Development tools only — they need Pillow and local
fonts, and the graded entry never runs them.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
