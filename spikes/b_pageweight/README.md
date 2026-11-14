# Spike B: page weight on a throttled phone

Throwaway prototypes and a measuring harness. Result and recommendation: `docs/spikes/m0-report.md`.

## What was measured
The same four page kinds (home, catalogue with a client-side filter, course page with an enrol button, lesson page with a video
facade and a "mark complete" button) in three builds, in Chromium emulating a phone (390 px, 4x slower CPU), with a cold cache:

| Build | Folder |
|---|---|
| **Today**: Mek Academy on Flask, behind a gzip proxy (what nginx does), real demo data | (runs from the other repository) |
| **Option 1**: Next.js 16 App Router, static pages, client components only for the interactive parts | `next-app/` |
| **Option 2**: Astro 6 with React islands (`client:visible`), static pages | `astro-app/` |

Network profiles: **fast 3G** (1.6 Mbps, 150 ms; the Lighthouse mobile profile) and **slow 3G** (400 Kbps, 400 ms).
Results are in `results/`.

## Run it
```bash
cd next-app && pnpm install && pnpm build && pnpm start        # port 3055
cd astro-app && pnpm install && pnpm build && pnpm start       # port 3056
node gzip-proxy.js 3057 3056                                   # compression in front of the Astro preview server
node measure.js fast3g "label" http://127.0.0.1:3055/ http://127.0.0.1:3055/courses
```
`measure.js` needs Playwright (`npm i playwright` or the one preinstalled in the Claude environment). It reports transferred
bytes by type, first and largest contentful paint, and the time until the network is idle (a proxy for "buttons work"; it
includes a 500 ms idle detection window). Each number is the median of three runs.

## Limits of this measurement
Emulated throttling, not a real handset; no images or web fonts (real course covers and an Amharic font add weight to every
option); the prototype CSS is smaller than Mek's real stylesheet (1 KB against 11 KB compressed), which flatters first paint for
both prototypes. Cold cache only: repeat visits reuse immutable scripts.
