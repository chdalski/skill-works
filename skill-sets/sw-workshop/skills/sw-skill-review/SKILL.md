---
name: sw-skill-review
description: Reviews an agent skill, fixes what an audit finds, and puts the rest to the user. Changes the skill. Use when the user asks to review a skill.
compatibility: Needs a harness that can start a subagent, through the sw-skill-audit skill it runs, and Python 3 for its scripts.
---

# Skill Review

Run a review cycle on one skill: a full audit, fixes, and
follow-up passes on the diff, until a pass leaves no `fail`
and no `warn` open that you agree with; then the user decides
on the rest. The result is the reviewed skill, changed in
place, and the plugin's shared files where the user took a fix
to them. Commit nothing.

Below, `<review-dir>` is the directory of this file: in Claude
Code `${CLAUDE_SKILL_DIR}`; in another harness, or if the
previous word shows no absolute path, the directory you read
this file from. Read `<review-dir>/../../shared/terms.md`
first: this file uses its terms (record, pass, agreed finding,
held finding, churn, and the others) as defined there.

To ask the user anything, in this file or its references:
read `<review-dir>/../../shared/asking.md` first, then ask
with your harness's question tool, or in plain text if it has
none, and wait for the answer.

## Input

`$ARGUMENTS`, else the request that started you:

- the path of a draft whose header has `status: created` and
  whose skill directory holds a `SKILL.md`, from the skill
  that creates skills; its header names the skill
  (`target`, `skill`), `root`, the brief, the run mode, and the
  earlier record that is this cycle's reason, if any;
- or the path of a skill: a directory with a `SKILL.md`, not
  inside an installed copy of a plugin;
- or the path of a record: an open one resumes its cycle;
- optional, with a skill path only: `--new`, which starts a new
  cycle and closes the skill's open ones after confirmation.

A record handed back to sw-skill-design: decline and quote its
Final state, which names design's command. Anything else, or
`--new` without a skill path: decline with the reason and
stop. For an installed copy, ask for the skill's source in the
repository: a path given → start over with it; none → stop.

## The Record

The record, `<skill>-review.md` in `work/` of the workspace,
in the shape of `<review-dir>/../../shared/templates/review.md`,
is a work document and the cycle's only state: a resume reads
the record and nothing else. Never overwrite one. Find `temp/`, name
a new record, list open records, and delete only through
`python3 <review-dir>/../../shared/scripts/workspace.py --root <root> …`
(below `workspace.py`): `next-name <skill> review` names a new
record, `path temp` gives `temp/`, `delete <path> …` deletes;
inside the review directory, `review_files.py` works (Helper
Files).
`<root>` is the record's `root`; before a record exists, the
draft header's `root`, else the repository root of the
skill's directory. The first call creates the workspace and
`.skill-works.json` at `<root>` if they are missing; when the
script prints `created <path>` on stderr, tell the user that
the settings file was created and is meant to be committed.
A record is open while its `status` starts with `review:`; a
record handed back to sw-skill-design has
`status: handed-back`.

The cycle's work documents are the record, the record its
header names as `reason`, and the draft and the brief where
the record names a draft. They have no use once the user
accepted the reviewed skill in step 7: step 8 deletes those
of them that lie in the workspace. A file outside it is a
handed-in file and stays; name it to the user. A hand-back
keeps the record, the draft and the brief, since the flow
goes on in sw-skill-design; it deletes the record named as
`reason`, which this record replaces (Hand-back in
`references/decisions.md`).

Write each step's `status` to the header when the step starts,
with the pass it concerns: n = the pass count + 1 for steps 3
and 6. The pass count is the number of Passes entries with a
report. Write each user answer under Decisions, with the pass
count, before you act on it.

## Resume

Every resume of an open record — from a record path, from
the one open record step 2 finds, or after a compaction —
goes to the step the table below gives for its `status`.
After a compaction, read the record again (its path is in the
resume command you gave), `<review-dir>/../../shared/terms.md`,
the project's instructions at `root`. If you lost
the path, list the skill's open records with
`workspace.py open review review --field skill-path=<path>`:
exactly one → resume it; none or more → tell the user what
you found and ask for the record. Never open a cycle there.

| status | resume at |
|---|---|
| `review:auditing <n>`, `review:following-up <n>` | that step; if Passes has a report for pass n, write the snapshot and go to step 4 |
| `review:sorting`, `review:fixing`, `review:deciding`, `review:closing` | that step; fixes and decisions already in the record are not redone |

