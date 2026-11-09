# Skill and Set Naming

Every skill set and every skill made in this repository
carries the prefix `sw-`. A set's prefix goes on its
directory under `sets/` and on the `name` in its plugin
manifest; a skill's prefix goes on its directory and on the
`name` field in its `SKILL.md` frontmatter. The set
`sets/sw-skills/` holds `skills/sw-skill-audit/`, which
Claude Code invokes as `/sw-skills:sw-skill-audit`.

## Why

In Claude Code a skill from a plugin appears under the
plugin's name, so the set prefix gathers all our skills
under `/sw-`. Not every harness adds that namespace — some
show plugin skills by their own name alone — so the skill
keeps its prefix too, and its name stays distinct from a
project's own skills, other plugins' skills, and the
harness's built-in commands everywhere. One skill text
serves every harness, so the name cannot differ by harness.

## How to Apply

- Prefix every new set and every new skill, including the
  ones this repository uses itself.
- Name a set's directory like the set, as a skill's
  directory is named like the skill.
- A skill or set taken over from elsewhere gets the prefix
  when it moves here, and every reference to it changes with
  it. An unchanged reference points to a name that no
  longer exists.
- Prefix a skill's directory and `name` together. The Agent
  Skills specification requires `name` to match the
  directory name.
- The prefix counts toward the 64-character limit for a
  skill's `name`.
- Refer to other skills by their full prefixed name.
