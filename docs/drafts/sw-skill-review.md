# Draft: sw-skill-review

Status: draft 12, ACCEPTED by the user with its six assumptions

## Purpose and trigger

Runs the review cycle on one skill: a full audit, fixes, and
follow-up passes on the diff, until a pass leaves no `fail`
and no `warn` the agent agrees with; then the user decides on
the rest. Last chain link of the skill flow of `sw-workshop`
(brainstorm → design → create → review); also started alone,
on a user's request, for example after a change by hand.
Changes the reviewed skill; that is its result.

Description (draft, I10 with its four rules, I11): "Reviews an
agent skill, fixes what an audit finds, and puts the rest to
the user. Changes the skill. Use when the user asks to review
a skill."

No user-only flag: sw-skill-create starts it by name in run
mode "straight through" (D41), so the description needs no
trigger for that case. The trigger names only a request, so a
hand edit does not start a cycle that changes files.

## Inputs

- The path of a draft whose header has `status: created`,
  from sw-skill-create. Its header names the skill (`target`,
  `skill`), `root`, the brief, the run mode, and, after a
  hand-back, the earlier record that is the new cycle's
  reason.
- Or, started alone, the path of a skill: a directory with a
  `SKILL.md`. A path inside the installed copy of a plugin →
  decline and ask for its source.
- Or the path of a record: an open one resumes its cycle; a
  closed one is declined with its Final state, which names
  what follows, if anything. Every resume command the review gives names
  the record.
- Optional, with a skill path only: `--new` starts a new cycle
  and closes the open ones for that skill, after confirmation.
- Anything else → decline with the reason.

## Result

The reviewed skill, changed in place, and the plugin's shared
files where the user took a fix to them (step 7). No commit.
A fix to a shared file changes the plugin's other skills too,
so it is always held for the user (step 4).

## The record

The record, `<skill>-review.md` in the work-document
directory, from `shared/templates/review.md`, is a work
document (D54) and holds the whole state of one cycle (C5,
D55): a resume reads the record and nothing else. It belongs
to the user and is never overwritten: when the name is taken,
the record is `<skill>-review-<n>.md` with the lowest free
`n`. A record is open as `shared/terms.md` defines an open
work document: its `status` starts with `review:`. Every exit
that writes a Final state also writes `status: closed`, in
the same edit. `docs` below is the work-document directory
of `shared/terms.md`; started on a skill path, it is the one
the project's instructions name, else the review asks; on a
resume, it is the record's directory. The template is shared because sw-skill-audit and
sw-skill-design read the record too (D43).

Sections:

- Header: `skill-path` (the skill's absolute path), `root`, the draft's path
  or "none", the earlier record that is its reason or "none",
  the records it closes or "none", `stop-at` (the pass after
  which the audit loop stops for the user), and `status` with
  the number of the pass it concerns.
- Passes: one entry per pass — full audit or follow-up pass
  and why; the audit's findings, condensed (item, quoted
  place, grade, issue, fix); churn, if named; then the fixes
  made after it, each with the finding it targets. The pass
  count is the number of entries with a report.
- Sorted: one entry per finding — the pass it came from, its
  sort (agreed, disputed, trade-off, `info`), the reason, and
  a mark: open, fixed, taken, accepted, or dropped. A finding
  that a later pass reports again under the same item and
  quoted place updates its entry; it keeps an accepted or
  taken mark, and a dropped mark while its grade stays
  `info`. A finding a follow-up pass reports resolved gets the
  mark fixed.
- Accepted: item, quoted place, reason.
- Decisions: each user decision and each change of `stop-at`
  or `draft`, each with the pass count at its time.
- Final state: passes run, fixes, accepted findings, what is
  open, how to see the changes (for example `git diff
  <paths>`); or "abandoned", "superseded by <record>",
  "stopped: <reason>", or "handed back to sw-skill-design"
  with the command that starts it with this record; each with
  how to see the changes and what follows, if anything.

