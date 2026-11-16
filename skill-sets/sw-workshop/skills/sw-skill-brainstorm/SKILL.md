---
name: sw-skill-brainstorm
description: Clarifies the idea for a new agent skill, or for a change to a skill's purpose, trigger, input or result, checks whether the skill is needed at all, and writes a brief for sw-skill-design. Use when the user asks for a new skill or for such a change; not for changing how a skill's steps work.
compatibility: Needs Python 3 for the plugin's workspace script. Starts a subagent for the contrarian pass where the harness can; without one, the brief records that no contrarian pass ran.
---

# Skill Brainstorm

Clarify a planned skill before any procedure is designed: what
it is for, when it triggers, what it delivers, where it will
live, and whether a skill is needed at all. This skill writes
the brief, a work document that sw-skill-design works from. Write
no other file; the workspace script may create the workspace
and its settings file.

Below, `<skill-dir>` is the directory of this file: in Claude
Code `${CLAUDE_SKILL_DIR}`; in another harness, or if the
previous word shows no absolute path, the directory you read
this file from. Read `<skill-dir>/../../shared/terms.md`
first: this file uses its terms (brief, hypothesis, form,
gate, round, advisor, objection, target, and the others) as
defined there.

To ask the user anything: read
`<skill-dir>/../../shared/asking.md` first, then ask with your
harness's question tool, or in plain text if it has none, and
wait for the answer. The clarifying questions of step 2 follow
only its wording rules: open questions, one at a time, without
preset answers or a recommendation.

## Input

`$ARGUMENTS`, else the request that started you:

- the user's wish, from the request or the conversation;
  missing → step 1 asks for it;
- optional `--mode step|through`, the run mode: `step` (step
  by step) or `through` (straight through); missing → step 1
  asks;
- optional, the path of a skill to change: a directory with a
  `SKILL.md`. It fills `skill`, `target` and `change: yes` in
  the header and names the brief;
- or the path of a brief: an open one is resumed.

Decline, with the reason and what is accepted, and stop: an
invalid `--mode`, or anything else. A brief with
`status: briefed` belongs to sw-skill-design: decline and name
the command that starts it with the brief (in Claude Code:
`/sw-workshop:sw-skill-design <brief>`), stop. A skill path
inside an installed copy of a plugin is no place to change a
skill, since an update replaces it: ask for the skill's source
in the repository; a path given → start over with it; none →
stop.

## The Brief

The brief, `<name>-brief.md` in `work/` of the workspace, in
the shape of `<skill-dir>/../../shared/templates/brief.md`,
carries the flow's state in its header; sw-skill-design gets
its path. `<name>` is the skill's name when a skill path is
given, else a short kebab-case name for the wish, which you
show the user; it stays when the skill's name changes later.
A new brief never replaces an existing file: `next-name`
gives a free name.

Find, name, list and delete briefs only through
`python3 <skill-dir>/../../shared/scripts/workspace.py --root <root> …`
(below `workspace.py`): `next-name <name> brief` names a new
brief, `open brief brainstorm` lists the open ones,
`delete <path>` deletes one. `<root>` is the brief's `root`;
before a brief exists, the repository root of the working
directory. When the script prints `created <path>` on stderr,
tell the user that the settings file was created and is meant
to be committed. A brief is open while its `status` starts with
`brainstorm:`.

Write each step's `status` to the header when the step starts,
as the steps say. Before every write, read the brief again, so
that you write over the current file. The brief belongs to the
user: you do not look for edits by hand, and a header the user
changed is what the flow uses. Where you show the brief's
path at step 1, at a pause, or at step 7, say in one line
that a change is named at the next question, and that steps 3 and 6 rewrite Hypothesis, Target,
Goals and non-goals, Form and Open objections.

The round of a contrarian pass is n = the number of Advice
entries + 1, set by step 4 in its readiness entry. At most 3
rounds run; a "no contrarian pass" note counts as one.

**Ending without a hand-over.** Where a step ends the flow
without a hand-over, tell the user the outcome and delete the
brief with `workspace.py delete <brief>`. Whenever `delete`
does not delete a brief, here or in step 1 — the script
fails, or the brief lies outside the workspace — the brief
stays: tell the user so, with its path.

