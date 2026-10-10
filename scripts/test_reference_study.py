"""Tests for reference_study.py on generated clips with known cuts, colours and sound."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from reference_study import find_shots, shot_stats
from test_fixtures import encode, needs_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "reference_study.py")
CREAM, INK, CLAY = (245, 243, 238), (23, 23, 26), (217, 119, 87)


class CutRuleTest(unittest.TestCase):
    def test_a_cut_needs_a_big_change_or_a_one_frame_spike_and_never_sits_in_a_flash(self):
        fps, scores = 30.0, [(frame / 30.0, 0.01) for frame in range(90)]
        for frame, score in ((10, 0.5), (11, 0.5), (20, 0.22), (30, 0.22), (40, 0.6), (50, 0.1)):
            scores[frame] = (frame / fps, score)
        cuts, shots = find_shots(scores, 3.0, fps, 0.3, 0.2, spiking={20, 40, 50}, flashed={40, 41})
        self.assertEqual([int(round(cut * fps)) for cut in cuts], [10, 20])
        self.assertEqual(len(shots), 3)

    def test_percentiles_stay_inside_the_shots_measured(self):
        stats = shot_stats([(0.0, 1.0), (1.0, 11.0)], 11.0)
        self.assertGreaterEqual(stats["p10"], 1.0)
        self.assertLessEqual(stats["p90"], 10.0)


def colour(rgb):
    return "0x%02X%02X%02X" % rgb


def near(hex_value, rgb, tolerance=10):
    value = tuple(int(hex_value[i:i + 2], 16) for i in (1, 3, 5))
    return all(abs(a - b) <= tolerance for a, b in zip(value, rgb))


@needs_ffmpeg
class ReferenceStudyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="reference-study-test-")
        cls.film = os.path.join(cls.tmp, "film.mp4")
        segment = "color=c=%s:s=320x180:r=30:d=2"
        graph = ("[0][3]overlay=x=20:y=20[a];[a][1][2]concat=n=3:v=1:a=0[v];"
                 "[4][5][6]concat=n=3:v=0:a=1,volume=0.5[s]")
        encode(cls.film, ["-f", "lavfi", "-i", segment % colour(CREAM), "-f", "lavfi", "-i", segment % colour(INK),
                            "-f", "lavfi", "-i", segment % colour(CREAM),
                            "-f", "lavfi", "-i", "color=c=%s:s=40x40:r=30:d=2" % colour(CLAY),
                            "-f", "lavfi", "-i", "sine=f=440:d=3:sample_rate=48000",
                            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono:d=0.5",
                            "-f", "lavfi", "-i", "sine=f=660:d=2.5:sample_rate=48000",
                          "-filter_complex", graph, "-map", "[v]", "-map", "[s]", "-c:a", "aac"], "-crf", "12")
        cls.copy = os.path.join(cls.tmp, "copy.mp4")
        shutil.copy(cls.film, cls.copy)
        cls.draft = os.path.join(cls.tmp, "draft.mp4")
        encode(cls.draft, ["-f", "lavfi", "-i", segment.replace("d=2", "d=6") % colour(CREAM)], "-crf", "12")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, True)

    def study(self, *args):
        out = tempfile.mkdtemp(dir=self.tmp)
        done = subprocess.run([sys.executable, SCRIPT] + list(args) + ["--out", out], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        return out

    def test_finds_cuts_holds_sound_colours_and_sheets(self):
        folder = os.path.join(self.study(self.film), "film")
        with open(os.path.join(folder, "study.json"), encoding="utf-8") as handle:
            result = json.load(handle)
        self.assertEqual(result["shots"]["count"], 3)
        for cut, expected in zip(result["cuts"], (2.0, 4.0)):
            self.assertAlmostEqual(cut, expected, delta=0.05)
        self.assertGreater(result["hold_share"], 0.9)
        self.assertLess(result["loudness"]["integrated"], 0)
        self.assertLess(min(result["loudness"]["momentary"][1:-1]), min(result["loudness"]["momentary"][1:3]))
        top = result["palette"]["colours"]
        self.assertTrue(near(top[0]["hex"], CREAM), top)
        self.assertAlmostEqual(top[0]["share"], 0.66, delta=0.06)
        self.assertTrue(near(top[1]["hex"], INK), top)
        self.assertTrue(near(result["palette"]["accents"][0]["hex"], CLAY, 16), result["palette"]["accents"])
        self.assertTrue(os.path.isfile(os.path.join(folder, "sheet-01.png")))
        with open(os.path.join(folder, "study.md"), encoding="utf-8") as handle:
            text = handle.read()
        self.assertIn("sheet-01 cell  3", text)
        self.assertNotIn("sheet-01 cell  4", text)

    def test_declared_cuts_set_the_drafts_shots_and_report_how_visible_each_is(self):
        out = self.study(self.film, "--draft", self.draft, "--draft-cuts", "1.5,3.0")
        with open(os.path.join(out, "draft", "study.json"), encoding="utf-8") as handle:
            draft = json.load(handle)
        self.assertEqual(draft["shots"]["count"], 3)
        self.assertEqual(draft["cuts"], [1.5, 3.0])
        self.assertEqual(len(draft["cut_strength"]), 2)
        self.assertLess(max(draft["cut_strength"]), 0.2)
        with open(os.path.join(out, "film", "study.json"), encoding="utf-8") as handle:
            self.assertIsNone(json.load(handle)["cut_strength"])

    def test_a_cut_declared_a_frame_late_still_reads_as_a_hard_cut(self):
        out = self.study(self.copy, "--draft", self.film, "--draft-cuts", "2.0333,4.0")
        with open(os.path.join(out, "film", "study.json"), encoding="utf-8") as handle:
            self.assertGreaterEqual(json.load(handle)["cut_strength"][0], 0.3)

    def test_length_comes_from_the_video_not_a_longer_audio_track(self):
        tail = encode(os.path.join(self.tmp, "tail.mp4"), [
            "-f", "lavfi", "-i", "testsrc2=s=160x90:r=30:d=2", "-f", "lavfi", "-i", "sine=d=3.5", "-c:a", "aac"])
        with open(os.path.join(self.study(tail), "tail", "study.json"), encoding="utf-8") as handle:
            result = json.load(handle)
        self.assertAlmostEqual(result["duration"], 2.0, delta=0.1)
        self.assertLessEqual(result["shots"]["final"], 2.1)

    def test_films_with_the_same_name_get_their_own_folders(self):
        twins = [os.path.join(self.tmp, side, "film.mp4") for side in ("left", "right")]
        for path in twins:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            shutil.copy(self.film, path)
        out = self.study(*twins)
        self.assertTrue(os.path.isfile(os.path.join(out, "film", "study.json")))
        self.assertTrue(os.path.isfile(os.path.join(out, "film-2", "study.json")))

    def test_refs_from_reuses_studies_already_measured(self):
        measured = self.study(self.film, self.copy)
        out = self.study("--refs-from", measured, "--draft", self.draft)
        with open(os.path.join(out, "board.md"), encoding="utf-8") as handle:
            board = handle.read()
        for name in ("film.mp4", "copy.mp4", "draft.mp4 (draft)"):
            self.assertIn(name, board)
        self.assertFalse(os.path.exists(os.path.join(out, "film")))

    def test_board_marks_where_the_draft_leaves_the_references_range(self):
        out = self.study(self.film, self.copy, "--draft", self.draft)
        with open(os.path.join(out, "board.md"), encoding="utf-8") as handle:
            text = handle.read()
        self.assertIn("draft.mp4 (draft)", text)
        rows = {line.split(" | ")[0].strip("| "): line for line in text.splitlines() if line.startswith("| ")}
        self.assertIn("outside", rows["cuts a minute"])
        self.assertNotIn("LUFS", rows)
        with open(os.path.join(out, "draft", "study.md"), encoding="utf-8") as handle:
            self.assertIn("Loudness: no audio track", handle.read())


if __name__ == "__main__":
    unittest.main()
