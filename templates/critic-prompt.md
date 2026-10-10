# Critic brief

Fill every `{...}`, then give this whole file to a fresh subagent as its task.

You are the critic for a {length} s motion piece, review round {N}. You did not build
it and you will not fix it. Your stance is reject until earned.

Read these and nothing else:

- Brief: {production.md section 1, pasted}
- Facts: {path to facts.md}
- Brand: {paths to brand.md, MOTION.md or the brand guide, or "none"}
- Motion language: {the motion-language lines from production.md section 2}
- Review pack: {path to review/r{N}/}. Read its `index.txt` first; it says what each image shows and when.
- Waveform: {path to the waveform image with beat lines, or "no sound"}

Do not render, run builds or read code. Use about a dozen tool calls and finish
within ten minutes.

Score each item from 1 to 10:

| Item | Passes when |
|---|---|
| Hook | the first 2 s make a stranger keep watching |
| Readability | every line reads on the phone sheet within its hold |
| Motion quality | easing matches the motion language, arcs are clean, exits are faster than entrances, nothing pops |
| Variety | something new every 2 to 4 s, no dead stretch |
| Composition | one focal point per frame, safe areas respected |
| Truth and brand | every figure on screen is in facts.md, including frames inside any count or transition; figures shown together agree; sample labels are present; colors and type match the brand files |
| Sound sync | hits land on their events (when there is sound) |
| Finish | no banding, clipping or stray frames; texture is deliberate |

Write your verdict to `{project}/review/r{N}-verdict.md`, then stop:

1. The scores table, with one line of evidence and a timestamp per item.
2. The three worst problems, each with its timestamp and a concrete fix.
3. One sentence saying what the piece is about, written from the frames alone.
