# Phase 6: Sound

Sound is designed from the same timeline as the picture and measured, not guessed.
Output: the cue table in `production.md` section 6, a mastered mix, and loudness
measured on the delivered file.

## 1. Sources

- **Synthesized effects (default, license-clean)**: clicks, ticks, blips, pops with a falling pitch, whooshes from filtered noise as long as the move, a riser that ends on the hit, an impact (low sine plus a noise transient so phone speakers hear it), pads for a bed. `claude-motion` ships a stdlib Python engine with generators, placement, mastering and loudness measurement; it runs inside projects scaffolded from that template.
- **Music**: a licensed track (record the license in `production.md`), or generated music when the person accepts it and its terms cover the use (registered skill `sogni-creative-agent-skill`). No track ships without a license record.
- **Voice**: a real take or text-to-speech; a scratch voice first. Word timings come from a transcriber (faster-whisper locally). Paid voices only with the person's own key and a stated cost before the full run.

## 2. Which events get a sound

Accent changes of state, do not narrate motion: a click on selection, a blip when
an element lands, a whoosh on the merge, a settle tone when the result rests.
Continuous drifts stay silent. One riser and one impact per piece; the riser leads
into the payoff as described under dramaturgy.

## 3. Timing

- A sound that starts 1 to 3 frames before its visual reads as in sync; late reads as broken.
- Place stock effects by their measured peak, not by the start of the file; trim to the first transient.
- Hits land on downbeats when a grid or song drives the piece.

## 4. Levels and space

| Layer | Gain (linear) | Note |
|---|---|---|
| hero hits | 0.25-0.35 | at most one per moment |
| support effects | 0.08-0.20 | |
| bed or pad | about 0.03 | ducked about 9 dB under hero moments and under voice |
| music under voice | 14-20 dB below the voice | |

Pan follows the element's position on screen. Keep one musical key and let pitch
rise toward the payoff.

## 5. Dramaturgy

Build, cut, pay off: the riser builds and then cuts into a short near silence (0.3
to 1 s, or 15 to 35 dB down for up to 4 s in longer pieces), and the payoff hit
breaks that silence as the loudest moment. Pieces under 10 s may skip the silence
and land the riser straight on its hit. The busiest stretch is not the loudest.
Sub-bass only on the thesis and the call to action.

## 6. When a song leads

Find the tempo and the drop from band energy rather than trusting an automatic
grid, take the beat phase from the kick band, and check for double or half time.
Start the song at `drop_in_song - drop_in_film`. Splice only on grid points with
short crossfades (around 12 ms).

## 7. Mix and master

```bash
# Pass 1: measure
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
# Pass 2: apply the measured values, then limit (alimiter must not add makeup gain)
ffmpeg -i mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<I>:measured_TP=<TP>:measured_LRA=<LRA>:measured_thresh=<thresh>:offset=<offset>:linear=true,alimiter=limit=0.84:level=disabled" -ar 48000 master.wav
# Mux without re-encoding the picture
ffmpeg -i silent.mp4 -i master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest final.mp4
# Measure the delivered file, not the WAV
ffmpeg -i final.mp4 -af ebur128=peak=true -f null -
```

Targets on the delivered MP4: -14 LUFS integrated (plus or minus 0.5) and true
peak at or below -1 dBTP. Voice-led social pieces may sit near -16 LUFS. A sparse
mix cannot reach -14 without crushing; add sustained sound instead of more gain.

## 8. Prove sync and audibility

- Draw a waveform with a line at every beat (`claude-motion` has `npm run wave`; plain ffmpeg `showwavespic` works too). A hit between lines means a hardcoded time or a stale render.
- Read a 100 ms loudness envelope around each cue. A cue that does not rise above the bed is inaudible whatever its gain says.
- Watch once muted: the message must survive without sound.
- You cannot hear the mix. Report the measurements and ask the person to listen on headphones and on a phone speaker.

## Library reads for this phase

| Need | Read |
|---|---|
| Cue sheets, gain hierarchy, panning, key, mastering to -14 LUFS | `claude-motion/sound-design` |
| Sound arithmetic, leveling assets, two-pass master, cue verification scripts | `launch-film/product-launch-motion` (sound-and-master reference, `scripts/master.sh`, `scripts/verify-cue.sh`, `scripts/level-sfx.mjs`) |
| A synthesized score, silence before the payoff, voice as the clock | `animate/animate` (`craft.md`, voice tools) |
| ADSR-to-motion mapping, music maps, beat analysis | `klik-anim/klik-anim`, `klik-anim/klik-remotion-method` (`scripts/analyze-audio.py`) |
| Beat grid from the kick band, splicing, mixing | `hf-kit/motion-showreel` (`music-grid`, `splice-music`, `mix`) |
| Sound placement 2-3 frames early, a synthesized kit in Node | `remotion-mg/remotion-motion-graphics` |
| Code-generated score on the shared beat table (HyperFrames) | `hf-reel/hyperframes-motion-reel` |
| HyperFrames audio tracks and volume automation | `hyperframes/hyperframes-audio` |
| Captions timed to words | `remotion/remotion-captions` or `hf-kit/short-form-edit` |
