# D33: Temporary files

Status: accepted

## Decision

Sets also run outside skill-works, as plugins. So skills describe temporary files in general terms, never as a fixed path such as `/tmp`. A temporary file is one that only the skill reads and whose loss costs only work ([D54](D54-files-by-reader.md)). There are two kinds:

1. Scratch files for one run go into a new directory from the system's temp mechanism (`mktemp -d`, `tempfile.mkdtemp()`), or into the scratch directory that the harness names. The skill deletes it at the end of the run.
2. Helper files that must outlive one run but hold no state, such as a snapshot for a diff, go into a new directory from the system's temp mechanism with a fixed prefix and a random rest (`mktemp -d -t <skill>.XXXXXX`), never into the harness's scratch directory, which a new session does not see. A file in it names what it belongs to, so the agent finds it again. The skill says what it does when the directory is gone, and deletes it when it no longer needs it.

State never lives in a temp directory; it lives in a work document, the result, or a handed-in file ([D55](D55-no-flow-directory.md)).

Never write into the skill directory. Never write temporary files into the project tree.

This is check item I16 for all skills ([D29](D29-instruction-guideline-split-by-scope.md)).

## Reasons

- With a fixed prefix, the agent finds a helper directory again after a compaction from the `SKILL.md` alone. With a random rest, nobody can create the name in advance.
- A reboot can empty the temp facility (on Linux `/tmp` is often a tmpfs), so nothing a later step cannot do without may live there.
- An update replaces the skill directory, and an audit would read the file as part of the skill (F7).
- Temporary files in the project tree show in `git status` and can be committed by mistake.
- A fixed `/tmp` is missing on Windows. `mktemp` and `tempfile` follow a redirected `TMPDIR`; a fixed path does not.
