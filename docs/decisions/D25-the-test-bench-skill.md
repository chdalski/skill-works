# D25: The test bench skill

Status: accepted

## Decision

The test bench skill tests audits and skills that generate something with the same loop: freeze the inputs, write down the expectations before the run, run in a fresh context, compare, classify, calibrate.

- For audits, the expectations are findings that must come or must not come.
- For skills that generate something, the expectations are: a realistic request with a described result, assertions that can be checked after the first run, a review by a person, and a comparison run without the skill (agentskills.io, "Evaluating skills").

The tests stay in `tests/`, outside the sets.

## Reasons

The objects under test must not ship with a set.
