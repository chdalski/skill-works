# D48: Tested phrases for common actions

Status: accepted

## Decision

`sw-workshop` gets a collection of tested phrases for actions that many skills need: launch a fresh subagent, start another skill, ask the user, create a temp directory, refer to the skill's own directory. It is in `shared/harness-phrases.md`.

Each entry has three parts:

- the action;
- a harness-neutral phrase that works in every harness;
- the evidence: in which harness it was tested, and how.

There are no forms for each harness. A note on one harness is added only when a test shows that the harness misreads the neutral phrase. The note then has its evidence and is as short as possible.

A skill leaves the limits of a harness, for example how many options a question tool takes, to the harness, unless it needs a specific layout.

- `sw-skill-create` copies the phrases into new skills, because a skill in another project cannot refer to files of the workshop.
- `sw-skill-audit` accepts them as a valid form at I13.
- The advisor checks in the draft where a phrase is needed.

It is not a set of its own, because sets do not refer to each other ([D3](D3-sets-never-refer-to-each-other.md)).

The file comes with step 5c.
