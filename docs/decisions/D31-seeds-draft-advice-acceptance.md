# D31: Seeds come from draft, advice, and acceptance

Status: accepted

## Decision

A seed is made in this order:

1. Clarify with the user what the user wants.
2. Write a draft as a file.
3. An advisor checks the draft. Is it consistent in itself? Do the sets fit together as [D3](D3-sets-never-refer-to-each-other.md) describes? Are the needs that the sets state for the project met? Does it reach the user's goal?
4. The user accepts the draft.
5. Only then is the seed generated. `sw-seed-audit` also checks the result against the draft.

Step 7 of the plan thus becomes "design, advise, generate": a design skill with its advisor, and a generating skill. The accepted draft connects them. The advisors are agents of their own in the workshop set ([D26](D26-sets-carry-their-flow-without-rules.md), [D27](D27-skills-use-their-own-agents.md)).

Skills with a procedure are made the same way ([D36](D36-skills-start-from-a-draft.md)).

## Reasons

EGM (the elephant-goldfish-model repository) is the model.
