# Draft: sw-skill-brainstorm

Status: draft 12, ACCEPTED by the user with its six assumptions (rebuilt on D54 and D55 from draft 6)

## Purpose and trigger

Clarifies the idea for a new skill, or for a change to a
skill's purpose, trigger, input or result, before any
procedure is designed. It settles what the skill is for, when
it triggers, what it delivers, where it will live, and whether
a skill is needed at all. Entry skill of the skill flow of
`sw-workshop`: brainstorm → design → create → review. A change
that only alters how a skill's steps work goes straight to
sw-skill-design (step 2 exits there). Runs in any repository
and knows nothing of how a project organizes its skills
beyond what the harness loads and what the project's
instructions say (D46).

Note for the author, not for SKILL.md: the skill text says
"skills directory" and "plugin", never "skill set" — that is
skill-works' word, which another project does not know. Which
conventions a new skill follows (a name prefix, shared files,
a license file) comes from the project's instructions.

Description (draft, I10 with its four rules, I11):
"Clarifies the idea for a new agent skill, or for a change to
a skill's purpose, trigger, input or result, checks whether
the skill is needed at all, and writes a brief for
sw-skill-design. Use when the user asks for a new skill or
for such a change; not for changing how a skill's steps
work."

No user-only flag (D41): a seed may route a user's request
here, and sw-skill-design points users to it.

## Inputs

- The user's wish, from the request or the conversation.
  Missing → step 1 asks for it before it creates the brief.
- Optional `--mode step|through`, the run modes "step by
  step" and "straight through" of the glossary. Missing →
  step 1 asks.
- Optional: the path of a skill to change: a directory with a
  `SKILL.md`. It pre-fills `skill`, `target` and
  `change: yes`, and names the brief. Inside the installed
  copy of a plugin (`shared/terms.md`) → decline and ask for
  its source in the repository: a path given → step 1 with it;
  none → end.
- Or the path of a brief: an open one is resumed. Every resume
  command the skill gives names the brief.
- Anything else, or an invalid `--mode` → decline with the
  reason and name what is accepted; end.

## Result

The brief: `<name>-brief.md` in the work-document directory,
from `shared/templates/brief.md`. The description names it,
so it is this skill's result; for the flow it is also the work
document that carries the flow's state in its header (D55).
Either way it stays and belongs to the user (D54), and it is
handed to sw-skill-design by its path. `<name>` is the skill's
name when a skill path is given, else a short kebab-case name
taken from the wish and shown to the user. When the name is
taken, the brief is `<name>-brief-<n>.md` with the lowest
free `n`; an existing file is never overwritten. A brief that
ends without a hand-over — no new skill needed, a step-only
change, or abandoned — stays too, with its end recorded.

## Terms

The skill text uses workshop terms: flow, work document,
work-document directory, open work document, hand-over, run
mode, gate, brief, hypothesis, contrarian pass, advisor,
round, target, form, phase, sub-skill, repository root,
installed copy. They are defined once in `shared/terms.md`
(I17, one home by I8), which the skill reads at its first
step and which sw-skill-review shares. The definitions below
are design notes for that file and for the brief's template;
the skill text names which fields and sections each step
writes, and keeps only how it finds targets.

