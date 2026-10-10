# Phase 2: Direction

Choose a look and a motion language on purpose instead of shipping the first idea.
Output: `production.md` section 2. Look frames come later, in the storyboard phase,
rendered from the scaffolded project.

## 1. Measure the references

Pick two to four films of the same kind as the piece (a product launch with
interface, a model launch, a social cut, a brand spot) and measure them all the
same way:

```bash
python3 <this skill>/scripts/reference_study.py refs/*.mp4 --out refs/study
```

Each film gets contact sheets with one frame per shot, shot lengths, still holds,
motion and loudness each second, integrated loudness and its colours;
`refs/study/board.md` puts the films side by side. Open every sheet. Write the
piece's targets into `production.md` from the board (median shot, cuts a minute,
final hold, loudness and range, brightness) and from what the sheets show that
numbers miss: type size against frame height, words on screen, how the product is
framed, the signature device. Compare proportions, not pixels.

- Launch films, feature films, social cuts and brand spots: read `references/launch-films.md` first. It holds these measurements for 14 recent launch films; with no references supplied, name the two or three closest to the piece and use their numbers.
- Frame grabs and palettes in more depth: `animate/animate` (`new-style.md` and its measuring tools). Musical onsets and beat grids: `hf-kit/motion-showreel` (`analyze-reference`).
- Reference media stays local, out of git, and out of every deliverable.

## 2. Three directions, kill two

Write three directions, one paragraph each, filling the Direction table in
`production.md`. Dials: pace (cuts per second), density, camera (locked, push,
flythrough), texture (flat, grain, paper), palette, type, sound (bed and hits,
music-led, voice-led), and structure (opening state, where the turn lands, how it
ends). Any two directions differ on at least four dials.

Judge each one: Does it serve the one sentence from the brief? Is it the brand,
done better? Could a competitor use it unchanged (if yes, kill it)? Would it
survive weak assets or a slow render? The direction that matches the most obvious
reading of the brief is usually one of the two you kill. A direction that copies a
worked example from a library skill is killed and replaced, even when two
examples fit.
`launch-film/product-launch-motion` (creative-direction reference) has the full dial set.

Then name one **signature move**: a device you can say in one sentence that recurs
two or three times and pays off on the last motion beat, before any held call to
action (late in the motion, not at the end of the runtime).

## 3. Motion language

One value per row, recorded in `production.md`. Engines translate it; nobody invents
new values per scene.

| Personality | Durations | Overshoot |
|---|---|---|
| Playful | 150-300 ms | 10-20% |
| Premium | 350-600 ms | none |
| Corporate | 200-400 ms | 0-3% |
| Energetic | 100-250 ms | 15-30% |

The personality sets durations and overshoot. Easing always comes from the three
house curves below; a brand with its own signature curve swaps it in for the
entrance curve. Never add a curve per scene.

House curves and defaults:

- Entrances `cubic-bezier(0.16, 1, 0.3, 1)`; exits `cubic-bezier(0.7, 0, 0.84, 0)` at 60 to 75 percent of the entrance length; moves between states `cubic-bezier(0.65, 0, 0.35, 1)`. Linear only for continuous motion (rotation, drift, grain).
- Springs in one vocabulary, the damping ratio ζ = damping / (2·√(stiffness·mass)). Type and UI stay at ζ ≥ 0.7 (a hair of overshoot at most); one hero accent per piece may drop to about 0.5.
- A base unit (for example 100 ms, or 3 frames at 30 fps); every duration is a multiple.
- Stagger: words 60-90 ms, list items 40-80 ms, grid cells 20-40 ms; a whole group reveal finishes within 500 ms (700 ms when the group fills the frame), and the last item lands before the next beat.
- Intensity budget: nothing travels more than a third of the frame without an intermediate key; entrance scale 0.94 to 1.0; at most 2 or 3 things moving at once.
- Layers: primary at full amplitude, secondary at 30-50 percent and 50-100 ms behind, ambient at 10-20 percent. One hero per moment.
- Holds: at least 0.3 s of stillness after each beat. No frame is fully dead except the final hold; keep one small thing alive (grain, a caret, a slow drift).

