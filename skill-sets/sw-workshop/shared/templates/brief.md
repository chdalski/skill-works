---
wish: none
root: none
target: none
skill: none
change: none
parent: none
mode: none
status: brainstorm:clarifying
---

# Brief: <name>

What `sw-skill-brainstorm` clarified about a planned skill, and
what it hands to `sw-skill-design`. The header above is the
flow's state; both skills read it, and where the header and a
section disagree, the header holds. A field without a value
holds `none`; every path is absolute. Header fields:

- `wish`: the user's wish, in one line.
- `root`: the repository root.
- `target`: where the skill will live: `skills-dir <path>`, a
  skills directory the harness loads; `plugin <path>`, an
  existing plugin; or `new-plugin <path>`, a plugin that
  `sw-skill-create` makes at that path.
- `skill`: the skill's name, which is its directory name.
- `change`: `yes` when the brief changes an existing skill,
  else `no`.
- `parent`: for a sub-skill, the name of the skill that calls
  it.
- `mode`: the run mode, `step` (step by step) or `through`
  (straight through).
- `status`: `brainstorm:<step>` while `sw-skill-brainstorm`
  works on the brief; `briefed` once the user has released it
  to `sw-skill-design`.

The brief is a work document in `work/` of the workspace. The
skill that ends the flow deletes it after the user's
acceptance.

## Clarified

<!-- Appended. Answers in the order they came; for each topic
the last answer holds:
- <topic>: <answer>
A change request opens with its heading and what should
change; its answers follow below it:
### change request <k>
<what should change>
-->

## Hypothesis

<!-- Replaced each time. 2–3 sentences: what the skill does,
when it triggers, what it delivers. -->

## Target

<!-- Replaced each time. Where the skill will live and why;
the project's rules on where skills go and how they are
named, where its instructions give any. -->

## Goals and non-goals

<!-- Replaced each time.
- goal: <what the skill must achieve>
- non-goal: <what it does not do> -->

## Alternatives weighed

<!-- Appended. One entry per alternative:
- <alternative>: rejected — <reason> -->

## Decisions

<!-- Appended. One entry per decision of the user: a choice
made while clarifying, with its reason, or an answer at a gate:
- clarified: <the choice> — <reason>
- readiness, round <n>: <hypothesis, form, skill and target as confirmed>
- readiness: change request <k>
- release: <named change, before and after>
- release: change request <k> -->

## Form

<!-- Replaced each time. What the brief proposes: a new
skill, a sub-skill of `parent`, or a change of a skill or of
a phase of a skill; and its shape in a few sentences. The
header follows this section. -->

## Open objections

<!-- Replaced each time. The 2–3 main objections of the
latest round, or its "no contrarian pass" note. Objections
still here when the user releases the brief are accepted open
items for sw-skill-design. -->

## Advice

<!-- Appended. One entry per contrarian round:
### round <n>
<the advisor's complete report, or "no contrarian pass: <reason>">
-->
