"""Shared helpers for the video tests: skip when ffmpeg is missing, and encode generated clips."""
import shutil
import subprocess
import unittest

needs_ffmpeg = unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg and ffprobe")


def encode(path, inputs, *extra):
    """Encode generated inputs (with any filter, map or audio arguments) to H.264 yuv420p at path."""
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + list(inputs) + ["-c:v", "libx264"] + list(extra)
                   + ["-pix_fmt", "yuv420p", path], check=True)
    return path
