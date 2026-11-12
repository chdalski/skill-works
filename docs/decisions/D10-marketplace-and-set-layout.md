# D10: Marketplace and set layout

Status: accepted

## Decision

A marketplace `skill-works` in the repository root lists all sets. Each set is in `skill-sets/sw-<set>/` with `.claude-plugin/plugin.json`. Its skills are in `skills/`. Each set is a plugin of its own.

The directory was first named `sets/`. It was renamed to make it easier to understand.

## Reasons

Each set must stay installable alone.
