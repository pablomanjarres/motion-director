---
name: motion
description: "Use when making anything that moves: motion graphics, animated or explainer videos, product demos and launch films, social clips and reels, logo stings, kinetic type, showreels, B-roll over footage, Lottie files, or UI and website animation, and whenever Remotion, HyperFrames, GSAP, Motion (Framer Motion), Lottie or ffmpeg rendering is involved."
---

# Motion director

Every motion piece runs one production pipeline that draws on a pinned library of
about a hundred audited specialist skills. The result is directed, measured and
reviewed instead of being the first idea that renders.

## Start every piece here

1. **Library.** Run `python3 <this skill>/scripts/motion_library.py verify`. If it reports anything stale or missing, run the same script with `install` (about a minute; it fetches pinned commits into `~/.local/share/motion-studio`). Skim `~/.local/share/motion-studio/INDEX.md`: every skill with its phases, grade and notes.
2. **Production bible.** In the project folder (location rules in `phases/toolchain.md`), copy `templates/production.md` to `production.md`. If one exists, read it and resume from its status line.
3. **Track.** Film, web or asset, chosen in `phases/brief.md`. Then work the phases in order.

## Pipeline

| # | Phase | Read | Gate before the next phase |
|---|---|---|---|
| 1 | Brief | `phases/brief.md` | one-sentence message, the clock, formats, `facts.md` |
| 2 | Direction | `phases/direction.md` | three directions with two killed, a motion-language spec, look frames that pass the still-frame gate |
| 3 | Storyboard | `phases/storyboard.md` | beat table with visible bridges, the timeline file, panels, the lesson stated from the table alone |
| 4 | Toolchain | `phases/toolchain.md` | engine chosen with a reason, scaffolded, versions pinned |
| 5 | Build | `phases/build.md` | rough cut at final timing before polish, determinism proven |
| 6 | Sound | `phases/sound.md` | cues from the timeline, loudness measured on the delivered file |
| 7 | Review | `phases/review.md` | a fresh critic scores every item 8 or more and its one sentence matches the brief, within two rounds |
| 8 | Deliver | `phases/deliver.md` | every format re-laid out and gated, packaged with licenses |

The web track runs phases 1 and 2, then `phases/web.md`.

## Rules

- **Use the library, not memory.** Each phase file names the library skills for that phase. On the film track read at least two of them in every phase from Direction on, and write one ledger row per skill in `production.md` (skill id and the decision it drove). Find any skill with `motion_library.py where <id or name>`.
- **Never ship the first idea.** Three directions, two killed, reasons written down.
- **Truth.** No number, name, quote or claim appears on screen without a `facts.md` entry. Sample content is labeled on screen.
- **The builder never grades its own film.** The critic is a separate subagent that sees frames and the brief, not the code.
- **Measure.** `scripts/frame_qa.py` on renders, loudness on the delivered file, the ffprobe gate.
- **Memory.** Update `production.md` at the end of every phase.
- **Safety.** HyperFrames runs only through `scripts/hf.sh`. Never run installers that add skills or edit agent configuration (`npx skills add`, `npx remotion skills add`, `npx motion-ai`, `hyperframes skills update`). A source's notes in `INDEX.md` override its skill text. State the cost and ask before paid services or large model downloads.

## The person present or away

Present: check in at the story, the look and the storyboard, once each, with
options and a recommended default. Away, or "just make it": decide, record the
decision and the alternatives in `production.md`, and keep going.

## Scripts

| Script | Use |
|---|---|
| `scripts/motion_library.py install, verify, where, outdated, scaffold` | the library and project templates |
| `scripts/frame_qa.py <video> [--cuts s,s] [--against other.mp4]` | pops, flashes, frozen stretches, black frames, determinism |
| `scripts/hf.sh <command>` | the only way to run HyperFrames |

## Registered skills that join in

`create-logo` when no logo exists yet; `frontend-design`, `ui-ux-pro-max` and
`ui-glowup` for product screens inside a film and for the web track; `dataviz` for
charts; `human-writing` for voice-over scripts, on-screen copy, captions and
portfolio captions; `sogni-creative-agent-skill` for generated images, video or
music when the person accepts them; `media` for nella brand assets (swap the
palette first); `forge` for Forge templates; `stitch-design` and `remotion` when
the interface source is a Stitch project; `claude-in-chrome` for browser evidence.

## Red flags

| The thought | Do instead |
|---|---|
| "I know this engine well enough" | read its library skills and log the ledger rows |
| "The first concept is strong" | write two more and kill two |
| "A plausible number makes it look real" | a `facts.md` entry or a labeled sample |
| "The stills look fine" | spawn the critic and run `frame_qa.py` |
| "A quick bare `npx hyperframes` is fine" | `hf.sh` |
| "Install the official skills so they auto-load" | they are already in the library |
| "Ship it silent" | `phases/sound.md` |
| "Crop the 16:9 for vertical" | re-layout per `phases/deliver.md` |
