# Launch films, measured

What 14 launch films from OpenAI and Anthropic (September 2025 to October 2026) actually
do: cuts checked frame by frame, type measured on full-resolution frames, motion counted
in frames, loudness by EBU R128. Use it for product launches, model launches, social cuts
and brand spots. The numbers describe the films, not quotas: name the two or three films
closest to the piece, then match their numbers on the reference board
(`scripts/reference_study.py`). Sizes are cap height as a percentage of frame height.

## The set

| Film | Kind | Length | Shots | First line on screen | End hold | Loudness, range |
|---|---|---|---|---|---|---|
| Claude Opus 5.5 (2026-09) | model launch | 20.1 s | 38 | 8.7 s (43%) | 4.1 s | -16.4 LUFS, 10.4 LU |
| Claude Fable 5 (2026-06, square) | model launch | 20.5 s | 65 | 16.3 s (79%) | 4.3 s | -11.6, 18.2 |
| Claude Haiku 5.5 (2026-10) | social cut | 11.1 s | 1 | 4.8 s (43%) | name 3.1 s | silent |
| GPT-6 Astra, "new star" (2026-09) | social cut | 15.3 s | 1 | none | loops | -23.4, 4.2 |
| GPT-6 Astra (2026-09) | model launch | 163 s | 57 | year cards from 0 s | 8.7 s | -15.2, 7.6 |
| Sora 2 (2025-09) | model launch | 57.4 s | 14 | title card at 0 s | 4.6 s | -16.1, 6.4 |
| Claude Fable 5 safeguards (2026-06) | interview explainer | 113 s | 55 | lower thirds | 4.2 s | -13.6, 2.3 |
| Claude Dashboards and Motion (2026-10) | product launch | 81.6 s | one canvas | 10.3 s (13%) | 4.6 s | -15.9, 3.7 |
| ChatGPT Atlas (2025-10) | product launch | 97.8 s | 32 | typed title at 3.5 s | 11.3 s | -15.4, 11.3 |
| GPT-6 Intelligent UI (2026-10) | product launch | 70.2 s | 40 | 58.2 s (83%) | 4.5 s | -15.2, 5.6 |
| dots (2026-09) | product launch | 148 s | 72 | title lockup at 0 s | 6.8 s | -16.4, 6.9 |
| Keep thinking (2025-09) | brand spot | 90 s | 98 | 70.9 s (79%) | 4.4 s | -14.1, 4.2 |
| Ads are coming to AI (2026-02) | brand spot | 60.1 s | 11 | 48.6 s (81%) | 3.0 s | -15.4, 7.3 |
| You can just build things (2026-02) | brand spot | 60.1 s | 30 | 51.8 s (86%) | 3.5 s of brand | -14.6, 10.1 |

"First line" is the first message or brand line; a title card, year or genre word that opens
a film is listed as such.

## What they all do

1. **One idea, shown before it is said.** Opus 5.5 runs 8.7 s of horizons in every material before its first word. Keep thinking presses the word "problems" into 13 different surfaces in 20 s before any line. Intelligent UI shows people buried in printed instructions for 52% of its runtime. The line, when it comes, names what the picture already proved.
2. **The product is the answer, not the subject.** Brand spots show legible product UI for 0-6% of the runtime; people or hands carry 61-95%. Intelligent UI shows no product UI until 55%. dots puts its interface only on physical screens inside a set. Atlas and Dashboards are interface-only, and even they give each section one task and one idea.
3. **Very few words.** Short films use at most four words before the name, often none ("There's more to discover", then "Opus 5.5"). Cards hold 1-8 words, usually 1-4. A word appears whole on a cut or switches on at 1-2 frames a character with the first word already there; nothing fades up, flies in or twinkles letter by letter.
4. **One signature device, repeated until it pays off.** A curved horizon held at the same height across 37 materials (Opus 5.5); one numeral built from 41 collections at 3 frames each (Fable 5); a fixed word "Keep" beside a chip whose verb swaps every second cut (Keep thinking); chapter titles typed like prompts (Atlas); the film turning out to be a file inside the product (Dashboards); stand-in objects swapped for letters (GPT-6 Astra). Each is built from the product's own world.
5. **Hard cuts.** None of the 137 cuts in the brand spots is a dissolve. Cuts sit on a graphic match, on action, inside a continuing move, or behind a wipe made by the world (a butterfly crossing the lens, a head crossing frame).
6. **The edit accelerates into the reveal, then stops.** Opus 5.5 shortens its shots 1.1, 0.5, 0.39, 0.36, 0.27 s; Fable 5 ramps 36 frames down to 3; GPT-6 Astra climbs 17.5, 37, 61 shots a minute. Then one still shot carries the end for 3-9 s.
7. **The sound shapes the argument.** A near-silence (0.4-3.9 s, 20-30 dB down) sits right before the payoff, or the music is pulled out under the name (Opus 5.5: 28 dB in 0.84 s). The loudest moment lands on the reveal, and the end card plays in near-silence. Integrated loudness -16.4 to -11.6 LUFS (median -15.4; one social cut sits at -23.4), loudness range 2.3-18.2 LU (median 6.9).
8. **The end holds and only the sound leaves.** No product film or brand spot fades its picture out. The final card or shot holds 3-11 s (median 4.4 s) while the sound falls 20-50 LU over the last 1.5-6 s.

