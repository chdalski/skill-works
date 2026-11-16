# Workshop Terms

The terms the skills of this plugin share. A skill reads this
file at its first step and uses each term as defined here.

## Places and files

- **plugin**: the package a skill ships in, with the other
  skills it ships with and the files they share.
- **target**: where a skill lives or will live: a skills
  directory the harness loads skills from (in Claude Code a
  project's `.claude/skills/` or the user's
  `~/.claude/skills/`); an existing plugin in the repository,
  a package the harness installs, with a `skills/` directory
  (in Claude Code a directory with `.claude-plugin/plugin.json`
  and `skills/`); or a new plugin, named by the path it will
  have, which loads only once the project installs it. A
  skill's path is `<skills directory>/<skill>` or
  `<plugin>/skills/<skill>`, and a given skill path maps back
  the same way: when the parent of `skills/` is a plugin, the
  target is that plugin, else the skills directory.
- **installed copy**: the copy of a plugin that the harness
  keeps for loading, which an update replaces (in Claude Code
  under `~/.claude/plugins/`). A plugin loaded in place from a
  repository is no installed copy. A skill is never changed
  in an installed copy; its source in the repository is.
- **repository root**: the top directory of the repository a
  file lives in (`git rev-parse --show-toplevel` from that
  file's directory), else that directory.
- **workspace**: the directory in the project that holds the
  plugin's work documents and temporary files:
  `.skill-works/`, unless `.skill-works.json` at the top of
  the project names another in its key `directory`. It has its own `.gitignore` (`*`), `work/` for
  work documents, and `temp/` for temporary files. The script
  `shared/scripts/workspace.py` creates what is missing — when
  it writes `.skill-works.json`, a settings file meant to be
  committed, it says `created <path>` on stderr — and is the
  only way a skill finds `work/` and `temp/`, names a new work
  document, lists open ones, and deletes work documents and
  the directories it made in `temp/`; inside such a directory
  the skill's own scripts may replace files. A skill deletes
  its work documents and temporary files only inside the
  workspace.
- **work document**: a file the user reads, comments on, or
  accepts while a flow runs, such as a brief, a draft, or the
  record of a review cycle. It lives in `work/`; the skill
  that ends the flow deletes it after the user's acceptance.
  Any skill of the flow may delete it earlier, once a later
  work document of the same flow replaces it, or when the
  user confirms abandoning the flow or replacing the cycle it
  belongs to, such as a review cycle.
- **temporary file**: a file only skills read, such as a
  scratch file, a diff, or a snapshot. It lives in `temp/`;
  the skill deletes it as soon as nothing needs it.
- **handed-in file**: a file outside the workspace that the
  request, the skill's arguments, or the project's
  instructions name. The skill may change or extend it, but
  not delete or move it unless that is its task and the user
  confirms. Work documents the skills of a flow hand each
  other are not handed-in files.
- **open work document**: a work document whose header
  `status` starts with its skill's prefix, such as `review:`.

## Flow

- **flow**: the work that one or more skills of a plugin do,
  from the first skill that runs to the last one that hands
  nothing on.
- **hand-over**: passing work on to the next skill, a
  subagent, a script, or the user. Between skills, the next
  skill gets the path of the work document it works from.
- **run mode**: how far a flow runs on its own between its
  skills, chosen for each run: **step by step** (each skill
  ends and names the command for the next one) or **straight
  through** (each skill starts the next one). The work
  document that carries the flow holds it in its header.
- **sub-skill**: a skill with its own input and result that
  another skill starts inside its own work and that returns
  to that skill. It can also be started alone.
- **phase**: a part of a skill without its own input or
  result, kept in that skill's `references/` and read when
  the phase starts.
- **gate**: a point where the user decides before the flow
  goes on, such as the readiness gate (the user confirms the
  hypothesis and the target before any advisor runs) and the
  release gate (the user releases the brief to the next
  skill), and acceptance (the user accepts a draft, or the
  result at the end of a flow).

## Briefs

- **brief**: the work document that sw-skill-brainstorm writes
  and sw-skill-design works from, in the shape of
  `shared/templates/brief.md`. Its header holds the flow's
  state.
- **hypothesis**: two or three sentences on what a skill
  does, when it triggers, and what it delivers, confirmed by
  the user at the readiness gate.
- **form**: what a brief proposes: a new skill, a sub-skill,
  or a change of a skill or of a phase of a skill. Not the
  audit's form check.
- **advisor**: the agent `sw-draft-advisor`, which argues
  against a planned skill in a fresh context and reports
  objections.
- **contrarian pass**: one check of a brief by the advisor,
  against the checklist the skill gives it.
- **round**: one contrarian pass on a brief. The rounds are
  counted by the brief's Advice entries; a "no contrarian
  pass" note counts as one.
- **objection**: one reason against a planned skill, with
  what it rests on and what would answer it; it has no grade.
  Objections still
  open when the user releases a brief are accepted open items
  for the next skill.

## Review

- **audit**: one check of a skill against the guideline by a
  fresh agent, the auditor; it reports and changes nothing.
- **finding**: one shortfall an audit reports, graded `fail`
  (the skill does not load, breaks the specification, or its
  procedure goes wrong),
  `warn` (it departs from a guideline without breaking), or
  `info` (worth knowing).
- **review cycle**: a full audit, fixes, and follow-up passes
  until a pass leaves no `fail` and no `warn` open that the
  agent agrees with; then the user decides on the rest.
- **pass**: one audit in a review cycle. The first is a **full
  audit** of every file against every item; each later one is
  a **follow-up pass**: it checks that each fix resolves its
  finding, checks new or changed text against every item, and
  reads unchanged text only where the changed text refers to
  it.
- **record**: the work document of one review cycle. Its
  header holds the cycle's state; it is the cycle's only
  state.
- **audit loop**: the part of a review cycle that runs on its
  own: sort the findings, fix the agreed ones, run a
  follow-up pass, until no agreed finding is open, churn is
  named, or the limit is reached.
- **agreed finding**: a `fail` or `warn` the agent can show
  in the cited text, whose fix changes only text at the cited
  place and no input, result, gate, step order, file kind, or
  shared file. It is fixed without asking.
- **held finding**: a finding kept for the user: **disputed**
  (the agent can cite text that refutes it), **trade-off**
  (any other `fail` or `warn`), or `info`.
- **accepted finding**: a finding the user decided to leave
  as it is, with the reason. It is not reported again in the
  same review cycle.
- **churn**: a new finding that undoing an earlier fix would
  resolve. It stops the audit loop early and goes to the user.
- **snapshot**: a copy of a skill's files as the last pass
  audited them, kept in `temp/` for the next diff. It
  holds no state: losing it only makes the next pass a full
  audit.
