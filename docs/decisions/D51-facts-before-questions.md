# D51: Look up facts, ask for decisions

Status: accepted

## Decision

The guide for asking (`.claude/rules/asking-the-user.md` and its identical copy `shared/asking.md` in the workshop set) gets a first rule under "Questions": look up what you can find yourself, in the code, the files, the docs, before you ask; ask the user only for what they decide or what only they know, such as intent, preferences, and limits.

`sw-skill-brainstorm` applies it when it clarifies: it first looks for existing skills, plugins, scripts, and skills directories, shows what it found, and asks only for the choice and for what it cannot see.

## Reasons

A question about a fact the agent could find costs the user a round, and the answer is often worse than the lookup. mattpocock/skills states the rule in its grilling skill: "Finding facts is your job, never the user's."

## Consequences

- The rule and its copy stay identical ([D30](D30-the-guide-for-asking-lives-in-the-set.md)).
- The copy of the same rule in the claude_orchestration repository is not changed by this decision.
