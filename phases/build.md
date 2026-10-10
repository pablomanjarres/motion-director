# Phase 5: Build

Make the film frame-exact, rough first, polished second. Output: the source
project, versioned drafts and the build log in `production.md` section 5.

## 1. Rough cut first

Block every beat with final timing, real text and placeholder shapes at half
resolution. Judge reading time and rhythm on that draft. Shadows, texture and
grade come after the rough cut works.

## 2. Determinism contract (every engine)

Every visual is a pure function of the current frame or time. Then any single
frame renders on its own, parallel renders agree, motion blur and QA work, and
cues stay locked to words.

- No CSS transitions or animations, timers, `requestAnimationFrame` clocks, `Date.now`, `performance.now` or `Math.random` in anything that renders. Use a seeded generator (for example mulberry32) keyed by element index.
- Seek third-party animation instead of letting it play: a GSAP timeline stays paused and is set per frame (`tl.pause(t)`; when seeking to the same time twice, nudge it first, `tl.totalTime(t + 0.001, true); tl.totalTime(t, true)`), WAAPI animations get `pause()` and `currentTime = t * 1000`, Lottie gets `goToAndStop(frame, true)` and dotLottie `setFrame(frame)`. Libraries that only run in real time stay out of renders.
- Fonts and images finish loading before frame 0 (`await document.fonts.ready`, decoded images). Fonts are local files; nothing fetches from the network while rendering.
- Springs are closed-form. A value retargeted several times is the sum of one spring per change, so seeking stays continuous.
- Canvas that reads pixels back uses `getContext('2d', { willReadFrequently: true })`. Guard `pow()` bases and NaN: one bad pixel can black out a bloomed frame.
- Prove it with `python3 <this skill>/scripts/frame_qa.py a.mp4 --against b.mp4` on two renders of the same frames.

## 3. Structure

- Palette, type, easing and durations live in one tokens module filled from the motion-language spec; scenes import it.
- Repeated content is data: one card component plus an array, one scene component per beat, one layout function that knows every format.
- Every start and end time comes from the timeline file.
- Each element has one owner per property at a time; two overlapping tweens on the same opacity strobe in the final render.

## 4. Craft with numbers

- Entrances move two or three properties together (opacity, 10 to 40 px of travel, scale from 0.94); never opacity alone and never from scale 0.
- Exits are performed by elements, not by fading the whole scene, and they accelerate out faster than they came in.
- A stagger finishes as one phrase. Organic lists can take one frame of seeded jitter.
- Camera: two nested transforms, the outer one dollies (scale) and the inner one turns (perspective around 2200 to 2800 px). Put the transform origin on the point of interest so cursor coordinates survive a push. Pair a zoom with a slight rotation or lateral drift instead of a pure scale, end in a tiny residual drift, and give every camera move a visible cause 10 to 14 frames before it starts.
- Cursor as a prop: larger than life (about 44x54 px on a 1920 frame), white with a dark stroke and a shadow, a curved path (different easing on x and y), a click that presses for about two frames with a ripple while the control itself depresses, and gone before the final hold.
- Texture: grain at roughly 0.05 to 0.12 opacity reseeded every two frames (every frame bloats the file), a vignette, a slow drift. A clean flat finish is a valid choice when made on purpose.
- Motion blur only on fast moves (beyond about 30 px per frame): average 4 to 8 subframes across a 180 degree shutter, never across a hard cut, never on text meant to be read.
- Type: masked reveals (words rise about 105 to 110 percent inside a padded mask); no per-letter twinkle as the main reveal; nothing moves while it is being read.
- Numbers change with a masked swap to the next sourced value, never by counting through figures that are not in `facts.md` (the truth gate in `phases/brief.md`).

## 5. Drafts

Render a half-resolution draft after each meaningful change, log it in
`production.md` with what to judge, and keep every version.

## 6. Parallel scene builds

Only after the storyboard is approved. One scene file per subagent; the main
session owns the tokens, the timeline, transitions and sound. Each subagent gets
`production.md`, its beat rows and the motion-language spec, and returns a draft
of its scene.

## 7. Engine notes

- **Remotion**: `useCurrentFrame()` and `useVideoConfig()` for fps and size; `interpolate` clamped on both sides with an explicit easing; `spring()` for physical hits; `Sequence`, `Series` and `TransitionSeries` for structure (transitions overlap scenes, so total length shrinks); `premountFor={fps}` on timed elements; `@remotion/media` for audio and video; assets through `staticFile()`; one `<Composition>` per format in `src/Root.tsx`. CSS animations and Tailwind `animate-*` do not render deterministically.
- **HyperFrames**: one paused GSAP timeline per composition, registered on `window.__timelines` under its `data-composition-id`; clips carry `data-start` and duration attributes; tween the children of a clip, not the clip; repeat `fromTo` start values on the end side or parallel workers lose them; keep CSS (and `font-family`) in an inline `<style>` so fonts get embedded; give every `<audio>` an `id` or it renders silent; run every CLI command through `bash <this skill>/scripts/hf.sh`, and `hf.sh lint` and `hf.sh check` must reach zero findings.
- **HTML capture**: the page exposes `window.seek(t)`, freezes when loaded with `?render`, sets `window.__ready = true` after fonts load, and the capture waits two animation frames after each seek before the screenshot.
- **Canvas (animate kit)**: scenes are functions of time drawn by the kit; build and export with its tools from the project folder.

## Library reads for this phase

| Need | Read |
|---|---|
| Remotion engine: creating, markup rules (timing, sequencing, transitions, audio, fonts, effects), Studio, rendering, captions, media | `remotion/remotion-create`, `remotion/remotion-markup`, `remotion/remotion-studio`, `remotion/remotion-render`, `remotion/remotion-captions`, `remotion/remotion-multimedia`, `remotion/remotion-interactivity`, `remotion/remotion-docs` |
| Element craft, kinetic type, finishes, a motion linter for Remotion | `klik-anim/klik-anim` |
| Camera craft and the camera dial | `klik-anim/klik-cam` |
| Remotion craft components, verify loop | `remotion-mg/remotion-motion-graphics`, `claude-motion/motion-design` |
| HyperFrames engine and workflows | `hyperframes/hyperframes-core`, `hyperframes/hyperframes-animation`, `hyperframes/hyperframes-keyframes`, `hyperframes/hyperframes-creative`, `hyperframes/hyperframes-registry`, `hyperframes/hyperframes-cli` |
| HyperFrames failures that pass every preview | `hf-reel/hyperframes-motion-reel` |
| GSAP timelines, plugins, utilities | `gsap/gsap-timeline`, `gsap/gsap-core`, `gsap/gsap-plugins`, `gsap/gsap-utils` |
| Launch-film camera rig, cursor, grade, determinism for seek renderers | `launch-film/product-launch-motion` |
| Seek contract, effect recipes | `launch-kit/motion-effects` |
| Simulations and 3D captured frame by frame | `claude-motion/web-sims`, `launch-kit/title-sequence-3d` |
| Morphing-shape B-roll engine with subframe blur | `broll/motion-broll` |
| Stylized canvas pieces | `animate/animate` |
| Lottie inside Remotion, Lottie on the web | `remotion/remotion-markup` (Lottie rules), `dotlottie/dotlottie-web` |
