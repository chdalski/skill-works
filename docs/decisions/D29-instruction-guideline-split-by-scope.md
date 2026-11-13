# D29: The instruction guideline is split by scope

Status: accepted

## Decision

The guideline for instructions is split into files by scope. It is not marked by scope inside one file.

- `shared/instructions.md` holds what applies to all instruction files: I1, I2, I3, I4, I7, and the cores of I5 and I12.
- `shared/instructions-skills.md` holds what applies only to skills: I6, I8, I9, I10, I11, and the skill parts of I5 and I12.
- `instructions-seeds.md` holds what applies only to seed files: the cost in every session ([D19](D19-knowledge-placement.md)), and `paths:` set correctly. At first it lives with `sw-seed-audit`. It moves to `shared/` when the seed generator needs it ([D23](D23-shared-files-in-shared.md)).

I1 to I12 keep their IDs. Since step 5b:

- I13 and I14 are the skill parts of I5 and I12.
- I15 is asking the user ([D30](D30-the-guide-for-asking-lives-in-the-set.md)).
- I16 is the place of every file a skill writes ([D56](D56-workspace-in-the-project.md)).
- Seed items follow from I17 on.

The terms of Claude Code are in the shared I5. They apply to every file written for one harness only: to seeds and to such skills. So the list exists only once.

## Reasons

Each audit reads only what fits its object. Without the split, I6 and I10 would report wrongly on seed rules.
