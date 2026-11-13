# Draft: sw-skill-brainstorm

Status: draft 6, after advisor passes 1–4 (pass 4 by the user's choice); for acceptance

## Purpose and trigger

Clarifies the idea for a new skill, or for a change to a
skill's purpose, trigger, input or result, before any
procedure is designed. It settles what the skill is for, when
it triggers, what it delivers, where it will live, and whether
a skill is needed at all. Entry skill of the skill flow of `sw-workshop`:
brainstorm → design → create → review. A change that only
alters how a skill's steps work goes straight to
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
a skill's purpose, trigger, input or result, and checks
whether the skill is needed at all; produces a brief for
sw-skill-design and, on request, keeps a copy in the project.
Use when the user asks for a new skill or for such a change;
not for changing how a skill's steps work."

No user-only flag (D41): a seed may route a user's request
here, and sw-skill-design points users to it.

## Inputs

- The user's wish, from the request or the conversation.
  Missing → step 2 asks for it.
- Optional `--mode step|through`, the run modes "step by
  step" and "straight through" of the glossary. Another value
  → decline and name the two. Missing → step 1 asks.
- Optional: the path of a skill to change: a directory with a
  `SKILL.md`. Inside the installed copy of a plugin → decline
  and ask for its source in the repository. Anything else →
  decline. It pre-fills `skill`, `target` and `change: yes`.

## Result

- Normal: the released brief, `brief.md`, in the flow
  directory, handed to sw-skill-design (temporary).
- On request: a kept copy of the brief in the project
  (lasting result, step 8).
- Or: the conclusion that no new skill is needed, with the
  reason; or the pointer to sw-skill-design for a step-only
  change. The flow directory is deleted in both cases.

## Terms

The skill text uses workshop terms: flow, flow directory,
hand-over, run mode, gate, brief, hypothesis, contrarian pass,
advisor, round, target, form, phase, sub-skill. A project that
runs the skill does not have skill-works' glossary, so the
terms the workshop's skills share are defined once in
`shared/terms.md` (I17, one home by I8), and the skill reads
it at its first step. The definitions below are design notes:
target and its kinds, and the flow directory, go into
`shared/terms.md`; the fields of `state.md` and the sections
of `brief.md` go into their templates. The skill text names
which fields and sections each step writes, and keeps only
how it finds targets.

- **Target kinds**: a skills directory the harness loads (in
  Claude Code the project's `.claude/skills/` or the user's
  `~/.claude/skills/`); an existing plugin in the repository
  (a package the harness installs, with a `skills/`
  directory; in Claude Code a directory with
  `.claude-plugin/plugin.json` and `skills/`), found from the
  repository root at most three levels deep; a new plugin
  (name and parent directory; sw-skill-create makes it, and it
  loads only once the project installs it). Never the
  installed copy of a plugin, which an update replaces. A
  skill's path is `<skills directory>/<skill>` or
  `<plugin>/skills/<skill>`; a given path maps back the same
  way: if the parent of `skills/` is a plugin, the target is
  that plugin, else the skills directory.
- **Repository root**: `git rev-parse --show-toplevel` from
  the working directory, else the working directory.
- **Flow directory**: created with
  `mktemp -d -t sw-skill-flow.XXXXXX` (in Python
  `tempfile.mkdtemp(prefix="sw-skill-flow.")`), looked up in
  the temp facility's directory (`tempfile.gettempdir()`; in a
  shell `dirname "$(mktemp -u)"`).
