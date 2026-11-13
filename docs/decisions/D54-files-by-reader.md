# D54: Files by who reads them

Status: accepted

## Decision

Every file a set writes is one of five kinds. The set's draft assigns each of its files to one kind; the kinds and what holds for each are fixed here.

| Kind | Read by | Examples | Where | Removed by |
|---|---|---|---|---|
| Scratch file of one run | the skill alone, while it runs | intermediate results, script output | a new temp directory | the skill, when the run ends |
| Helper file of a skill | the skill alone, across runs; it holds no state | a snapshot for a diff | a temp directory with a fixed prefix | the skill, when it no longer needs it; if lost, the skill redoes the work |
| Work document | the user, during the flow: reads, comments, accepts | brief, draft, a check report shown at a gate | a directory in the project that the project's instructions name; else a skill that receives no work document asks once, and one that receives a work document takes the directory of that work document | the user |
| Result | the user, other people and agents, after the flow | the finished skill, an ADR, a seed, a design document | where the project's instructions say; else where the user picks | the user |
| Handed-in file | whoever handed it in | a plan the user passes in | where it is; the skill extends it | the user |

The test for one file: does a person read it or want to keep it? Then it is a work document or a result: it stays, and it belongs to the user. Does only a skill read it, and does losing it cost only work? Then it is temporary. The state of a flow is never temporary: it stands in the work document that carries the flow ([D55](D55-no-flow-directory.md)).

A skill never deletes a work document or a result. At the end of a flow it names the work documents that remain, so the user can keep, commit, or delete them.

## Reasons

A reboot emptied `/tmp` (a tmpfs on Linux) and took a draft that was waiting for the user's acceptance with it; temporary files cannot carry work a person still needs. A state directory per user (such as `~/.local/state/`) would survive, but then the skills must clean up after themselves, including after abandoned flows. The elephant-goldfish-model repository writes its briefs, drafts, and reports to the user's working directory, or to a directory a line in the project's instructions names, and leaves them to the user; only helper files of its workers go to a temp directory. Files meant for the user are the user's to keep or remove; files only skills need are the system's to clean up.

## Consequences

- Replaces [D38](D38-skills-leave-only-their-result.md) and [D44](D44-temporary-or-lasting-output.md).
- Guideline item I16 sorts every file a skill writes into these kinds.
- `skill-sets/CLAUDE.md` holds the table above.
- The glossary has "work document".
- skill-works names its directory for work documents in `CLAUDE.md`: `docs/drafts/`.
