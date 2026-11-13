---
name: sw-skill-audit
description: Audits an agent skill for its form, the quality of its instructions, the coherence of its procedure, and the files it ships, and reports findings with fixes. Use when a skill was created or changed, before a skill is committed, or when asked to audit a skill. Reports only; it does not edit the skill.
compatibility: Needs a harness that can start a subagent; without one it stops. Uses Python 3 for its bundled scripts and network access to agentskills.io for the specification check; without them it checks by reading and says what it could not check.
---

# Skill Audit

Audit one skill and report where it falls short of the
guidelines in this skill's `references/` and in the
`shared/` directory of the plugin it ships in. Report only: never
change a file of the audited skill. The requester decides
what to fix; an audit that fixes would end up checking its
own fixes. Keep any scratch file in the plugin's workspace,
never in the audited skill, where it would be audited with
it: run
`python3 <audit-dir>/../../shared/scripts/workspace.py --root <project> new-temp audit`,
which creates the workspace when it is missing and prints a
new directory in its `temp/`. When it prints
`created <path>` on stderr, it also wrote `.skill-works.json`
in `<project>`, a settings file that stays for the project to
commit: name it in the report header. Delete the directory
with `workspace.py --root <project> delete <dir>` before you
write the report, which must be your last message. If the
script fails or Python 3 is missing, write no scratch files,
say so in the report header, and do every check that would
need one by reading.

Below, `<audit-dir>` is the directory of this file: in
Claude Code `${CLAUDE_SKILL_DIR}`; in another harness, or if
the previous word shows no absolute path, the directory you
read this file from.

## Input

`$ARGUMENTS` — the path to the skill directory (the one that
holds `SKILL.md`), optionally followed by options. If no path
appears here, take the path and the options from the request
that started the audit.

- `--prefix <prefix>`: the name prefix to check (below).
- `--record <file>`: the record of a review cycle, in the
  shape of `<audit-dir>/../../shared/templates/review.md`. A
  finding that matches an entry of its Accepted section by
  item and quoted place is not reported; find the place by
  the quote, not by a line number.
- `--follow-up <diff>`: a follow-up pass instead of a full
  audit, on the diff in that file; needs `--record`. See
  "Follow-up Pass" below.

An unknown option, `--follow-up` without `--record`,
`--follow-up` with a record that has no Passes entry, or a
named file that does not exist: report that and stop.

The project is the directory the request names as the
project, else the repository root of the working directory
(`git rev-parse --show-toplevel`), else the working
directory. Its instructions are
the instruction files its harness loads: in Claude Code its
`CLAUDE.md` files and `.claude/rules/`, elsewhere for
example `AGENTS.md`. Its skill directories are the ones its
instructions name for its skills, and in Claude Code also
`.claude/skills/`. Its glossary is the file its instructions
name as one, if any; I5 checks the skill against it. If
that file is missing, say so in the report header and check
I5 without it.

- Without a path, or when the path holds no `SKILL.md`,
  report that and stop. Do not pick a skill yourself. A
  skill name counts as a path only when exactly one
  directory of that name with a `SKILL.md` lies under the
  project's skill directories.
- Only the auditor decides on a name prefix; the
  agent that starts it passes on a `--prefix` it was given
  and invents none. Check a prefix only for a skill that
  lies under the project's skill directories, wherever it
  came from. A skill outside them — a fixture, a third-party
  skill reviewed where it lies — gets no prefix check. Take
  the prefix from `--prefix`, else from the project's
  instructions.

## Fresh Context

The audit judges a skill by its files alone: what its
author meant but did not write is a finding, not a gap to
fill. That needs a context that has not seen how the skill
came about.

- If you were started as the auditor for this audit, go on
  with the Procedure.
- Otherwise, once Input has a valid skill directory, start a
  fresh subagent that does not inherit this conversation,
  with your harness's subagent tool: in Claude Code the Agent
  tool with the type `sw-workshop:sw-skill-auditor`; if the
  harness does not know that type, a fresh general subagent
  told to read `<audit-dir>/../../agents/sw-skill-auditor.md`
  (made absolute) first. Never use a fork, which would carry
  the conversation along. Give it the absolute path of this
  file, the absolute paths of the skill directory and the
  project, and every option of Input that was given, with
  absolute paths; tell it that it is the auditor and
  follows this whole file except this section. Relay its
  report unchanged.
- If your harness has no subagent tool, or the subagent
  returns no complete report, say so and stop. Do not run
  the audit in this conversation instead: an audit in the
  context that produced the skill is not independent.

## Procedure

Run every step, in this order. A clean result in one step
says nothing about the next: a skill with perfect form can
still contradict itself.

1. **List the skill.** List every file in the skill
   directory, and every file outside it that `SKILL.md`
   names by a path relative to the skill directory, such as
   a shared file of its plugin under `../../shared/`. An
   agent definition under `../../agents/` is not a file of
   the skill (F7). Project
   files the skill works on are not files of the skill.
