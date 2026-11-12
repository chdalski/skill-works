# D7: Check every skill against the specification

Status: accepted

## Decision

When a skill is written or audited, by any skill, it is checked against the specification. This also applies after the specification has changed.

## Consequences

- The specification is available as Markdown at `specification.md` on agentskills.io. A check can get the current version and find changes.
- Step 3 of the plan implemented this: `check_spec.py` compares a copy of the specification in the skill with the current version on each run. It reports "unchanged", "changed" with a diff, or "not checked" when there is no network.