- **state.md**: in the shape of `shared/templates/state.md`:
  `wish` (one line), `root` (absolute repository root),
  `target` (kind and absolute path, or name and absolute
  parent), `skill` (the skill's name, its directory name),
  `change` (yes or no), `parent` (for a sub-skill: the name
  of the skill that calls it), `mode`, `status`, `round`. All
  paths absolute; where a skill lives is given by `target`.
- **brief.md**: created in step 1 from
  `shared/templates/brief.md`, with the sections Clarified,
  Hypothesis, Target, Goals and non-goals, Alternatives
  weighed, Decisions, Form, Open objections. The template
  states that open objections released with the brief are
  accepted open items for sw-skill-design.
- **Complete advisor report**: it answers every item of
  `references/contrarian.md` and ends with its summary line.

## Status values and resume

Each step writes its status to `state.md` when it starts.

| status | written by | resume at |
|---|---|---|
| `brainstorm:clarifying` | step 2 | step 2, with the answers already in `brief.md` |
| `brainstorm:ready` | step 3 | step 3, which rewrites the hypothesis |
| `brainstorm:advising` | step 5 | step 5 with the stored `round`; if `advice-<round>.md` is complete, step 6 |
| `brainstorm:briefing` | step 6 | step 6 |
| `brainstorm:deciding` | step 7 | step 7 |
| `brainstorm:keeping` | step 8 | step 8 |
| `briefed` | step 9 | not resumed here: the directory belongs to sw-skill-design |

## Procedure model

The procedure waits for the user between steps, so its state
lives in a file. After a compaction the agent reads
`state.md`, `brief.md`, `../../shared/terms.md` and `../../shared/asking.md` again
before the next question. A resumed flow reads the project's
instructions at its stored `root`. Every step can also be entered by a
resume from step 1, at the step the status table names.

| Step | Entry | Exits | Reads / writes | Actor |
|---|---|---|---|---|
| 1 Open the state | start | no flow directory with a `brainstorm:` status → create one, write `state.md` (`wish` if known, `root`, `mode` from `--mode` else ask, the fields from a given skill path) and `brief.md` from its template → 2; one or more → Q1 "which flow, or a new one?" (each listed by `wish`, `root`, target and status): a flow → Q2 "resume or delete?": resume → the step its status names (the stored mode wins unless the user confirms a new one); delete → after confirmation delete it and ask Q1 again with the rest (none left → create a new one → 2); a "no" returns to Q2; a new one → create (the others stay) → 2; directories without `state.md` are listed apart, with an offer to delete them | flow directories, `state.md`, `brief.md`; reads `../../shared/terms.md` first and `asking.md` before asking | agent, user |
| 2 Clarify | from 1, 4 or 7 | done when each topic has an answer under Clarified in `brief.md`, or the user said it does not apply → 3; the change only alters how a skill's steps work → ask the user to confirm (reads `asking.md` first): yes → name the command to start `sw-workshop:sw-skill-design` on that skill (in Claude Code: `/sw-workshop:sw-skill-design <skill path>`), delete the directory, end; no → go on clarifying; the user pauses → keep the directory and give the command to resume it (in Claude Code: `/sw-workshop:sw-skill-brainstorm`); end; the user abandons → delete after confirmation (a "no" returns to the question), end | `status: brainstorm:clarifying`; first looks up what it can find itself (existing skills, plugins, scripts, skills directories, how the task is done today in the repository) and shows it, then asks only for choices and for what it cannot see; a choice among found items is still an open question, with the found items shown as examples (D51); reads `asking.md` for its wording rules only: clarifying questions are open, one at a time, without preset answers or a recommendation; topics: the problem or need, who or what starts the skill and when, its input, its result, how success is measured, hard limits and non-goals, how it is done today, the target (the three kinds always named, with the skills directories and plugins found as examples; where the project's instructions say where skills go or how they are named, those rules apply and the question says so), a name, new skill or change; answers go under "Clarified" in `brief.md` as they come; `wish` (if empty), `target`, `skill`, `change` go into `state.md` as soon as they are known | agent, user |
| 3 Hypothesis | from 2 | → 4 | `status: brainstorm:ready`; replaces the Hypothesis section of `brief.md` with 2–3 sentences: what the skill does, when it triggers, what it delivers | agent |
| 4 Readiness gate | from 3 | the user confirms → 5 with `round` = number of `advice-*.md` + 1, written to `state.md`; wants to clarify more → 2; pauses or abandons → as in 2 | reads `asking.md` (in full); one question with the hypothesis, the target, the options and a recommendation | user |
| 5 Contrarian pass | from 4 | done when `advice-<round>.md` holds a complete report or the "no contrarian pass" note → 6 | `status: brainstorm:advising`; writes an empty `advice-<round>.md`; start a fresh subagent, never a fork (in Claude Code: the Agent tool with type `sw-workshop:sw-draft-advisor`; if the harness does not know that type, a fresh general subagent told to read the agent definition first, at `../../agents/sw-draft-advisor.md` made absolute) with focus "idea" and absolute paths to `brief.md`, `references/contrarian.md`, and a list of the skills the harness lists plus those of every plugin in the repository; the agent running this skill writes a complete report to `advice-<round>.md`; no complete report → retry once; still none, or no subagent tool → write "no contrarian pass: <reason>" to `advice-<round>.md` | advisor agent |
| 6 Write the brief | from 5 | done when the six sections are filled and `state.md` matches the Form section → 7 | `status: brainstorm:briefing`; fills the remaining sections of `brief.md` from Clarified, the hypothesis and the latest round's advice file: Target, Goals and non-goals, Form and Open objections (the 2–3 main ones, or the "no contrarian pass" note) are replaced; Alternatives weighed (rejected with reason) and Decisions are extended; rewrites `state.md` from the form: new skill → `change: no`; sub-skill → `change: no`, `skill` = the new sub-skill, `parent` = the skill that calls it, `target` = the skills directory or plugin the parent lives in; change of a skill or a phase of a skill → `change: yes`, `skill` and `target` = that skill and its place | agent |
| 7 Release gate | from 6 | Q1: release → Q2 "keep a copy?": yes → 8, no → 9; change direction (only while `round` < 3) → 2; no new skill (also: an existing skill suffices) → report the conclusion and reason, delete the directory, end; stop for now → Q2 "pause (to continue later), keep the brief and end (for people to read; it cannot be continued), or abandon": pause → as in 2; keep and end → 8; abandon → as in 2 | `status: brainstorm:deciding`; reads `asking.md` (in full); Q1 states the form, `skill` and the target, the 2–3 main objections or the "no contrarian pass" note, and the path of `brief.md`, then the options and a recommendation; when the form, `skill` or the target differs from what the user confirmed at step 4, Q1 names the change, before and after | user |
| 8 Keep the brief | from 7 | written → 9, or, for "keep and end", delete the directory and end; the user declines to overwrite → ask for another name | `status: brainstorm:keeping`; reads `asking.md` before asking; file `<skill>-brief.md` in the directory the project's instructions name for such documents, else ask with a detected default (`docs/`); confirm before overwriting an existing file | agent, user |
| 9 Hand over | from 7 or 8 | mode "straight through": start `sw-workshop:sw-skill-design` (in Claude Code: the Skill tool) with the flow directory, end; mode "step by step": end | `status: briefed`, written first; then, in both modes, print the command to start sw-skill-design with the flow directory (in Claude Code: `/sw-workshop:sw-skill-design <flow directory>`), so a stopped start can be resumed | agent |

