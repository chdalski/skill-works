# D24: What `sw-skill-create` works on

Status: accepted

## Decision

`sw-skill-create` creates new skills and revises existing ones. `sw-skill-audit` stays usable everywhere.

A flow works on one of three targets: a skills directory, an existing plugin, or a new plugin ([D46](D46-targets-in-harness-terms.md)).

## Reasons

`sw-skill-audit` only checks, so it can run anywhere.
