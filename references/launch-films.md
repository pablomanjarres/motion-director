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
| GPT-6 Intelligent UI (2026-10) | product launch | 70.2 s | 37 | 58.2 s (83%) | 4.5 s | -15.2, 5.6 |
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
- **Entrances.** Elements land in 7-13 frames with half the travel in the first 15-33%. Intelligent UI's card grows from the top to 98% in 8 frames (29, 59, 74, 84, 90, 94, 97, 99%). Messages rise 20-32 px while fading in over 4-5 frames. No overshoot, except reply cards that settle 4-15 px within 5-7 frames.
- **Moves.** Camera and scroll moves are S-curves of 0.4-1.7 s, with the velocity peak at about 40%. A state change accelerates for about 5 frames, swaps on one frame and settles over 19-25. A cut inside a move continues the same direction and settles in 0.4-0.8 s.
- **Directing attention.** Fade everything but the subject over about 10 frames, magnify, or cut from the screen to the face watching it (inserts 1.5-2.1 s, faces about 1.3 s).
- **Cursor.** Visible and clicking in interface-only films; an agent gets its own labelled cursor; live-action films show none.
- **Finish.** None of the four interface films carries measurable grain.
