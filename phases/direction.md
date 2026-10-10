# Phase 2: Direction

Choose a look and a motion language on purpose instead of shipping the first idea.
Output: `production.md` section 2 and two to four look frames.

## 1. Measure the references

For each reference, write down numbers, not adjectives: palette (hex and the role
of each color), type (families, weights, size relative to frame height), motion
(entrance length, easing feel, stagger, hold length), cuts per second, camera
behavior, texture. Compare proportions, not pixels.

- Frame grabs and palettes: `animate/animate` (`new-style.md` and its measuring tools).
- Cut detection, contact sheets, onsets: `hf-kit/motion-showreel` (`analyze-reference`).
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
reading of the brief is usually one of the two you kill.
`launch-film/product-launch-motion` (creative-direction reference) has the full dial set.

Then name one **signature move**: a device you can say in one sentence that recurs
two or three times and pays off late (around 80 to 95 percent of the runtime).

## 3. Motion language

One value per row, recorded in `production.md`. Engines translate it; nobody invents
new values per scene.

| Personality | Durations | Easing | Overshoot |
|---|---|---|---|
| Playful | 150-300 ms | back-out | 10-20% |
| Premium | 350-600 ms | cubic-bezier(0.4, 0, 0.2, 1) | none |
| Corporate | 200-400 ms | cubic-bezier(0.2, 0, 0, 1) | 0-3% |
| Energetic | 100-250 ms | expo-out | 15-30% |

House defaults when the brand has no motion system:

- Entrances `cubic-bezier(0.16, 1, 0.3, 1)`; exits `cubic-bezier(0.7, 0, 0.84, 0)` at 60 to 75 percent of the entrance length; moves between states `cubic-bezier(0.65, 0, 0.35, 1)`. Linear only for continuous motion (rotation, drift, grain).
- Springs in one vocabulary, the damping ratio ζ = damping / (2·√(stiffness·mass)). Type and UI stay at ζ ≥ 0.7 (a hair of overshoot at most); one hero accent per piece may drop to about 0.5.
- A base unit (for example 100 ms, or 3 frames at 30 fps); every duration is a multiple.
- Stagger: words 60-90 ms, list items 40-80 ms, grid cells 20-40 ms; a whole group reveal stays under about 700 ms, and the last item lands before the next beat.
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

- At most three families (display, UI sans, mono). Display type around 120-140 px on a 1080 px tall frame with slightly negative tracking. Small labels twice the size you first think.
- Palette: one primary, one accent, two or three neutrals tinted toward the primary; roughly 60/30/10 by area. Build ramps and gradients in OKLCH (`linear-gradient(in oklch, ...)`); add 3 to 5 percent grain against banding.
- One focal point per frame. Everything that must be read stays legible on a phone, judged at 360 px wide.
- Color management for video (Rec.709, tags, the QuickTime gamma trap): `iart/color-motion`.

## 6. Look frames (still-frame gate)

Render two to four full-size stills of the most different beats in the chosen
direction. A weak still will not be rescued by motion: fix it here. When the person
is present, show the stills and get a yes before animating.

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
| Product UI that looks designed, not templated | registered skills `frontend-design`, `ui-ux-pro-max`, `ui-glowup` |
| A logo that does not exist yet | registered skill `create-logo` |
| Charts and stat tiles in motion | registered skill `dataviz` |
