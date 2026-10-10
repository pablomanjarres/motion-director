#!/usr/bin/env python3
"""Find motion defects in a rendered video by measuring frame-to-frame change.

Reports one-frame position jumps (pops), one-frame flashes, frozen stretches (the
final hold excepted), black frames away from the edges, and more than three general
flashes in any one second (the photosensitivity limit). With --against it
hashes every decoded frame of two renders at full resolution, which proves a render
is deterministic when the same frames are rendered twice (at different concurrency). Needs ffmpeg and ffprobe; Python stdlib only.

Exit status: 0 nothing to look at, 1 findings listed, 2 the video could not be read.
"""
import argparse
import json
import sys

from media import MediaError, frame_hashes, probe_fps, raw_frames


# Grey levels to linear light, the basis of relative luminance in the general flash rule.
LINEAR = [level / 255.0 / 12.92 if level <= 10 else ((level / 255.0 + 0.055) / 1.055) ** 2.4 for level in range(256)]


def integral(flags, width):
    """Summed-area table with a zero row and column in front."""
    table = [0] * ((len(flags) // width + 1) * (width + 1))
    for y in range(len(flags) // width):
        running = 0
        for x in range(width):
            running += flags[y * width + x]
            table[(y + 1) * (width + 1) + x + 1] = table[y * (width + 1) + x + 1] + running
    return table


def busiest_window(flags, width, area=0.25):
    """Whether flagged pixels fill `area` of any window a third of the frame wide and high (the general flash rule's
    10-degree field), testing windows every sixth of the frame."""
    height = len(flags) // width
    win_w, win_h = max(1, width // 3), max(1, height // 3)
    table, row = integral(flags, width), width + 1
    for top in range(0, height - win_h + 1, max(1, height // 6)):
        for left in range(0, width - win_w + 1, max(1, width // 6)):
            count = (table[(top + win_h) * row + left + win_w] - table[top * row + left + win_w]
                     - table[(top + win_h) * row + left] + table[top * row + left])
            if count >= area * win_w * win_h:
                return True
    return False


def general_flashes(frames, fps, width):
    """The most general flashes in any one second, and the frame that second starts on. A transition is a frame
    where a quarter of any window a third of the frame wide and high changes relative luminance by 0.1 or more
    in one direction, the darker side below 0.8; a flash is a pair of opposite transitions."""
    transitions = []
    for i in range(1, len(frames)):
        darker, brighter = [], []
        for x, y in zip(frames[i - 1], frames[i]):
            a, b = LINEAR[x], LINEAR[y]
            changed = abs(b - a) >= 0.1 and min(a, b) < 0.8
            darker.append(1 if changed and b < a else 0)
            brighter.append(1 if changed and b > a else 0)
        if busiest_window(darker, width):
            transitions.append((i, -1))
        elif busiest_window(brighter, width):
            transitions.append((i, 1))
    window, most, start = max(1, int(round(fps))), 0, 0
    for k, (first, _) in enumerate(transitions):
        signs = [sign for frame, sign in transitions[k:] if frame < first + window]
        flashes = (sum(1 for a, b in zip(signs, signs[1:]) if a != b) + 1) // 2
        if flashes > most:
            most, start = flashes, first
    return most, start


def change(a, b):
    """Mean absolute difference between two grey frames, 0 (same) to 255."""
    return sum(abs(x - y) for x, y in zip(a, b)) / float(len(a))


def changes(frames):
    """The change into each frame from the one before it (0 for the first frame)."""
    return [0.0] + [change(frames[i - 1], frames[i]) for i in range(1, len(frames))]


def neighbours(diffs, i):
    return max(diffs[i - 1] if i > 1 else 0.0, diffs[i + 1] if i + 1 < len(diffs) else 0.0)


def spikes(frames, diffs, min_jump, ratio):
    """One-frame flashes (a frame unlike both neighbours), and jumps: frames whose change is at least
    min_jump and more than ratio times the change on either side. Returns (flashes, jumps, flashed)."""
    flashes, flashed = [], set()
    for i in range(1, len(diffs) - 1):
        if (diffs[i] >= min_jump and diffs[i + 1] >= min_jump
                and change(frames[i - 1], frames[i + 1]) < 0.5 * min(diffs[i], diffs[i + 1])):
            flashes.append(i)
            flashed.update((i, i + 1))
    jumps = [i for i in range(1, len(diffs))
             if i not in flashed and diffs[i] >= min_jump and diffs[i] > ratio * neighbours(diffs, i)]
    return flashes, jumps, flashed


def find_defects(frames, fps, cuts, min_jump, ratio, freeze_seconds, events=(), width=160):
    findings, notes = [], []
    diffs = changes(frames)
    stamp = lambda i: "%.3f s (frame %d)" % (i / fps, i)
    flashes, jumps, _ = spikes(frames, diffs, min_jump, ratio)
    findings += ["flash at %s: one frame unlike both neighbours" % stamp(i) for i in flashes]
    near = lambda i, moments: any(abs(i / fps - moment) <= 1.5 / fps for moment in moments)
    for i in jumps:
        if near(i, cuts):
            notes.append("declared cut at %s" % stamp(i))
        elif near(i, events):
            notes.append("declared event at %s" % stamp(i))
        else:
            findings.append("jump at %s: change %.1f vs %.1f around it (pop or undeclared cut)"
                            % (stamp(i), diffs[i], neighbours(diffs, i)))
    start = None
    for i in range(1, len(frames) + 1):
        still = i < len(frames) and diffs[i] < 0.1
        if still and start is None:
            start = i - 1
        elif not still and start is not None:
            length = (i - 1 - start) / fps
            if i == len(frames):
                notes.append("final hold of %.2f s from %s" % (length, stamp(start)))
            elif length > freeze_seconds:
                findings.append("frozen for %.2f s from %s" % (length, stamp(start)))
            start = None
    most, start = general_flashes(frames, fps, width)
    if most > 3:
        findings.append("%d general flashes in the second from %s (the photosensitivity limit is 3)"
                        % (most, stamp(start)))
    edge = int(0.5 * fps)
    dark = [i for i in range(edge, len(frames) - edge) if sum(frames[i]) / float(len(frames[i])) < 10]
    if dark:
        findings.append("%d black frames, first at %s" % (len(dark), stamp(dark[0])))
    return findings, notes


def compare(video, other_video, width, height, fps):
    """Frames whose full-resolution hashes differ, with the largest visible difference among them; frames are
    decoded for that only when the hashes disagree. Returns (findings, frame count)."""
    hashes, other_hashes = frame_hashes(video), frame_hashes(other_video)
    if len(hashes) != len(other_hashes):
        return ["frame counts differ: %d vs %d" % (len(hashes), len(other_hashes))], len(hashes)
    differing = [i for i, (a, b) in enumerate(zip(hashes, other_hashes)) if a != b]
    if not differing:
        return [], len(hashes)
    line = "renders differ in %d of %d frames, first at frame %d (%.3f s)" % (
        len(differing), len(hashes), differing[0], differing[0] / fps)
    frames, other = raw_frames(video, width, height), raw_frames(other_video, width, height)
    visible = [i for i in differing if i < len(frames) and i < len(other)]
    if visible:
        worst = max(visible, key=lambda i: change(frames[i], other[i]))
        line += "; largest visible difference at frame %d (%.1f)" % (worst, change(frames[worst], other[worst]))
    return [line], len(hashes)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("video")
    parser.add_argument("--against", help="a second render of the same frames to compare")
    parser.add_argument("--cuts", default="", help="comma-separated seconds of intended hard cuts")
    parser.add_argument("--events", default="",
                        help="comma-separated seconds of intended one-frame changes that are not cuts "
                             "(a caption switching whole, an inversion)")
    parser.add_argument("--size", default="160x90", help="analysis size, default 160x90")
    parser.add_argument("--min-jump", type=float, default=1.0, help="smallest change worth flagging (0-255)")
    parser.add_argument("--ratio", type=float, default=3.0, help="how far a jump must exceed its neighbours")
    parser.add_argument("--freeze-seconds", type=float, default=3.0, help="longest acceptable still stretch")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    width, height = (int(n) for n in args.size.lower().split("x"))
    cuts = [float(c) for c in args.cuts.split(",") if c.strip()]
    events = [float(e) for e in args.events.split(",") if e.strip()]
    try:
        fps = probe_fps(args.video)
        if args.against:
            (findings, count), notes = compare(args.video, args.against, width, height, fps), []
        else:
            frames = raw_frames(args.video, width, height)
            count = len(frames)
            findings, notes = find_defects(frames, fps, cuts, args.min_jump, args.ratio, args.freeze_seconds, events,
                                           width)
    except MediaError as error:
        print(error, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"video": args.video, "fps": fps, "frames": count,
                          "findings": findings, "notes": notes}, indent=1))
    else:
        print("%s: %d frames at %.3f fps" % (args.video, count, fps))
        for line in findings:
            print("  finding: " + line)
        for line in notes:
            print("  ok: " + line)
        if not findings:
            print("  no findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
