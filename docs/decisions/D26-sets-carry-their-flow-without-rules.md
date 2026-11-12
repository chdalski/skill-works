# D26: Sets carry their flow without rules

Status: accepted

## Decision

Inside a set, the skills and `shared/` carry the flow, without rules. Only the seed writes rules: to link sets, and for rules that a set asks for in every session. Without a seed, the user links sets.

The set protects itself against compaction:

- The core procedure is in `SKILL.md`, under 5,000 tokens.
- The state of the flow is in files (C5).
- The skill says what it reads again after an interruption.

A set may some day ask for a rule in every session, such as a setting it needs (for example the switch for agent teams, or a path for plans). Then, without a seed, an init skill may offer that rule. It does so only on request and does not overwrite changes of the user. We build this only when a set needs it.

There is no SessionStart hook in a set, because sets hold no harness code ([D14](D14-no-missing-harness-capabilities.md)).

## Reasons

After a compaction, Claude Code keeps the first 5,000 tokens of each invoked skill, and 25,000 tokens for all of them together.

EGM (the elephant-goldfish-model repository) works without rules. Each skill names its place in the flow and the next step. Hand-over is through files. Shared working rules are in a file that each skill reads first. How the skills of a set work together therefore belongs in the set: in the skill texts and in `shared/`.

## Consequences

- The seed of skill-works holds only rules for the repository, none that a set needs for its flow.
