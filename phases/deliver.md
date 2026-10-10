# Phase 8: Deliver

Every format is designed, encoded to spec, measured and packaged with its sources
and licenses. Output: the delivery folder and `production.md` section 8.

## 1. Re-layout, never crop

Each format is its own composition that shares the timeline and scenes and takes
a layout from a single function. Vertical stacks what sat side by side, raises
type sizes, and keeps the payload in the central band. Timing and message stay
identical.

| Format | Keep text and key UI inside |
|---|---|
| 9:16 at 1080x1920 (Reels, TikTok, Shorts) | x 90 to 960, y 360 to 1420 (platform UI covers the top 360 px, the bottom 500 px and the right 120 px) |
| 16:9 at 1920x1080 | 110 px from every edge |
| 4:5 at 1080x1350 and 1:1 at 1080x1080 | 80 px from every edge |

Feeds that autoplay muted show frame 0 as the thumbnail. If frame 0 is weak,
burn the poster into it: `-vf "overlay=0:0:enable='eq(n,0)'"` with the poster as
the second input.

## 2. Captions

When there is speech: one to three word pops or three to seven word karaoke lines,
each held at least 0.7 s, at most 17 characters per second, lines of 32 to 42
characters, timed from the word timings. Burn them in for social cuts and ship an
`.srt` beside every file.

## 3. Encode

Render one master per format, then encode every deliverable from it. Remotion:
`npx remotion render <id> master.mov --codec=prores --prores-profile=hq`, after
removing any global `Config.setCrf()` from `remotion.config.ts` (Remotion rejects a
CRF with ProRes, and the claude-motion template sets one). HyperFrames:
`hf.sh render --format mov`.

```bash
# H.264 delivery: limited range and BT.709 tags (setparams keeps the tags on current ffmpeg), fast start
ffmpeg -i master.mov -c:v libx264 -preset slow -crf 16 -profile:v high \
  -vf "scale=out_range=tv:out_color_matrix=bt709,format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709" \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart name_16x9_1920x1080_30p.mp4
# Platforms that reject silent uploads: add a silent track
ffmpeg -i silent.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -c:v copy -c:a aac -shortest out.mp4
# Editor masters: ProRes 422 HQ, or ProRes 4444 with alpha for overlays
ffmpeg -i in.mov -c:v prores_ks -profile:v 3 master_422hq.mov
ffmpeg -i in.mov -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le overlay_4444.mov
# Looping GIF for inboxes: frame 1 is the finished picture, no dithering on flat art
ffmpeg -i loop.mp4 -vf "fps=20,scale=896:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=full[p];[b][p]paletteuse=dither=none" loop.gif
# WebM for web-native loops
ffmpeg -i loop.mp4 -c:v libvpx-vp9 -b:v 0 -crf 32 -an loop.webm
```

Pick the poster frame at 200 px wide: if it does not read there, choose another.

## 4. Gate every file, not just the master

Run on each delivered file: the ffprobe gate and loudness check from
`phases/review.md`, and `scripts/frame_qa.py`. A vertical re-layout is a new film;
look at its contact sheet too.

## 5. Package

```
delivery/
  name_16x9_1920x1080_30p.mp4
  name_9x16_1080x1920_30p.mp4
  name_poster.png
  name.srt                 # when there is speech
  LICENSES.md              # engine, fonts, music, footage, icons, generated media
  source/                  # the project without node_modules, caches or renders, plus a README to re-render
  direction.md  facts.md  # the look, type, palette and motion language; production.md stays in the project
```

## 6. Licenses to record

| Item | Rule to check |
|---|---|
| Remotion | free for individuals, non-profits and companies up to three people; larger companies need a company license (confirm at remotion.dev/license for the commercial setup) |
| HyperFrames | Apache-2.0 |
| GSAP | free "no charge" license, including all plugins; not allowed inside a no-code visual animation builder that competes with Webflow |
| Motion, lottie-web, dotLottie | MIT (Motion+ components are paid) |
| Fonts | the font's own license (OFL fonts are fine to embed) |
| Music, footage, icons | the license record written at intake |
| Generated media | provider, model, seed, rights and likeness notes |

## 7. Sharing

Self-initiated work is labeled as a concept and never implies a client
relationship. A portfolio caption names the problem, your role and the formats
delivered. Open every share link while logged out before sending it.

## 8. Learn

In `production.md`, record estimated versus actual effort, what the critic caught,
and any new trap as symptom, cause, fix and proof, so the next piece starts ahead.

## Library reads for this phase

| Need | Read |
|---|---|
| Encode flags, silent track and ffprobe gate for 9:16 (skip its letterbox layout: re-layout instead) | `launch-kit/reel-export` |
| Looping GIF engineering and seam measurement | `launch-kit/loop-cover` |
| Deliverable sets, captions from word timings, poster choice | `launch-film/product-launch-motion` |
| One timeline laid out per format | `animate/animate` |
| Rec.709 tags, the QuickTime gamma trap | `iart/color-motion` |
| Clip naming, timing notes, compare page for B-roll | `broll/motion-broll` |
| Remotion rendering | `remotion/remotion-render` |
| HyperFrames rendering | `hyperframes/hyperframes-cli` |
