"""ffmpeg and ffprobe plumbing shared by the motion scripts. Python stdlib only."""
import re
import subprocess


class MediaError(Exception):
    """ffmpeg or ffprobe could not read or write a file."""


def run(args, text=True):
    """Run a tool and return its stdout; raise MediaError with the end of stderr on failure."""
    done = subprocess.run(args, capture_output=True, text=text)
    if done.returncode != 0:
        stderr = done.stderr if text else done.stderr.decode(errors="replace")
        raise MediaError("%s failed: %s" % (args[0], stderr.strip()[-300:] or "no output"))
    return done.stdout


def ffmpeg(*args):
    run(["ffmpeg", "-v", "error", "-y"] + list(args))


def probe(path, entries, stream=None):
    """Read ffprobe fields as comma-separated text, for example probe(path, "format=duration")."""
    selector = ["-select_streams", stream] if stream else []
    return run(["ffprobe", "-v", "error"] + selector + ["-show_entries", entries, "-of", "csv=p=0", path]).strip()


def parse_rate(text):
    """Read the first 'num/den' fraction; ffprobe sometimes appends separators such as '30/1,'."""
    match = re.search(r"(\d+)/(\d+)", text)
    if not match or int(match.group(2)) == 0:
        raise MediaError("no frame rate in %r" % text.strip())
    return int(match.group(1)) / float(match.group(2))


def probe_fps(path):
    return parse_rate(probe(path, "stream=r_frame_rate", "v:0"))


def duration(path):
    return float(probe(path, "format=duration"))


def video_duration(path):
    """The video stream's own length, so a longer audio track does not stretch it; the container's as a fallback."""
    try:
        return float(probe(path, "stream=duration", "v:0"))
    except ValueError:
        return duration(path)


def frame_size(path):
    width, height = probe(path, "stream=width,height", "v:0").split(",")[:2]
    return int(width), int(height)


def has_audio(path):
    return bool(probe(path, "stream=index", "a:0"))


def frame_hashes(path):
    """An MD5 of every decoded video frame at full resolution, for proving two renders identical."""
    out = run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:v:0", "-f", "framemd5", "-"])
    return [line.rsplit(",", 1)[1].strip() for line in out.splitlines() if line.strip() and not line.startswith("#")]


def tile(columns, rows):
    """The tile filter for contact sheets; unused cells are mid grey so they never read as black frames."""
    return "tile=%dx%d:color=0x808080" % (columns, rows)


def raw_frames(path, width, height, pix_fmt="gray", rate=None):
    """Decoded frames scaled to width x height, one bytes object each (gray: 1 byte a pixel, rgb24: 3). Without a
    rate every real frame appears once, never duplicated to a constant rate, so indices match frame hashes and
    scene scores on variable-frame-rate files too."""
    filters = ("fps=%s," % rate if rate else "") + "scale=%d:%d:flags=area,format=%s" % (width, height, pix_fmt)
    data = run(["ffmpeg", "-v", "error", "-i", path, "-vf", filters, "-fps_mode", "passthrough", "-f", "rawvideo", "-"],
               text=False)
    size = width * height * (3 if pix_fmt == "rgb24" else 1)
    return [data[i:i + size] for i in range(0, len(data) - size + 1, size)]
