# D6: Specification fields first

Status: accepted

## Decision

Skills use the fields of the Agent Skills specification. A field of one harness is allowed only where the skill does not work without it. The skill then gives the reason.

Seeds target only Claude Code. pi is a test harness. It shows that the skills do not depend on Claude Code. pi is not a target for seeds.

Step 3 of the plan made this stricter: "specification first, without a bias to one harness". Step 4 limited pi to a test harness.

## Consequences

- The reference validator `skills-ref` rejects every field outside the specification. A skill with harness fields fails there. Our check must judge such fields for each harness.
