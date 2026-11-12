# D33: Temporary files

Status: accepted

## Decision

Sets also run outside skill-works, as plugins. So skills describe temporary files in general terms, never as a fixed path such as `/tmp`. There are three kinds:

1. Scratch files for one run go into a new directory from the system's temp mechanism (`mktemp -d`, `tempfile.mkdtemp()`), or into the scratch directory that the harness names. The skill deletes it at the end.
2. State that must survive a compaction or a new session, and a hand-over to the next skill, goes into a new directory from the system's temp mechanism with a fixed prefix and a random rest (`mktemp -d -t <skill>.XXXXXX`), never into the harness's scratch directory, which a new session does not see. A file in it names what the state belongs to, so the agent finds it again. Item 2 was narrowed after the self-test of I16: at first it also allowed the harness's scratch directory.
3. Inside a set, a skill leaves only its result for good. At most it extends an artifact that comes in from outside ([D38](D38-skills-leave-only-their-result.md)).

What a seed passes on for good between sets is still open in the source: how a seed chains sets after one set leaves an artifact.

Never write into the skill directory. Never write scratch files into the project tree.

`sw-skill-audit` follows this itself from now on. Since step 5b, it is the check item I16 for all skills ([D29](D29-instruction-guideline-split-by-scope.md)).

## Reasons

- With a fixed prefix, the agent finds the state again after a compaction from the `SKILL.md` alone. With a random rest, nobody can create the name in advance.
- An update replaces the skill directory, and an audit would read the file as part of the skill (F7).
- Scratch files in the project tree show in `git status` and can be committed by mistake.
- A fixed `/tmp` is missing on Windows. `mktemp` and `tempfile` follow a redirected `TMPDIR`; a fixed path does not.
