# world-news-2026-11-23

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ricaiueo/world-news-2026-11-23/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ricaiueo/world-news-2026-11-23/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A dense printed-newspaper front page summarising the world news of Monday
23 November 2026: a six-figure numbers row, a region tally bar, seven lead
stories with flat illustrations, a located map, six further reports and a
24-hour UTC filing strip.

`main.py` writes `entry.png` to the output directory. The image is rendered
ahead of time and committed here, so the run uses only the standard library,
touches no network, and writes the same bytes every time. Before writing, the
program checks the committed file is a whole PNG within the bounty's caps.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```

## The stories

Every headline, figure and location comes from a report published on
23 November 2026. Nothing is invented. Where sources gave different figures
for a still-developing toll, the figure is attributed to the outlet that
published it. The numbers on the map match the numbers beside the stories.

| # | Desk | Story | Figure | Source |
| --- | --- | --- | --- | --- |
| 1 | War | Russian strikes kill at least 15 in the Kyiv region | 15 killed | France 24 |
| 2 | Energy | Houthis hit Saudi refinery as attacks widen | Brent $92.35 | CNBC |
| 3 | Rights | Attacks on medics up 350%, group says | +350% | Al Jazeera |
| 4 | Disaster | Factory fire: 24 recovered at Cikande, Banten | 24 recovered | Al Jazeera |
| 5 | Sport | New Zealand draw first Test at 239-5 | 239-5 | France 24 |
| 6 | Security | Warsaw says Russia twice targeted a rapper | 2 plots | Al Jazeera |
| 7 | Markets | AI-bubble fears drag Asian stocks lower | — | Al Jazeera |

Story 7 carries no figure: no second source could date-confirm a percentage
for the selloff, so none is shown rather than guessed. The time strip plots
only the two reports whose filing time was published, and says so for the
other five.

## Design

Portrait broadsheet, designed at 1200x1700 and rendered to 723x1024 — the
bounty caps entries at 1024x1024 px, so the page keeps its proportions at a
legal size. Drawn at 2x device scale and downsampled so the type stays crisp.

Newsprint paper `#F1ECE1`, ink `#161412`, a single vermilion accent `#D2381E`.
Playfair Display for headlines, Source Serif 4 for body, IBM Plex Mono for
labels. Columns are divided by hairline rules, not cards. The world map is
real country geometry (Natural Earth via `world-atlas`, drawn with `d3-geo`),
the lead illustration is flat shapes over an SVG halftone pattern, and an
`feTurbulence` grain sits over the whole page.

## Rebuilding the image

`tools/poster.html` is the poster; `tools/render.py` shoots it with headless
Chrome and writes `entry.png`. Development tools only — they need Chrome and
Pillow, and the graded entry never runs them. `tools/vendor/` holds pinned
copies of d3, topojson-client and the Natural Earth atlas.
