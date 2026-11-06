# skill-works

A workshop for agent skills and the setups built from them.
It does two things:

1. **Design skills.** New skills follow this repository's
   guidelines and pass its audits: for their form, for the
   quality of their instructions, and for coherence — a
   skill's steps, transitions, gates, and state must fit
   together.
2. **Assemble seeds.** A seed is a ready-made initial setup
   for a coding agent (`.claude/`, `.pi/`), composed of
   skills, agents, rules, and settings. A project copies a
   seed once. The seed carries the skills it needs to
   improve itself inside that project, so the project never
   comes back to this repository for updates.

skill-works builds itself: it runs on its own seed, and that
seed is made and audited with the skills made here.

## Components

| Path | Purpose |
|---|---|
| `.claude/` | Symlink to `seeds/skill-works/.claude/` — this repository runs on its own seed |
| `skills/` | Skill library — the single source of every skill |
| `seeds/` | Seeds assembled from the library |
| `seeds/skill-works/` | The seed this repository runs on |

## Skill Naming

Every skill made in this repository carries the prefix `sw-`,
on its directory and on the `name` field in its `SKILL.md`
frontmatter: `skills/sw-implement/` with `name: sw-implement`,
invoked as `/sw-implement`. A seed copies these skills into a
target project, where they sit next to the project's own
skills, skills from plugins, and the commands built into the
harness; the prefix keeps the names apart and shows which
skills came with the seed.

- Prefix every new skill, including the ones this repository
  uses itself.
- A skill taken over from elsewhere gets the prefix when it
  moves here, and every reference to it changes with it — an
  unchanged reference points to a name that no longer exists.
- Prefix the directory and `name` together: the Agent Skills
  specification requires `name` to match the directory name.
- The prefix counts toward the 64-character limit for `name`.
- Refer to other skills by their full prefixed name.

This section lives here, not in a rule under `.claude/`,
because `.claude/` is the seed: a project that uses the seed
to make its own skills names them its own way.

## Language

Everything written to this repository is in English —
skills, rules, seeds, tests, docs, and commit messages —
regardless of the language the user chats in. Translate
quoted non-English material, such as user feedback or notes
from a target project, before it goes into a file or a
commit message. Chat replies may use the user's language.

## Conventions

- Skills carry the prefix `sw-` (see Skill Naming)
- What applies only to this repository goes into this file, never into `.claude/` — everything under `.claude/` ships with the seed
- Once a skill for a job exists here, this repository's own work uses it — the first skills are written by hand and then audited with themselves
- A seed links its skills to the library instead of copying them, so an edit made through `.claude/` lands in the library; copying a seed into a project resolves the links
- Copying a seed takes only the files Git tracks — Claude Code writes local files such as `settings.local.json` into `.claude/`, and through the symlink they land in the seed directory
- A seed is self-contained: nothing in it refers back to this repository, and nothing syncs between a project's copy and this repository
- CLAUDE.md files and rule files target under 200 lines — agent adherence degrades beyond that threshold
- CLAUDE.md files, rules, and agent files stay static — no dates, counters, or versions — because they sit in the cached prompt prefix

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code documentation](https://code.claude.com/docs)
