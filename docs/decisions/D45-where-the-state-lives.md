# D45: Where the state lives

Status: accepted

## Decision

Where the state of a procedure lives is decided for each skill by the criterion of C5. A procedure needs a file in its temp directory when nothing limits its length:

- it waits for the user between steps,
- it repeats steps for each file, task, or round, or
- it runs until a condition holds.

Any other procedure may keep its state in the conversation.

The draft shows the choice in the "Reads / writes" column of the procedure model, and the advisor checks it.

Examples: `sw-skill-audit` keeps its state in the conversation (one pass). `sw-skill-brainstorm` and `sw-skill-review` keep it in files.

## Reasons

`egm-review-loop` of EGM (the elephant-goldfish-model repository) keeps the settled findings only in the conversation, although it waits for the user and repeats rounds. After a compaction, disputed findings would count as open again.

## Consequences

- The rules of [D41](D41-run-modes.md) to D45 are in `skill-sets/CLAUDE.md`, with decision tables.
