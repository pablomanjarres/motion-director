"""Tests for hf.sh with a stand-in npx that echoes what it was asked to run."""
import os
import shutil
import stat
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
WRAPPER = os.path.join(HERE, "hf.sh")
FAKE_NPX = """#!/bin/sh
echo "args: $*"
echo "env: $HYPERFRAMES_NO_TELEMETRY $DO_NOT_TRACK $HYPERFRAMES_SKIP_SKILLS $HYPERFRAMES_NO_UPDATE_CHECK $HYPERFRAMES_NO_AUTO_INSTALL"
"""


class HfWrapperTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="hf-wrapper-test-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        bin_dir = os.path.join(self.tmp, "bin")
        os.makedirs(bin_dir)
        npx = os.path.join(bin_dir, "npx")
        with open(npx, "w", encoding="utf-8") as handle:
            handle.write(FAKE_NPX)
        os.chmod(npx, os.stat(npx).st_mode | stat.S_IEXEC)
        self.project = os.path.join(self.tmp, "project")
        os.makedirs(self.project)
        self.env = dict(os.environ, PATH=bin_dir + os.pathsep + os.environ["PATH"])
        self.env.pop("HYPERFRAMES_VERSION", None)

    def run_hf(self, *args, **env):
        return subprocess.run(["bash", WRAPPER] + list(args), cwd=self.project, capture_output=True,
                              text=True, env=dict(self.env, **env))

    def test_refuses_commands_that_read_credentials_install_skills_or_send_data(self):
        for command in ("usage", "feedback", "events", "skills", "upgrade", "auth", "open",
                        "catch-up", "telemetry", "publish", "cloud", "lambda"):
            refused = self.run_hf(command, "--json")
            self.assertEqual(refused.returncode, 2, command)
            self.assertIn("refusing", refused.stderr)
            self.assertNotIn("args:", refused.stdout)

    def test_runs_the_pinned_cli_with_every_opt_out_set(self):
        ran = self.run_hf("render", "--quality", "draft")
        self.assertEqual(ran.returncode, 0, ran.stderr)
        self.assertIn("args: --yes hyperframes@0.8.144 render --quality draft", ran.stdout)
        self.assertIn("env: 1 1 1 1 1", ran.stdout)

    def test_a_project_pin_or_an_explicit_version_wins(self):
        with open(os.path.join(self.project, "package.json"), "w", encoding="utf-8") as handle:
            handle.write('{"scripts": {"render": "npx --yes hyperframes@0.8.120 render"}}')
        self.assertIn("hyperframes@0.8.120 check", self.run_hf("check").stdout)
        self.assertIn("hyperframes@0.9.0 check", self.run_hf("check", HYPERFRAMES_VERSION="0.9.0").stdout)


if __name__ == "__main__":
    unittest.main()
