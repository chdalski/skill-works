# D24: What `sw-skill-create` works on

Status: amended by [D46](D46-targets-in-harness-terms.md)

## Decision

`sw-skill-create` creates new skills and revises existing ones. `sw-skill-audit` stays usable everywhere.

What changed: this decision first limited `sw-skill-create` to skill-works and its forks. The target skill had to be in `skill-sets/<set>/skills/` of a repository with `.claude-plugin/marketplace.json`; otherwise the skill stopped. [D46](D46-targets-in-harness-terms.md) replaces this limit. A flow now works on one of three targets: a skills directory, an existing plugin, or a new plugin.

## Reasons

`sw-skill-audit` only checks, so it can run anywhere.
