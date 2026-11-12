# D28: The check groups of `sw-seed-audit`

Status: accepted

## Decision

At first, `sw-seed-audit` checks four groups. The group letters are names of these groups, not guideline items.

- Group A: form, by script. Static files, length, frontmatter, references, a valid `settings.json`.
- Group B: instructions, for each file.
- Group C: coherence across the files. Contradictions, stale references, duplicates, values from `settings.json`, documentation.
- Group F, the simple part: the sets the seed names are enabled, and the skills it names exist. For now only for sets that are on the local disk.

Later groups come when a seed needs them:

- Group D: agents in the seed.
- Group E: cache and hooks.
- The chaining of sets (step 6 of the plan).
- The comparison with a draft ([D31](D31-seeds-draft-advice-acceptance.md), step 7).

Each group has a reference file of its own. So a group can be added with one file, one entry in the procedure, and expectations in the test bench. The report names the groups it did not check.

## Reasons

Without a seed that has hooks or agents, there are no expectations to test groups D and E against, and no way to calibrate them. Also, each group is one more reference that the audit must read.
