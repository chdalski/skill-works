# D50: The glossary lists words to avoid

Status: accepted

## Decision

Each term in `docs/glossary.md` names the words to avoid for the same thing, and a section "Ambiguities" resolves words with two meanings in this repository, such as "draft" or "review".

The audit uses a project's glossary where the project's instructions name one: item I5 then also checks that a skill uses the glossary's terms and none of the words it lists to avoid. In skill-works that glossary is `docs/glossary.md`. In another project the check applies only if the project has a glossary of its own; the shipped audit assumes nothing of skill-works.

The root `CLAUDE.md` says when agents read and change the glossary, the decisions, and the rules for sets.

## Reasons

A definition alone does not keep a term consistent; a list of the words to avoid does. mattpocock/skills keeps its glossary this way. A case in point: the glossary and `skill-sets/CLAUDE.md` said "hand-over", while item C6 in `coherence.md` said "handoff".

## Consequences

- C6 changes "handoff" to "hand-over", and I5 gets the glossary clause. Both go into the same review cycle as I17, I18, and the F7 extension.
