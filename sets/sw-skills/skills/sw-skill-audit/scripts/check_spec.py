#!/usr/bin/env python3
"""Compare the live Agent Skills specification with the copy the guidelines were written against.

Usage: check_spec.py [--snapshot <path>]

Prints one of:
  specification: unchanged
  specification: changed      followed by a unified diff, at most 60 lines
  specification: not checked (<reason>)

Exit code: 0 unchanged, 1 changed, 2 not checked. "Not checked" is never a
pass: without network access the guidelines may be out of date unnoticed.
Both texts are compared from their first top-level heading on, with trailing
whitespace removed; the copy is assets/spec-snapshot.md next to this script's
directory. Standard library only.
"""

import difflib
import os
import sys
import urllib.error
import urllib.request

SPEC_URL = "https://agentskills.io/specification.md"
DIFF_LINE_LIMIT = 60


def normalize(text):
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("# ")), 0)
    kept = [line.rstrip() for line in lines[start:]]
    while kept and not kept[-1]:
        kept.pop()
    return kept


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    snapshot = os.path.join(here, "..", "assets", "spec-snapshot.md")
    if argv[:1] == ["--snapshot"] and len(argv) == 2:
        snapshot = argv[1]
    elif argv:
        print("usage: check_spec.py [--snapshot <path>]", file=sys.stderr)
        return 2
    try:
        with open(snapshot, encoding="utf-8") as handle:
            expected = normalize(handle.read())
    except OSError as error:
        print(f"specification: not checked (cannot read the copy {snapshot}: {error.strerror})")
        return 2
    request = urllib.request.Request(SPEC_URL, headers={"User-Agent": "sw-skill-audit"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            live = normalize(response.read().decode("utf-8", errors="replace"))
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        reason = getattr(error, "reason", error)
        print(f"specification: not checked (cannot fetch {SPEC_URL}: {reason})")
        return 2
    except Exception as error:  # noqa: BLE001 - e.g. http.client.IncompleteRead
        print(f"specification: not checked (fetching {SPEC_URL} failed: {type(error).__name__})")
        return 2
    if live == expected:
        print("specification: unchanged")
        return 0
    print("specification: changed")
    diff = list(difflib.unified_diff(expected, live, "copy", "live", lineterm="", n=1))
    for line in diff[:DIFF_LINE_LIMIT]:
        print(line)
    if len(diff) > DIFF_LINE_LIMIT:
        print(f"... {len(diff) - DIFF_LINE_LIMIT} more diff lines")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
