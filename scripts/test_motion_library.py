"""Hermetic tests for motion_library.py: a local git repo stands in for upstream."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "motion_library.py")


def git(cwd, *args):
    done = subprocess.run(["git", "-C", cwd] + list(args), check=True,
                          capture_output=True, text=True)
    return done.stdout.strip()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class MotionLibraryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="motion-library-test-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.upstream = os.path.join(self.tmp, "upstream")
        os.makedirs(self.upstream)
        git(self.upstream, "init", "-q", "-b", "main")
        git(self.upstream, "config", "user.email", "test@example.com")
        git(self.upstream, "config", "user.name", "test")
        git(self.upstream, "config", "uploadpack.allowFilter", "true")
        git(self.upstream, "config", "uploadpack.allowAnySHA1InWant", "true")
        write(self.up("skills/alpha/SKILL.md"),
              '---\nname: alpha-skill\ndescription: "Use when timing | easing matters"\n---\n# Alpha\n')
        write(self.up("skills/alpha/references/curves.md"), "curves\n")
        write(self.up("skills/beta/SKILL.md"),
              "---\nname: beta\ndescription: >\n  Use when the cut\n  needs sound.\n---\nBody\n")
        write(self.up("docs/notes.md"), "not a skill\n")
        self.sha1 = self.commit("first")
        self.home = os.path.join(self.tmp, "home")
        self.manifest = os.path.join(self.tmp, "library.json")
        self.write_manifest(self.sha1)

    def up(self, rel):
        return os.path.join(self.upstream, rel)

    def lib(self, *parts):
        return os.path.join(self.home, "library", "fixture", *parts)

    def commit(self, message):
        git(self.upstream, "add", "-A")
        git(self.upstream, "commit", "-q", "-m", message)
        return git(self.upstream, "rev-parse", "HEAD")

    def write_manifest(self, sha, **overrides):
        source = {
            "id": "fixture", "url": "file://" + self.upstream, "sha": sha,
            "license": "MIT", "verdict": "SAFE", "audited": "2026-10-10",
            "sparse": ["skills"],
            "skills": [{"path": "skills/alpha", "phases": ["direction", "build"]},
                       "skills/beta"],
        }
        source.update(overrides)
        with open(self.manifest, "w", encoding="utf-8") as handle:
            json.dump({"version": 1, "sources": [source]}, handle)

    def cli(self, *args):
        env = dict(os.environ, MOTION_STUDIO_HOME=self.home)
        return subprocess.run([sys.executable, SCRIPT, "--manifest", self.manifest] + list(args),
                              capture_output=True, text=True, env=env)

    def assertOk(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_install_builds_library_and_index(self):
        self.assertOk(self.cli("install"))
        self.assertTrue(os.path.isfile(self.lib("alpha", "SKILL.md")))
        self.assertTrue(os.path.isfile(self.lib("alpha", "references", "curves.md")))
        self.assertTrue(os.path.isfile(self.lib("beta", "SKILL.md")))
        self.assertFalse(os.path.exists(os.path.join(self.home, "src", "fixture", "docs")))
        with open(os.path.join(self.home, "index.json"), encoding="utf-8") as handle:
            skills = {s["id"]: s for s in json.load(handle)["skills"]}
        self.assertEqual(skills["fixture/alpha"]["name"], "alpha-skill")
        self.assertEqual(skills["fixture/alpha"]["description"], "Use when timing | easing matters")
        self.assertEqual(skills["fixture/alpha"]["phases"], ["direction", "build"])
        self.assertEqual(skills["fixture/beta"]["description"], "Use when the cut needs sound.")
        index_md = read(os.path.join(self.home, "INDEX.md"))
        self.assertIn("fixture/alpha", index_md)
        self.assertIn("timing \\| easing", index_md)
        self.assertOk(self.cli("verify"))
        self.assertOk(self.cli("install"))

    def test_verify_fails_until_new_pin_is_installed(self):
        self.assertOk(self.cli("install"))
        write(self.up("skills/beta/SKILL.md"), "---\nname: beta\ndescription: Use when v2.\n---\n")
        sha2 = self.commit("second")
        self.write_manifest(sha2)
        stale = self.cli("verify")
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("fixture", stale.stdout + stale.stderr)
        self.assertOk(self.cli("install"))
        self.assertOk(self.cli("verify"))
        self.assertEqual(git(os.path.join(self.home, "src", "fixture"), "rev-parse", "HEAD"), sha2)
        self.assertIn("v2", read(self.lib("beta", "SKILL.md")))

    def test_removed_skill_disappears_from_library(self):
        self.assertOk(self.cli("install"))
        self.write_manifest(self.sha1, skills=["skills/beta"])
        self.assertNotEqual(self.cli("verify").returncode, 0)
        self.assertOk(self.cli("install"))
        self.assertFalse(os.path.exists(self.lib("alpha")))
        self.assertTrue(os.path.isfile(self.lib("beta", "SKILL.md")))

    def test_rejects_unapproved_or_broken_manifest(self):
        self.write_manifest(self.sha1, verdict="REJECT")
        self.assertEqual(self.cli("install").returncode, 2)
        self.write_manifest(self.sha1, skills=[{"path": "skills/alpha", "phases": ["vibes"]}])
        self.assertEqual(self.cli("install").returncode, 2)
        self.write_manifest(self.sha1, skills=["skills/missing"])
        missing = self.cli("install")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("skills/missing", missing.stderr)

    def test_symlink_escaping_checkout_is_refused(self):
        os.symlink("/etc", self.up("skills/alpha/escape"))
        self.write_manifest(self.commit("link"))
        refused = self.cli("install")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("escape", refused.stderr)
        self.assertFalse(os.path.exists(self.lib("alpha", "escape")))

    def test_where_resolves_ids_dir_names_and_skill_names(self):
        self.assertOk(self.cli("install"))
        expected = self.lib("alpha", "SKILL.md")
        for query in ("fixture/alpha", "alpha", "alpha-skill"):
            found = self.cli("where", query)
            self.assertOk(found)
            self.assertEqual(found.stdout.strip(), expected)
        self.assertNotEqual(self.cli("where", "nope").returncode, 0)

    def test_outdated_reports_moved_upstream(self):
        self.assertOk(self.cli("install"))
        current = self.cli("outdated")
        self.assertOk(current)
        self.assertNotIn("fixture", current.stdout)
        write(self.up("skills/alpha/SKILL.md"), "---\nname: alpha-skill\ndescription: Use when moved.\n---\n")
        self.commit("moved")
        moved = self.cli("outdated")
        self.assertEqual(moved.returncode, 1)
        self.assertIn("fixture", moved.stdout)


if __name__ == "__main__":
    unittest.main()
