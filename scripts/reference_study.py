#!/usr/bin/env python3
"""Measure films the way the pipeline measures its own drafts.

For each video: hard cuts and shot lengths, still holds, a motion curve, loudness, colours,
and contact sheets with one frame per shot (one every two seconds through long shots). Each
film gets study.json, study.md and sheet-NN.png in its own folder under --out, which defaults
to a studies folder beside the library, outside any project, because a study holds frames of
the film. study.md says
which moment each sheet cell shows, because many ffmpeg builds lack drawtext. With several
films, or with --draft, board.md compares them, and marks each measure where the draft falls
outside the references. Needs ffmpeg and ffprobe; Python stdlib only.
"""
import argparse
import json
import math
import os
import statistics
import sys

from frame_qa import changes, spikes
from media import MediaError, duration, ffmpeg, frame_size, has_audio, probe_fps, raw_frames, run, tile
from motion_library import default_home

BARS = "▁▂▃▄▅▆▇█"
SHEET_ROWS = 6
SPIKE_RATIO = 4.0


def scene_scores(video):
    """(seconds, score) for every frame: ffmpeg's scene change, 0 for the same picture to 1 for a new one."""
    out = run(["ffmpeg", "-v", "error", "-i", video, "-an", "-vf",
               "scale=160:-2,select='gte(scene,0)',metadata=mode=print:key=lavfi.scene_score:file=-",
               "-f", "null", "-"])
    scores, moment = [], None
    for line in out.splitlines():
        if "pts_time:" in line:
            moment = float(line.rsplit("pts_time:", 1)[1])
        elif line.startswith("lavfi.scene_score=") and moment is not None:
            scores.append((moment, float(line.split("=", 1)[1])))
    return scores


def spiking_frames(video):
    """Frames whose picture change is a one-frame spike, and frames inside one-frame flashes."""
    frames = raw_frames(video, 160, 90)
    _, jumps, flashed = spikes(frames, changes(frames), 1.0, SPIKE_RATIO)
    return set(jumps), flashed


def find_shots(scores, length, fps, threshold, floor, spiking=(), flashed=()):
    """Hard cuts and the shots between them. A frame is a cut when its scene change reaches threshold, or
    reaches floor on a one-frame spike in picture change (a cut between similar pictures); never inside a
    flash, and at least two frames after the previous cut."""
    cuts, gap = [], 1.5 / fps
    for frame, (moment, score) in enumerate(scores):
        if frame in flashed or not (score >= threshold or (score >= floor and frame in spiking)):
            continue
        if gap <= moment <= length - gap and (not cuts or moment - cuts[-1] >= gap):
            cuts.append(moment)
    edges = [0.0] + cuts + [length]
    return cuts, list(zip(edges, edges[1:]))


def find_holds(rates, still, min_hold, fps):
    """Stretches of at least min_hold seconds whose change per second stays below still."""
    holds, start, last = [], None, None
    for moment, rate in rates + [(float("inf"), float("inf"))]:
        if rate < still:
            start = moment - 1.0 / fps if start is None else start
            last = moment
            continue
        if start is not None and last - start >= min_hold:
            holds.append((max(0.0, start), last))
        start = None
    return holds


def curve(pairs, length, step=1.0):
    """Mean of the (seconds, value) pairs falling in each step-long bucket; None for an empty bucket."""
    buckets = [[] for _ in range(max(1, int(math.ceil(length / step))))]
    for moment, value in pairs:
        buckets[min(max(int(moment / step), 0), len(buckets) - 1)].append(value)
    return [round(sum(bucket) / len(bucket), 4) if bucket else None for bucket in buckets]


def bars(values, floor=0.0):
    """One block character per value, scaled from floor to the largest value; a space where empty."""
    present = [value - floor for value in values if value is not None]
    top = max(present) if present and max(present) > 0 else 1.0
    return "".join(" " if value is None else BARS[int(max(0.0, value - floor) / top * (len(BARS) - 1) + 0.5)]
                   for value in values)