2. **Run the form check.** Run
   `python3 <audit-dir>/scripts/check_form.py <skill-dir> [--prefix <prefix>]`.
   It ran if its output ends with a `summary:` line,
   whatever the exit code; exit 1 then only means it found a
   `fail`. Without that line it did not run: check every
   item in `<audit-dir>/references/form.md` by reading and
   record that in the report header. After a run, read
   `<audit-dir>/references/form.md`, judge the parts marked
   "by reading", and check by reading whatever the script
   reports as skipped. Done when every item of `form.md`
   this step checks by reading — every item if the script
   did not run — and every check the script reports as
   skipped, has a finding, holds, or has a reason it does not
   apply.
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
   of the skill into the kinds it describes. Read `SKILL.md` and every
   reference: a step in `SKILL.md` may be defined in a
   reference, and a contradiction often spans two files. Of
   each script, read the part that tells how to call it and
   what it prints — its docstring, header comment, or
   argument parsing — without running it, since a script
   may change files or call other systems and the audit
   only reports: steps 5 and 6 compare what `SKILL.md`
   says about the script with it. Done when every file of
   step 1 has a kind, and `SKILL.md`, every reference, and
   the usage part of every script have been read.
5. **Audit the instructions.** Read
   `<audit-dir>/../../shared/instructions.md` and
   `<audit-dir>/../../shared/instructions-skills.md`, and
   check `SKILL.md` and the references against each item of
   both. Done when every item has a finding, holds, or has a
   reason it does not apply.
6. **Audit the coherence.** Read
   `<audit-dir>/references/coherence.md`, build the
   procedure model it describes, and check the items as it
   directs. Done when the model has a row for every step and
   every item has a finding, holds, or has a reason it does
   not apply.
7. **Audit the shipped content and data.** Check shipped
   content against A1–A3 and data against A1 in
   `<audit-dir>/references/shipped.md`, and both against
   nothing else. Done when every file of these two kinds has
   been checked, or step 4 found none.
8. **Report** in the format below. The audit ends by
   returning the report: as your last message, which the
   agent or skill that started the audit receives and goes
   on from.

Carry every finding line of `check_form.py` — a line that
starts with `fail`, `warn` or `info` — into the report as
one entry, and give each `fail` and `warn` a fix. Keep its
item ID and grade it by the severity definitions below; the
script's severity is a proposal.

One cause can fall short of several items. Report a finding
under each item that gives a different reason for it; where
two items would give the same reason, report it once.

Before you report a finding, find the line that shows it
and cite it. For something missing, cite the line where it
belongs, or the file alone; for a finding cited by the file
alone, the place is the file's name in quotes, such as
`place: "SKILL.md"`. Write `unverified` after the
item ID of a finding you cannot point to; it still counts in
the scorecard.

No skill is exempt from this procedure, this one included.

## Follow-up Pass

With `--follow-up`, the audit checks a revision instead of
the whole skill. Read the record's last Passes entry: its
findings and the fixes made after it. Then run the procedure
above on this scope only:

- each fix the entry records: does it resolve the finding it
  targets? Report each earlier finding that a recorded fix
  targets as resolved or not resolved, with the place;
- new or changed text, as the diff shows it: check it
  against every item of the steps above;
- unchanged text: read it only where the changed text refers
  to it, and check it only against what the change touches.

Steps 1 and 3 run as in a full audit. Run the form check
(step 2) when the diff touches a file the script checks.
Steps 4 to 7 are done when every file and step the diff
touches, and what it refers to, has been read and checked;
show the procedure model when the diff changes a step;
otherwise write one line that it is unchanged. Name **churn**: a new finding that undoing a
fix recorded in any Passes entry would resolve; give the fix
it would undo.

## Report

Start with the skill's name and path, how the checks ran,
and a scorecard:

```
SKILL AUDIT: <name>  (<path>)
Specification  <unchanged | changed | not checked: reason>
Prefix         <the prefix checked | none: reason>
Form check     <script | by reading: reason>
Glossary       <path | none | missing: path>
Workspace      <path of its temp directory | created .skill-works.json | none: reason>
Pass           <full audit | follow-up pass: diff path>
Form           [N fail, N warn]
Instructions   [N fail, N warn]
Coherence      [N fail, N warn]
Shipped        [N fail, N warn]
```

For a skill with a procedure, add the procedure model from
`<audit-dir>/references/coherence.md` (in a follow-up pass,
as "Follow-up Pass" says). Then one entry per
finding, grouped by part:

```
<file>:<line>  <fail|warn|info>  <item, e.g. C4>
  place: "<a short quote of the cited text>"
  issue: <what falls short, in one sentence>
  fix:   <the concrete change>
```

A follow-up pass adds, before the entries, one line per
earlier finding that a recorded fix targets (`resolved` or
`not resolved`, with its item and place) and one line `Churn: <finding and the fix it
would undo>` or `Churn: none`.

- `fail` — the skill does not load, breaks the
  specification, or its procedure goes wrong: an unreachable
  step, a path without an end, a contradiction, lost state.
- `warn` — the skill departs from a guideline without
  breaking.
- `info` — worth knowing, not wrong.

The report is complete when it has the header and the
scorecard, the procedure model (or, in a follow-up pass,
the line that it is unchanged) if the skill has a procedure,
every entry, in a follow-up pass the lines on earlier
findings and churn, and its last part: ranked fixes or the
clean line. End with up to five of the most
important `fail` and `warn` fixes: `fail` before `warn`, and within one severity first
the fix that removes the most findings. A clean audit — no
`fail`, no `warn` — shows the header, the specification
diff and its note if step 3 printed `changed`, the
procedure model (or, in a follow-up pass, the line that it
is unchanged) if the skill has a procedure, in a follow-up
pass the lines on earlier findings and churn, any
`info` entries, and one line that says it is clean; it has
no ranked fixes.