| Spec | CSS | GSAP | Remotion | Motion (motion.dev) |
|---|---|---|---|---|
| entrance | `cubic-bezier(0.16,1,0.3,1)` | `"expo.out"` | `Easing.bezier(0.16,1,0.3,1)` | `ease: [0.16,1,0.3,1]` |
| exit | `cubic-bezier(0.7,0,0.84,0)` | `"expo.in"` | `Easing.bezier(0.7,0,0.84,0)` | `ease: [0.7,0,0.84,0]` |
| move | `cubic-bezier(0.65,0,0.35,1)` | `"power2.inOut"` | `Easing.bezier(0.65,0,0.35,1)` | `ease: [0.65,0,0.35,1]` |
| spring | `linear()` sampled from the spring | CustomEase sampled from the spring | `spring({frame, fps, config: {stiffness, damping, mass}})` | `type: "spring", stiffness, damping, mass` |

Lottie keyframes take the same bezier as tangents: `o: {x: [x1], y: [y1]}, i: {x: [x2], y: [y2]}`.
At 30 fps, frames = ms × 0.03 (300 ms is 9 frames).

## 4. House rules where the sources disagree

- Particles only when each particle is data or the subject (a number assembled from points), never as decoration.
- At most one overshoot or elastic accent per piece, and none on financial or otherwise serious content.
- Typing animation only inside an input field, never for headlines.
- No gradient-filled text (`background-clip: text` also vanishes in some captures).
- Glow only on the single hero element. No rainbow or purple-to-blue backgrounds, emoji used as icons, lorem ipsum, generic particle bursts, or a centered title on a gradient as the opening. A logo sting is never the whole ending.
- One accent color, and it means one thing for the whole piece.
- Avoid the default look: set the brand typeface, avoid crowded vertical stacks, and never make "everything fades up" the only entrance.

## 5. Type, color, composition

- House defaults when there is no brand: a warm off-white ground (`#F7F5F0`), near-black ink (`#17171A`) and one saturated accent chosen here for one meaning; one display grotesk (Instrument Sans, Manrope or General Sans) plus a mono for labels (JetBrains Mono), embedded locally.
- Video is not a web page. On a 1080 px tall frame: headlines 64-140 px, body 28-42 px, labels at least 28 px in 16:9 and 32 px in 9:16, strokes 2-4 px and chart lines 4 px or more. A 16:9 film watched on a phone shows at about a fifth of its size, so interface scenes scale up 1.6 to 2 times and frame tight on the action. Specs from other skills are sized for screens seen up close; judge everything on the phone sheet.
- Check every bitmap and 3D render against the palette and the one-accent rule before it goes in: renders from a brand kit can carry extra hues (golds, gradients) that read as a second accent. A hero object also needs a bridge, something already on screen that leads the eye into it.
- At most three families (display, UI sans, mono). Display type around 120-140 px on a 1080 px tall frame with slightly negative tracking. Small labels twice the size you first think.
- Palette: one primary, one accent, two or three neutrals tinted toward the primary; roughly 60/30/10 by area. Build ramps and gradients in OKLCH (`linear-gradient(in oklch, ...)`); add 3 to 5 percent grain against banding.
- One focal point per frame. Everything that must be read stays legible on a phone, judged at 360 px wide.
- Color management for video (Rec.709, tags, the QuickTime gamma trap): `iart/color-motion`.

## Library reads for this phase

| Need | Read |
|---|---|
| Direction dials, signature move, motion grammar | `launch-film/product-launch-motion` |
| Personality, durations, choreography, Disney principles for UI | `motion-principles/motion-principles` |
| Motion-language spec, brand words to motion | `iart/motion-art-direction` |
| Palettes, OKLCH, grading, color management | `iart/color-motion` |
| Grids, focal point, safe areas, camera vocabulary | `iart/shot-composition` |
| Easing, spring and timing numbers, texture | `claude-motion/motion-design` |
| Five-layer scene stack, hero color, grade and grain | `remotion-mg/remotion-motion-graphics` |
| Sixteen premium effect recipes | `launch-kit/motion-effects` |
| One persistent world, spotlight luminance, token discipline | `hf-kit/video-storytelling` |
| Ready styles, or a style built from references | `animate/animate` |
| 406 HyperFrames reference cards | `hf-kit/style-library` |
| Product UI that looks designed, not templated | an installed interface-design skill |
| A logo that does not exist yet | an installed logo skill |
| Charts and stat tiles in motion | an installed data-visualization skill (scale its specs up for video) |
