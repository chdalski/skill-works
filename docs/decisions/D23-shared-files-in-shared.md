# D23: Shared files go in `shared/`

Status: accepted

## Decision

What at least two skills of a set need goes in `skill-sets/<set>/shared/`. What only one skill needs goes in that skill's `references/`. A skill always reaches `shared/` as `../../shared/<file>`, relative to its `SKILL.md`. This applies to all sets.

## Reasons

The specification knows only paths inside a skill. This is acceptable, because a skill ships only with its set ([D1](D1-skills-ship-in-sets.md)).

EGM (the elephant-goldfish-model repository) is the model. EGM keeps shared files at plugin level in `resources/`, and what only one skill needs in `skills/<skill>/references/`. But EGM uses three different path forms. We use one fixed path.

## Consequences

- [D43](D43-hand-over-templates.md) applies this rule to templates.
