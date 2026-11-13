# D32: The review cycle

Status: accepted

## Decision

A skill is improved in a review cycle. The plan review of the blueprints in claude_orchestration is the model.

- The first pass is a full audit.
- Each later pass is a follow-up pass: one auditor gets the findings of the previous pass, the fixes made since, and the diff of the revision. It checks that each fix resolves its finding, checks new or changed text against every item, and reads unchanged text only where the changed text refers to it.
- Each `fail` and each `warn` that the agent agrees with is fixed; any other is held for the user, who fixes it or accepts it explicitly.
- The audit loop repeats until a pass leaves no `fail` and no `warn` open that the agent agrees with. `info` alone does not start a pass.
- At the end, the user gets the `info` findings of the last pass, together with the held findings. What the user takes is worked in and gets a follow-up pass on the diff. The rest is dropped or accepted.

So the user decides when to stop, and no fix stays unchecked (run 5 → 6).

`sw-skill-review` runs the cycle (step 5c, [D37](D37-skill-work-in-chained-skills.md)), not the audit, because the audit only reports. The auditor is an agent of its own ([D27](D27-skills-use-their-own-agents.md)).

Requirements for `sw-skill-review`:

- Findings it thinks are wrong, or whose fix needs a trade-off, it collects and presents at the end ([D30](D30-the-guide-for-asking-lives-in-the-set.md)).
- The state of the loop is in a file (C5, [D26](D26-sets-carry-their-flow-without-rules.md)), because the cycle runs until a condition holds.
- The cycle needs only the workshop set ([D13](D13-a-skill-belongs-to-one-set.md)), no seed.

The self-test of `sw-skill-audit` follows the cycle from run 7 on (`tests/sw-skill-audit/expectations.md`). An accepted finding is kept in the record of the review cycle, a work document ([D56](D56-workspace-in-the-project.md)), and applies only to that cycle: a later cycle reports it again, and the user decides again.

## Reasons

A full audit finds a different subset on each run (runs 2 to 6 of the self-test). A fix can itself cause a finding (run 6). One auditor per follow-up pass suffices: a diff is small, and every self-test series from run 7 on reached a clean pass with one auditor. EGM (the elephant-goldfish-model repository) runs three reviewers per round, but each round there reads the whole text again.
