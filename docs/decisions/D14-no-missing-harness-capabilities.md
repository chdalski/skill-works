# D14: Do not supply missing harness capabilities

Status: accepted

## Decision

When a harness lacks a capability that a skill set needs, we do not supply it. Users of pi adapt their setup themselves. Skill sets hold no harness code. They name what they need in the `compatibility` field.

The plan first had a set `sw-pi-subagents` for this. That variant is rejected.

## Reasons

For example, pi has no subagent tool in its core. People who use pi often have their own mechanism. A seed that brought a second one could break its configuration.