- **Target kinds** (terms): a skills directory the harness
  loads (in Claude Code the project's `.claude/skills/` or the
  user's `~/.claude/skills/`); an existing plugin in the
  repository (a package the harness installs, with a
  `skills/` directory; in Claude Code a directory with
  `.claude-plugin/plugin.json` and `skills/`), found from the
  repository root at most three levels deep; a new plugin
  (name and parent directory; sw-skill-create makes it, and it
  loads only once the project installs it). A skill's path is
  `<skills directory>/<skill>` or `<plugin>/skills/<skill>`;
  a given path maps back the same way: if the parent of
  `skills/` is a plugin, the target is that plugin, else the
  skills directory.
- **Installed copy** (terms): the copy of a plugin that the
  harness keeps for loading, which an update replaces (in
  Claude Code: under `~/.claude/plugins/`). A plugin loaded in
  place from the repository is no installed copy.
- **Repository root** (terms): `git rev-parse --show-toplevel`
  from the working directory, else the working directory.
- **Work-document directory** (terms): the one the project's
  instructions name for work documents; where they name none,
  a skill that receives no work document asks once, and a
  skill that receives one takes the directory of that work
  document.
- **Open work document** (terms): one whose header `status`
  starts with the skill's prefix, here `brainstorm:`. Open
  briefs are the files `*-brief*.md` in the work-document
  directory with such a status.
- **Form** (terms): what the brief proposes: a new skill, a
  sub-skill, or a change of a skill or of a phase of a skill.
  Not the form check of the audit.
- **Brief header** (template): `wish` (one line), `root`
  (absolute repository root), `target` (kind and absolute
  path, or name and absolute parent), `skill` (the skill's
  name, its directory name), `change` (yes or no), `parent`
  (for a sub-skill: the skill that calls it), `mode`,
  `status`. A field without a value holds `none`. All paths
  absolute. The round is not stored in the header: step 4
  sets it to the number of Advice entries + 1 and writes it in
  its readiness entry under Decisions; each Advice entry is
  headed "round <n>".
- **Brief sections** (template): Clarified (answers are
  appended in order; for each topic the last answer holds),
  Hypothesis,
  Target, Goals and non-goals, Alternatives weighed,
  Decisions, Form, Open objections, Advice (one entry per
  contrarian round, headed "round <n>": a complete report or
  the "no contrarian pass" note), End. The template states that open objections
  released with the brief are accepted open items for
  sw-skill-design.
- **Complete advisor report**: it answers every item of
  `references/contrarian.md` and ends with its summary line.

## Status values and resume

Each step the table names writes `status` to the brief's
header when it starts.

| status | written by | resume at |
|---|---|---|
| `brainstorm:clarifying` | step 1 (a new brief), step 2 | step 2, with the answers already under Clarified |
| `brainstorm:ready` | step 3 | step 3, which rewrites the hypothesis |
| `brainstorm:advising` | step 5 | step 5; if Advice holds an entry headed with the round of the latest readiness entry, step 6 |
| `brainstorm:briefing` | step 6 | step 6 |
| `brainstorm:deciding` | step 7 | step 7 |
| `briefed` | step 8 | not resumed here: the brief belongs to sw-skill-design |
| `closed` | steps 1, 2, 7 | not resumed: the End section says why |

Every exit that ends without a hand-over names the brief and
its path.

## Procedure model

The procedure waits for the user between steps, so its state
lives in a file: the brief (C5, D55). After a compaction the
agent reads the brief (its path is in every resume command
and was shown in step 1), `../../shared/terms.md`, the
project's instructions at `root`, and, before the next
question, `../../shared/asking.md` again. If the path is
lost, it lists the open briefs in the work-document directory
(the project's instructions, else it asks) with
`../../shared/scripts/work_documents.py`: exactly one → it
resumes that brief and tells the user; none or more than one →
it says what it found and asks for the brief; the script
fails → it says so and asks for the brief's path. It never
starts a new brief there.

The brief belongs to the user. The skill does not look for
edits by hand: a user who wants a change says so at the next
question, and the header is what the flow uses. Wherever the
skill shows the brief's path (step 1, every pause, step 7),
it says so in one line and names the sections steps 3 and 6
rewrite. Before every write, the agent reads the brief again,
so it writes over the current file.

| Step | Entry | Exits | Reads / writes | Actor |
|---|---|---|---|---|
| 1 Open the brief | start | **Invalid input** (an invalid `--mode`, or anything Inputs does not accept) → decline with the reason and name what is accepted, end. **A skill path inside an installed copy** → decline and ask for its source in the repository: a path given → step 1 with it; none → end. **A brief handed in:** open → the step its `status` names (the stored mode wins unless the user confirms a new one); `briefed` → decline and name the command that starts sw-skill-design with it, end; `closed` → decline and quote its End section, end. **Otherwise** find the work-document directory (the project's instructions, else ask), then the open briefs there, those for a given skill first: none → a new brief → 2; one or more → ask (each listed by file name, `wish`, target and status): resume one (→ its step); close one (after confirmation `status: closed`, "abandoned" under End, then ask again with the rest; when none is left: start a new brief → 2, or stop (→ name the briefs closed in this run, end); a "no" returns to the question); start a new one (the others stay) → 2; or stop (→ name the briefs that remain, end). **A new brief:** a missing wish is asked for first. **The script fails** → tell the user and name the command that starts the skill again with the same input, end; no brief was created. Done when the brief is open, its `status` is set, and the user has its path and the resume command | reads `../../shared/terms.md` first and `asking.md` before asking; the open briefs and the next free name from `../../shared/scripts/work_documents.py`; a new brief from its template, header: `wish`, `root`, `mode` from `--mode` else asked, the fields from a given skill path, `status: brainstorm:clarifying`, the rest `none` | agent, user |
| 2 Clarify | from 1, 4 or 7 | when the latest Decisions entry is "change request <k>" (from step 4 or 7, also on a resume) and Clarified has no heading "change request <k>", it first asks what should change and appends the answer under that heading in Clarified, with the new answers below it. Done when each topic has an answer under Clarified, or the user said it does not apply. After a change request it is also done only when each topic the change touches has an answer below its heading → 3; the change only alters how a skill's steps work → ask the user to confirm (reads `asking.md` first): yes → `status: closed`, "step-only change, sent to sw-skill-design" under End, name the brief and the command to start `sw-workshop:sw-skill-design` on that skill with the brief's mode (in Claude Code: `/sw-workshop:sw-skill-design <skill path> --mode <mode>`), end; no → go on clarifying; the user pauses → give the resume command with the brief's path (in Claude Code: `/sw-workshop:sw-skill-brainstorm <brief>`), end; the user abandons → after confirmation `status: closed`, "abandoned" under End, name the brief, end (a "no" returns to the question) | `status: brainstorm:clarifying`; first looks up what it can find itself (existing skills, plugins, scripts, skills directories, how the task is done today in the repository) and shows it, then asks only for choices and for what it cannot see; a choice among found items is still an open question, with the found items shown as examples (D51); reads `asking.md` for its wording rules only: clarifying questions are open, one at a time, without preset answers or a recommendation; topics: the problem or need, who or what starts the skill and when, its input, its result, how success is measured, hard limits and non-goals, how it is done today, the target (the three kinds always named, with the skills directories and plugins found as examples; where the project's instructions say where skills go or how they are named, those rules apply and the question says so), a name, new skill or change; answers go under Clarified as they come; `target`, `skill`, `change` go into the header as soon as they are known | agent, user |
| 3 Hypothesis | from 2 | → 4 | `status: brainstorm:ready`; replaces the Hypothesis section with 2–3 sentences: what the skill does, when it triggers, what it delivers | agent |
| 4 Readiness gate | from 3 | the user confirms → write "readiness, round <n>: the hypothesis, the form, `skill` and the target as confirmed" under Decisions, with n = the number of Advice entries + 1 → 5; wants to clarify more → write "readiness: change request <k>" under Decisions, with k = the number of change requests in Decisions + 1 → 2; pauses or abandons → as in 2 | reads `asking.md` (in full); one question with the hypothesis, the form as known so far, `skill`, the target, the options and a recommendation | user |
| 5 Contrarian pass | from 4 | done when Advice holds an entry headed with the round n of the latest readiness entry → 6 | `status: brainstorm:advising`; start a fresh subagent, never a fork (in Claude Code: the Agent tool with type `sw-workshop:sw-draft-advisor`; if the harness does not know that type, a fresh general subagent told to read the agent definition first, at `../../agents/sw-draft-advisor.md` made absolute) with focus "idea", the absolute paths of the brief and `references/contrarian.md`, a list of the skills the harness lists plus those of every plugin in the repository, and the instruction to read earlier Advice entries only to check whether their objections were answered; the agent running this skill writes the complete report as the Advice entry headed "round <n>"; no complete report → retry once; still none, or no subagent tool → write "no contrarian pass: <reason>" as that entry | advisor agent |
| 6 Write the brief | from 5 | done when the sections are filled and the header matches the Form section → 7 | `status: brainstorm:briefing`; fills the sections from Clarified, the hypothesis and the latest Advice entry: Target, Goals and non-goals, Form and Open objections (the 2–3 main ones, or the "no contrarian pass" note) are replaced; Alternatives weighed (rejected with reason) and Decisions are extended; sets the header from the form: new skill → `skill` = its name from Clarified, `target` = the chosen target, `parent: none`, `change: no`; sub-skill → `skill` = the new sub-skill, `target` = the skills directory or plugin the calling skill lives in, `parent` = the calling skill, `change: no`; change of a skill or a phase of a skill → `skill` and `target` = that skill and its place, `parent: none`, `change: yes` | agent |
| 7 Release gate | from 6 | release → 8; a named change that leaves the hypothesis as it is (target, name, details of the form) → record it under Decisions and append it under Clarified as the new answer for its topic, update the header and its section, ask the gate again; change direction (only while Advice has fewer than 3 entries; at 3 the question says that the limit is reached and that a new direction needs a new brief: abandon this one and start the skill again) → write "release: change request <k>" under Decisions, k as in step 4 → 2; no new skill, or no change needed when `change: yes` (also: an existing skill suffices) → `status: closed`, the conclusion and reason under End, report them and name the brief, end; pause → as in 2; abandon → as in 2 | `status: brainstorm:deciding`; reads `asking.md` (in full); one question that states the form, `skill` and the target, the 2–3 main objections or the "no contrarian pass" note, and the brief's path, then the options and a recommendation; pause and abandon stay open as at every question; when the form, `skill` or the target differs from the latest readiness entry under Decisions, it names the change, before and after | user |
| 8 Hand over | from 7 | mode "straight through": start `sw-workshop:sw-skill-design` (in Claude Code: the Skill tool) with the brief's path, end; mode "step by step": end | `status: briefed`, written first; then, in both modes, print the command to start sw-skill-design with the brief (in Claude Code: `/sw-workshop:sw-skill-design <brief>`), so a stopped start can be resumed | agent |

## Gates

- Readiness (step 4): the user confirms the hypothesis and the
  target before any advisor runs; the confirmation is recorded
  under Decisions.
- Release (step 7): the user sees the target and the main
  objections and decides what goes to sw-skill-design. Only
  `status: briefed` lets design start from the brief.

## Loops and limits

- Clarification (2 → 4 → 2): no limit; every turn waits for
  the user, who can pause or abandon at any question.
- Advisor rounds: at most 3, counted as Advice entries; a
  "no contrarian pass" note counts as a round.

## Hand-over

To sw-skill-design: the brief's path. Design reads the brief,
header and sections, in the shape of
`shared/templates/brief.md`, which both skills name, and
takes the brief's directory as the work-document directory.
Design reads Open objections, not every Advice entry. Where
the header and a section disagree, the header holds.

## Files

- `skills/sw-skill-brainstorm/SKILL.md`
- `skills/sw-skill-brainstorm/references/contrarian.md`: the
  idea-level checklist for the advisor: is it needed, does an
  existing skill do most of it, is it a phase or sub-skill of
  another skill, what are the non-goals, which alternative was
  not weighed; ends with a summary line
- `shared/templates/brief.md`
- `shared/terms.md`: the workshop terms its skills share,
  defined for a reader who does not know skill-works
- `shared/scripts/work_documents.py`: the next free name for a
  work document, and the open work documents of a kind in a
  directory, for a given skill; shared with sw-skill-review
  (I9)
- `agents/sw-draft-advisor.md`: the advisor's agent
  definition, shared with sw-skill-design

## Needs outside this skill

- sw-skill-design takes a brief's path with `status: briefed`,
  or a skill path without a brief, for a change that only
  alters how the steps work, with an optional `--mode`.
- sw-skill-review uses `shared/scripts/work_documents.py` for
  its record's name and its open records, and `shared/terms.md`
  for the terms marked "(terms)" above.
- The glossary gets "round", "form" (with an Ambiguities
  row against the audit's form check), "work-document
  directory", "open work document", "installed copy" and
  "repository root"; its "brief" names the header and all
  sections.
- `shared/terms.md` defines an open work document by its
  status prefix.

## Writing notes for sw-skill-create

- Each step's exit conditions become a "Done when" line (I18).
- The description follows I10's four rules; the draft above
  is the proposal.
- Terms: only common words, harness terms, and terms defined
  in `shared/terms.md` or in the skill (I17). Decision numbers
  (D…) in this draft are for the author; they do not go into
  `SKILL.md`.
- Header fields and sections of the brief are defined in its
  template; the skill names which ones each step writes (I8).
- `compatibility`: Python 3 for the shared script.
- Phrase sites for `shared/harness-phrases.md` (D48): start a
  fresh subagent (step 5), start another skill (step 8), ask
  the user (steps 1, 2, 4, 7), refer to the skill's own
  directory (step 5), recognize the installed copy of a plugin
  (step 1), give the resume command with the brief's path
  (steps 1, 2, 4, 7), name another skill's command (steps 1,
  2, 8), give the command that starts this skill with the same
  input (step 1).

## Assumptions to confirm

1. The release gate is one question: release, a named change
   that keeps the hypothesis, change direction (while fewer
   than 3 advisor rounds ran), or no new skill (no change
   needed). Pause and abandon are open at
   every question. Keeping the brief is no choice: it stays in
   every case.
2. Brainstorm handles changes to a skill's purpose, trigger,
   input or result; changes to how its steps work go to
   sw-skill-design.
3. Advisor fallback: a fresh general subagent reads the agent
   definition; with no subagent tool, the brief records "no
   contrarian pass" and the gate shows it. Such a note counts
   as one of the 3 rounds.
4. The advisor's reports are kept in the brief (Advice), so
   the user can read them and a resume finds them; the brief
   grows with each round, and a new round reads earlier
   entries only to check whether they were answered.
5. The brief's file name comes from the skill's name when a
   skill path is given, else from a short name for the wish,
   chosen in step 1; it keeps that name if the skill's name
   changes later.
6. The skill does not detect edits by hand in the brief; it
   tells the user so wherever it shows the brief's path, and
   the user names a change at the next question. At the
   release gate a named change that keeps the hypothesis is
   applied without a new advisor round.
