# Phase 7: Review

The builder does not grade its own film. Output: `production.md` section 7 with
measurements, critic scores and what changed.

## 1. Render for review

- A half-resolution draft first (for example 960x540 with a fast preset). Judge rhythm, not sharpness.
- Then build the review pack from the timeline's beat times and transition windows:

```bash
python3 <this skill>/scripts/review_pack.py draft.mp4 --beats 0.5,3.5,6.5 --transitions 3.0-3.6 --out review/v1-r1
```

It writes frame 0 at full size (the thumbnail), one frame per beat taken 0.3 s after
it so motion has settled, a beat contact sheet, every frame across each transition,
a 360 px phone sheet, and `index.txt` saying what each image shows.

- Then put the draft on the board beside the references chosen in Direction:

```bash
python3 <this skill>/scripts/reference_study.py <refs>/*.mp4 --draft draft.mp4 --draft-cuts <cut times from the timeline> \
  --out ~/.local/share/motion-studio/studies/<project>/v1-r1
```

`board.md` lists each measure with the references' lowest, median and highest value
and marks it `outside` where the draft leaves that range. Every `outside` gets a fix
or a written reason in `production.md`: a draft that holds its end card half as long
as its references, or has a third of their loudness range, is usually wrong. Median
motion reads low for any small subject on an empty ground; treat a low value as a
prompt to check scale and density on the sheets, not as a number to chase.

Open and look at every image. Never claim a fix you have not re-rendered and looked at.

## 2. Measure

- `python3 <this skill>/scripts/frame_qa.py draft.mp4` reports pops, one-frame flashes, frozen stretches and black frames; `--against` hashes every frame of two renders (render the same frames twice, at different concurrency, to prove determinism).
- Text: every string sits inside the frame and outside platform UI zones, nothing overlaps, and it is legible on the phone sheet.
- Loops: the last frame and frame 0 match in position and in velocity.
- Sound: loudness and true peak measured on the delivered file, and a loudness envelope around each cue (`phases/sound.md`).
- File gate:

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt,color_space,color_transfer,color_primaries -show_entries format=duration -of compact final.mp4
```

Expect h264, the planned size and fps, the exact duration, `yuv420p`, `bt709` tags, and one audio stream.

- Remotion code: `node <library>/klik-anim/klik-anim/scripts/lint-motion.mjs src` flags random numbers, clocks, timers, linear easing and unclamped interpolation. It accepts easing curves only from a module whose file name starts with `motion` (for example `src/motion.ts`), so keep the shared curves there.
- HyperFrames: `bash <this skill>/scripts/hf.sh lint` then `hf.sh check` must report zero findings.

## 3. A fresh critic

Spawn a separate subagent with `templates/critic-prompt.md` filled in as its task.
It gets the brief, `facts.md`, the brand files, the motion-language spec, the review
pack and the reference board with the references' contact sheets, never the code or
the builder's reasoning; without the brand files it judges brand fit blind, and
without the references it judges the draft against nothing. It looks and writes only, scores the rubric in that
template, and leaves `review/v<V>-r<N>-verdict.md`. Read that file instead of waiting
for a reply: a subagent's report can land with the session that started the job
rather than with you.

Pass means every score is at least 8 and the critic's sentence matches the brief's
sentence.

Fix only items scored 7 or lower. Leave items at 8 or above alone unless a fix forces a change to
them, and then check them again.

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