## Scale, density and life

- **The subject is big.** A held figure fills 77-87% of the frame height (Fable 5's numeral, GPT-6 Astra's particle 6); plates and live action fill the whole frame; Haiku 5.5's three windows each take a third of the height and its line crosses 93% of the width; Atlas's window spans 78% of the width. No film leaves a small object alone on an empty ground.
- **The frame keeps changing.** Montages bring a new image every 3-15 frames (Fable 5, Opus 5.5); Haiku 5.5 swaps all three windows every 0.5 s; a one-shot film keeps its whole field moving (GPT-6 Astra's particles gather, wind, hold turning and disperse).
- **Moving by 0.75 s at the latest.** A 13% push-in from frame 0 (Opus 5.5), a snap-back on threes (Fable 5), windows swapping from the first frame (Haiku 5.5), particles gathering from 0.75 s (GPT-6 Astra social cut).
- **Repeat the device, change the material.** The device holds its shape and place while its material changes every time: 37 materials under one horizon (Opus 5.5), 41 collections in one numeral (Fable 5), 12 crops on one arc (Haiku 5.5), the word "problems" on 13 surfaces (Keep thinking). The same move repeated in the same framing reads as a loop, not a device.
- **Figures are rare.** Outside product names and dates, only the Dashboards film steps one small count up; the others show data as dots, relative bars or interface texture.
- **The short films' end cards stay alive.** The mark holds still while something keeps moving: butterflies crossing the title (Fable 5), a line that boils and then retracts (Haiku 5.5), a final move that carries the wordmark away and lands on frame 0 (Opus 5.5). None of them freezes the whole frame for longer than about 2.3 s.

## Type

| Role | Cap height | Seen in |
|---|---|---|
| One display word, at most one per film | 14-26% (53% for a one-word genre slam) | Fable 5 title 14.4%, GPT-6 Astra years 22%, "YOU CAN JUST BUILD THINGS" 26.2%, "BETRAYAL" 53% |
| Statements and supers | 3.9-6.5% | Atlas cards 6.5%, Intelligent UI 6.0-6.1%, Keep thinking 5.7-5.9%, Dashboards 4.8-5.5%, Sora 2 title 4%, Ads super 3.9% |
| End wordmark or name | 6.4-9.1% (8.8-15% in short social cuts) | brand spots 8.6-9.1%, Opus 5.5 6.4%, Haiku 5.5 8.8% |
| Taglines, lower thirds | 3.1-4.6% | Keep thinking tagline 3.3%, safeguards lower thirds 3.1 and 4.6% |
| Product UI read as texture | 0.65-1.6% | whole windows and phones |
| Product UI meant to be read | 2.1-3.4% | Atlas macro 2.2%, Dashboards 2.6-2.8%, Atlas lifted message 3.3-3.4% |

- One family per film, one or two weights. Supers are centred or locked to one position; a fixed word never moves while the rest of the line changes.
- A card holds 1.3-3.5 s. Each cut can carry a new background under the same word (Opus 5.5 holds one word across 5-13 plates).
- Type is laid into the picture: graded to the plate, arched to a horizon, set on a drawn line (Haiku 5.5), never on a scrim.

## Product interface

- **Scale ladder.** A whole window or phone is texture (body text 0.65-1.6%). Before a line must be read, cut or push to a macro so that line reads at 2.1-3.4%, or lift the one message out onto plain ground. Statements at 4.8-6.5%. The closing mark is the largest object in the film.
- **Framing.** A window on a soft two-colour gradient over white (Atlas); one canvas the camera travels across (Dashboards); flat white cards composited into locked-off live action, tracking the action (Intelligent UI); real screens inside lit sets (dots); the product's output shown inside the world rather than its chrome (Keep thinking).
- **Time budget, not typing speed.** A typed request takes 0.9-1.6 s whatever its length (17-160 characters a second). An answer lands whole, resolves in about 0.5 s, or streams fast enough to finish within 1.9 s. Nothing streams at reading speed.
- **Entrances.** Elements land in 7-13 frames with half the travel in the first 15-33%. Intelligent UI's card grows from the top to 98% in 8 frames (29, 59, 74, 84, 90, 94, 97, 99%). Messages rise 20-32 px while fading in over 4-5 frames. No overshoot, except in the Dashboards film: reply cards overshoot 4-15 px, a comment pin grows to 103%, and the logo slides 9 px past its rest, each settling within about 4-7 frames.
- **Moves.** Camera and scroll moves are S-curves of 0.4-1.7 s, with the velocity peak at about 40%. A state change accelerates for about 5 frames, swaps on one frame and settles over 19-25. A cut inside a move continues the same direction and settles in 0.4-0.8 s.
- **Directing attention.** Fade everything but the subject over about 10 frames, magnify, or cut from the screen to the face watching it (inserts 1.5-2.1 s, faces about 1.3 s).
- **Cursor.** Visible and clicking in interface-only films; an agent gets its own labelled cursor; live-action films show none.
- **Finish.** None of the four interface films carries measurable grain.

## Edit and motion

- **Cut rate by kind.** Short launch montages run 111-188 cuts a minute (median shot 0.13-0.32 s); product films 19-33; brand spots 10-65; one-canvas and one-shot films none.
- **Pace by section.** The problem goes fast (Keep thinking 108 cuts a minute; Intelligent UI 1.35 s shots), the answer slower (2.4 s, then 3.0 s; Keep thinking halves its cut rate), the payoff fast again (90 a minute), and one still shot ends it.
- **A hinge between problem and answer.** 2-2.5 s of an almost empty frame with the sound near silent (Keep thinking), a foreground object closing the frame to black for 2-3 frames (Intelligent UI), or 3 black frames and a 1.75 s fade up at the midpoint (dots).
- **Camera.** Spend the one move on the opening (Opus 5.5: a 13% push-in over 1.24 s). A pull-back that speeds up per frame as shots shorten makes many cuts read as one move (Fable 5: 3.5-10% a shot). In interface films the camera is the transition: Dashboards has about 10 hard switches in 82 s, and every other change is a camera move.
- **Steps for a handmade feel.** Fable 5 animates on twos inside 24 fps, Haiku 5.5 runs at 12 fps with a line that boils on twos, and the safeguards film moves its paper graphics in 2-6 frame holds. Interface moves stay on ones.
- **Timing templates repeat to the frame.** Sora 2 runs five blocks of exactly 239 frames; lower thirds pop on a 3, 8, 3, 3 frame pattern; GPT-6 Astra's year cards take 18 frames in and 17 out.
- **Numbers.** Data appears as dots, relative bars or a figure built from the subject (the safeguards film collapses a field to 0 against 1 dot). The set's only count-up steps four times on twos with shrinking increments (+2, +3, +2, +1).
- **Letters from stand-ins.** A wordmark assembled from the film's own objects, one letter swapped per frame, out of reading order (GPT-6 Astra, the safeguards film).
- **Loops for feeds.** The last frame returns to frame 0 within 1-3 levels out of 255 (Opus 5.5, GPT-6 Astra social cut), or the film ends in its opening state (Haiku 5.5).

## Sound

- Most films build into the reveal: +10 LU across a montage (Fable 5), a steady climb under the line to its loudest window just before the name (Opus 5.5).
- The turn gets one sound event: 0.4 s of near-silence (Keep thinking), a 23 dB step on a single frame (You can just build things), the music entering with the first super (Ads), an 11 LU drop before the key demo (Atlas).
- Before or under the reveal: a 25 LU drop while the cuts slow (Fable 5), 3.9 s of near-silence (Ads), or the music pulled out under the name (Opus 5.5).
- Hits sit on cuts: one 2 frames before a word lands, the wordmark with its own hit on the frame it appears, cuts 2-3 frames ahead of musical onsets.
- The end: the sound falls 20-50 LU over the last 1.5-6 s; Keep thinking holds 1.85 s of silence on its lockup; dots fades only its audio over the last 1.5 s.
- No score at all is a valid choice: Sora 2 lets each clip carry its own sound between silent black cards.

## End cards

- **Short films.** The end takes 20-30% of the runtime: the name alone for 1.3-2.3 s, then the wordmark for 0.9-1.7 s, one centred line on a plain ground each time, then the loop. Haiku 5.5 lets the name be the ending (3.1 s) and returns to its opening state.
- **Longer films.** Interface films hold the mark 1.8-4.4 s inside a 4.5-7.8 s card. Brand spots put the wordmark at 8.6-9.1% cap height and the tagline at 3.3-4.3% for the last 3.0-3.5 s.
- **Entrances.** A hard cut, or a mark built in about 0.9 s (dots: from light over 22 frames, letters 3 frames apart), or a logo growing from 53-67% to full size in 9-15 frames with a fast start.
- **Clear the stage first.** Dashboards removes its working grid in about 5 frames and warms the ground slightly before the logo builds.

## Recipes by kind

**Short launch or social cut, 10-20 s** (Opus 5.5, Fable 5, Haiku 5.5, GPT-6 Astra social cut)
1. From 0 to about 45%: the motif without words. A montage locked to one shape (a horizon at one height, a numeral in one box), or one continuous build (particles forming a figure on an S-curve: 10% at about 2 s, 50% at 3.2 s, 90% at 4.9 s).
2. From about 45 to 80%: at most one line of up to four words, one word across each group of cuts, while the cuts accelerate. No words at all also works.
3. At the top of the build, cut to the name, one centred line, for 1.3-3.1 s, in near-silence or on the loudest hit.
4. Wordmark for 0.9-1.7 s, then back to frame 0 for the loop.

**Product launch, 60-150 s** (Atlas, Intelligent UI, Dashboards, dots)
1. Open on the finished output or on the human problem, not on interface chrome (Dashboards: its output full frame for 2.5 s; Intelligent UI: no interface for 52%).
2. A hinge, with the sound dipped.
3. The product as the answer in three or four chapters, one idea and one card or line each (2-8 words, about 6.5% cap height, 1.8-3.0 s).
4. Interface on the scale ladder and the time budget; inserts cut to the person watching.
5. The fastest cutting and the loudest moment at the payoff; then the line, late (79-89% of the runtime), the name, and the mark held 1.8-4.4 s while the sound leaves.

**Brand spot, 60-90 s** (Keep thinking, Ads are coming to AI, You can just build things)
1. One idea carried by people and objects; product interface at most 6% of the runtime.
2. The cut rate follows the story: a fast problem montage, a hinge, a slower answer, a fast payoff, one long final shot.
3. Words late (79-86% of the runtime), switched on whole on cuts; one sound event marks the turn.
4. Wordmark about 9% cap height and tagline 3.3-4.3% for the last 3-3.5 s; the picture outlasts the sound.

## Before calling a launch film done

- The idea reads from the frames alone, before any line appears.
- The subject fills the frame (a figure at least half the frame height, or full-frame imagery), and the picture is moving by 0.75 s.
- The device repeats with a new material each time, never as the same move in the same framing.
- Count the words: a 15 s piece carries at most one line before the name.
- Every line meant to be read sits in the bands above: statements 3.9-6.5%, readable interface at least 2.1% (magnified, never a whole window), taglines at least 3.1%.
- One signature device, built from the brand's own material, repeated at least three times, paying off at the reveal.
- Hard cuts, or a written reason for each dissolve.
- Shots shorten into the reveal, and one still shot carries the end.
- A near-silence or a pulled-out bed before or under the name; loudness range at least 4 LU; the end card plays in near-silence.
- The end holds 3 s or more, and the picture does not fade.
- No grain on interface films unless the brand asks for it.
- On the board (`reference_study.py --draft`), every measure marked `outside` has a reason.

## Do not copy

Logos, wordmarks, symbols, typefaces, brand colours, product names, taglines ("There's more to discover", "Keep thinking", "You can just build things", "Sometimes words aren't enough"), music, characters, and the specific footage or plates. Take the measurements, the structures and the logic of each device, then build the device from the piece's own brand and material.
