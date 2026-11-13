# Glossary

The terms skill-works uses, and how it uses them. One term
names one thing: a skill, rule, or document that needs one of
these things uses the term given here and none of the words
in its Avoid column. A new term goes in here before it
appears in a skill or a rule.

## Model

| Term | Meaning | Avoid |
|---|---|---|
| skill | A directory with a `SKILL.md` per the Agent Skills specification. Every skill made in this repository belongs to a skill set; the workshop can also make a single skill elsewhere. |  |
| skill set, set | Skills that do one job together, with their shared files, templates, and agents. Ships as one plugin; never refers to another set. | bundle; "set" for a setting |
| single skill | A skill outside any set, such as one in a project's `.claude/skills/`. It counts its own directory as its set and brings what it needs itself. | standalone skill, loose skill |
| seed | The setup a skill-works skill generates for one project: rules and working methods that link sets, settings, and the activation of the set plugins. It holds no skills. | template, scaffold |
| harness | The program that runs an agent and loads skills, such as Claude Code or pi. | client, host, runtime |
| plugin | A package a harness installs; in Claude Code a directory with `.claude-plugin/plugin.json` and `skills/`. Every skill set ships as one; another project knows only plugins, not sets. | extension, package (as a noun for it) |
| skills directory | A directory the harness loads skills from, such as a project's `.claude/skills/` or the user's `~/.claude/skills/` in Claude Code. | skill folder, skills path |
| target | Where a skill lives or will live: a skills directory, an existing plugin, or a new plugin. Skill text that other projects run names targets in these words, never as a skill set. | destination, location |
| workshop set | The set `sw-workshop`: the skills this repository builds skills and seeds with. |  |
| maintenance set | A set bundled with a seed, with which a project improves its seed in place. |  |
| seed generator | The skills of the workshop set that design and generate a seed for a project. |  |
| entry skill | The skill of a set that a user or a seed starts first. It defines the set's input, declines unfit input, and asks for the run mode where the set offers one. | start skill, first skill, main skill |

## Parts of a flow

| Term | Meaning | Avoid |
|---|---|---|
| flow | The work a set does from its entry skill to its result, across one or more skills. | pipeline, workflow |
| chain link | A skill with its own input and result that passes its work on to the next skill through a hand-over; the caller has ended. | stage, step skill |
| sub-skill | A skill with its own input and result that another skill calls inside its own flow and that returns to the caller. It can also be started alone. | child skill, nested skill, helper skill |
| phase | A part of a skill without its own input or result, kept in that skill's `references/` and read at the start of the phase. | stage, sub-step |
| hand-over | Passing work to a receiver: the next skill, a subagent, a script, or the user. Between skills, the receiving skill gets the path of the flow directory. | handoff, hand-off |
| hand-over template | The shape of a file one skill writes and another reads, in `shared/templates/`; both skills name it. | format file, schema |
| run mode | How far a flow runs on its own between the skills of a set, chosen per run: **step by step** (each skill ends and names the next command) or **straight through** (each skill starts the next). | preset, autonomy level |
| gate | A point where the user decides before the flow goes on. The workshop's gates: **readiness gate** (the user confirms the hypothesis), **release gate** (the user releases the brief), **acceptance** (the user accepts the draft), and the decisions at the end of a review cycle. | checkpoint, approval step |

## Files a flow uses

| Term | Meaning | Avoid |
|---|---|---|
| temporary file | A scratch file of one run, or the machine state of a flow: files only skills read, which can be rebuilt, or, for the answer about the work-document directory, asked again. Work documents and results are never temporary. |  |
| flow directory | The temp directory, with a fixed prefix, that holds a flow's machine state and moves from skill to skill. The skill that ends the flow deletes it. Never the harness's scratch directory. | state directory |
| work document | A file the user reads, comments on, or accepts during a flow, such as a brief or a draft. It lives in the directory the project's instructions name for work documents, and belongs to the user. | working file, scratch document |
| state | What a procedure needs to go on after an interruption: progress, decisions, open items. Lives in the conversation only when the procedure runs once and ends with its result; otherwise in a file (C5). |  |
| result | What a skill's description says it produces or changes. | output, for the result |
| lasting result | A result meant to stay, such as a design document, an ADR, or a kept brief, at the place the project's instructions name, else where the user picks. | deliverable; artifact, alone |

## The workshop's flow

| Term | Meaning | Avoid |
|---|---|---|
| brief | What `sw-skill-brainstorm` hands to `sw-skill-design`; a kept copy is its lasting result. It holds what was clarified, the hypothesis, goals and non-goals, alternatives weighed, decisions, the form of the part, and open objections. | concept brief, summary |
| hypothesis | Two or three sentences on what a skill does, when it triggers, and what it delivers, confirmed by the user at the readiness gate. |  |
| draft | The procedure of a skill before any text is written, in the shape of the procedure model; written by `sw-skill-design`, accepted by the user. | plan, spec; design, for the draft |
| procedure model | The table of a skill's steps with entry, exits, reads and writes, and actor, as `coherence.md` describes it. | flow table, step table |
| contrarian pass | The advisor's check of an idea: is the skill needed, does an existing skill do most of it, is it a phase or sub-skill of another skill. | devil's advocate, YAGNI check |

## Checking

| Term | Meaning | Avoid |
|---|---|---|
| test bench | The tests of a skill under `tests/<skill>/`: frozen fixtures, expectations written before a run, and the reports of runs. | test harness, test suite |
| fixture | A frozen copy of a skill or seed that a test bench runs a check against. | test object, sample skill |
| guideline | The items a skill is checked against: form (F), instructions (I), coherence (C), shipped content (A). | checklist, standard |
| audit | One check of a skill against the guideline by a fresh agent; reports only. | review, for one check |
| auditor | The agent that runs an audit (`sw-skill-auditor`). | reviewer, checker |
| advisor | The agent that checks an idea or a draft before any skill text exists (`sw-draft-advisor`). | consultant, critic |
| finding | One shortfall an audit or advisor reports, graded **fail** (the skill does not load or its procedure goes wrong), **warn** (it departs from a guideline without breaking), or **info** (worth knowing). | problem, defect |
| accepted finding | A finding the user decided to leave as it is, with the reason; not reported again in the same review cycle. | waived finding, exception |
| review cycle | A full audit, fixes, and follow-up passes until a pass reports no fail and no warn, then the user's decisions. | review loop |
| follow-up pass | An audit of the diff since the previous pass: it checks that the fixes resolve the previous findings and contradict nothing unchanged. | re-review, re-audit, second pass |
| churn | A new finding that undoing an earlier fix would resolve; it stops a review cycle early. | flip-flop, oscillation |

## Ambiguities

| Word | Resolved as |
|---|---|
| draft | The procedure draft of a skill. A design document, as in other projects, is called "design document". |
| review | `sw-skill-review` runs a review cycle. One check is an audit or a follow-up pass, never "a review". |
| set | Always a skill set. A configuration value is a "setting". |
| result, output | The result is what a skill's description names. Anything else a skill writes is a work document, a handed-in file it extends, or a temporary file. |
| harness, test bench | A harness runs agents. The tests of a skill are its test bench, never a "test harness". |
| target | Covers both a new skill and a skill to change. |
