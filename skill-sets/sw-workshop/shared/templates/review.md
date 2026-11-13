---
skill-path: none
root: none
draft: none
reason: none
closes: none
stop-at: none
status: review:auditing 1
---

# Review record: <skill>

The record of one review cycle of the skill at `skill-path`.
The header above is the cycle's state; `sw-skill-review` reads
it to resume. Header fields:

- `skill-path`: the absolute path of the reviewed skill.
- `root`: the absolute repository root the audit treats as
  the project.
- `draft`: the absolute path of the accepted draft, or `none`.
- `reason`: the earlier record this cycle answers, or `none`.
- `closes`: the records this cycle replaces and deletes,
  separated by commas, or `none`.
- `stop-at`: the pass count at which the audit loop stops for
  the user, or `none` until the first pass sets it.
- `status`: `review:<step> [<pass>]` while the cycle is open;
  `handed-back` once it is handed back to sw-skill-design.

The record is a work document in `work/` of the workspace.
When the user has accepted the result, `sw-skill-review`
deletes it, together with the cycle's draft and brief.

## Passes

<!-- One entry per pass, appended in order:
### Pass <n> — full audit | follow-up pass (<why>)
Findings, condensed: <file>:<line> <grade> <item> — "<quoted place>" — <issue> — fix: <fix>
Churn: <the finding and the fix it would undo> | none
Fixes after this pass: <finding> → <what changed>
-->

## Sorted

<!-- One entry per finding:
- pass <n>, <item>, "<quoted place>": <agreed | disputed | trade-off | info> — <reason> — <open | fixed | taken | accepted | dropped>
A finding a later pass reports again under the same item and quoted place updates its entry.
-->

## Accepted

<!-- - <item>, "<quoted place>": <reason> -->

## Decisions

<!-- One entry per user decision and per change of stop-at or draft:
- pass count <n>: <question or change> — <answer>
-->

## Final state

<!-- Written only at a hand-back to sw-skill-design:
"handed back to sw-skill-design: <command>", what is open,
and how to see the changes: <for example git diff <paths>>.
-->
