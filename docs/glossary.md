# Glossary

The terms skill-works uses, and how it uses them. One term
names one thing: a skill, rule, or document that needs one of
these things uses the term given here and no other word for
it. A new term goes in here before it appears in a skill or a
rule.

## Model

| Term | Meaning |
|---|---|
| skill | A directory with a `SKILL.md` per the Agent Skills specification. Every skill made in this repository belongs to a skill set; the workshop can also make a single skill elsewhere. |
| skill set, set | Skills that do one job together, with their shared files, templates, and agents. Ships as one plugin; never refers to another set. |
| single skill | A skill outside any set, such as one in a project's `.claude/skills/`. It counts its own directory as its set and brings what it needs itself. |
| seed | The setup a skill-works skill generates for one project: rules and working methods that link sets, settings, and the activation of the set plugins. It holds no skills. |
| harness | The program that runs an agent and loads skills, such as Claude Code or pi. |
| plugin | A package a harness installs; in Claude Code a directory with `.claude-plugin/plugin.json` and `skills/`. Every skill set ships as one; another project knows only plugins, not sets. |
| skills directory | A directory the harness loads skills from, such as a project's `.claude/skills/` or the user's `~/.claude/skills/` in Claude Code. |
| target | Where a skill lives or will live: a skills directory, an existing plugin, or a new plugin. Skill text that other projects run names targets in these words, never as a skill set. |
| workshop set | The set `sw-workshop`: the skills this repository builds skills and seeds with. |
| maintenance set | A set bundled with a seed, with which a project improves its seed in place. |
| seed generator | The skills of the workshop set that design and generate a seed for a project. |
| entry skill | The skill of a set that a user or a seed starts first. It defines the set's input, declines unfit input, and asks for the run mode where the set offers one. |

## Parts of a flow

| Term | Meaning |
|---|---|
| flow | The work a set does from its entry skill to its result, across one or more skills. |
| chain link | A skill with its own input and result that passes its work on to the next skill through a hand-over; the caller has ended. |
| sub-skill | A skill with its own input and result that another skill calls inside its own flow and that returns to the caller. It can also be started alone. |
| phase | A part of a skill without its own input or result, kept in that skill's `references/` and read at the start of the phase. |
| hand-over | Passing work from one skill to the next: the receiving skill gets the path of the flow directory. |
| hand-over template | The shape of a file one skill writes and another reads, in `shared/templates/`; both skills name it. |
| run mode | How far a flow runs on its own between the skills of a set, chosen per run: **step by step** (each skill ends and names the next command) or **straight through** (each skill starts the next). |
| gate | A point where the user decides before the flow goes on. The workshop's gates: **readiness gate** (the user confirms the hypothesis), **release gate** (the user releases the brief), **acceptance** (the user accepts the draft), and the decisions at the end of a review cycle. |

## Files a flow uses

| Term | Meaning |
|---|---|
| temporary file | Any file a skill writes that is not its result. Scratch files go into a new temp directory and are deleted when the run ends (I16). |
| flow directory | The temp directory, with a fixed prefix, that holds a flow's state and hand-overs and moves from skill to skill. The skill that hands it to no one deletes it. Never the harness's scratch directory. |
| state | What a procedure needs to go on after an interruption: progress, decisions, open items. Lives in the conversation only when the procedure runs once and ends with its result; otherwise in a file (C5). |
| result | What a skill's description says it produces or changes. |
| lasting result | A result meant to stay, such as a design document, an ADR, or a kept brief. Worked out in the flow directory and written by a last step to the place the project's instructions name, else where the user picks. |

## The workshop's flow

| Term | Meaning |
|---|---|
| brief | The result of `sw-skill-brainstorm`: what was clarified, the hypothesis, goals and non-goals, alternatives weighed, decisions, the form of the part, and open objections. |
| hypothesis | Two or three sentences on what a skill does, when it triggers, and what it delivers, confirmed by the user at the readiness gate. |
| draft | The procedure of a skill before any text is written, in the shape of the procedure model; written by `sw-skill-design`, accepted by the user. |
| procedure model | The table of a skill's steps with entry, exits, reads and writes, and actor, as `coherence.md` describes it. |
| contrarian pass | The advisor's check of an idea: is the skill needed, does an existing skill do most of it, is it a phase or sub-skill of another skill. |

## Checking

| Term | Meaning |
|---|---|
| test bench | The tests of a skill under `tests/<skill>/`: frozen fixtures, expectations written before a run, and the reports of runs. |
| fixture | A frozen copy of a skill or seed that a test bench runs a check against. |
| guideline | The items a skill is checked against: form (F), instructions (I), coherence (C), shipped content (A). |
| audit | One check of a skill against the guideline by a fresh agent; reports only. |
| auditor | The agent that runs an audit (`sw-skill-auditor`). |
| advisor | The agent that checks an idea or a draft before any skill text exists (`sw-draft-advisor`). |
| finding | One shortfall an audit or advisor reports, graded **fail** (the skill does not load or its procedure goes wrong), **warn** (it departs from a guideline without breaking), or **info** (worth knowing). |
| accepted finding | A finding the user decided to leave as it is, with the reason; not reported again in the same review cycle. |
| review cycle | A full audit, fixes, and follow-up passes until a pass reports no fail and no warn, then the user's decisions. |
| follow-up pass | An audit of the diff since the previous pass: it checks that the fixes resolve the previous findings and contradict nothing unchanged. |
| churn | A new finding that undoing an earlier fix would resolve; it stops a review cycle early. |
