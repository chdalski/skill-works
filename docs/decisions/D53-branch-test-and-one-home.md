# D53: Branch test, and one home for each concept

Status: accepted

## Decision

Guideline item I8 (core first, details on demand) gets two rules:

1. Branch test: what every path through a skill needs stays in `SKILL.md`; what only some paths reach goes into a reference that exactly those paths read. The paths decide, not the length.
2. One home: the definition, rules, and limits of one concept stand in one place, under one heading. Another place that needs the concept points to that home instead of restating it.

`sw-skill-audit` checks both rules; `sw-skill-create` cuts skills by them.

## Reasons

mattpocock/skills teaches both in its writing-for-agents skill ("inline what every branch needs, and push behind a pointer what only some branches reach"; spreading one concept over several places is "sprawl"). Our own guideline shows the cost: the rules for state are split between C5 (`coherence.md`) and I16 (`instructions-skills.md`), and the self-test of I16 found a contradiction between the two in four passes in a row.

## Consequences

- C5 and I16 get one home each: C5 says when a procedure's state needs a file, I16 says where files go; each points to the other for the other part.
- The change goes into the same review cycle as the other guideline changes ([D49](D49-every-step-says-when-it-is-done.md), [D50](D50-glossary-avoid-lists.md), [D52](D52-description-rules.md)).
