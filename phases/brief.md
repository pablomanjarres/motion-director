# Phase 1: Brief

Decide the job before any effect. Output: `production.md` section 1, `facts.md`,
and brand files when the client has a brand.

## Pick the track

| Track | The result is | Phases |
|---|---|---|
| film | a rendered video: launch film, product demo, explainer, reel, showreel, logo sting, B-roll over footage | all eight |
| web | motion inside a site or app: micro-interactions, page transitions, scroll stories, loaders | brief, direction, then `phases/web.md` |
| asset | a motion file someone else ships: Lottie or dotLottie, looping GIF or WebM, animated logo kit | brief, direction, storyboard, build, review, deliver |

## Intake

Ask once, in one batch, with a recommended default on every question. When the
person is away or says "just make it", take the defaults and record each one in
`production.md` under Decisions.

1. After watching, what does the viewer know or do? One sentence.
2. Where does it play? Use the channel table below for formats.
3. How long? Defaults: product demo 15 s, launch film 30 to 45 s, loop 8 s, logo sting 3 to 5 s, explainer 30 to 60 s.
4. Brand: logo files (SVG), fonts, colors, screenshots or product access. None means house defaults and a "Concept demo" label.
5. Sound: voice-over, a music track, or neither (synthesized effects and a bed).
6. Facts: approved numbers and claims, each with a source.
7. References: one to three videos or frames. A named style ("Linear launch", "Apple bumper", "Vox explainer") beats adjectives like "premium modern".

## Channel defaults

| Channel | Master | Also deliver | Note |
|---|---|---|---|
| X | 1920x1080 or 1080x1080 | 9:16 cut | autoplays muted; frame 0 is the thumbnail |
| LinkedIn | 1080x1350 (4:5) | 1:1 | captions on, sound off by default |
| Reels, TikTok, Shorts | 1080x1920 | none | keep text in the platform safe zone |
| Site hero, YouTube | 1920x1080 (or 3840x2160) | poster PNG | loop seam if it autoplays |
| Portfolio or marketplace sample | 1920x1080 | 1080x1920 plus source project | label self-initiated work |

Frame rate: 30 by default, 60 for fast UI or 3D flythroughs, 24 for handmade looks animated on twos.

## Choose the clock

Every duration comes from one clock. Pick it now and write it in section 1.

- **Voice**: record or synthesize the voice-over first (a scratch voice such as macOS `say` is fine until the real take exists). Measure each line; a shot holds for the measured line plus about 0.25 s, and the next shot starts at that hold.
- **Song**: map the beats before animating. The song decides the arc: the turn lands on the drop, the payoff on the loudest hit.
- **Grid**: choose fps and BPM so beats fall on whole frames (30 fps at 120 BPM is 15 frames per beat; 24 fps at 120 BPM puts an eighth note on 6 frames).
- **Reading time**: a short phrase holds at least 1 s plus 0.25 s per word beyond three; the closing line at least 2 s; a call to action at least 3 s.

## Truth gate

- Every number, name, quote and claim that appears on screen is listed in `facts.md` with its source and date. No entry, no number on screen.
- Never round up, add "+", or turn a target into a result. Keep measured results, targets and sample data apart.
- Sample content says so on every frame where it appears ("Concept demo", "Illustrative data"). Prefer relative bars and skeleton text to invented figures.
- Product screens are captured from the real product or rebuilt from real screenshots. Never present an invented screen as the product.
- Logos come from files. Never redraw a logo from memory and never imitate another company's brand.

## Brand files

When the client has a brand, write `brand.md` (under 300 words) and `MOTION.md` in
the project: colors with roles, type and sizes, timing, easing, texture, five
"never" rules, and "ASK ME" wherever the brand is unclear. `launch-kit/brand-intake`
runs the interview. Keep the files in the project and link them from
`production.md`; do not write rules into the project's CLAUDE.md.

## Decide deliverables now

Master plus every re-layout (9:16, 1:1, 4:5), captions, poster frame, loop or
silent cut, and the source project. Re-layouts are designed, never cropped, so
they shape the storyboard from the start.

## Library reads for this phase

| Need | Read |
|---|---|
| Turning a rough idea into a build brief | `launch-kit/motion-brief-writer` |
| Brand files from reference frames | `launch-kit/brand-intake` |
| Launch or product film intake, truth pass | `launch-film/product-launch-motion` (its story-and-truth reference) |
| Stylized explainer or short | `animate/animate` (`intake.md`) |
| Beginner-friendly interview and BRIEF.md | `hf-kit/make-a-video` |
| Talking-head footage | `hf-kit/short-form-edit` |

Create `production.md` from `templates/production.md`, fill section 1, add the
ledger rows, then move to `phases/direction.md`.
