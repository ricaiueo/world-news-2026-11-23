# world-news-2026-11-23

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ricaiueo/world-news-2026-11-23/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ricaiueo/world-news-2026-11-23/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summarising the world news of Monday 23 November 2026.

`main.py` writes `entry.png` to the output directory. The image is rendered
ahead of time and committed here, so the run uses only the standard library,
touches no network, and writes the same bytes every time. Before writing, the
program checks the committed file is a whole PNG within the competition's
size caps.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```

## What the image shows

Headlines are drawn from reports published on 23 November 2026 by Al Jazeera,
France 24 and CNBC. Where sources gave different figures for a still-developing
story, the image describes the scale in words rather than fixing on a number.

| Region | Story |
| --- | --- |
| Ukraine | Russian strikes kill at least 15 in the Kyiv region |
| Gulf | Houthis strike a Saudi refinery as Hormuz attacks widen |
| Markets | AI-bubble fears drag Asian stocks lower |
| Turkey | Thousands rally in Istanbul over the media crackdown |
| Indonesia | Dozens killed in a factory fire as the search goes on |
| DR Congo | WHO urges peace as fighting reaches an Ebola-zone hospital |
| Belgium | An anti-austerity strike shuts the country's airports |

## Rebuilding the image

`tools/render_entry.py` regenerates `entry.png`. It is a development tool only
— it needs Pillow and local fonts, and the graded entry never runs it.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
