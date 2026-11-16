# D57: A plugin's terms live in the plugin

Status: accepted

## Decision

A term that the skills of a set use is defined in the set's `shared/terms.md`, which ships with the set's plugin. `docs/glossary.md` keeps a row for it with "→ terms.md" and the words to avoid, and defines in full only the terms of this repository: seed, skill set, test bench, and the others no shipped skill uses.

## Reasons

A plugin runs in other projects from its installed copy, where `docs/glossary.md` does not exist; guideline item I17 needs every term a skill uses defined in the skill or its plugin's shared files. Defining the same terms in both files gave each two homes, which [D53](D53-branch-test-and-one-home.md) rules out: the two wordings had already drifted apart, for example "repository root", which fell back to the working directory in one file and to the file's directory in the other.

## Consequences

- The glossary points to `skill-sets/sw-workshop/shared/terms.md` for the workshop plugin's terms; what only the glossary said about them moved into `terms.md`.
- [D50](D50-glossary-avoid-lists.md) holds unchanged: every row of the glossary keeps its words to avoid, and the audit's item I5 reads them there.
- The root `CLAUDE.md` says where a new term goes.
- Every further set brings its own `shared/terms.md`, like its workspace script ([D56](D56-workspace-in-the-project.md)); the glossary then names the set in its pointer.
