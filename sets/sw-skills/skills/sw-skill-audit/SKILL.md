---
name: sw-skill-audit
description: Audits an agent skill for its form, the quality of its instructions, and the coherence of its procedure, and reports findings with fixes. Use when a skill was created or changed, before a skill is committed, or when asked to audit, check, or review a skill. Reports only; it does not edit the skill.
argument-hint: <skill-directory> [--prefix <name-prefix>]
compatibility: Designed for Claude Code. Runs scripts/check_form.py with Python 3 when available.
context: fork
background: false
---

# Skill Audit

Audit one skill and report where it falls short of the
guidelines in `references/`. Report only: never edit the
audited skill. The requester decides what to fix; an audit
that fixes would end up checking its own fixes.

You run in a fresh context and see none of the conversation
that produced the skill. Judge the skill by its files alone:
what its author meant but did not write is a finding, not a
gap for you to fill.

## Input

`$ARGUMENTS` — the path to the skill directory (the one that
holds `SKILL.md`), optionally followed by `--prefix <prefix>`.

- Without a path, or when the path holds no `SKILL.md`,
  report that and stop. Do not pick a skill yourself.
- Without `--prefix`, read the project's `CLAUDE.md`: if it
  requires a prefix for skills made in the project, use
  that prefix.

## Procedure

Run every step, in this order. A clean result in one step
says nothing about the next: a skill with perfect form can
still contradict itself.

1. **List the skill.** List every file in the skill
   directory.
2. **Check the form.** Run
   `python3 ${CLAUDE_SKILL_DIR}/scripts/check_form.py <skill-dir> [--prefix <prefix>]`
   — if `${CLAUDE_SKILL_DIR}` was not replaced by a path,
   use the directory this file lives in. Then read
   `references/form.md` and check the items the script does
   not cover. If Python 3 is missing or the script fails,
   check every item in `references/form.md` by reading, and
   say so in the report.
3. **Read the whole skill.** Read `SKILL.md` and every other
   text file in the skill directory. A step in `SKILL.md`
   may be defined in a reference file, and a contradiction
   often spans two files.
4. **Check the instructions.** Read
   `references/instructions.md` and check the skill against
   each item.
5. **Check the coherence.** Read `references/coherence.md`,
   build the procedure model it describes, then check each
   item.
6. **Report** in the format below. The audit ends with the
   report.

Before you report a finding, find the line that shows it
and cite it. Mark a finding you cannot point to as
`unverified`.

No skill is exempt from this procedure, this one included.

## Report

Start with the skill's name and path and a scorecard:

```
SKILL AUDIT: <name>  (<path>)
Form          [N fail, N warn]
Instructions  [N fail, N warn]
Coherence     [N fail, N warn]
```

For a skill with a procedure, add the procedure model from
`references/coherence.md`. Then one entry per finding,
grouped by part:

```
<file>:<line>  <fail|warn|info>  <item, e.g. C4>
  issue: <what falls short, in one sentence>
  fix:   <the concrete change>
```

- `fail` — the skill does not load, breaks the
  specification, or its procedure goes wrong: an unreachable
  step, a path without an end, a contradiction, lost state.
- `warn` — the skill departs from a guideline without
  breaking.
- `info` — worth knowing, not wrong.

End with the five most important fixes, ranked. A clean
audit ends after the scorecard with one line that says so.
