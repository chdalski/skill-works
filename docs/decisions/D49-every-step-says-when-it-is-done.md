# D49: Every step says when it is done

Status: accepted

## Decision

The shared instruction guideline (`shared/instructions.md` of the workshop set) gets a new item, I18: every step of a procedure ends with a condition the agent can check, such as "Done when each topic has an answer in `brief.md`, or the user said it does not apply". A check is something observable: a file exists, a list is complete, a command printed a given line, the user answered. A step whose end is its single action, such as "write file X", needs no separate condition.

The item applies to every instruction file with a procedure, rules included. `sw-skill-audit` checks it. `sw-skill-create` writes the conditions from the "Exits" column of the accepted draft.

## Reasons

A vague end lets the agent stop early: a step looks done, and the next one builds on a gap. The skills of mattpocock/skills end each step with "Done when …" for this reason. Our guideline had I3 (mandatory steps), I4 (bright lines) and C12 (the whole skill says when it is done), but no item for the end of each step.

## Consequences

- I18 goes into the same review cycle as I17 (words the reader knows) and the F7 extension for `../../agents/`.
- Seed items of the guideline start at I19 ([D29](D29-instruction-guideline-split-by-scope.md)).