## Gates

- Readiness (step 4): the user confirms the hypothesis and the
  target before any advisor runs.
- Release (step 7): the user sees the target and the main
  objections and decides what goes to sw-skill-design. Only
  `status: briefed` lets design start from this directory.

## Loops and limits

- Clarification (2 → 4 → 2): no limit; every turn waits for
  the user, who can pause or abandon at any question.
- Advisor rounds: at most 3. `round` is set when step 4 sends
  a round to step 5; a resumed round keeps its number.

## Hand-over

To sw-skill-design: the flow directory's path. Design reads
`state.md` and `brief.md` there, in the shapes of
`shared/templates/state.md` and `shared/templates/brief.md`,
which both skills name.

## Files

- `skills/sw-skill-brainstorm/SKILL.md`
- `skills/sw-skill-brainstorm/references/contrarian.md`: the
  idea-level checklist for the advisor: is it needed, does an
  existing skill do most of it, is it a phase or sub-skill of
  another skill, what are the non-goals, which alternative was
  not weighed; ends with a summary line
- `shared/templates/brief.md`, `shared/templates/state.md`
- `shared/terms.md`: the workshop terms its skills share,
  defined for a reader who does not know skill-works
- `agents/sw-draft-advisor.md`: the advisor's agent definition, shared
  with sw-skill-design

## Needs outside this skill

- sw-skill-design takes a skill path without a flow directory,
  for a change that only alters how the steps work.

## Writing notes for sw-skill-create

- Each step's exit conditions become a "Done when" line (I18).
- The description follows I10's four rules; the draft above
  is the proposal.
- Terms: only common words, harness terms, and terms defined
  in `shared/terms.md` or in the skill (I17). Decision numbers
  (D…) in this draft are for the author; they do not go into
  `SKILL.md`.
- Fields of `state.md` and sections of `brief.md` are defined
  in their templates; the skill names which ones each step
  writes (I8).
- Phrase sites for `shared/harness-phrases.md` (D48): start a
  fresh subagent (step 5), start another skill (step 9), ask
  the user (steps 1, 2, 4, 7, 8), create a temp directory
  (flow directory), refer to the skill's own directory
  (step 5).

## Assumptions to confirm

1. Release gate as two questions — first what to do with the
   brief, then whether to keep a copy or how to stop — for
   clarity, not because of a tool's limit (D48).
2. Brainstorm for changes to a skill's purpose, trigger, input
   or result; changes to how its steps work go to
   sw-skill-design.
3. Advisor fallback: a fresh general subagent reads the
   agent definition; with no subagent tool, the brief records "no
   contrarian pass" and the gate shows it.
