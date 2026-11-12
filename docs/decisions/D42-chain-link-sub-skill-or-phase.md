# D42: Chain link, sub-skill, or phase

Status: accepted

## Decision

A part of a flow has one of three forms:

- Chain link: a skill of its own as [D35](D35-own-skill-or-phase.md) describes. It passes its work on to the next skill through a hand-over. The caller has ended.
- Sub-skill: a skill of its own, as a sibling in `skills/`. Another skill calls it in the middle of its own flow through the skill tool, and it returns afterwards. It states what it returns. As a sub-skill it starts no further skill and no closing for the user. It can also be started alone.
- Phase: a part without its own input and its own result, in the `references/` of its skill. The skill reads it at the start of the phase.

Example: the audit loop is a phase of `sw-skill-review`. `sw-skill-audit`, which the loop calls in each pass, is a sub-skill.

A skill in a subdirectory of another skill would probably not be found as a skill by the harness (not tested).

## Reasons

EGM (the elephant-goldfish-model repository) is the model. There, `egm-review-loop` and `egm-resolve` run as sibling skills, alone and as a part of the flow of `egm-review`. As a part of the flow they return without a closing of their own.

Unlike EGM, we use the skill tool. EGM reads the `SKILL.md` of the sub-skill, because all its skills set `disable-model-invocation`. With the skill tool, sub-skills stay invocable by the model ([D41](D41-run-modes.md)), and F7 needs no path into the directory of another skill.
