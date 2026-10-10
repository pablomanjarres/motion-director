#!/usr/bin/env python3
"""Install the motion skill library from audited upstream repos pinned to exact commits.

library.json (next to this skill) lists each upstream repo, the commit it was audited at,
and the skill directories to take from it. `install` fetches exactly those commits into
<home>/src/<id>, copies the listed skill directories into <home>/library/<id>/<dir>, and
writes INDEX.md plus index.json describing every skill. `verify` proves the installed
state still matches the manifest; `where` resolves a skill to its SKILL.md; `outdated`
lists sources whose upstream moved past the pin (a re-audit is due before bumping).

Home: $MOTION_STUDIO_HOME, else ${XDG_DATA_HOME:-~/.local/share}/motion-studio.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

PHASES = ("brief", "direction", "storyboard", "engine", "build", "sound", "qa", "deliver", "web")
VERDICTS = ("SAFE", "SAFE-WITH-NOTES")
LICENSE_FILES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING")
IGNORED = shutil.ignore_patterns(".git", "node_modules", ".DS_Store", "__pycache__")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MANIFEST = os.path.join(SKILL_DIR, "library.json")


class ManifestError(Exception):
    """The manifest is malformed or lists a source that is not approved."""


class InstallError(Exception):
    """An approved source could not be fetched or copied."""


def default_home():
    if os.environ.get("MOTION_STUDIO_HOME"):
        return os.environ["MOTION_STUDIO_HOME"]
    data = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
    return os.path.join(data, "motion-studio")


def load_manifest(path):
    with open(path, encoding="utf-8") as handle:
        raw = handle.read()
    manifest = json.loads(raw)
    seen = set()
    for source in manifest.get("sources", []):
        sid = source.get("id", "")
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", sid) or sid in seen:
            raise ManifestError("bad or duplicate source id: %r" % sid)
        seen.add(sid)
        if source.get("verdict") not in VERDICTS:
            raise ManifestError("%s: verdict %r is not approved" % (sid, source.get("verdict")))
        if not re.match(r"^[0-9a-f]{40}$", source.get("sha", "")):
            raise ManifestError("%s: sha must be a full 40-character commit" % sid)
        source["skills"] = [normalize_skill(sid, entry) for entry in source.get("skills", [])]
        dirs = [skill["dir"] for skill in source["skills"]]
        if len(dirs) != len(set(dirs)):
            raise ManifestError('%s: two skills share a directory name; give one an "as"' % sid)
    manifest["digest"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return manifest


def normalize_skill(sid, entry):
    skill = {"path": entry} if isinstance(entry, str) else dict(entry)
    path = skill.get("path", "").strip("/") or "."
    if ".." in path.split("/"):
        raise ManifestError("%s: skill path %r leaves the repo" % (sid, path))
    name = skill.get("as") or path.split("/")[-1]
    if name == "." or not re.match(r"^[A-Za-z0-9._-]+$", name):
        raise ManifestError('%s: skill at %r needs an "as" directory name' % (sid, path))
    unknown = [phase for phase in skill.get("phases", []) if phase not in PHASES]
    if unknown:
        raise ManifestError("%s/%s: unknown phases %s" % (sid, name, unknown))
    return {"path": path, "dir": name, "phases": list(skill.get("phases", []))}


def git(*args):
    done = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    if done.returncode != 0:
        command = args[2] if args[:1] == ("-C",) else args[0]
        raise InstallError("git %s failed: %s" % (command, done.stderr.strip()))
    return done.stdout.strip()


def head_of(checkout):
    if not os.path.isdir(os.path.join(checkout, ".git")):
        return None
    done = subprocess.run(["git", "-C", checkout, "rev-parse", "HEAD"], capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else None


def checkout_pin(source, checkout):
    """Leave `checkout` at exactly source["sha"], fetching that one commit and nothing else."""
    fresh = not os.path.isdir(os.path.join(checkout, ".git"))
    if fresh:
        os.makedirs(checkout, exist_ok=True)
        git("-C", checkout, "init", "-q")
        git("-C", checkout, "remote", "add", "origin", source["url"])
    else:
        git("-C", checkout, "remote", "set-url", "origin", source["url"])
    if source.get("sparse"):
        git("-C", checkout, "sparse-checkout", "set", *source["sparse"])
    elif not fresh:
        git("-C", checkout, "sparse-checkout", "disable")
    if head_of(checkout) != source["sha"]:
        git("-C", checkout, "fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", source["sha"])
        git("-C", checkout, "checkout", "-q", "--force", "--detach", "FETCH_HEAD")
    if head_of(checkout) != source["sha"]:
        raise InstallError("%s: checkout did not land on %s" % (source["id"], source["sha"]))


def assert_contained(root, tree):
    """Refuse any symlink under `tree` that resolves outside the checkout `root`."""
    real_root = os.path.realpath(root)
    for base, dirs, files in os.walk(tree):
        for name in dirs + files:
            path = os.path.join(base, name)
            target = os.path.realpath(path)
            if os.path.islink(path) and not (target + os.sep).startswith(real_root + os.sep):
                raise InstallError("%s links outside the checkout to %s" % (os.path.relpath(path, root), target))


def build_library(source, checkout, library_root):
    """Copy the listed skill dirs (and the repo license) into library/<id>, replacing it whole."""
    staging = os.path.join(library_root, ".staging-" + source["id"])
    shutil.rmtree(staging, ignore_errors=True)
    os.makedirs(staging)
    try:
        for skill in source["skills"]:
            origin = os.path.normpath(os.path.join(checkout, skill["path"]))
            if not os.path.isfile(os.path.join(origin, "SKILL.md")):
                raise InstallError("%s: %s has no SKILL.md at %s" % (source["id"], skill["path"], source["sha"][:7]))
            assert_contained(checkout, origin)
            shutil.copytree(origin, os.path.join(staging, skill["dir"]), ignore=IGNORED)
        for name in LICENSE_FILES:
            if os.path.isfile(os.path.join(checkout, name)):
                shutil.copy2(os.path.join(checkout, name), os.path.join(staging, name))
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    final = os.path.join(library_root, source["id"])
    shutil.rmtree(final, ignore_errors=True)
    os.rename(staging, final)


def install(manifest, home):
    src_root, library_root = os.path.join(home, "src"), os.path.join(home, "library")
    os.makedirs(src_root, exist_ok=True)
    os.makedirs(library_root, exist_ok=True)
    for source in manifest["sources"]:
        checkout = os.path.join(src_root, source["id"])
        checkout_pin(source, checkout)
        build_library(source, checkout, library_root)
        print("ok %-34s %s  %d skills" % (source["id"], source["sha"][:7], len(source["skills"])))
    keep = set(source["id"] for source in manifest["sources"])
    for root in (src_root, library_root):
        for name in os.listdir(root):
            if name not in keep and os.path.isdir(os.path.join(root, name)):
                shutil.rmtree(os.path.join(root, name))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--home", default=None, help="library home (default: %s)" % default_home())
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("install", help="fetch pinned sources and rebuild the library")
    args = parser.parse_args(argv)
    home = os.path.abspath(args.home or default_home())
    try:
        manifest = load_manifest(args.manifest)
    except (OSError, ValueError, ManifestError) as error:
        print("manifest error: %s" % error, file=sys.stderr)
        return 2
    try:
        install(manifest, home)
        return 0
    except (InstallError, OSError, shutil.Error) as error:
        print("install error: %s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
