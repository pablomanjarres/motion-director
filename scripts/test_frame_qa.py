"""Tests for frame_qa.py using tiny generated videos with one known defect each."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from test_fixtures import encode, needs_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "frame_qa.py")
FLASH_AT_FRAME_30 = ",drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='eq(n,30)'"


@needs_ffmpeg
class FrameQaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="frame-qa-test-")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, True)

    def make(self, name, x_expr, extra="", seconds=2):
        """A white square over grey at 30 fps; x_expr positions it, extra appends filters."""
        out = os.path.join(self.tmp, name + ".mp4")
        size = "color=c=gray:s=192x108:r=30:d=%s" % seconds
        square = "color=c=white:s=20x20:r=30:d=%s" % seconds
        graph = "[0][1]overlay=x='%s':y=40%s" % (x_expr, extra)
        return encode(out, ["-f", "lavfi", "-i", size, "-f", "lavfi", "-i", square, "-filter_complex", graph],
                      "-crf", "10")

    def qa(self, *args):
        return subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True)

    def assertClean(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_smooth_motion_is_clean(self):
        self.assertClean(self.qa(self.make("smooth", "t*60")))

    def test_one_frame_flash_is_reported_with_its_time(self):
        found = self.qa(self.make("flash", "t*60", FLASH_AT_FRAME_30))
        self.assertEqual(found.returncode, 1, found.stdout + found.stderr)
        self.assertIn("flash", found.stdout)
        self.assertIn("1.000", found.stdout)

    def test_jump_is_reported_unless_declared_as_a_cut(self):
        jump = self.make("jump", "if(lt(t,1.5),20,120)")
        found = self.qa(jump)
        self.assertEqual(found.returncode, 1, found.stdout + found.stderr)
        self.assertIn("jump", found.stdout)
        self.assertIn("1.500", found.stdout)
        self.assertClean(self.qa(jump, "--cuts", "1.5"))
        switched = self.qa(jump, "--events", "1.5")
        self.assertClean(switched)
        self.assertIn("declared event", switched.stdout)

    def test_frozen_stretch_is_reported_but_the_final_hold_is_not(self):
        self.assertClean(self.qa(self.make("held", "min(t,1)*60", seconds=4)))
        frozen = self.make("frozen", "if(lt(t,0.5),t*60,if(lt(t,3.8),30,30+(t-3.8)*60))", seconds=4.5)
        found = self.qa(frozen)
        self.assertEqual(found.returncode, 1, found.stdout + found.stderr)
        self.assertIn("frozen", found.stdout)

    def test_against_proves_matching_renders_and_names_the_first_difference(self):
        first, second = self.make("first", "t*60"), self.make("second", "t*60")
        self.assertClean(self.qa(first, "--against", second))
        differs = self.qa(first, "--against", self.make("flash-b", "t*60", FLASH_AT_FRAME_30))
        self.assertEqual(differs.returncode, 1, differs.stdout + differs.stderr)
        self.assertIn("frame 30", differs.stdout)


if __name__ == "__main__":
    unittest.main()
