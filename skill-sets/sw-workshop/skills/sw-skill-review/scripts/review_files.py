#!/usr/bin/env python3
"""Keep the snapshot of a review cycle and write the diff against it.

The review directory is <temp>/<record name without .md>, where
<temp> is the temp/ directory of the workspace. It holds snapshot/:
a copy of the skill directory, and of the plugin's shared/ directory
when the skill's SKILL.md names a file under ../../shared/, as the
last recorded pass audited it. It holds no state; losing it only makes
the next pass a full audit.

Usage:
  review_files.py snapshot <review-dir> <skill-dir>
      Replace the snapshot with the current files, creating the review
      directory if it does not exist. Print the review directory.
  review_files.py diff <review-dir> <skill-dir>
      Write the unified diff from the snapshot to the current files
      into <review-dir>/diff.txt and print that path. Print "none" and
      write nothing when the review directory has no snapshot.

Exit codes: 0 done; 1 any other error, reason on stderr; 2 bad
arguments or a skill directory without SKILL.md.
"""
import difflib
import os
import shutil
import sys


def sources(skill_dir):
    """Map snapshot names to the directories they copy."""
    result = {"skill": skill_dir}
    with open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8") as handle:
        names_shared = "../../shared/" in handle.read()
    shared = os.path.normpath(os.path.join(skill_dir, "..", "..", "shared"))
    if names_shared and os.path.isdir(shared):
        result["shared"] = shared
    return result


def snapshot(review_dir, skill_dir):
    os.makedirs(review_dir, exist_ok=True)
    target = os.path.join(review_dir, "snapshot")
    fresh = target + ".new"
    shutil.rmtree(fresh, ignore_errors=True)
    os.makedirs(fresh)
    for name, path in sources(skill_dir).items():
        shutil.copytree(path, os.path.join(fresh, name))
    shutil.rmtree(target, ignore_errors=True)
    os.rename(fresh, target)
    return review_dir


def files_under(root):
    result = {}
    for folder, _, names in os.walk(root):
        for name in names:
            full = os.path.join(folder, name)
            result[os.path.relpath(full, root)] = full
    return result


def read_lines(path):
    if path is None:
        return []
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.readlines()
    except UnicodeDecodeError:
        return [f"<binary file {os.path.basename(path)}>\n"]


def diff(review_dir, skill_dir):
    base = os.path.join(review_dir, "snapshot")
    if not os.path.isdir(base):
        return None
    chunks = []
    for name, path in sources(skill_dir).items():
        old = files_under(os.path.join(base, name))
        new = files_under(path)
        for rel in sorted(set(old) | set(new)):
            label = f"{name}/{rel}"
            chunks.extend(difflib.unified_diff(
                read_lines(old.get(rel)), read_lines(new.get(rel)),
                fromfile="a/" + label, tofile="b/" + label))
    out = os.path.join(review_dir, "diff.txt")
    with open(out, "w", encoding="utf-8") as handle:
        handle.writelines(chunks)
    return out


def main(argv):
    if len(argv) != 3 or argv[0] not in ("snapshot", "diff"):
        print(__doc__, file=sys.stderr)
        return 2
    command, review_dir, skill_dir = argv[0], os.path.abspath(argv[1]), os.path.abspath(argv[2])
    if not os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
        print(f"error: no SKILL.md in {skill_dir}", file=sys.stderr)
        return 2
    try:
        if command == "snapshot":
            print(snapshot(review_dir, skill_dir))
        else:
            print(diff(review_dir, skill_dir) or "none")
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
