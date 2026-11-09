---
name: sw-skill-audit
description: Audits an agent skill for its form, the quality of its instructions, the coherence of its procedure, and the files it ships, and reports findings with fixes. Use when a skill was created or changed, before a skill is committed, or when asked to audit, check, or review a skill. Reports only; it does not edit the skill.
compatibility: Needs a harness that can start a subagent; without one it stops. Uses Python 3 for its bundled scripts and network access to agentskills.io for the specification check; without them it checks by reading and says what it could not check.
---

# Skill Audit

Audit one skill and report where it falls short of the
guidelines in this skill's `references/`. Report only: never
change a file of the audited skill, and delete any scratch
file you create. The requester decides what to fix; an
audit that fixes would end up checking its own fixes.

Below, `<audit-dir>` is the directory of this file: in
Claude Code `${CLAUDE_SKILL_DIR}`; in another harness, or if
the previous word shows no absolute path, the directory you
read this file from.

## Input

`$ARGUMENTS` — the path to the skill directory (the one that
holds `SKILL.md`), optionally followed by `--prefix
<prefix>`. If no path appears here, take the path and the
option from the request that started the audit.

- Without a path, or when the path holds no `SKILL.md`,
  report that and stop. Do not pick a skill yourself.
- Check a name prefix only for a skill made in the project
  the audit runs in: one under the project's own skill
  directories (`.claude/skills/`, or the directories the
  project's instructions name for its skills). Take the
  prefix from `--prefix`, else from the project's
  instructions: `CLAUDE.md` and the project's rule files (in
  Claude Code, `.claude/rules/`). A skill from elsewhere — a
  fixture, a third-party skill under review — gets no prefix
  check.

## Fresh Context

The audit judges a skill by its files alone: what its
author meant but did not write is a finding, not a gap to
fill. That needs a context that has not seen how the skill
came about.

- If you were started as the subagent for this audit, go on
  with the Procedure.
- Otherwise, once Input has a valid skill directory, start a
  fresh subagent that does not inherit this conversation,
  with your harness's subagent tool. In Claude Code that is
  the Agent tool with a fresh agent type such as
  `general-purpose`, never a fork, which would carry the
  conversation along. Give it the absolute path of this
  file, the absolute path of the skill directory, and the
  prefix or that there is none; tell it that it is the audit
  subagent and follows this whole file except this section;
  relay its report unchanged.
- If your harness has no subagent tool, or the subagent
  returns no complete report, say so and stop. Do not run
  the audit in this conversation instead: an audit in the
  context that produced the skill is not independent.

## Procedure

Run every step, in this order. A clean result in one step
says nothing about the next: a skill with perfect form can
still contradict itself.

1. **List the skill.** List every file in the skill
   directory.
2. **Run the form check.** Run
   `python3 <audit-dir>/scripts/check_form.py <skill-dir> [--prefix <prefix>]`.
   It ran if its output ends with a `summary:` line,
   whatever the exit code; exit 1 then only means it found a
   `fail`. Without that line it did not run: check every
   item in `<audit-dir>/references/form.md` by reading and
   record that in the report header. After a run, read
   `<audit-dir>/references/form.md`, judge the parts marked
   "by reading", and check by reading whatever the script
   reports as skipped.
3. **Run the specification check.** Run
   `python3 <audit-dir>/scripts/check_spec.py`. It compares
   the live specification with
   `<audit-dir>/assets/spec-snapshot.md`, the copy the
   guidelines were written against, and prints
   `unchanged`, `changed` with a diff, or `not checked`
   with a reason. Put that result into the report header.
   If it prints none of these, write `not checked: the
   script did not run` with the error. On `changed`, write
   the diff under the header with the note that this
   audit's guidelines may be out of date; that note concerns
   the audit, not the audited skill, so it counts in no part
   and does not make the audit unclean. Never report `not
   checked` as unchanged.
4. **Sort and read the skill.** Read
   `<audit-dir>/references/shipped.md` and sort every file
   of the skill into references, scripts, shipped content,
   and data as it describes. Read `SKILL.md` and every
   reference: a step in `SKILL.md` may be defined in a
   reference, and a contradiction often spans two files.
5. **Audit the instructions.** Read
   `<audit-dir>/references/instructions.md` and check
   `SKILL.md` and the references against each item.
6. **Audit the coherence.** Read
   `<audit-dir>/references/coherence.md`, build the
   procedure model it describes, and check the items as it
   directs.
7. **Audit the shipped content.** Check shipped content
   against A1–A3 and data against A1 in
   `<audit-dir>/references/shipped.md`, and both against
   nothing else.
8. **Report** in the format below. The audit ends with the
   report.

Carry every finding line of `check_form.py` — a line that
starts with `fail`, `warn` or `info` — into the report as
one entry, and give each `fail` and `warn` a fix. Keep its
item ID and grade it by the severity definitions below; the
script's severity is a proposal.

One defect can fall short of several items. Report it under
each item that gives a different reason for it; where two
items would give the same reason, report it once.

Before you report a finding, find the line that shows it
and cite it. For something missing, cite the line where it
belongs, or the file alone. Write `unverified` after the
item ID of a finding you cannot point to; it still counts in
the scorecard.

No skill is exempt from this procedure, this one included.

## Report

Start with the skill's name and path, how the checks ran,
and a scorecard:

```
SKILL AUDIT: <name>  (<path>)
Specification  <unchanged | changed | not checked: reason>
Prefix         <the prefix checked | none: reason>
Form check     <script | by reading: reason>
Form           [N fail, N warn]
Instructions   [N fail, N warn]
Coherence      [N fail, N warn]
Shipped        [N fail, N warn]
```

For a skill with a procedure, add the procedure model from
`<audit-dir>/references/coherence.md`. Then one entry per
finding, grouped by part:

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

End with up to five of the most important fixes, ranked. A
clean audit — no `fail`, no `warn` — shows the header, the
procedure model, any `info` entries, and one line that says
it is clean; it has no ranked fixes.