The brief and the run mode are read from the draft's header
when the record names a draft; the record does not copy them.

## Terms

Workshop terms come from `shared/terms.md` (I17), which this
skill shares with sw-skill-brainstorm: flow, work document,
work-document directory, open work document, installed copy,
hand-over, run mode, sub-skill, review cycle, record, pass,
full audit, follow-up pass, finding (`fail`, `warn`, `info`),
agreed finding, held finding (disputed, trade-off, `info`),
accepted finding, churn, audit loop, snapshot.

## Temporary files

The review hands nothing on through a temp directory (D55).
Its own helpers (I16):

- **Review directory**: a helper directory with the prefix
  `sw-skill-review.` (`mktemp -d -t sw-skill-review.XXXXXX`),
  holding `record.txt` (the record's absolute path) and
  `snapshot/`: a copy of the skill directory, and of the
  plugin's `shared/` directory where `SKILL.md` names files in
  it, as the last recorded pass audited it. Found by listing
  the prefix and matching `record.txt`; more than one match →
  the newest is kept, the others are deleted. It holds no
  state: none found → the next pass is a full audit, which
  counts as a pass and is noted under Passes. Deleted before
  the record gets its Final state, so a crash in between
  leaves an open record, not a stray directory.
- **Scratch**: the diff goes into a new temp directory,
  deleted when step 6 ends, on every exit.

The deterministic work runs in scripts: the next free record
name and the open records in `../../shared/scripts/work_documents.py`,
the review directory, the snapshot and the diff in
`scripts/review_files.py`. A script that fails → tell
the user, give the resume command if a record exists, else
the command that starts the review again with the same input;
end.

## Status values and resume

Each step writes `status` to the record's header when it
starts, with the pass it concerns: n = the pass count + 1 for
steps 3 and 6.

| status | written by | resume at |
|---|---|---|
| `review:auditing <n>` | step 2 (a new cycle), step 3 | step 3; if Passes has a report for pass n, write the snapshot and go to step 4 |
| `review:sorting` | step 4 | step 4 |
| `review:fixing` | step 5 | step 5; fixes already in the record are not redone |
| `review:following-up <n>` | step 6 | step 6; if Passes has a report for pass n, write the snapshot and go to step 4 |
| `review:deciding` | step 7 | step 7; decided items stay decided |
| `review:closing` | step 8 | step 8 |
| `closed` | every exit that writes Final state | not resumed: the Final state says what follows, if anything |

A step that runs a pass records the report first and writes
the snapshot after it, so a retry or a resume diffs against
the state the last recorded pass audited, and a pass is never
counted twice: the count comes from Passes.

Every exit that ends a cycle, and every closing of another
cycle, names the work documents that remain: the record, and
the draft and the brief where the record names a draft.

## Procedure model

The audit loop repeats and step 7 waits for the user, so the
state lives outside the conversation, in the record. Step 2
ends by giving the user the record's path and the resume
command. After a compaction the agent reads the record (its
path is in that command), `../../shared/terms.md`, the
project's instructions at `root`, and, before it asks,
`../../shared/asking.md` again. If the path is lost, it looks
for the open records of the skill in `docs` (see The record):
exactly one → it resumes that record; none or more than one →
it tells the user what it found and asks for the record. It
never opens a cycle there.

| Step | Entry | Exits | Reads / writes | Actor |
|---|---|---|---|---|
| 1 Check the input | start | a draft with `status: created` whose skill path exists, a skill path that exists and is no installed copy, or an open record → 2; a closed record → decline and quote its Final state; when it names nothing that follows, say that a start on the skill path resumes the skill's open record or, with none, begins a new cycle; end; a draft with another status, anything else, or `--new` without a skill path → decline with the reason, end; done when the input is known and checked | input; reads `../../shared/terms.md` first | agent |
| 2 Open the cycle | from 1 | **An open record** → the step its `status` names. **Otherwise find `docs`** (see The record). **(a) Open records** of this skill in `docs`, from `../../shared/scripts/work_documents.py`; a record that another open record's header closes counts as closed (finish closing it as in (c)). *Handed a draft:* an open record that names this draft and has no report under Passes → it is this cycle → the step its `status` names; other open records → ask once: close them and start the new cycle, resume the one that names this draft (only when exactly one does; its findings may be stale if the draft changed since), or stop (→ end, with the command that hands the draft in again); none → (c). *Skill path without `--new`:* none → (b); one → resume it (→ the step its `status` names), telling the user which record and that `--new` starts a new cycle; more than one → list them and ask which goes on, saying the others will be closed; they are closed with the answer (their review directories deleted, then "abandoned" and `status: closed`). *Skill path with `--new`:* open records → ask to confirm closing them (a "no" ends) → (b); none → (b). **(b) Version control,** for a new cycle on a skill path only: uncommitted changes in the skill's directory or in the shared files its `SKILL.md` names, or no version control → ask: go on (the review's fixes then mix with those changes) or stop to commit first (→ end; nothing has changed). **(c) A new cycle** → 3. Done when the cycle's record is open, its `status` is set, and the user has its path and the resume command | reads `asking.md` before asking. (c): `draft` = the handed-in draft; else, with `--new` and exactly one record to close, that record's draft; else none, and with two or more records to close the user is told that the new cycle runs without a draft; writes the new record (header: `skill-path`, `root` from the draft's header, else the repository root of the skill's directory, else that directory; `draft`; the reason from the draft's header; the records it closes; `stop-at` unset; `status: review:auditing 1`); then, for each record its header closes, deletes that record's review directory and writes "superseded by <new record>" under its Final state and `status: closed` | agent, user |
| 3 Full audit | from 2 or 6 | complete report recorded → 4; the audit stopped because the harness has no subagent tool → delete the review directory, write "stopped: no subagent tool" under Final state and `status: closed`, tell the user, end; no complete report otherwise → retry once, then tell the user, give the resume command, end; done when Passes has the report | `status: review:auditing <n>`; records the header closes that still have no Final state → close them as in step 2 (c); `stop-at` unset → n + 5 (the full audit and 5 follow-up passes), under Decisions; `draft` names a file that is missing → ask: go on without it (`draft: none`, under Decisions) or pause (give the resume command, end), reading `asking.md` first; starts the sub-skill sw-skill-audit on the skill with `root` as the project, `--record <record>`, and `--draft <draft>` when `draft` names a file; records the report under Passes, then writes the snapshot (creating the review directory if none names this record) | sw-skill-audit |
| 4 Sort | from 3 or 6 | an agreed `fail` or `warn` open, the pass count < `stop-at`, no churn in the last pass → 5; agreed ones open and the count ≥ `stop-at`, or churn in the last pass → 7; no agreed one open → 7; done when every finding of the last pass has an entry under Sorted | `status: review:sorting`; agreed: the agent can cite the text that shows it, and the fix changes only text at the cited place, no input, result, gate, step order, file kind or shared file, and contradicts no decision in the brief, the draft or the record; disputed: the agent can cite the text that refutes it; trade-off: any other `fail` or `warn`; `info` is always held | agent |
| 5 Fix | from 4 or 7 | done when every open agreed or taken finding is fixed and marked → 6 | `status: review:fixing`; changes the skill's files (shared files only where taken); records each fix under Passes with the finding it targets | agent |
| 6 Follow-up pass | from 5 | no review directory for this record → step 3's audit and exits instead, noted under Passes; complete report recorded → 4; failure exits as in step 3; done when Passes has the report and the scratch directory is deleted | `status: review:following-up <n>`; writes the diff from the snapshot to the current files into a scratch directory; starts sw-skill-audit with `root`, `--record <record>`, `--follow-up <diff>`, and `--draft` as in step 3; records the report under Passes, then replaces the snapshot with the audited files; deletes the scratch directory on every exit | sw-skill-audit |
| 7 User decisions | from 4 | **Agreed entries open** (the limit or churn stopped the loop) → first one question naming them and why the loop stopped (from Passes): go on fixing all (→ taken), decide each, or back to sw-skill-design (only when `draft` names a file); skipped when Decisions has one of its three answers (go on fixing all, decide each, back to sw-skill-design) at the current pass count; then that answer applies (back to sw-skill-design → the hand-back below; go on fixing all → taken). Each of these three answers is written under Decisions before the step acts on it. **Then one question per item:** `info`: take or drop; disputed, trade-off, or an agreed entry to decide: take, or accept with a reason. **At any question:** pause → give the resume command, end; abandon → after confirmation (a "no" returns to the question) delete the review directory, write "abandoned" under Final state and `status: closed`, end. Nothing to decide → 8, telling the user the last pass was clean. Done when every item has a mark and a Decisions entry → something taken → 5; nothing taken → 8. **Back to design** → delete the review directory; write under Final state "handed back to sw-skill-design" with the command that starts it with this record, and `status: closed`; print that command; the draft header's mode "straight through" → start sw-skill-design with the record's path; end | `status: review:deciding`; reads `asking.md`; opens with the number of items and one line each; asks only on open entries: `info`, disputed, trade-off and agreed; each with the finding, the proposed fix and a recommendation; each answer under Decisions with the pass count; something taken → `stop-at` = the pass count + 5, under Decisions | user |
| 8 Close | from 7 | done when the review directory is deleted, Final state and `status: closed` are written, and the user has the summary → end | `status: review:closing`; deletes the review directory, then writes Final state and `status: closed`; names the work documents that remain; deletes no work document | agent |

## Gates

- A pass that leaves no agreed `fail` or `warn` open ends the
  audit loop (D32, one auditor per pass). One clean follow-up pass suffices: it
  checks the diff and the recorded fixes, and the earlier
  passes checked the rest.
- Step 7: the user decides on every held finding, on findings
  to accept, and on what happens at the limit or on churn.

## Loops and limits

- Audit loop (4 → 5 → 6 → 4): runs on its own (D41) until no
  agreed finding is open, churn is named, or the pass count
  reaches `stop-at`: 5 follow-up passes after the full audit,
  or after the last decision that took something.
- User decisions (7 → 5 → 6 → 4 → 7): each round needs a user
  decision, so the user ends it.
- After a hand-back, design revises the draft, create the
  skill, and create hands the draft in again: a new cycle with
  its own record, which names the earlier one as its reason.
  Accepted findings do not carry over (D32).

## Hand-over

- To sw-skill-audit, a sub-skill (D42): the skill's path,
  `root` as the project, and the flags above; it returns its
  report and starts nothing further.
- Back to sw-skill-design (step 7, only with a draft): the
  record's path, also written as a command into the record's
  Final state, so a stopped start can be redone by hand. The
  review does not track whether design received it. Design
  takes the draft's path from the record, writes the record
  into the draft's header as the reason, keeps the draft's
  other header fields, and then revises the draft.
- Otherwise the review ends the flow.

## Files

- `skills/sw-skill-review/SKILL.md`; the sort rules of step 4
  stay in it, since every path passes them.
- `skills/sw-skill-review/scripts/review_files.py`: finding
  the review directory, snapshot, diff; prints only what the
  step needs.
- `shared/templates/review.md`.
- `shared/terms.md`, `shared/harness-phrases.md`.

## Needs outside this skill

- sw-skill-audit:
  - `--record <file>`: a finding that matches an Accepted
    entry by item and quoted place is not reported; the audit
    finds the place by the quote, not by a line number. It
    names `shared/templates/review.md`.
  - `--follow-up <diff>` (needs `--record`): a follow-up pass.
    It checks each fix recorded in the last Passes entry
    against the finding it targets, and each other finding of
    the last pass for whether it is resolved; checks new or
    changed text against every item; and reads unchanged text
    only where the changed text refers to it. It names churn:
    a new finding that undoing a fix recorded under Passes
    would resolve.
  - The Fresh Context section forwards these flags and the
    project to the subagent; today it forwards only
    `--prefix`.
  - A defined complete report, including for a follow-up pass:
    the header, a line per earlier finding (resolved or not),
    the new findings, and churn.
  - Started by another skill, it returns the report to that
    skill, which goes on.
  - It starts `sw-workshop:sw-skill-auditor`, a new agent
    definition (D27); a harness that does not know that type
    gets a fresh general subagent told to read the definition
    first, as sw-skill-brainstorm does for its advisor.
  - `--draft` comes with sw-skill-design.

  These changes get one review cycle on sw-skill-audit.
- The draft's header (template `shared/templates/draft.md`)
  carries `target`, `skill`, `root`, `brief`, `mode`,
  `status`, create's answer about earlier changes, and the
  earlier record as the reason after a hand-back (D55).
- sw-skill-create writes `status: created` into the draft's
  header and hands the draft's path over. Before it changes an
  existing skill with changes made before the flow started, it
  asks once per flow and keeps the answer in the draft's
  header, so a hand-back does not ask again about the flow's
  own changes.
- sw-skill-design takes a record's path as a hand-back, in
  the order Hand-over gives, and names
  `shared/templates/review.md`.
- `shared/scripts/work_documents.py` (shared with
  sw-skill-brainstorm) gives the next free record name and the
  open records of a skill. It matches the skill by its
  absolute path: `skill-path` in a record's header, or
  `target` and `skill` in a brief's or a draft's header.
  `review_files.py` keeps only the review directory, the
  snapshot and the diff.
- The glossary gets "audit loop", "record", "pass", "full
  audit", "agreed finding", "held finding" and "snapshot".

## Writing notes for sw-skill-create

- Each step's "done when" in Exits becomes its "Done when"
  line (I18).
- D-numbers are for the author only (I17).
- Phrase sites (D48): start a sub-skill (steps 3, 6), ask the
  user (steps 2, 3, 7), create a temp directory (steps 3, 6),
  give the resume command with the record's path (steps 2, 3,
  6, 7, and a script failure), start another skill or name
  its command (step 7), recognize the installed copy of a
  plugin (step 1).
