# D40: `sw-skill-brainstorm` comes before `sw-skill-design`

Status: accepted

## Decision

Designing a skill is split into two skills, as [D35](D35-own-skill-or-phase.md) describes. `egm-brainstorm` and `egm-draft` of EGM (the elephant-goldfish-model repository) are the model.

`sw-skill-brainstorm` clarifies the idea:

1. Open exploring questions without given answers, so that the agent does not steer in one direction too early.
2. A working hypothesis in two or three sentences: what the skill does, when it triggers, what it delivers. At a readiness gate the user confirms it.
3. A contrarian pass by the advisor, also on YAGNI grounds: is there already a skill that can almost do this? Is it only a phase of another skill?

The result is the brief: hypothesis, goals and non-goals, rejected alternatives, and decisions. The gate releases what goes to `sw-skill-design`. When the brainstorm ends with "no new skill", there is no hand-over.

`sw-skill-design` designs the procedure from the brief ([D36](D36-skills-start-from-a-draft.md)). Without a brief, it accepts only a change to an existing skill. For a new skill it refers to `sw-skill-brainstorm`, so that the contrarian check is not skipped.

Decision gates keep a recommendation with a reason, as `asking.md` says. This differs from EGM.

Work on a skill thus has four skills: brainstorm → design → create → review.

This decision adds to [D37](D37-skill-work-in-chained-skills.md).
