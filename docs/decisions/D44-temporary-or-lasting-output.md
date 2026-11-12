# D44: Temporary or lasting output

Status: accepted

## Decision

When a set is designed, each output is fixed as temporary or as a lasting result.

Temporary are:

- scratch files of a run (temp directory, deleted at the end);
- state and hand-overs in the set (flow directory with a fixed prefix, deleted by the last skill, [D38](D38-skills-leave-only-their-result.md)).

A lasting result is, for example, an ADR, a design document, a kept brief, or a file for another machine. It is worked out in the temp directory. A last step of its own writes it to its place: the place the project's instructions name (for example `docs/adr/`). Otherwise the skill asks, with a proposal it has found. Only there is it the skill's result, and the skill's description names it (I16).

The seed handles hand-overs between sets; how it does that is still open in the source.

For `sw-workshop`: at the release gate of `sw-skill-brainstorm` there is an added choice "keep brief". Then the skill writes the brief to a place the user picks.

## Reasons

EGM (the elephant-goldfish-model repository) is the model. Its working files are plain Markdown files. A closing step writes lasting documents to `docs/designs/` or to a chosen place, and enters them in `SITEMAP.md`. Unlike EGM, our working files are not in the working directory ([D38](D38-skills-leave-only-their-result.md)).