**At every question** of steps 2, 4 and 7 the user may pause
or abandon:

- pause → give the resume command, stop;
- abandon → ask to confirm; yes → end without a hand-over;
  no → back to the question.

## Resume

A brief handed in, or chosen in step 1, resumes at the step
its `status` names below. Its stored mode holds; a different
`--mode` → ask whether to switch, and write the answer to the
header.

| status | resume at |
|---|---|
| `brainstorm:clarifying` | step 2, with the answers already under Clarified |
| `brainstorm:ready` | step 3, which rewrites the hypothesis |
| `brainstorm:advising` | step 5; if Advice holds the entry for the round of the latest readiness entry, step 6 |
| `brainstorm:briefing` | step 6 |
| `brainstorm:deciding` | step 7 |

After a compaction, read the brief again (its path is in the
resume command you gave), `<skill-dir>/../../shared/terms.md`,
the project's instructions at `root`, and
`<skill-dir>/../../shared/asking.md` before the next question.
If you lost the path, list the open briefs with
`workspace.py open brief brainstorm`: exactly one → resume it
and tell the user; none or more → tell the user what you found
and ask for the brief; the script fails → say so and ask for
the brief's path. Never start a new brief there.

The resume command is the command that starts this skill with
the brief's path (in Claude Code:
`/sw-workshop:sw-skill-brainstorm <brief>`).

## Procedure

Run the steps in order. Each one ends at its "Done when".

1. **Open the brief.** Check the input against Input. A brief
   handed in → resume it as Resume says. Otherwise list the
   open briefs, those whose `skill` is the given skill first:
   - none → start a new brief;
   - one or more → ask, each listed by file name, `wish`,
     `target` and `status`: resume one (→ Resume); delete one
     (after confirmation; then ask again with the rest, and
     when none is left, ask: start a new brief, or stop; a "no"
     returns to the question); start a new one, the others
     stay; or stop.

   **A new brief:** ask for a missing wish, then for a missing
   mode, one question each. Name it with `next-name`, and write
   it from the template: `# Brief: <name>`; header `wish`,
   `root`, `mode`, `status: brainstorm:clarifying`; with a
   skill path, `skill` (its directory name), `change: yes` and
   `target`: `plugin <path>` when the parent of its `skills/`
   directory is a plugin, else `skills-dir <path>` of the
   directory that holds it; every other field `none`. Give the
   user the brief's path with the one line on changes, and the
   resume command. The script fails → tell the user and give
   the command that starts this skill with the same input,
   stop; no brief exists. Done when the brief is open, its
   `status` is set, and the user has its path and the resume
   command — or the step stopped.
2. **Clarify.** Write `status: brainstorm:clarifying`. When the
   latest Decisions entry is a change request `<k>` and
   Clarified has no heading `change request <k>`, first ask
   what should change, and append the answer under that
   heading; the new answers go below it.

   First look up what you can find yourself, and show it: the
   skills your harness lists; the skills directories and
   plugins in the repository, from the repository root at most
   three levels deep; scripts; how the task is done in the
   repository today. Then ask only for choices and for what you
   cannot see; a choice among found items is still an open
   question, with the found items as examples. Topics:
   - the problem or need;
   - who or what starts the skill, and when;
   - its input, and its result;
   - how success is measured;
   - hard limits and non-goals;
   - how the task is done today;
   - the target: name the three kinds, with the skills
     directories and plugins you found as examples; where the
     project's instructions say where skills go or how they are
     named, those rules apply, and the question says so;
   - a name;
   - a new skill or a change.

   Append each answer under Clarified as it comes,
   `- <topic>: <answer>`; write `target`, `skill` and `change`
   to the header as soon as they are known. When the change
   only alters how a skill's steps work, ask the user to
   confirm: yes → tell the user that sw-skill-design takes such
   a change, give its command with the skill and the brief's
   mode (in Claude Code:
   `/sw-workshop:sw-skill-design <skill path> --mode <mode>`),
   and end without a hand-over; no → go on clarifying. Done
   when each topic has an answer under Clarified, or the user
   said it does not apply — after a change request, each topic
   the change touches has an answer below its heading — or the
   flow ended.
