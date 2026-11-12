# D32: The review cycle

Status: accepted

## Decision

A skill is improved in a review cycle. The plan review of the blueprints in claude_orchestration is the model.

- The first pass is a full audit. Later, three auditors run in parallel, each with one focus: form and shipped files, instructions, coherence.
- Each fail and each warn is fixed, or the user accepts it explicitly.
- A follow-up pass gets the findings of the previous pass and the diff of the revision. It checks that the revision resolves the findings and does not contradict the unchanged text. It does not read the unchanged text again.
- This repeats until a follow-up pass reports no fail and no warn. Info alone does not start a pass.
- At the end, the user gets the info findings of the last pass, together with the disputed findings. What the user adopts is worked in and gets a follow-up pass on the diff. The rest is dropped.

So the user decides when to stop, and no fix stays unchecked (run 5 → 6).

`sw-skill-review` runs the cycle (step 5c, [D37](D37-skill-work-in-chained-skills.md)), not the audit, because the audit only reports. The auditor is an agent of its own ([D27](D27-skills-use-their-own-agents.md)). At its start it gets its focus or the diff.

Requirements for `sw-skill-review`:

- Findings it thinks are wrong, or whose fix needs a trade-off, it collects and presents at the end ([D30](D30-the-guide-for-asking-lives-in-the-set.md)).
- The state of the loop is in a file (C5, [D26](D26-sets-carry-their-flow-without-rules.md)), because the cycle runs until a condition holds.
- The cycle needs only the workshop set ([D13](D13-a-skill-belongs-to-one-set.md)), no seed.

The self-test of `sw-skill-audit` follows the cycle from run 7 on (`tests/sw-skill-audit/expectations.md`). [D38](D38-skills-leave-only-their-result.md) says where an accepted finding is kept.

## Reasons

A full audit finds a different subset on each run (runs 2 to 6 of the self-test). A fix can itself cause a finding (run 6).
