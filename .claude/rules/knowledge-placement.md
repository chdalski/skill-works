# Where Knowledge Goes

skill-works builds skills, sets, and seeds, and its own
setup follows the same model. Each piece of knowledge has
one place, chosen by when it is needed:

| Needed | Place |
|---|---|
| Only while a skill does its job | The skill's `references/`, or its set's `shared/` when several skills of the set need it |
| In every session, whatever the task | A rule in the seed (`.claude/rules/`), kept short |
| Facts about this repository: purpose, layout, language, references | `CLAUDE.md` |

Auto memory is off in this repository. Knowledge that should
outlast a session goes into one of these three places, also
when the user asks to remember something.

## Why

A rule loads into every session. Detail that only one task
needs then costs context everywhere and dilutes the rules
that must always hold. A skill's references load only when
the skill runs, so they can be thorough. Facts about the
repository change with the repository, not with how the
work is done.

## How to Apply

- Before adding a rule, ask whether it must hold in sessions
  that never touch its subject. If not, it belongs to a
  skill.
- Keep one source. A rule that needs detail names the skill
  that carries it instead of repeating the detail.
- When knowledge moves to another place, remove it from the
  old one.