3. **Hypothesis.** Write `status: brainstorm:ready`. Replace the
   Hypothesis section with a new hypothesis. Done when
   the section holds the new hypothesis.
4. **Readiness gate.** Ask one question: the hypothesis, the
   form as far as it is known, `skill`, the target, the
   options, and your recommendation. The answer goes under
   Decisions before you act on it:
   - confirmed → `- readiness, round <n>: <the hypothesis, the
     form, skill and target as confirmed>` → step 5;
   - clarify more → `- readiness: change request <k>`, with
     k = the number of change requests under Decisions + 1 →
     step 2.

   Done when Decisions holds the entry for the answer, or the
   run stopped.
5. **Contrarian pass.** Write `status: brainstorm:advising`.
   Start a fresh subagent that does not inherit this
   conversation, with your harness's subagent tool (in Claude
   Code: the Agent tool with the type
   `sw-workshop:sw-draft-advisor`; if the harness does not know
   that type, a fresh general subagent told to read the agent
   definition at `<skill-dir>/../../agents/sw-draft-advisor.md`,
   made absolute, first). Never use a fork, which carries the
   conversation along and with it the bias the contrarian pass
   is meant to avoid. Give it the absolute paths of the brief and of
   `<skill-dir>/references/contrarian.md`, and a list of the
   skills your harness lists and those of every plugin in the
   repository. Tell it that Clarified, the Hypothesis and the
   latest readiness entry under Decisions state the plan, and
   that Target, Goals and non-goals, Form, Open objections and
   the header's `parent` are empty or from an earlier round.
   Append its report, if complete as
   `contrarian.md` defines, under Advice as `### round <n>`,
   with n from the latest readiness entry. No complete report →
   start it once more; still none, or your harness has no
   subagent tool → append `no contrarian pass: <reason>` as
   that entry. Done when Advice holds the entry for round n.
6. **Write the brief.** Write `status: brainstorm:briefing`.
   From Clarified, the hypothesis and the latest Advice entry,
   replace Target, Goals and non-goals, Form, and Open
   objections (the main objections its summary line names, or
   its "no contrarian pass" note); append to Alternatives
   weighed the alternatives rejected, with the reason, and to
   Decisions the choices the user made while clarifying; each
   one only if it is not there yet. Set
   the header from the form:
   - new skill → `skill` = its name from Clarified, `target` =
     the chosen target, `parent: none`, `change: no`;
   - sub-skill → `skill` = the new sub-skill, `target` = the
     skills directory or plugin of the calling skill,
     `parent` = the calling skill, `change: no`;
   - change of a skill or of a phase of a skill → `skill` and
     `target` = that skill and its place, `parent: none`,
     `change: yes`.

   Done when the sections are filled and the header matches
   the Form section.
7. **Release gate.** Write `status: brainstorm:deciding`. Ask
   one question that states the form, `skill`, the target, the
   main objections or the "no contrarian pass" note, and the
   brief's path with the one line on changes; where the form,
   `skill` or the target differs from the latest readiness
   entry, name the change, before and after. Then the options
   and your recommendation:
   - release → step 8;
   - a named change that leaves the hypothesis as it is, such
     as the target, the name, or a detail of the form → write
     `- release: <the change, before and after>` under
     Decisions, append it under Clarified as the new answer for
     its topic, update the header and the section, and ask
     again;
   - change direction → `- release: change request <k>`, k as
     in step 4 → step 2. Offer it only while Advice has fewer
     than 3 entries; at 3 the question says that the limit is
     reached and that a new direction needs a new brief: abandon
     this one and start the skill again;
   - no new skill is needed, or with `change: yes` no change,
     also because an existing skill suffices → tell the user
     the conclusion and its reason, and end without a
     hand-over.

   Done when the user released the brief, or the run went to
   step 2, or the flow ended or stopped.
8. **Hand over.** Write `status: briefed` first. Then print the
   command that starts sw-skill-design with the brief (in
   Claude Code: `/sw-workshop:sw-skill-design <brief>`), so the
   user can start it by hand if a start stops. Mode `through`
   → start the skill `sw-workshop:sw-skill-design` with your
   harness's skill tool, with the brief's path, as your last
   action; mode `step` → stop. Done when the header says
   `briefed` and the user has the command.
