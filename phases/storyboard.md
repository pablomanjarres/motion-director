# Phase 4: Storyboard

Turn the direction into a timed plan that picture, sound and review all read, in
the project the toolchain phase scaffolded. Output: the beat table in
`production.md` section 4, a timeline file, look frames, and one still per beat.

## 1. Choose the structure

Structure comes before shots. Name the one that fits and write it down.

| Structure | Use for | Transition habit |
|---|---|---|
| Problem, turn, resolution | product demo, feature film | one object carries the change (cards merge, a cursor acts) |
| Motif montage | short launch films, social cuts | one shape held at one position across every cut (a graphic match), cuts accelerating into the name |
| Chronology | histories, timelines | transitions grow out of the scene (morphs, draw-offs), few cuts |
| Journey or path | maps, flows, architecture | a follow camera that never cuts |
| List or catalogue | features, examples | cut on the beat |
| Process | how it works | one shape transformed step by step |
| Showreel | brand or studio reel | one motif through labeled chapters on a BPM grid |
| Loop | covers, feeds, ambient | start, change, hold, return |

## 2. Beat table

Fill the table in `production.md`: time in seconds and frames at the project fps,
what happens, motion and camera, on-screen text with its hold, the sound's job,
and the bridge to the next beat. Every bridge is a reason a viewer can see: a
moving object, a match on position or shape, cause and effect. No generic wipes.

Before animating anything, read the table and say what the viewer learns. If you
cannot, fix the story; motion will not.

## 3. Pacing rules

- Frame 0 is already a finished image: feeds autoplay muted and show it as the thumbnail.
- The hook lands inside 1.5 to 3 s.
- Something new every 2 to 4 s; nothing sits fully static for longer than 3 s except the final hold.
- Hit, hold, build, hit. Keep at least three moments of relative stillness per 30 s; contrast reads as expensive.
- Shots shorten toward the climax. A drop to near silence comes right before the payoff, and the payoff is the single loudest moment.
- The end echoes the opening, changed.
- Text never moves while it has to be read. Holds follow the reading rule from the brief.
- Montage-led pieces follow the board's still share, not klik-anim's 40-60% rest ratio: the measured montages hold still for 0% (Fable 5, Opus 5.5) to 35% (Haiku 5.5) of their runtime while the device itself stays in place.
- Words come late. In the measured launch films the message line lands at 43 to 89 percent of the runtime, after the picture has made the point; a title card or a genre word may open a film, a slogan does not.
- The end takes 20 to 30 percent of a short piece and holds at least 3 s. The picture never fades out; the sound leaves instead.

Starting templates (adjust to the clock). Launch templates come from `references/launch-films.md`:

| Piece | Beats |
|---|---|
| 10-20 s launch or social cut | the motif without words to about 45%; at most one line of up to four words across the accelerating cuts to about 80%; the name alone in near-silence for 1.3-3.1 s; the wordmark 0.9-1.7 s; back to frame 0 so it loops |
| 15 s feature demo | 0-3 s the outcome or the problem as an image; 3-10 s the product doing one thing at a readable scale, at most one line; 10-12 s the result lands; 12-15 s the name or mark held while the sound falls away |
| 30-45 s launch film | the problem as images for the first third, no interface; a hinge with the sound dipped; the product as the answer in two or three chapters with one card each; the payoff with the fastest cuts and the loudest moment; the line at about 80%; the end held 3-5 s |
| 30 s reel | hook 0-1.5 s, context to 3 s, body to 22 s in three or four beats, payoff to 27 s, call to action to 30 s |
| 3-5 s logo sting | mark, wordmark, tagline, a breath, a short exit |
| 8 s loop | the move in 0-2.2 s, a living hold to 6.6 s, the return by 8.0 s; frame at 0 equals frame at 8 |

## 4. One timeline file

Write the beats into one file (`timeline.json` or `src/timeline.ts`) as named
times. Scenes, the sound cue sheet and or the review script all read it; no component
or cue hardcodes a start time. Write times as integer frames at the project fps (or exact
frame / fps values) and compare in frames: seconds rounded to a few decimals put landings a
frame late. Retiming means editing that file, then re-rendering
picture and sound.

- With voice-over: keep the word timings file next to it and anchor beats to words. Cue to the meaning word (the verb, not the noun); lead a reveal that must be read by 0.02 to 0.06 s; land hits exactly on the word.
- With a song: keep the beat analysis next to it and snap cuts to the grid (2, 4 or 8 beat phrases, not every beat).

## 5. Look frames, panels and check-ins

First render two to four full-size look frames of the most different beats, from
the scaffolded project. This is the still-frame gate: a weak still will not be
rescued by motion, so fix the look here. Put each look frame beside two reference
contact sheets at the same size: a frame emptier, smaller or wordier than every
reference frame (scale, density and words in `references/launch-films.md`) fails
here. Build the gate sheet in one command, and send any look a critic round changes
back through it:

```bash
ffmpeg -i look-01.png -i <studies>/<film-a>/sheet-01.png -i <studies>/<film-b>/sheet-01.png -filter_complex \
  "[0]scale=1920:-2[a];[1]scale=1920:-2[b];[2]scale=1920:-2[c];[a][b][c]vstack=inputs=3" gate-01.png
```
 Then render one still per beat from the
real scene code, so panels become the build instead of throwaway drawings. Three
cheap check-ins happen before full animation: the story (beat table), the look
(look frames) and the storyboard (panels). When the person is present, ask at each one with options and a
recommended default. When they are away, decide, record the decision and the
alternatives in `production.md`, and continue.

## 6. Plan every format now

For each beat, write how it re-lays out in 9:16 (stack instead of side by side,
larger type, payload in the central band, platform safe zones). Formats designed
late come out as crops.

## Library reads for this phase

| Need | Read |
|---|---|
| Story formats, beat types and pace, link types, check-ins | `animate/animate` (`grammar/`) |
| Timeline-first beats, reading holds, frame-0 rules | `claude-motion/motion-design` |
| Word-locked cueing to a voice-over | `launch-film/product-launch-motion` |
| Reading-time arithmetic, energy arc, holds with idle life | `klik-anim/klik-anim` |
| Discovery questions, HTML storyboard with transition cards | `klik-anim/klik-remotion-method` |
| Launch, explainer, promo and Apple-style beat templates | `launch-kit/launch-video`, `launch-kit/vox-explainer`, `launch-kit/newsletter-promo`, `launch-kit/apple-launch-film` |
| Loops and looping covers | `launch-kit/motion-effects`, `launch-kit/loop-cover` |
| Showreels on a BPM grid | `hf-kit/motion-showreel`, `hf-reel/hyperframes-motion-reel` |
| Long-form camera storytelling, open loops | `hf-kit/video-storytelling` |
| Beat arithmetic, J, L and match cuts, speed ramps | `iart/beat-sync-editing` |
| B-roll plans over talking-head footage | `broll/motion-broll`, `hf-kit/hyperframes-video-beats`, `hf-kit/short-form-edit` |
