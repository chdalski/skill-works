# skill-works

A workshop for agent skills and the setups built from them.

## Why

Coding-agent setups grow by hand: one long instruction file,
a rule added after each incident, skills nobody checks. They
contradict themselves in ways no single reader notices, and
every project that copied one drifts away from where it came
from.

## Goal

skill-works makes the skill the building block of an agent
setup:

- Every skill is designed against shared guidelines and
  audited for its form, the quality of its instructions, and
  its internal coherence.
- Skills ship in skill sets, installed as plugins of your
  coding agent and updated like any plugin.
- A project's own setup, its seed, is generated once from
  rules that link the sets it uses, and then maintained in
  the project with a bundled maintenance set.

## How it fits together

- **Skill set** — skills that do one job together, written
  to the Agent Skills specification so the text does not
  depend on one coding agent. Sets never depend on each
  other.
- **Seed** — the `.claude/` a project gets: rules and
  working methods that link the sets, settings, and the
  activation of the set plugins. It holds no skills. Seeds
  target Claude Code only.

## Use a set

In Claude Code:

```sh
claude plugin marketplace add chdalski/skill-works
claude plugin install sw-workshop@skill-works --scope project
```

| Set | Skills |
|---|---|
| `sw-workshop` | `/sw-workshop:sw-skill-audit` — audits a skill for its form, the quality of its instructions, and the coherence of its procedure; `/sw-workshop:sw-skill-review` — reviews a skill in a cycle of audits and fixes until you accept it |

## Eat your own dog food

skill-works builds itself. Its first skills are the tools
for designing and auditing skills. Once they exist, every
further skill is made and checked with them. This repository
loads its own sets straight from `skill-sets/`, so a change is
live in the next session.

## Status

Early. Nothing here is ready to use yet.

## License

- **Sets and everything else in this repository:**
  [MIT](LICENSE). Each set carries its own copy of the
  license, so an installed set keeps its notice.
- **Seeds**, the files a project gets from the seed
  generator: [MIT No Attribution](https://spdx.org/licenses/MIT-0.html).
  A project uses and changes its seed without carrying a
  license notice along.
