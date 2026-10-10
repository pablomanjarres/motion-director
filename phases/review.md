# Phase 7: Review

The builder does not grade its own film. Output: `production.md` section 7 with
measurements, critic scores and what changed.

## 1. Render for review

- A half-resolution draft first (for example 960x540 with a fast preset). Judge rhythm, not sharpness.
- A contact sheet with one frame per beat, taken about 0.3 s after each beat so motion has settled.
- A strip of every frame across each transition.
- A phone sheet scaled to 360 px wide.
- Frame 0 on its own: it is the thumbnail.

```bash
# one frame per beat (times come from the timeline file), then tile them
ffmpeg -v error -ss 3.3 -i draft.mp4 -frames:v 1 -vf scale=640:-1 beat-02.png
ffmpeg -v error -pattern_type glob -i 'beat-*.png' -vf tile=4x2 contact.png
# every frame across a transition (frames 90 to 120)
ffmpeg -v error -i draft.mp4 -vf "select='between(n,90,120)',scale=320:-1,tile=8x4" -frames:v 1 strip-02.png
# phone-width sheet, two frames per second
ffmpeg -v error -i draft.mp4 -vf "fps=2,scale=360:-1,tile=6x5" -frames:v 1 phone.png
```

Open and look at every image. Never claim a fix you have not re-rendered and looked at.

## 2. Measure

- `python3 <this skill>/scripts/frame_qa.py draft.mp4` reports pops, one-frame flashes, frozen stretches and black frames; `--against` compares two renders frame by frame (run the same frames twice to prove determinism).
- Text: every string sits inside the frame and outside platform UI zones, nothing overlaps, and it is legible on the phone sheet.
- Loops: the last frame and frame 0 match in position and in velocity.
- Sound: loudness and true peak measured on the delivered file, and a loudness envelope around each cue (`phases/sound.md`).
- File gate:

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt,color_space,color_transfer,color_primaries -show_entries format=duration -of compact final.mp4
```

Expect h264, the planned size and fps, the exact duration, `yuv420p`, `bt709` tags, and one audio stream.

- Remotion code: `node <library>/klik-anim/klik-anim/scripts/lint-motion.mjs src` flags random numbers, clocks, timers, linear easing and unclamped interpolation.
- HyperFrames: `bash <this skill>/scripts/hf.sh lint` then `hf.sh check` must report zero findings.

## 3. A fresh critic

Spawn a separate subagent as the critic. Give it the brief section, `facts.md`,
the brand files when they exist (`brand.md`, `MOTION.md` or the brand guide), the
motion-language spec, the contact sheet, the strips, the phone sheet and this
rubric. Without the brand files it judges brand fit blind. Do not give it the code or the builder's reasoning. Its stance is reject
until earned.

It scores each item from 1 to 10:

| Item | Passes when |
|---|---|
| Hook | the first 2 s make a stranger keep watching |
| Readability | every line reads on the phone sheet within its hold |
| Motion quality | easing matches the spec, arcs are clean, exits are faster than entrances, nothing pops |
| Variety | something new every 2 to 4 s, no dead stretch |
| Composition | one focal point per frame, safe areas respected |
| Truth and brand | only numbers from `facts.md`, sample labels present, brand colors and type correct |
| Sound sync | hits land on their events (when there is audio) |
| Finish | no banding, clipping or stray frames; texture is deliberate |

It also returns the three worst problems with timestamps, and one sentence saying
what the film is about, written from the frames alone. Pass means every score is
at least 8 and that sentence matches the brief's sentence.

Fix only items scored 7 or lower and leave anything at 9 or above alone.

## 4. Bound the loop

At most two critic rounds. Round two checks the fixes and looks for regressions.
If round two still fails, stop and report the open problems with timestamps to the
person instead of starting a third round.

## 5. Notes from a person

Treat a note as a symptom. Ask at which second, grab that frame, translate the
symptom into a mechanism ("make it feel more premium" might mean longer holds,
less travel, no overshoot), change one thing per note, keep everything else
identical, and report the change in the person's own words. Never overwrite a
render: version them (`v1`, `v2`, ...).

## Library reads for this phase

| Need | Read |
|---|---|
| Beat contact sheets, the review checklist | `claude-motion/review-loop` |
| Measured review: cut grid, text tracing, determinism, dead beats | `animate/animate` (`tools/review.mjs`, `textcheck.mjs`, `tile.mjs`, `framehash.mjs`) |
| QA, director's notes, three-pass self-review, the trap index | `launch-film/product-launch-motion` |
| Fresh-context QA, the distraction test, motion lint | `klik-anim/klik-remotion-method`, `klik-anim/klik-anim` |
| Transition-strip defect signatures, validators with controls | `hf-kit/video-storytelling`, `hf-kit/short-form-edit` |
| Remotion stills and the verify loop | `remotion-mg/remotion-motion-graphics` |
| HyperFrames lint, check and snapshot | `hyperframes/hyperframes-cli` |
