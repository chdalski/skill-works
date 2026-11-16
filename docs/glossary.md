# Glossary

The terms skill-works uses, and how it uses them. One term
names one thing: a skill, rule, or document that needs one of
these things uses the term given here and none of the words
in its Avoid column.

Each term has one home ([D57](decisions/D57-plugin-terms-in-the-plugin.md)).
A term the skills of the workshop plugin use is defined in
`skill-sets/sw-workshop/shared/terms.md` (below: terms.md),
which ships with the plugin; its row here says "→ terms.md"
and keeps the words to avoid. Every other term is defined
here. A new term goes into its home, and gets its row here,
before it appears in a skill or a rule.

## Model

| Term | Meaning | Avoid |
|---|---|---|
| skill | A directory with a `SKILL.md` per the Agent Skills specification. Every skill made in this repository belongs to a skill set; the workshop can also make a single skill elsewhere. |  |
| skill set, set | Skills that do one job together, with their shared files, templates, and agents. Ships as one plugin; never refers to another set. | bundle; "set" for a setting |
| single skill | A skill outside any set, such as one in a project's `.claude/skills/`. It counts its own directory as its set and brings what it needs itself. | standalone skill, loose skill |
| seed | The setup a skill-works skill generates for one project: rules and working methods that link sets, settings, and the activation of the set plugins. It holds no skills. | template, scaffold |
| harness | The program that runs an agent and loads skills, such as Claude Code or pi. | client, host, runtime |
| plugin | → terms.md. Every skill set ships as one; another project knows only plugins, not sets. | extension, package (as a noun for it) |
| skills directory | → terms.md, under target. | skill folder, skills path |
| target | → terms.md. Skill text that other projects run names targets in these words, never as a skill set. | destination, location |
| installed copy | → terms.md. | plugin cache |
| repository root | → terms.md. | project root |
| workshop set | The set `sw-workshop`: the skills this repository builds skills and seeds with. |  |
| maintenance set | A set bundled with a seed, with which a project improves its seed in place. |  |
| seed generator | The skills of the workshop set that design and generate a seed for a project. |  |
| entry skill | The skill of a set that a user or a seed starts first. It defines the set's input, declines unfit input, and asks for the run mode where the set offers one. | start skill, first skill, main skill |

## Parts of a flow

| Term | Meaning | Avoid |
|---|---|---|
| flow | → terms.md. | pipeline, workflow |
| chain link | A skill with its own input and result that passes its work on to the next skill through a hand-over; the caller has ended. | stage, step skill |
| sub-skill | → terms.md. | child skill, nested skill, helper skill |
| phase | → terms.md. | stage, sub-step |
| hand-over | → terms.md. | handoff, hand-off |
| hand-over template | The shape of a file one skill writes and another reads, in `shared/templates/`; both skills name it. | format file, schema |
| handed-in file | → terms.md. In skill-works, a seed counts among the project's instructions. |  |
| run mode | → terms.md. | preset, autonomy level |
| gate | → terms.md. | checkpoint, approval step |

## Files a flow uses

| Term | Meaning | Avoid |
|---|---|---|
| temporary file | → terms.md. | flow directory, state directory |
| work document | → terms.md. | working file, scratch document |
| workspace | → terms.md. | work-document directory, artifact directory |
| open work document | → terms.md. | active document |
| state | What a procedure needs to go on after an interruption: progress, decisions, open items. Lives in the conversation only when the procedure runs once and ends with its result; otherwise in a file (C5): the work document that carries the flow, the result, or a handed-in file; never in `temp/`. |  |
| result | What a skill's description says it produces or changes. | output, for the result |
| lasting result | A result meant to stay, such as a finished skill, a design document or an ADR, at the place the project's instructions name, else where the user picks. No skill deletes it. | deliverable; artifact, alone |

## The workshop's flow

| Term | Meaning | Avoid |
|---|---|---|
| brief | → terms.md; its header and sections are those of `shared/templates/brief.md`. | concept brief, summary |
| hypothesis | → terms.md. |  |
| draft | The procedure of a skill before any text is written, in the shape of the procedure model; written by `sw-skill-design`, accepted by the user. | plan, spec; design, for the draft |
| procedure model | The table of a skill's steps with entry, exits, reads and writes, and actor, as `coherence.md` describes it. | flow table, step table |
| contrarian pass | → terms.md; its checks are those of `sw-skill-brainstorm/references/contrarian.md`. | devil's advocate, YAGNI check |
| round | → terms.md. | pass, for the advisor; iteration |
| form | → terms.md. | type, kind |

## Checking

| Term | Meaning | Avoid |
|---|---|---|
| test bench | The tests of a skill under `tests/<skill>/`: frozen fixtures, expectations written before a run, and the reports of runs. | test harness, test suite |
| fixture | A frozen copy of a skill or seed that a test bench runs a check against. | test object, sample skill |
| guideline | The items a skill is checked against: form (F), instructions (I), coherence (C), shipped content (A). | checklist, standard |
| audit | → terms.md. | review, for one check |
| auditor | → terms.md, under audit; the agent `sw-skill-auditor`. | reviewer, checker |
| advisor | → terms.md. | consultant, critic |
| objection | → terms.md. | finding, for the advisor; concern |
| finding | → terms.md. | problem, defect |
| accepted finding | → terms.md. | waived finding, exception |
| review cycle | → terms.md. | review loop |
| pass | → terms.md. | round, for an audit |
| full audit | → terms.md, under pass. | complete review |
| follow-up pass | → terms.md, under pass. | re-review, re-audit, second pass |
| audit loop | → terms.md. | fix loop |
| agreed finding | → terms.md. |  |
| held finding | → terms.md. | open question |
| churn | → terms.md. | flip-flop, oscillation |
| record | → terms.md; its header and sections are those of `shared/templates/review.md`. | review log, report |
| snapshot | → terms.md. |  |

## Ambiguities

| Word | Resolved as |
|---|---|
| draft | The procedure draft of a skill. A design document, as in other projects, is called "design document". |
| review | `sw-skill-review` runs a review cycle. One check is an audit or a follow-up pass, never "a review". |
| set | Always a skill set. A configuration value is a "setting". |
| result, output | The result is what a skill's description names, except a work document the skill hands on within its flow, such as a brief. Anything else a skill writes is a work document or a temporary file in the workspace, or a handed-in file it extends. |
| harness, test bench | A harness runs agents. The tests of a skill are its test bench, never a "test harness". |
| target | Covers both a new skill and a skill to change. |
| form | In a brief, what it proposes. The audit's form items (F) check whether a skill loads and works in every harness; that check is the form check. |