- `compatibility`: needs a harness that can start a subagent,
  through sw-skill-audit, and Python 3 for its script.

## Assumptions to confirm

1. The record of a cycle is a work document the user keeps,
   and it is the cycle's only state. Each cycle has its own
   record, also the one after a hand-back to design, and does
   not carry the earlier cycle's accepted findings. The
   snapshot is the only helper file; it holds no state, and
   losing it turns the next pass into a full audit.
2. Limits: the audit loop stops for the user after 5 follow-up
   passes, counted from the full audit or from the last
   decision that took something; churn stops it early. The
   longest self-test series needed 4.
3. Agreed findings are fixed without asking, by the rule in
   step 4; everything else is held for the user.
4. A new cycle started on a skill path asks first when the
   skill has uncommitted changes or no version control; from
   sw-skill-create it does not ask, since all changes are then
   the flow's, and create asks before it changes such a skill.
5. One open cycle per skill. A start on the skill path resumes
   the one open record without a question and says so; a new
   cycle while one is open needs `--new`, which closes the open
   ones after one confirmation. The resume command names the
   record.
6. The review does not follow up a hand-back to design: it
   writes design's command into the record's Final state,
   prints it, and in run mode "straight through" starts
   design. If that start stops, the user runs the command from
   the record. A review started by hand before create hands the draft in
   again runs as its own cycle; create may later change its
   fixes without asking.