The resume command is the command that starts this skill with
the record's path (in Claude Code:
`/sw-workshop:sw-skill-review <record>`).

## Procedure

Run the steps in order. Each one ends at its "Done when".

1. **Check the input** against Input. Done when you have a
   draft, a skill path, or an open record, or have declined.
2. **Open the cycle.** An open record → resume it as the
   table under Resume says. Otherwise read
   `<review-dir>/references/open-cycle.md` and follow it. Done
   when the cycle's record is open, its `status` is set, and
   the user has its path and the resume command — or the step
   ended the run as that file says.
3. **Full audit.** First finish deleting every record the
   header lists under `closes` that still exists (see Closing
   in `<review-dir>/references/open-cycle.md`). Run
   the full audit as described under "Audit" with no
   `--follow-up`. Record the report under
   Passes, then write the snapshot. Done when Passes has the
   report.
4. **Sort.** Give every finding of the last pass an entry
   under Sorted:
   - **agreed**: you can cite the text that shows it, and the
     fix changes only text at the cited place: no input,
     result, gate, step order, file kind, or shared file, and
     it contradicts no decision in the brief, the draft, or the
     record;
   - **disputed**: you can cite the text that refutes it;
   - **trade-off**: any other `fail` or `warn`;
   - `info`: always held for the user.

   A finding reported again under the same item and quoted
   place updates its entry; it keeps an accepted or taken
   mark, and a dropped mark while it stays `info`. A finding
   the pass reports resolved gets the mark fixed; one it
   reports not resolved that is marked fixed gets the mark
   open again, with its sort kept; any other mark stays. Then: an
   agreed `fail` or `warn` open, the pass count below
   `stop-at`, and no churn in the last pass → 5; otherwise
   → 7. Done when every finding of the last pass has an entry.
5. **Fix** every agreed entry that is open and every entry
   marked taken, in the skill's files; change a shared file
   only for an entry marked taken. Record each fix under
   Passes with the finding it targets, and mark the entry
   fixed. Done when no agreed entry is open and no entry is
   marked taken.
6. **Follow-up pass.** No snapshot in the review directory →
   run step 3 instead, noted under Passes. Otherwise write the
   diff and run the audit as described under "Audit" with
   `--follow-up <diff>`. Record the report under Passes, then
   write the snapshot. Go to step 4. Done when Passes has the
   report.
7. **User decisions.** Read `<review-dir>/references/decisions.md`
   and follow it. Done when the run ended as that file says,
   or every open held or agreed entry has a mark other than
   open and a Decisions entry and the run went on to step 5,
   or to step 8 after the user accepted the reviewed skill.
8. **Close.** Only after the user accepted the reviewed skill
   in step 7. Give the user the summary: passes run, fixes,
   accepted findings, what is open, and how to see the
   changes, for example `git diff <paths>`. Then delete, with
   one `workspace.py delete` call in this order, those of the
   review directory, the brief, the draft, the record named
   as `reason`, and this record that lie in the workspace;
   name the others to the user as kept. Done when the user
   has the summary and the call printed its count.

## Audit

Start the skill `sw-workshop:sw-skill-audit` with your
harness's skill tool (in Claude Code: the Skill tool), with the
skill's path, `root` as the project, `--record <record>`,
`--draft <draft>` when `draft` names a file, and
`--follow-up <diff>` in a follow-up pass. It returns its report
to you; go on with this step when it has.

- `stop-at` is unset → set it to n + 5 (the full audit and 5
  follow-up passes) and write it under Decisions first.
- `draft` names a file that is missing → ask: go on
  without it (`draft: none`, under Decisions) or pause (give
  the resume command and stop).
- The audit stopped because the harness has no subagent tool
  → tell the user, give the resume command, and stop; the
  cycle goes on once a subagent tool is there.
- No complete report → start it once more; still none → tell
  the user, give the resume command, stop.

## Helper Files

The review directory is `<temp>/<record name without .md>`,
with `<temp>` from `workspace.py path temp`. It holds the
snapshot and the diff and nothing that counts as state. Use
`python3 <review-dir>/scripts/review_files.py`:
`snapshot <review directory> <skill-dir>` and
`diff <review directory> <skill-dir>`, which prints the diff's
path, or `none` without a snapshot.
A script that fails → tell the user, delete nothing, give the
resume command if this cycle's record exists, else the command
that starts this skill again with the same input, and stop.
