# D8: The `sw-` prefix

Status: accepted

## Decision

Our sets and the skills in them both carry the prefix `sw-`: the set `sw-workshop`, the skill `sw-skill-audit`. In Claude Code the skill is called as `/sw-workshop:sw-skill-audit`.

The skill keeps its own prefix. There are no names for each harness ([D2](D2-harness-independent-sets.md)).

## Reasons

Not every harness shows plugin skills under the plugin's name. For example, pi calls skills as `/skill:<name>`, without the name of the package.
