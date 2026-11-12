# D30: The guide for asking lives in the set

Status: accepted

## Decision

For skills, how to ask the user and how to explain is in the set, not in a rule. The workshop set gets `shared/asking.md` in step 5b, because `sw-skill-create` and later the design skill of [D31](D31-seeds-draft-advice-acceptance.md) ask the user.

A new item in `instructions-skills.md` (I15) requires: a skill that asks the user reads the guide for asking of its set at the step where it asks. `sw-skill-create` puts the reference in. `sw-skill-audit` reports when it is missing.

The text then exists more than once: as a rule in skill-works, and in `shared/` of each set that asks. This is a second case of an open question: how shared knowledge gets into several sets, by one source that a script copies and a test compares, or by one version per set.

The seed generator (step 7 of the plan) decides if generated seeds get such a rule for the conversation outside skills.

## Reasons

A skill also runs in projects that do not have the rule `asking-the-user.md` of skill-works. Sets carry their own knowledge of their flow ([D26](D26-sets-carry-their-flow-without-rules.md)).

EGM (the elephant-goldfish-model repository) is the model. EGM works without rules: each skill names its place in the flow, and shared working rules are in a file that each skill reads first.
