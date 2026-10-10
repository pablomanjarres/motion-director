"""Tests for review_pack.py on a generated three-second clip."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from test_fixtures import encode, needs_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "review_pack.py")


@needs_ffmpeg
class ReviewPackTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="review-pack-test-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.video = encode(os.path.join(self.tmp, "clip.mp4"), ["-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=3"])
        self.out = os.path.join(self.tmp, "pack")

    def pack(self, *args):
        return subprocess.run([sys.executable, SCRIPT, self.video, "--out", self.out] + list(args),
                              capture_output=True, text=True)

    def size(self, name):
        done = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0",
                               os.path.join(self.out, name)], capture_output=True, text=True, check=True)
        return tuple(int(value) for value in done.stdout.strip().split(","))

    def test_builds_frame0_beats_contact_strips_phone_sheet_and_index(self):
        done = self.pack("--beats", "0.5,1.5,2.5", "--transitions", "1.0-1.5")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.size("frame0.png"), (320, 180))
        for number in (1, 2, 3):
            self.assertTrue(os.path.isfile(os.path.join(self.out, "beat-%02d.png" % number)))
        self.assertTrue(os.path.isfile(os.path.join(self.out, "contact.png")))
        self.assertTrue(os.path.isfile(os.path.join(self.out, "strip-01.png")))
        self.assertEqual(self.size("phone.png")[0] % 360, 0)
        with open(os.path.join(self.out, "index.txt"), encoding="utf-8") as handle:
            index = handle.read()
        self.assertIn("beat-02.png", index)
        self.assertIn("1.80 s", index)
        self.assertIn("strip-01.png", index)
        self.assertIn("1.00 s to 1.50 s", index)

    def test_empty_contact_cells_are_grey_not_black(self):
        done = self.pack("--beats", "0.2,0.6,1.0,1.4,1.8")
        self.assertEqual(done.returncode, 0, done.stderr)
        sys.path.insert(0, HERE)
        from media import raw_frames
        sheet = raw_frames(os.path.join(self.out, "contact.png"), 8, 2, "rgb24")[0]
        self.assertTrue(all(abs(value - 128) <= 8 for value in sheet[-3:]), list(sheet[-3:]))

    def test_beats_past_the_end_are_reported_and_skipped(self):
        done = self.pack("--beats", "0.5,9.0")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("9.00", done.stderr)
        self.assertTrue(os.path.isfile(os.path.join(self.out, "beat-01.png")))
        self.assertFalse(os.path.exists(os.path.join(self.out, "beat-02.png")))


if __name__ == "__main__":
    unittest.main()
