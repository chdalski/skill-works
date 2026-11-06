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
- Setups, called seeds, are assembled from audited skills
  instead of being written as one large instruction file.
- A seed maintains itself: it brings the skills and
  guidelines to audit and improve itself inside the project
  that copied it.

## What it does

- **Design skills.** New skills follow shared guidelines and
  pass audits: for their form, for the quality of their
  instructions, and for coherence — whether a skill's steps,
  transitions, gates, and state fit together.
- **Assemble seeds.** A seed is a ready-made initial setup
  for a coding agent — `.claude/` for Claude Code, `.pi/`
  for pi — composed of skills, agents, rules, and settings.
  You copy a seed into a project once. It brings the skills
  it needs to improve itself there, so the project never has
  to come back here for updates.

## Eat your own dog food

skill-works builds itself. Its first skills are the tools
for designing and auditing skills. Once they exist, every
further skill, and this repository's own setup, is made and
checked with them. This repository runs on its own seed:
`.claude/` links to `seeds/skill-works/.claude/`.

## Status

Early. Nothing here is ready to use yet.

## License

[MIT No Attribution](LICENSE): copy a seed into your project
without carrying a license notice along.
