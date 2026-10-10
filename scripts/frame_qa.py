#!/usr/bin/env python3
"""Find motion defects in a rendered video by measuring frame-to-frame change.

Reports one-frame position jumps (pops), one-frame flashes, frozen stretches (the
final hold excepted) and black frames away from the edges. With --against it
compares two renders frame by frame, which proves a render is deterministic when
the same frames are rendered twice. Needs ffmpeg and ffprobe; Python stdlib only.

Exit status: 0 nothing to look at, 1 findings listed, 2 the video could not be read.
"""
import argparse
import json
import re
import subprocess
import sys


def parse_rate(text):
    """Read the first 'num/den' fraction; ffprobe sometimes appends separators such as '30/1,'."""
    match = re.search(r"(\d+)/(\d+)", text)
    if not match or int(match.group(2)) == 0:
        raise ValueError("no frame rate in %r" % text.strip())
    return int(match.group(1)) / float(match.group(2))


def probe_fps(path):
    done = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                           "stream=r_frame_rate", "-of", "csv=p=0", path], capture_output=True, text=True)
    if done.returncode != 0:
        raise ValueError("cannot read %s: %s" % (path, done.stderr.strip() or "no video stream"))
    try:
        return parse_rate(done.stdout)
    except ValueError:
        raise ValueError("cannot read a frame rate from %s" % path)


def decode(path, width, height):
    """Every frame as a bytes object of width*height grey samples."""
    done = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf",
                           "scale=%d:%d:flags=area,format=gray" % (width, height),
                           "-f", "rawvideo", "-"], capture_output=True)
    if done.returncode != 0:
        raise ValueError("cannot decode %s: %s" % (path, done.stderr.decode(errors="replace").strip()))
    size = width * height
    data = done.stdout
    return [data[i:i + size] for i in range(0, len(data) - size + 1, size)]


def change(a, b):
    """Mean absolute difference between two grey frames, 0 (same) to 255."""
    return sum(abs(x - y) for x, y in zip(a, b)) / float(len(a))


def find_defects(frames, fps, cuts, min_jump, ratio, freeze_seconds):
    findings, notes = [], []
    diffs = [0.0] + [change(frames[i - 1], frames[i]) for i in range(1, len(frames))]
    stamp = lambda i: "%.3f s (frame %d)" % (i / fps, i)
    flashed = set()
    for i in range(1, len(frames) - 1):
        if diffs[i] >= min_jump and diffs[i + 1] >= min_jump:
            if change(frames[i - 1], frames[i + 1]) < 0.5 * min(diffs[i], diffs[i + 1]):
                findings.append("flash at %s: one frame unlike both neighbours" % stamp(i))
                flashed.update((i, i + 1))
    for i in range(1, len(frames)):
        before = diffs[i - 1] if i > 1 else 0.0
        after = diffs[i + 1] if i + 1 < len(frames) else 0.0
        if i in flashed or diffs[i] < min_jump or diffs[i] <= ratio * max(before, after):
            continue
        if any(abs(i / fps - cut) <= 1.5 / fps for cut in cuts):
            notes.append("declared cut at %s" % stamp(i))
        else:
            findings.append("jump at %s: change %.1f vs %.1f around it (pop or undeclared cut)"
                            % (stamp(i), diffs[i], max(before, after)))
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
    edge = int(0.5 * fps)
    dark = [i for i in range(edge, len(frames) - edge) if sum(frames[i]) / float(len(frames[i])) < 10]
    if dark:
        findings.append("%d black frames, first at %s" % (len(dark), stamp(dark[0])))
    return findings, notes


def compare(frames, other, fps):
    if len(frames) != len(other):
        return ["frame counts differ: %d vs %d" % (len(frames), len(other))]
    diffs = [change(a, b) for a, b in zip(frames, other)]
    first = next((i for i, diff in enumerate(diffs) if diff > 0.5), None)
    if first is None:
        return []
    worst = max(range(len(diffs)), key=diffs.__getitem__)
    return ["renders differ from frame %d (%.3f s); largest difference at frame %d (%.1f)"
            % (first, first / fps, worst, diffs[worst])]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("video")
    parser.add_argument("--against", help="a second render of the same frames to compare")
    parser.add_argument("--cuts", default="", help="comma-separated seconds of intended hard cuts")
    parser.add_argument("--size", default="160x90", help="analysis size, default 160x90")
    parser.add_argument("--min-jump", type=float, default=1.0, help="smallest change worth flagging (0-255)")
    parser.add_argument("--ratio", type=float, default=3.0, help="how far a jump must exceed its neighbours")
    parser.add_argument("--freeze-seconds", type=float, default=3.0, help="longest acceptable still stretch")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    width, height = (int(n) for n in args.size.lower().split("x"))
    cuts = [float(c) for c in args.cuts.split(",") if c.strip()]
    try:
        fps = probe_fps(args.video)
        frames = decode(args.video, width, height)
        if args.against:
            findings, notes = compare(frames, decode(args.against, width, height), fps), []
        else:
            findings, notes = find_defects(frames, fps, cuts, args.min_jump, args.ratio, args.freeze_seconds)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"video": args.video, "fps": fps, "frames": len(frames),
                          "findings": findings, "notes": notes}, indent=1))
    else:
        print("%s: %d frames at %.3f fps" % (args.video, len(frames), fps))
        for line in findings:
            print("  finding: " + line)
        for line in notes:
            print("  ok: " + line)
        if not findings:
            print("  no findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
