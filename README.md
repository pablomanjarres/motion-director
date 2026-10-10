# motion-director

A motion design director for coding agents. One skill runs every motion job
(product films, launch videos, explainers, reels, logo stings, Lottie files,
website animation) through an eight-phase production pipeline, and draws on a
library of about a hundred specialist skills from eighteen open repositories,
each pinned to an audited commit.

## Why

Asked for "a motion video", an agent tends to ship the first idea that renders,
with invented numbers on screen, no sound design and no real review. This skill
makes the work directed and measured: three directions with two killed, a facts
file behind everything shown on screen, one timeline that drives picture and
sound, a separate critic that only sees frames, and measurements taken on the
delivered files.

## What is in here

| Path | Role |
|---|---|
| `SKILL.md` | entry point: the pipeline, its gates and the rules |
| `phases/` | brief, direction, toolchain, storyboard, build, sound, review, deliver, and a web track |
| `templates/production.md` | the per-project production bible a later session can resume from |
| `library.json` | the audited sources: pinned commits, skill paths and phases, notes, and install-time edits |
| `scripts/motion_library.py` | installs, verifies and indexes the library, finds skills, lists upstream drift, scaffolds template projects |
| `scripts/frame_qa.py` | finds pops, one-frame flashes, frozen stretches and black frames in a render; compares two renders frame by frame |
| `scripts/hf.sh` | runs the HyperFrames CLI pinned, with telemetry, update checks and global skill installs off |

The library itself is not in this repository. `install` fetches each source from
its own repository at the commit listed in `library.json`, so authorship and
licenses stay with the original projects.

## Install

Requirements: git, Python 3.9 or newer, Node 20 or newer, ffmpeg, and a Chromium
browser for frame capture.

```bash
git clone https://github.com/pablomanjarres/motion-director ~/.claude/skills/motion
python3 ~/.claude/skills/motion/scripts/motion_library.py install
```

The library lands in `~/.local/share/motion-studio` (override with
`MOTION_STUDIO_HOME`), with a generated `INDEX.md` listing every skill, its
phases, grade and notes. Agents that read `SKILL.md` skills from another folder
work the same way; the HyperFrames notes assume the scripts live at
`~/.claude/skills/motion/scripts/`, so adjust that path if you install elsewhere.

## Use

Ask for any motion piece, or start with `/motion` and the brief. The skill
verifies the library, opens or resumes `production.md` in the project folder, and
works the phases in order, logging which library skills shaped each decision.

## Safety model

- Every source is pinned to a full commit SHA with an audit date, a verdict and a grade.
- Install-time edits remove text that would install software, edit agent configuration, read credentials, steer engine choice or add vendor promotion. Each edit must match exactly once, so an upstream change fails the install and forces a re-audit instead of slipping through.
- Symlinks that resolve outside a source checkout are refused.
- One audited repository is excluded, with the reason recorded in `library.json`.
- `hf.sh` refuses HyperFrames subcommands that read agent login tokens (`usage`), install or update skills, bump versions, send feedback or upload projects.
- `motion_library.py outdated` lists sources whose upstream moved past the pin.

## Updating a pin

Run `outdated`, read the upstream diff, then update the commit, skill paths and
edits for that source in `library.json` and run `install`. A stale edit stops the
install with the file and the text it expected.

## Tests

```bash
cd scripts && python3 -m unittest test_motion_library test_frame_qa test_hf_wrapper
```

The frame checker tests need ffmpeg; the installer tests use a local git repository
as the upstream and run offline.

## Sources

| Library id | Repository | License | Grade |
|---|---|---|---|
| claude-motion | whaleyxbt/claude-motion | MIT | A |
| launch-film | AbubakrChan/product-launch-motion | MIT | A |
| animate | cth9191/animate | MIT | A |
| klik-anim | t3knobox/klik-anim-skill-creation | none (local reference only) | A |
| launch-kit | charlie947/motion-graphics-skills | MIT | B |
| iart | iart-ai/motion-design-skills | MIT | B |
| hf-kit | nateherkai/hyperframes-student-kit | MIT, with brand assets excluded from reuse | A |
| hyperframes | heygen-com/hyperframes | Apache-2.0 | A |
| hf-reel | Sunwood-ai-labs/hyperframes-motion-reel-skill | MIT | B+ |
| remotion | remotion-dev/skills | Remotion License | A |
| remotion-mg | haidrrrry/claude-remotion-skill | MIT | B+ |
| gsap | greensock/gsap-skills | MIT | A |
| motion | motiondivision/ai-kit | MIT (package metadata) | A |
| motion-dev | 199-biotechnologies/motion-dev-animations-skill | MIT | C |
| dotlottie | LottieFiles/dotlottie-web | MIT | B+ |
| motion-principles | LottieFiles/motion-design-skill | MIT | B |
| broll | Barty-Bart/motion-graphics | MIT | A |
| awesome-motion | frankxai/awesome-motion-design-agent-skills | CC0-1.0 | C |

Excluded after review: howseen-ai/claude-motion-design (reason in `library.json`).
The engines the phases use (Remotion, HyperFrames, GSAP, Motion, lottie-web and
dotLottie) are installed per project under their own licenses; Remotion needs a
company license for companies larger than three people.

## License

MIT for the files in this repository. Library sources keep their own licenses,
which `library.json` and the generated index record for each one.
