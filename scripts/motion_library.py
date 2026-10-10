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

from library_index import find_skills, load_index, write_index

PHASES = ("brief", "direction", "storyboard", "engine", "build", "sound", "qa", "deliver", "web")
VERDICTS = ("SAFE", "SAFE-WITH-NOTES")
LICENSE_FILES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING")
JUNK = (".git", "node_modules", ".DS_Store", "__pycache__")
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
        template = source.get("template")
        if template is not None and not copy_rules_valid(template):
            raise ManifestError('%s: template takes "exclude" paths and {files, old, new} "edits"' % sid)
        source["skills"] = [normalize_skill(sid, entry) for entry in source.get("skills", [])]
        dirs = [skill["dir"] for skill in source["skills"]]
        if len(dirs) != len(set(dirs)):
            raise ManifestError('%s: two skills share a directory name; give one an "as"' % sid)
    for entry in manifest.get("excluded", []):
        if not (isinstance(entry.get("url"), str) and isinstance(entry.get("reason"), str)):
            raise ManifestError("each excluded entry needs a url and a reason")
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
    if not copy_rules_valid(skill):
        raise ManifestError('%s/%s: "exclude" takes paths and "edits" takes {files, old, new}' % (sid, name))
    return {"path": path, "dir": name, "phases": list(skill.get("phases", [])),
            "exclude": list(skill.get("exclude", [])), "edits": list(skill.get("edits", []))}


def copy_rules_valid(rules):
    return (all(isinstance(path, str) for path in rules.get("exclude", []))
            and all(set(edit) == {"files", "old", "new"} for edit in rules.get("edits", [])))


def copy_filter(base, excluded):
    """shutil.copytree ignore callback: drop junk plus `excluded` paths relative to `base`."""
    excluded = set(os.path.normpath(path) for path in excluded)

    def ignore(directory, names):
        rel = os.path.relpath(directory, base)
        return [name for name in names
                if name in JUNK or os.path.normpath(os.path.join(rel, name)) in excluded]
    return ignore


def apply_edits(root, edits, label):
    """Apply audited text edits under `root`; each must match exactly once or upstream changed."""
    for edit in edits:
        for rel in edit["files"]:
            path = os.path.join(root, rel)
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            if text.count(edit["old"]) != 1:
                raise InstallError("%s: expected exactly one %r in %s; re-audit before changing the pin"
                                   % (label, edit["old"], rel))
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text.replace(edit["old"], edit["new"]))


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
            copy = os.path.join(staging, skill["dir"])
            shutil.copytree(origin, copy, ignore=copy_filter(origin, skill["exclude"]))
            apply_edits(copy, skill["edits"], "%s/%s" % (source["id"], skill["dir"]))
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
    write_index(manifest, home)


def verify(manifest, home):
    problems = []
    for source in manifest["sources"]:
        head = head_of(os.path.join(home, "src", source["id"]))
        if head != source["sha"]:
            problems.append("%s: checkout at %s, pinned %s" % (source["id"], (head or "nothing")[:7], source["sha"][:7]))
        for skill in source["skills"]:
            if not os.path.isfile(os.path.join(home, "library", source["id"], skill["dir"], "SKILL.md")):
                problems.append("%s/%s: missing from the library" % (source["id"], skill["dir"]))
    index = load_index(home)
    if not index or index.get("manifest_digest") != manifest["digest"]:
        problems.append("index is missing or older than library.json")
    for problem in problems:
        print("stale: " + problem)
    if problems:
        print("run: python3 %s install" % os.path.abspath(__file__))
        return 1
    total = sum(len(source["skills"]) for source in manifest["sources"])
    print("ok: %d sources, %d skills at their pins in %s" % (len(manifest["sources"]), total, home))
    return 0


def where(home, query):
    index = load_index(home)
    if not index:
        print("no library at %s; run install first" % home, file=sys.stderr)
        return 1
    hits = find_skills(index, query)
    if len(hits) != 1:
        found = ", ".join(skill["id"] for skill in hits)
        print("ambiguous, pick one: " + found if hits else "no skill matches %r" % query, file=sys.stderr)
        return 1
    print(os.path.join(home, hits[0]["path"]))
    return 0


def outdated(manifest):
    moved = 0
    for source in manifest["sources"]:
        heads = git("ls-remote", source["url"], "HEAD").split()
        upstream = heads[0] if heads else "unknown"
        if upstream != source["sha"]:
            moved += 1
            print("%s: pinned %s, upstream HEAD %s (%s)" % (source["id"], source["sha"][:7], upstream[:7], source["url"]))
    if not moved:
        print("all %d sources still match upstream HEAD" % len(manifest["sources"]))
    return 1 if moved else 0


def scaffold(manifest, home, source_id, dest):
    """Start a project from a template source: copy its pinned checkout without .git and
    the template's excluded paths, then apply its audited edits, each matching exactly once."""
    source = next((s for s in manifest["sources"] if s["id"] == source_id), None)
    if not source or source.get("template") is None:
        raise InstallError("%s is not a template source in library.json" % source_id)
    checkout = os.path.join(home, "src", source_id)
    if head_of(checkout) != source["sha"]:
        raise InstallError("%s is not installed at its pin; run install first" % source_id)
    if os.path.lexists(dest):
        raise InstallError("%s already exists; scaffold into a new directory" % dest)
    template = source["template"]
    assert_contained(checkout, checkout)
    shutil.copytree(checkout, dest, ignore=copy_filter(checkout, template.get("exclude", [])))
    try:
        apply_edits(dest, template.get("edits", []), source_id)
    except Exception:
        shutil.rmtree(dest, ignore_errors=True)
        raise
    print("scaffolded %s @ %s into %s" % (source_id, source["sha"][:7], dest))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--home", default=None, help="library home (default: %s)" % default_home())
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("install", help="fetch pinned sources, rebuild the library, then verify")
    commands.add_parser("verify", help="exit 1 unless the library matches library.json")
    commands.add_parser("where", help="print the SKILL.md path for a skill").add_argument("query")
    commands.add_parser("outdated", help="list sources whose upstream moved past the pin")
    start = commands.add_parser("scaffold", help="start a new project from a template source")
    start.add_argument("source")
    start.add_argument("dest")
    args = parser.parse_args(argv)
    home = os.path.abspath(args.home or default_home())
    try:
        manifest = load_manifest(args.manifest)
    except (OSError, ValueError, ManifestError) as error:
        print("manifest error: %s" % error, file=sys.stderr)
        return 2
    try:
        if args.command == "install":
            install(manifest, home)
            return verify(manifest, home)
        if args.command == "verify":
            return verify(manifest, home)
        if args.command == "where":
            return where(home, args.query)
        if args.command == "scaffold":
            return scaffold(manifest, home, args.source, os.path.abspath(args.dest))
        return outdated(manifest)
    except (InstallError, OSError, shutil.Error) as error:
        print("install error: %s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
