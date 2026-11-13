#!/usr/bin/env python3
"""Find, create, and clean the workspace of this plugin's skills.

The workspace is a directory in the project that holds work documents
(work/) and temporary files (temp/). Its name comes from the key
"directory" in .skill-works.json at the top of the project, else
".skill-works". It has its own .gitignore with "*". The top of the
project is the directory given with --root, else the top of the Git repository
of the working directory, else the working directory.

A work document is a Markdown file whose header is a YAML front matter
block: a first line "---", then "key: value" lines, then "---".

Usage (each command takes an optional --root <dir> first):
  workspace.py path work|temp
      Create whatever of the workspace is missing (.skill-works.json
      with the default, the directory, its .gitignore, work/, temp/)
      and print the absolute path of work/ or temp/.
  Every command that creates .skill-works.json says so on stderr:
  "created <path>".
  workspace.py new-temp <name>
      Create a new directory <name>.<random> in temp/ and print its
      absolute path.
  workspace.py next-name <name> <kind>
      Print a free path in work/: <name>-<kind>.md, or
      <name>-<kind>-<n>.md with the lowest free n from 2 on.
      Creates nothing but the workspace.
  workspace.py open <kind> <prefix> [--field KEY=VALUE ...]
      Print one line "<path>\\t<status>" per open work document of
      <kind> in work/: a file <something>-<kind>.md or
      <something>-<kind>-<n>.md whose header "status" starts with
      "<prefix>:" and holds every given KEY with exactly VALUE.
  workspace.py delete <path> [<path> ...]
      Delete the given files or directories, in the given order;
      a relative path is taken from the working directory, and a
      path that does not exist is skipped. Every path must lie
      inside the workspace; if one does not, delete nothing.
      Print "deleted <count>".

Exit codes: 0 done; 1 any other error, such as an unreadable or
wrong .skill-works.json, reason on stderr; 2 bad arguments, or a
'directory' outside the project; 3 a path outside the workspace,
nothing deleted.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CONFIG = ".skill-works.json"
DEFAULT_DIRECTORY = ".skill-works"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class UsageError(Exception):
    pass


ROOT = None


def project_root():
    if ROOT:
        return os.path.realpath(ROOT)
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        return os.path.realpath(out.stdout.strip())
    except (OSError, subprocess.CalledProcessError):
        return os.path.realpath(os.getcwd())


def workspace(create=True):
    root = project_root()
    config = os.path.join(root, CONFIG)
    if os.path.exists(config):
        with open(config, encoding="utf-8") as handle:
            settings = json.load(handle)
        if not isinstance(settings, dict):
            raise ValueError(f"{CONFIG} must hold a JSON object")
        directory = settings.get("directory", DEFAULT_DIRECTORY)
        if not isinstance(directory, str) or not directory:
            raise ValueError(f"{CONFIG}: 'directory' must be a non-empty string")
    else:
        directory = DEFAULT_DIRECTORY
        if create:
            with open(config, "w", encoding="utf-8") as handle:
                json.dump({"directory": DEFAULT_DIRECTORY}, handle, indent=2)
                handle.write("\n")
            print(f"created {config}", file=sys.stderr)
    path = os.path.realpath(os.path.join(root, directory))
    if not path.startswith(root + os.sep):
        raise UsageError(f"{CONFIG}: 'directory' must lie inside {root}")
    if create:
        for sub in ("work", "temp"):
            os.makedirs(os.path.join(path, sub), exist_ok=True)
        ignore = os.path.join(path, ".gitignore")
        if not os.path.exists(ignore):
            with open(ignore, "w", encoding="utf-8") as handle:
                handle.write("*\n")
    return path


def read_header(path):
    with open(path, encoding="utf-8") as handle:
        if handle.readline().rstrip("\n") != "---":
            return None
        fields = {}
        for line in handle:
            line = line.rstrip("\n")
            if line == "---":
                return fields
            key, sep, value = line.partition(":")
            if sep and key.strip() and not key.startswith(" "):
                fields[key.strip()] = value.strip().strip('"')
    return None


def cmd_path(args):
    if len(args) != 1 or args[0] not in ("work", "temp"):
        raise UsageError("path needs 'work' or 'temp'")
    print(os.path.join(workspace(), args[0]))


def cmd_new_temp(args):
    if len(args) != 1 or not NAME_RE.match(args[0]):
        raise UsageError("new-temp needs <name>: lowercase letters, digits, hyphens")
    temp = os.path.join(workspace(), "temp")
    print(tempfile.mkdtemp(prefix=args[0] + ".", dir=temp))


def cmd_next_name(args):
    if len(args) != 2 or not all(NAME_RE.match(a) for a in args):
        raise UsageError("next-name needs <name> <kind>: lowercase letters, digits, hyphens")
    name, kind = args
    work = os.path.join(workspace(), "work")
    path = os.path.join(work, f"{name}-{kind}.md")
    n = 2
    while os.path.exists(path):
        path = os.path.join(work, f"{name}-{kind}-{n}.md")
        n += 1
    print(path)


def cmd_open(args):
    if len(args) < 2:
        raise UsageError("open needs <kind> <prefix>")
    kind, prefix, rest = args[0], args[1], args[2:]
    wanted = []
    while rest:
        if rest[0] != "--field" or len(rest) < 2 or "=" not in rest[1]:
            raise UsageError("open takes only --field KEY=VALUE")
        key, _, value = rest[1].partition("=")
        wanted.append((key, value))
        rest = rest[2:]
    work = os.path.join(workspace(), "work")
    pattern = re.compile(rf"^.+-{re.escape(kind)}(-\d+)?\.md$")
    for entry in sorted(os.listdir(work)):
        path = os.path.join(work, entry)
        if not pattern.match(entry) or not os.path.isfile(path):
            continue
        try:
            fields = read_header(path)
        except (OSError, UnicodeDecodeError) as error:
            print(f"skipped {path}: {error}", file=sys.stderr)
            continue
        if fields is None:
            print(f"skipped {path}: no header", file=sys.stderr)
            continue
        status = fields.get("status", "")
        if status.startswith(prefix + ":") and all(
                fields.get(key) == value for key, value in wanted):
            print(f"{path}\t{status}")


def cmd_delete(args):
    if not args:
        raise UsageError("delete needs at least one path")
    base = workspace(create=False)
    targets = [os.path.realpath(path) for path in args]
    outside = [t for t in targets if not t.startswith(base + os.sep)]
    if outside:
        print(f"outside the workspace, nothing deleted: {', '.join(outside)}",
              file=sys.stderr)
        return 3
    count = 0
    for target in targets:
        if os.path.isdir(target):
            shutil.rmtree(target)
            count += 1
        elif os.path.exists(target):
            os.remove(target)
            count += 1
    print(f"deleted {count}")
    return 0


def main(argv):
    global ROOT
    if argv[:1] == ["--root"]:
        if len(argv) < 2 or not os.path.isdir(argv[1]):
            print("error: --root needs an existing directory", file=sys.stderr)
            return 2
        ROOT, argv = argv[1], argv[2:]
    commands = {"path": cmd_path, "new-temp": cmd_new_temp, "next-name": cmd_next_name,
                "open": cmd_open, "delete": cmd_delete}
    if not argv or argv[0] not in commands:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        return commands[argv[0]](argv[1:]) or 0
    except UsageError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
