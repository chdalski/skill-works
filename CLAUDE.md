# skill-works

A workshop for agent skills and the setups built from them.

## Model

- **Skill** — a directory with a `SKILL.md` per the Agent
  Skills specification. A skill ships only as part of a
  skill set; it is never delivered alone.
- **Skill set** — skills that do one job together, with
  their personas and resources. One skill text serves every
  harness; each harness gets its own manifest and thin
  adapters. A set ships as a plugin of the harness,
  installed per project from this repository, and is
  improved only here. Sets never refer to each other.
- **Seed** — the setup a skill-works skill generates for one
  project: rules and working methods that link sets,
  settings, and the activation of the set plugins. It holds
  no skills. A project gets its seed once, as it is, and
  improves it in place with a bundled maintenance set;
  nothing flows back to this repository.

New skills follow this repository's guidelines and pass its
audits: for their form, for the quality of their
instructions, and for coherence — a skill's steps,
transitions, gates, and state must fit together.

## Components

| Path | Purpose |
|---|---|
| `.claude-plugin/marketplace.json` | Marketplace `skill-works`: lists every set as a plugin |
| `skill-sets/sw-skills/` | Set for designing and auditing skills; holds `sw-skill-audit` |
| `.claude/` | This repository's own setup: its rules, and settings that load the sets from this checkout |
| `.claude/rules/skill-naming.md` | Sets and skills made here carry the prefix `sw-` |

## Language

Everything written to this repository is in English —
skills, rules, seeds, tests, docs, and commit messages —
regardless of the language the user chats in. Translate
quoted non-English material, such as user feedback or notes
from a target project, before it goes into a file or a
commit message. Chat replies may use the user's language.

## Conventions

- Facts about this repository go into this file; how work is done here — rules, settings — goes into `.claude/`
- This repository uses its own sets: `.claude/settings.json` enables them from the local marketplace, which loads them in place from `skill-sets/`, so an edit takes effect after `/reload-plugins` or in a new session without a reinstall
- Every set carries its own `LICENSE` (MIT) and names it in its `plugin.json`: a set is installed without the repository root, and MIT requires the notice in every copy
- Seeds carry no license notice: what the seed generator writes into a project is MIT-0, so the project can use and change it freely
- Once a skill for a job exists here, this repository's own work uses it — the first skills are written by hand and then audited with themselves
- To try a set in a headless run (`claude -p`), load it with `--plugin-dir skill-sets/<set>`: a `-p` run does not load a marketplace that only the project settings declare
- CLAUDE.md files and rule files target under 200 lines — agent adherence degrades beyond that threshold
- CLAUDE.md files, rules, and agent files stay static — no dates, counters, or versions — because they sit in the cached prompt prefix

## References

- [Agent Skills overview](https://agentskills.io/home) — the open standard; its "For skill creators" pages below describe how to write skills
- [Agent Skills specification](https://agentskills.io/specification)
- [Skill creation: best practices](https://agentskills.io/skill-creation/best-practices)
- [Skill creation: optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Skill creation: evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)
- [Skill creation: using scripts](https://agentskills.io/skill-creation/using-scripts)
- [Claude Code documentation](https://code.claude.com/docs)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins/components)
