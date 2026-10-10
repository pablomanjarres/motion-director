"""Tests for media.py, the shared ffmpeg and ffprobe helpers."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import media  # noqa: E402


class RateParsingTest(unittest.TestCase):
    def test_reads_ffprobe_rates_including_trailing_separators(self):
        self.assertEqual(media.parse_rate("30/1,\n"), 30.0)
        self.assertAlmostEqual(media.parse_rate("30000/1001"), 29.97, places=2)
        for bad in ("N/A", "0/0", ""):
            with self.assertRaises(media.MediaError):
                media.parse_rate(bad)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg and ffprobe")
class ProbeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="media-test-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.silent = os.path.join(self.tmp, "silent.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=64x36:r=25:d=2",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", self.silent], check=True)

    def test_reads_rate_length_size_and_audio(self):
        self.assertEqual(media.probe_fps(self.silent), 25.0)
        self.assertAlmostEqual(media.duration(self.silent), 2.0, places=1)
        self.assertEqual(media.frame_size(self.silent), (64, 36))
        self.assertFalse(media.has_audio(self.silent))

    def test_raw_frames_returns_one_buffer_per_frame(self):
        grey = media.raw_frames(self.silent, 16, 9)
        self.assertEqual((len(grey), len(grey[0])), (50, 16 * 9))
        colour = media.raw_frames(self.silent, 16, 9, "rgb24", rate=5)
        self.assertEqual((len(colour), len(colour[0])), (10, 16 * 9 * 3))

    def test_unreadable_file_raises_media_error(self):
        with self.assertRaises(media.MediaError):
            media.probe_fps(os.path.join(self.tmp, "missing.mp4"))


if __name__ == "__main__":
    unittest.main()
