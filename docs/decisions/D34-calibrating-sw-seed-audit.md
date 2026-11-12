# D34: Calibrating `sw-seed-audit`

Status: accepted

## Decision

In step 5d, `sw-seed-audit` is calibrated on three frozen objects under test:

1. The seed of skill-works as the clean case, as it is in step 5d: `CLAUDE.md`, the three rules, and `settings.json`. The rules of step 5a come only after that.
2. A seed with built-in faults, at least one for each of the check groups A, B, C, and F ([D28](D28-sw-seed-audit-check-groups.md)).
3. An extract from the direct-review blueprint in claude_orchestration: `CLAUDE.md` and three to five rules. It is frozen before a commit that closed gaps in the text, for example `a634df5`. Its expectations come from the message of that commit, not from guesses.

Skills and agents stay out ([D5](D5-a-seed-per-project.md), [D28](D28-sw-seed-audit-check-groups.md)).

In step 7, the first generated seed comes in as a fourth object under test. There, no fail and no warn are expected, because the seed generator must not generate a faulty seed. A finding thus shows a fault in the generator or a false alarm of the audit. Both get fixed.

## Reasons

For object 3: in step 3, the most valuable finding came from a real object under test (a C5 fail in `ensure-ai-dirs`). Nobody builds in such a fault on purpose.
