# D37: Work on a skill is split into chained skills

Status: amended by [D40](D40-brainstorm-before-design.md), [D46](D46-targets-in-harness-terms.md)

## Decision

Work on a skill is split, as [D35](D35-own-skill-or-phase.md) describes, into skills that files connect. `sw-skill-brainstorm` comes first ([D40](D40-brainstorm-before-design.md)). Then:

- `sw-skill-design` clarifies with the user, writes the draft, gets the advisor, and has the user accept the draft ([D36](D36-skills-start-from-a-draft.md)).
- `sw-skill-create` writes `SKILL.md` and the references from the accepted draft.
- `sw-skill-review` runs the review cycle ([D32](D32-the-review-cycle.md)). It can also be started alone, for example after a change by hand or for the self-test of a skill.

Each one starts the next as its last step ([D35](D35-own-skill-or-phase.md)). If a session stops after the acceptance, one starts `sw-skill-create` again with the draft.

What changed: [D40](D40-brainstorm-before-design.md) added `sw-skill-brainstorm` before `sw-skill-design`. This decision also said that the limit of [D24](D24-sw-skill-create-scope.md) applies to all three skills: they work only on skills in skill-works and its forks. [D46](D46-targets-in-harness-terms.md) replaces that limit. A flow now works on one of three targets: a skills directory, an existing plugin, or a new plugin.

## Reasons

The accepted draft is an acceptance and a file. So it is the natural interface, as for the seed ([D31](D31-seeds-draft-advice-acceptance.md)).
