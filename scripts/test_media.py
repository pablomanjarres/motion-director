"""Tests for media.py, the shared ffmpeg and ffprobe helpers."""
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import media  # noqa: E402
from test_fixtures import encode, needs_ffmpeg  # noqa: E402


class RateParsingTest(unittest.TestCase):
    def test_reads_ffprobe_rates_including_trailing_separators(self):
        self.assertEqual(media.parse_rate("30/1,\n"), 30.0)
        self.assertAlmostEqual(media.parse_rate("30000/1001"), 29.97, places=2)
        for bad in ("N/A", "0/0", ""):
            with self.assertRaises(media.MediaError):
                media.parse_rate(bad)


@needs_ffmpeg
class ProbeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="media-test-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.silent = encode(os.path.join(self.tmp, "silent.mp4"), ["-f", "lavfi", "-i", "testsrc2=s=64x36:r=25:d=2"])

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

    def test_variable_frame_rate_files_decode_one_buffer_per_real_frame(self):
        uneven = encode(os.path.join(self.tmp, "uneven.mp4"), [
            "-f", "lavfi", "-i", "testsrc2=s=64x36:r=30:d=2", "-vf", "select='not(eq(mod(n,3),2))'",
            "-fps_mode", "vfr"])
        self.assertEqual(len(media.raw_frames(uneven, 16, 9)), len(media.frame_hashes(uneven)))

    def test_video_duration_ignores_a_longer_audio_track(self):
        long_tail = encode(os.path.join(self.tmp, "tail.mp4"), [
            "-f", "lavfi", "-i", "testsrc2=s=64x36:r=25:d=2", "-f", "lavfi", "-i", "sine=d=3.5", "-c:a", "aac"])
        self.assertGreater(media.duration(long_tail), 3.0)
        self.assertAlmostEqual(media.video_duration(long_tail), 2.0, places=1)

    def test_unreadable_file_raises_media_error(self):
        with self.assertRaises(media.MediaError):
            media.probe_fps(os.path.join(self.tmp, "missing.mp4"))


if __name__ == "__main__":
    unittest.main()
