# D52: Rules for a skill's description

Status: accepted

## Decision

Guideline item I10 (the description triggers correctly) gets four more rules:

1. The leading words say what the skill does.
2. One phrase for each situation that should start the skill; no lists of synonyms.
3. Nothing the skill's body carries: how it works belongs in the body. A sentence stays when it changes the model's choice to load the skill, such as "Reports only; it does not edit the skill."
4. A skill that only the user starts gets a short description for people, without triggers: the model never decides to load it.

`sw-skill-audit` checks the rules; `sw-skill-create` writes descriptions by them.

## Reasons

The description is in the context of every session, so each word costs there. mattpocock/skills writes descriptions this way. A case in point: the description of `sw-skill-audit` ends with "when asked to audit, check, or review a skill"; "review" overlaps with `sw-skill-review`. With rule 2 the overlap goes.

## Consequences

- Rule 4 seldom applies to the workshop set, whose skills stay invocable by the model ([D41](D41-run-modes.md)); it applies to skills the workshop makes for other projects.
- The change goes into the same review cycle as I17, I18, and the other guideline changes ([D49](D49-every-step-says-when-it-is-done.md), [D50](D50-glossary-avoid-lists.md)).
