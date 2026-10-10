"""Describe the installed motion library: INDEX.md for reading, index.json for lookups."""
import json
import os
import re


def read_frontmatter(path):
    """Return the top-level scalar fields of a SKILL.md YAML frontmatter block."""
    with open(path, encoding="utf-8", errors="replace") as handle:
        match = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(\r?\n|$)", handle.read(), re.S)
    fields, key, lines, style = {}, None, [], None
    if not match:
        return fields
    for line in match.group(1).splitlines() + ["__end__:"]:
        top = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if top:
            if key:
                fields[key] = fold(lines, style)
            key, value = top.group(1), top.group(2).strip()
            style = value[:1] if value[:1] in (">", "|") else None
            lines = [] if style else [value]
        elif key:
            lines.append(line.strip())
    fields.pop("__end__", None)
    return fields


def fold(lines, style):
    text = ("\n" if style == "|" else " ").join(line for line in lines if line).strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        text = text[1:-1].replace('\\"', '"') if text[0] == '"' else text[1:-1].replace("''", "'")
    return text


def cell(text, limit=240):
    text = " ".join(text.split())
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text.replace("|", "\\|")


def write_index(manifest, home):
    skills = []
    for source in manifest["sources"]:
        for skill in source["skills"]:
            rel = "/".join(("library", source["id"], skill["dir"], "SKILL.md"))
            meta = read_frontmatter(os.path.join(home, rel))
            skills.append({
                "id": source["id"] + "/" + skill["dir"], "name": meta.get("name") or skill["dir"],
                "description": meta.get("description", ""), "phases": skill["phases"],
                "source": source["id"], "path": rel,
            })
    with open(os.path.join(home, "index.json"), "w", encoding="utf-8") as handle:
        json.dump({"manifest_digest": manifest["digest"], "skills": skills}, handle, indent=1)
    lines = [
        "# Motion skill library", "",
        "Generated from library.json by motion_library.py; do not edit by hand.",
        "Every path below is relative to `%s`." % home, "",
    ]
    for source in manifest["sources"]:
        lines += ["## %s" % source["id"], "",
                  "%s @ `%s` · %s · %s · grade %s" % (source["url"], source["sha"][:7],
                                                     source.get("license", "unknown license"), source["verdict"],
                                                     source.get("grade", "unrated"))]
        if source.get("notes"):
            lines.append("Notes: " + source["notes"])
        lines += ["", "| skill | phases | use when |", "| --- | --- | --- |"]
        for skill in skills:
            if skill["source"] == source["id"]:
                lines.append("| `%s` | %s | %s |" % (skill["id"], ", ".join(skill["phases"]) or "-",
                                                    cell(skill["description"])))
        lines.append("")
    if manifest.get("excluded"):
        lines += ["## Excluded after review", "", "Not installed. Do not fetch these by hand.", ""]
        lines += ["- %s: %s" % (entry["url"], entry["reason"]) for entry in manifest["excluded"]]
        lines.append("")
    with open(os.path.join(home, "INDEX.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def load_index(home):
    try:
        with open(os.path.join(home, "index.json"), encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def find_skills(index, query):
    """Match a query against the full id, the directory name, or the frontmatter name."""
    return [skill for skill in index["skills"]
            if query in (skill["id"], skill["id"].split("/", 1)[1], skill["name"])]
