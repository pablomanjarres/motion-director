#!/usr/bin/env python3
"""Build the review pack for a render: frame 0, one frame per beat once it settles, a
contact sheet of those beats, every frame across each transition, and a phone-width sheet.

index.txt says what each image shows and when, because many ffmpeg builds lack drawtext and
nothing is labelled inside the images. Needs ffmpeg and ffprobe; Python stdlib only.
"""
import argparse
import math
import os
import sys

from media import MediaError, duration, ffmpeg, probe_fps


def numbers(text):
    return [float(value) for value in text.split(",") if value.strip()]


def windows(text):
    return [tuple(float(edge) for edge in part.split("-")) for part in text.split(",") if part.strip()]


def build(video, beats, transitions, settle, out):
    os.makedirs(out, exist_ok=True)
    path = lambda name: os.path.join(out, name)
    length, fps = duration(video), probe_fps(video)
    index = ["%s: %.2f s at %.3f fps" % (video, length, fps),
             "frame0.png  frame 0 at full size, the thumbnail feeds show"]
    ffmpeg("-i", video, "-frames:v", "1", path("frame0.png"))
    kept = 0
    for beat in beats:
        moment = beat + settle
        if moment >= length:
            print("skipped the beat at %.2f s: %.2f s is past the end (%.2f s)" % (beat, moment, length),
                  file=sys.stderr)
            continue
        kept += 1
        ffmpeg("-ss", "%.3f" % moment, "-i", video, "-frames:v", "1", "-vf", "scale=640:-1",
               path("beat-%02d.png" % kept))
        index.append("beat-%02d.png  %.2f s (beat at %.2f s plus %.2f s to settle)" % (kept, moment, beat, settle))
    if kept:
        columns = min(4, kept)
        ffmpeg("-start_number", "1", "-i", path("beat-%02d.png"), "-vf",
               "tile=%dx%d" % (columns, math.ceil(kept / float(columns))), "-frames:v", "1", path("contact.png"))
        index.append("contact.png  the beat frames in order, %d per row" % columns)
    for number, (start, end) in enumerate(transitions, 1):
        rows = math.ceil((int(round((end - start) * fps)) + 1) / 8.0)
        ffmpeg("-i", video, "-vf", "select='between(t,%.3f,%.3f)',scale=320:-1,tile=8x%d" % (start, end, rows),
               "-frames:v", "1", path("strip-%02d.png" % number))
        index.append("strip-%02d.png  every frame from %.2f s to %.2f s, 8 per row" % (number, start, end))
    ffmpeg("-i", video, "-vf", "fps=2,scale=360:-1,tile=6x%d" % max(1, math.ceil(length * 2 / 6.0)),
           "-frames:v", "1", path("phone.png"))
    index.append("phone.png  two frames per second at 360 px wide, 6 per row: judge readability here")
    with open(path("index.txt"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(index) + "\n")
    return index


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("video")
    parser.add_argument("--beats", default="", help="comma-separated beat times in seconds")
    parser.add_argument("--transitions", default="", help="comma-separated windows such as 3.0-3.6")
    parser.add_argument("--settle", type=float, default=0.3, help="seconds after a beat before grabbing it")
    parser.add_argument("--out", default="review/pack", help="output folder (default review/pack)")
    args = parser.parse_args(argv)
    try:
        index = build(args.video, numbers(args.beats), windows(args.transitions), args.settle, args.out)
    except (MediaError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print("\n".join(index))
    return 0


if __name__ == "__main__":
    sys.exit(main())
