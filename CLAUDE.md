# skill-works

A workshop for agent skills and the setups built from them.

## Model

- **Skill** — a directory with a `SKILL.md` per the Agent
  Skills specification. Every skill made in this repository
  is part of a skill set; the workshop can also make single
  skills elsewhere.
- **Skill set** — skills that do one job together, with
  their shared files and agents. A set ships as a Claude
  Code plugin, installed per project from this repository,
  and is improved only here.
- **Seed** — the setup a skill-works skill generates for one
  project: rules and working methods that link sets,
  settings, and the activation of the set plugins. It holds
  no skills. A project gets its seed once, as it is, and
  improves it in place with a bundled maintenance set;
  nothing flows back to this repository.

Every other term, and how this repository uses it, is in
`docs/glossary.md`; a new term goes there before it appears
in a skill or a rule. Decisions, with their reasons, are in
`docs/decisions/`; a new one gets a file there before skills
or rules rely on it.

The rules every set and every skill follows — layout,
input and output, temporary files, hand-overs — are in
`skill-sets/CLAUDE.md`. New skills follow them and this
repository's guidelines, and pass its audits: for their
form, for the quality of their instructions, and for
coherence — a skill's steps, transitions, gates, and state
must fit together.

## Components

| Path | Purpose |
|---|---|
| `.claude-plugin/marketplace.json` | Marketplace `skill-works`: lists every set as a plugin for Claude Code |
| `package.json` | pi package manifest, for testing sets in pi: declares the skills of every set |
| `docs/glossary.md` | The terms this repository uses and what each one means |
| `docs/decisions/` | The decisions that shape skill-works, one file each, with status and reasons |
| `skill-sets/CLAUDE.md` | Rules for every set and every skill: layout, input and output, temporary files, hand-overs |
| `skill-sets/sw-workshop/` | Workshop set: the tools this repository builds skills and seeds with; holds `sw-skill-audit` so far, and in `shared/` the files its skills share: the instruction guidelines and the guide for asking |
| `tests/pi.md` | How to load, run, and update a set in pi when testing it there |
| `.claude/` | This repository's own setup: its rules, and settings that load the sets from this checkout |
| `.claude/rules/skill-naming.md` | Sets and skills made here carry the prefix `sw-` |
| `.claude/rules/knowledge-placement.md` | Where knowledge goes: a skill's references, a rule, or this file |
| `.claude/rules/asking-the-user.md` | How to ask and explain: collected questions, one per dialog, each with purpose, a concrete example, and what each option means |

## Language

Everything written to this repository is in English —
skills, rules, seeds, tests, docs, and commit messages —
regardless of the language the user chats in. Translate
quoted non-English material, such as user feedback or notes
from a target project, before it goes into a file or a
commit message. Chat replies may use the user's language.

## Conventions

- This repository uses its own sets: `.claude/settings.json` enables them from the local marketplace, which loads them in place from `skill-sets/`, so an edit takes effect after `/reload-plugins` or in a new session without a reinstall
- Seeds target Claude Code only; pi is a test harness that keeps skills independent of Claude Code, not a seed target — pi lacks defaults such as a subagent tool, and a seed that added them could break a user's own setup
- A new set needs an entry in `marketplace.json` for Claude Code; for pi, `package.json` already covers it through the glob `./skill-sets/*/skills`
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
