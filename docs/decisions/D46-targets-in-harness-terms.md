# D46: Targets in the harness's terms

Status: accepted

## Decision

The workshop needs to know nothing about sets to make a skill. The target of a flow is one of three, in the terms of the harness:

- a skills directory that the harness loads (in Claude Code `.claude/skills/` in the project, or `~/.claude/skills/`);
- an existing plugin in the repository;
- a new plugin that the flow creates.

"Skill set" is a term of skill-works. Another project does not know it, so it is in no shipped skill text.

Which conventions a new skill follows (prefix, shared files, license file, marketplace entry) comes from the project's instructions. In skill-works it comes from `skill-sets/CLAUDE.md`.

The brainstorm asks for the target while it clarifies. The brainstorm itself runs everywhere, also in a fresh repository without sets.

The installed plugin is never a target. It is a copy in the plugin cache, which an update overwrites.

A single skill counts its own directory as its set (I16). It brings what it needs, for example the guide for asking in its own `references/` instead of in `shared/` (I15).

In skill-works itself, every skill still belongs to a set.

This decision replaces the limit of [D24](D24-sw-skill-create-scope.md), which [D37](D37-skill-work-in-chained-skills.md) also applied.
