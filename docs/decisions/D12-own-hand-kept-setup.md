# D12: skill-works keeps its own setup by hand

Status: accepted

## Decision

For now, skill-works has its own `.claude/`, kept by hand. It does not come from a seed. It enables its sets through the local marketplace with the path `.` and loads them directly from `skill-sets/`.

This is stage 1 of two. In stage 2, once the seed generator exists (step 7 of the plan), we generate the setup of skill-works with it as an acceptance test. If the result matches the hand-kept setup, skill-works becomes its own seed.

## Consequences

- A plugin from a local path loads without a copy. A change in `skill-sets/` takes effect without a reinstall.
