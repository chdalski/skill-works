# D55: No flow directory

Status: accepted

## Decision

The skills of a flow hand each other work documents, not a temp directory. There is no flow directory.

- **Hand-over:** the next skill gets the path of the work document it works from: `sw-skill-design` the brief, `sw-skill-create` the accepted draft, `sw-skill-review` the draft or the skill's path, and, back to design, the review record.
- **State of the flow:** the fields every skill needs — target, skill, run mode, status, counters — stand in the header of the work document that carries the flow at that point. The templates in `shared/templates/` define them.
- **Finding it again:** every resume command names the work document. Without one, the skill looks in the work-document directory for the open document of the skill it works on.
- **Work-document directory:** where the project's instructions name none, a skill that receives no work document asks for it once; a skill that receives one takes the directory of that work document.
- **Temporary files** are only a skill's own helpers: scratch files of one run, and files that must outlive a run but hold no state, such as a snapshot for a diff. Losing them costs only work.

## Reasons

State in a temp directory must be rebuildable from the work documents, since a reboot can empty the temp facility ([D54](D54-files-by-reader.md)). Such state is a copy of what the work documents hold: a second place for the same state, which C5 rules out. The draft of `sw-skill-review` showed the cost: advisor passes 3 to 6 found one edge case after another where the flow directory and the review record disagreed, until the record became the only state. The flow directory came from [D33](D33-temporary-files.md) and [D38](D38-skills-leave-only-their-result.md), when nothing but the result was allowed to stay in the project; after D54, nothing was left that it alone could hold.

EGM (the elephant-goldfish-model repository) hands over the same way: its skills pass plain files in the project and keep no shared temp directory.

## Consequences

- [D33](D33-temporary-files.md), [D41](D41-run-modes.md), [D45](D45-where-the-state-lives.md) and [D54](D54-files-by-reader.md) state the rules that follow from it: helper files instead of machine state of a flow, the run mode in the document's header, state in a work document.
- Guideline item I16 and coherence item C5 allow no state in a temp directory. The change gets a follow-up pass on `sw-skill-audit`.
- The glossary has no "flow directory"; "hand-over", "state" and "temporary file" follow this decision.
- `skill-sets/CLAUDE.md` follows it in its file table and its hand-over rules.
- The drafts of `sw-skill-brainstorm` and `sw-skill-review` keep the flow's fields in the headers of the brief, the draft, and the review record.