def sample_times(shots, every=2.0):
    """(shot number, seconds): the middle of each shot, or one every `every` seconds through a long shot."""
    picks = []
    for number, (start, end) in enumerate(shots, 1):
        span = end - start
        if span <= 1.5 * every:
            picks.append((number, start + span / 2))
            continue
        count = int(span // every)
        first = start + (span - (count - 1) * every) / 2
        picks += [(number, first + i * every) for i in range(count)]
    return picks


def write_sheets(video, picks, length, fps, out, columns):
    """Tile the picked frames into sheet-01.png, sheet-02.png...; returns one index line per cell."""
    last_frame = max(0, int(length * fps) - 2)
    chosen, seen = [], set()
    for number, moment in picks:
        frame = min(int(round(moment * fps)), last_frame)
        if frame not in seen:
            seen.add(frame)
            chosen.append((number, frame))
    select = "+".join("eq(n,%d)" % frame for _, frame in chosen)
    ffmpeg("-i", video, "-vf", "select='%s',scale=320:-2," % select + tile(columns, SHEET_ROWS),
           "-fps_mode", "vfr", os.path.join(out, "sheet-%02d.png"))
    per_sheet = columns * SHEET_ROWS
    return ["sheet-%02d cell %2d  %7.2f s  shot %d" % (i // per_sheet + 1, i % per_sheet + 1, frame / fps, number)
            for i, (number, frame) in enumerate(chosen)]


def loudness(video, length):
    """Integrated loudness, loudness range, true peak and momentary loudness each second; None if silent."""
    if not has_audio(video):
        return None
    out = run(["ffmpeg", "-nostats", "-v", "error", "-i", video, "-vn", "-af",
               "ebur128=peak=true:metadata=1,ametadata=mode=print:file=-", "-f", "null", "-"])
    moment, momentary, last, peak = None, [], {}, 0.0
    for line in out.splitlines():
        if "pts_time:" in line:
            moment = float(line.rsplit("pts_time:", 1)[1])
        elif line.startswith("lavfi.r128.") and moment is not None:
            key, value = line[len("lavfi.r128."):].split("=", 1)
            last[key] = float(value)
            if key == "M" and moment >= 0.4:
                momentary.append((moment, max(float(value), -70.0)))
            elif key == "true_peak":
                peak = max(peak, float(value))
    return {"integrated": round(last["I"], 1) if "I" in last else None,
            "range": round(last["LRA"], 1) if "LRA" in last else None,
            "true_peak": round(20 * math.log10(peak), 1) if peak > 0 else None,
            "momentary": curve(momentary, length)}


def palette(video, length, top=6):
    """Most common colours over frames sampled through the film, small saturated accents, and brightness."""
    rate = max(0.5, min(4.0, 240.0 / max(length, 1.0)))
    bins, accents, total, luma = {}, {}, 0, 0.0
    for frame in raw_frames(video, 48, 27, "rgb24", "%.3f" % rate):
        for i in range(0, len(frame), 3):
            red, green, blue = frame[i], frame[i + 1], frame[i + 2]
            total += 1
            luma += 0.2126 * red + 0.7152 * green + 0.0722 * blue
            tally(bins, red, green, blue)
            if max(red, green, blue) - min(red, green, blue) >= 72:
                tally(accents, red, green, blue)
    return {"colours": strongest(bins, total, top), "accents": strongest(accents, total, 3),
            "mean_luma": int(round(luma / max(total, 1)))}


def tally(bins, red, green, blue):
    entry = bins.setdefault((red >> 4, green >> 4, blue >> 4), [0, 0, 0, 0])
    for slot, value in enumerate((1, red, green, blue)):
        entry[slot] += value


def strongest(bins, total, top, near=40):
    """The `top` most common colours; a bin within `near` of a colour already chosen joins it."""
    chosen = []
    for count, red, green, blue in sorted(bins.values(), reverse=True):
        colour = (red / count, green / count, blue / count)
        home = next((pick for pick in chosen if sum((a - b) ** 2 for a, b in zip(pick[1], colour)) < near ** 2), None)
        if home:
            home[0] += count
        elif len(chosen) < top:
            chosen.append([count, colour])
    return [{"hex": "#%02X%02X%02X" % tuple(int(round(c)) for c in colour), "share": round(count / float(total), 3)}
            for count, colour in sorted(chosen, key=lambda pick: -pick[0])]


def shot_stats(shots, length):
    lengths = [end - start for start, end in shots]
    tenths = statistics.quantiles(lengths, n=10, method="inclusive") if len(lengths) > 1 else [lengths[0]] * 9
    return {"count": len(lengths), "mean": round(statistics.mean(lengths), 2),
            "median": round(statistics.median(lengths), 2), "p10": round(tenths[0], 2),
            "p90": round(tenths[-1], 2), "cuts_per_minute": round((len(lengths) - 1) / length * 60, 1),
            "final": round(lengths[-1], 2)}


def study(video, out, threshold, floor, still, columns):
    os.makedirs(out, exist_ok=True)
    length, fps, size = duration(video), probe_fps(video), frame_size(video)
    scores = scene_scores(video)
    cuts, shots = find_shots(scores, length, fps, threshold, floor, *spiking_frames(video))
    rates = [(moment, score * fps) for moment, score in scores]
    holds = find_holds(rates, still, 1.0, fps)
    result = {
        "video": os.path.basename(video), "duration": round(length, 2), "fps": round(fps, 3), "size": list(size),
        "shots": shot_stats(shots, length), "cuts": [round(cut, 3) for cut in cuts],
        "holds": [[round(start, 2), round(end, 2)] for start, end in holds],
        "hold_share": round(sum(end - start for start, end in holds) / length, 3),
        "motion": curve([rate for rate, (_, score) in zip(rates, scores) if score < threshold], length),
        "loudness": loudness(video, length), "palette": palette(video, length),
    }
    cells = write_sheets(video, sample_times(shots), length, fps, out, columns)
    with open(os.path.join(out, "study.json"), "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=1)
    with open(os.path.join(out, "study.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(summary(result) + ["", "## Contact sheets", ""] + cells) + "\n")
    return result


def median_motion(item):
    values = [value for value in item["motion"] if value is not None]
    return round(statistics.median(values), 3) if values else None


MEASURES = (
    ("median shot s", lambda item: item["shots"]["median"]),
    ("cuts a minute", lambda item: item["shots"]["cuts_per_minute"]),
    ("final shot s", lambda item: item["shots"]["final"]),
    ("still share", lambda item: item["hold_share"]),
    ("median motion", median_motion),
    ("LUFS", lambda item: (item["loudness"] or {}).get("integrated")),
    ("LRA", lambda item: (item["loudness"] or {}).get("range")),
    ("true peak", lambda item: (item["loudness"] or {}).get("true_peak")),
    ("brightness", lambda item: item["palette"]["mean_luma"]),
)


def show(value):
    if value is None:
        return "-"
    return str(value) if isinstance(value, int) else "%.2f" % value if abs(value) < 10 else "%.1f" % value


def board(studies, draft):
    """One row per film; with a draft, its value per measure against the references' range."""
    head = ["film", "length s", "shots"] + [name for name, _ in MEASURES]
    lines = ["# Reference board", "",
             "Median motion is how much of the whole frame changes each second: a small subject moving on an "
             "empty ground reads low however lively it is, because most of the frame stands still.", "",
             "| " + " | ".join(head) + " |", "|" + " --- |" * len(head)]
    for item in studies + ([draft] if draft else []):
        name = item["video"] + (" (draft)" if item is draft else "")
        cells = [name, show(item["duration"]), str(item["shots"]["count"])] + [show(get(item)) for _, get in MEASURES]
        lines.append("| " + " | ".join(cells) + " |")
    if draft:
        lines += ["", "## The draft against the references", "",
                  "| measure | lowest | median | highest | draft | |", "| --- | --- | --- | --- | --- | --- |"]
        for name, get in MEASURES:
            values, mine = sorted(v for v in map(get, studies) if v is not None), get(draft)
            if values and mine is not None:
                outside = "outside" if mine < values[0] or mine > values[-1] else ""
                lines.append("| %s | %s | %s | %s | %s | %s |" % (name, show(values[0]), show(statistics.median(values)),
                                                              show(values[-1]), show(mine), outside))
    return lines


def summary(result):
    shots = result["shots"]
    lines = ["# %s" % result["video"], "",
             "%.2f s, %dx%d at %.3f fps" % (result["duration"], result["size"][0], result["size"][1], result["fps"]),
             "Shots: %d, mean %.2f s, median %.2f s, 10th to 90th percentile %.2f to %.2f s, %.1f cuts a minute, "
             "final shot %.2f s" % (shots["count"], shots["mean"], shots["median"], shots["p10"], shots["p90"],
                                     shots["cuts_per_minute"], shots["final"]),
             "Still holds of 1 s or more: %d, %.0f%% of the running time" % (len(result["holds"]),
                                                                           result["hold_share"] * 100),
             "Motion each second (change per second): %s" % bars(result["motion"])]
    sound = result["loudness"]
    if sound:
        inner = [(second, value) for second, value in enumerate(sound["momentary"])
                 if value is not None and 0 < second < len(sound["momentary"]) - 1] or [(0, None)]
        quiet, loud = min(inner, key=lambda pair: pair[1] or 0), max(inner, key=lambda pair: pair[1] or 0)
        lines += ["Loudness: %s LUFS integrated, range %s LU, true peak %s dBTP; quietest second %d, loudest %d"
                  % (sound["integrated"], sound["range"], sound["true_peak"], quiet[0], loud[0]),
                  "Loudness each second (momentary): %s" % bars(sound["momentary"], floor=-60.0)]
    else:
        lines.append("Loudness: no audio track")
    colours = result["palette"]
    lines.append("Colours: %s; accents: %s; mean brightness %d of 255" % (
        ", ".join("%s %.0f%%" % (c["hex"], c["share"] * 100) for c in colours["colours"]),
        ", ".join("%s %.1f%%" % (c["hex"], c["share"] * 100) for c in colours["accents"]) or "none",
        colours["mean_luma"]))
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("videos", nargs="+")
    parser.add_argument("--draft", help="a render of your own, compared against the videos on board.md")
    parser.add_argument("--out", default=os.path.join(default_home(), "studies"),
                        help="output folder, outside the project (default: studies beside the library)")
    parser.add_argument("--threshold", type=float, default=0.3, help="scene change that is always a hard cut (0-1)")
    parser.add_argument("--spike-floor", type=float, default=0.2,
                        help="scene change that is a hard cut when the picture change also spikes for one frame")
    parser.add_argument("--still", type=float, default=0.005,
                        help="change per second (scene change times fps) below which the picture is still")
    parser.add_argument("--columns", type=int, default=6, help="contact sheet columns")
    args = parser.parse_args(argv)
    studies = []
    for video in args.videos + ([args.draft] if args.draft else []):
        folder = os.path.join(args.out, os.path.splitext(os.path.basename(video))[0])
        try:
            studies.append(study(video, folder, args.threshold, args.spike_floor, args.still, args.columns))
        except MediaError as error:
            print(error, file=sys.stderr)
            return 1
        print("\n".join(summary(studies[-1])) + "\n")
    draft = studies.pop() if args.draft else None
    if draft or len(studies) > 1:
        path = os.path.join(args.out, "board.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(board(studies, draft)) + "\n")
        print("board: " + path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
