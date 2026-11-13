# D36: Skills with a procedure start from a draft

Status: accepted

## Decision

A skill with a procedure is made like a seed ([D31](D31-seeds-draft-advice-acceptance.md)).

1. First a draft of the procedure is made, as a work document ([D54](D54-files-by-reader.md)) in the project's directory for work documents. It holds the steps, inputs, result, acceptances, where the state is kept, and the hand-over to the next skill ([D35](D35-own-skill-or-phase.md)). It has the shape of the procedure model that the audit builds.
2. An advisor checks it against C1 to C12.
3. The user accepts it.
4. Only then is `SKILL.md` written.

In the review cycle, the audit also checks the text against the accepted draft.

A skill without a procedure, that is pure background knowledge, needs no draft.

Seed and skill thus use the same way and the same advisor.

## Reasons

Faults in a procedure are cheap to fix in the draft. In the finished text each one costs a follow-up pass. In the self-test of `sw-skill-audit`, a part of the findings concerned the procedure (C5, C6).
