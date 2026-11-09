# Form

What a skill must look like to load at all and to work in
the harness it targets. `scripts/check_form.py` checks the
items marked *(script)*; check the others by reading.

## F1 — Layout *(script)*

A skill is a directory with a `SKILL.md`: YAML frontmatter
between two `---` lines, then a Markdown body. Optional
subdirectories are `scripts/` (code the agent runs),
`references/` (documents it reads on demand), and `assets/`
(templates and data).

## F2 — `name` *(script)*

- 1–64 characters: lowercase letters, digits, and hyphens;
  no leading, trailing, or consecutive hyphens.
- Equal to the directory name. The harness finds a skill by
  its directory, and a mismatch can hide the skill without
  an error.
- Starts with the prefix the project requires for its own
  skills, when the project's instructions define one.
- Free of the words `anthropic` and `claude`: the Claude
  API rejects such names.

## F3 — `description` *(script, partly by reading)*

- 1–1024 characters and no XML tags — the Claude API
  rejects descriptions with tags. *(script)*
- Claude Code shows `description` and `when_to_use`
  together and cuts the entry at 1,536 characters.
  *(script)*
- Says what the skill does and when to use it — see I10.
  *(reading)*

## F4 — Portable fields *(script)*

The Agent Skills specification defines, besides `name` and
`description`:

- `license` — a license name or a bundled license file;
- `compatibility` — 1–500 characters on what the skill
  needs: the harness, system packages, network access;
- `metadata` — a map of string keys to string values;
- `allowed-tools` — a space-separated string of
  pre-approved tools (experimental).

## F5 — Harness fields *(script, partly by reading)*

Fields beyond the specification work only in the harness
that defines them; another harness ignores them, and the
skill then behaves differently there. A skill that uses
them names the harness in `compatibility`. A key in neither
list is a typo or a field of another file type.

Claude Code fields:

| Field | Effect |
|---|---|
| `when_to_use` | Extra trigger text, shown with the description |
| `argument-hint` | Hint for the arguments in the `/` menu |
| `arguments` | Named arguments for `$name` substitution |
| `disable-model-invocation` | `true`: only the user can start the skill; the model cannot invoke it, not even from another skill |
| `user-invocable` | `false`: hidden from the `/` menu; only the model loads it |
| `allowed-tools` | Tools usable without a permission prompt during the invoking turn |
| `disallowed-tools` | Tools removed while the skill is active |
| `model`, `effort` | Model and effort for the invoking turn |
| `context` | `fork`: runs the skill as a subagent that sees none of the conversation |
| `agent` | Subagent type for `context: fork` (default `general-purpose`) |
| `background` | With `context: fork`, `false` waits for the result in the invoking turn |
| `hooks` | Hooks registered when the skill is invoked |
| `paths` | Globs that limit automatic activation to matching files |
| `shell` | Shell for injected commands: `bash` or `powershell` |

Check by reading that each field serves a choice I11
describes; a field nobody can explain is removed.

## F6 — Size *(script)*

`SKILL.md` stays under 500 lines and its body under about
5,000 tokens. The specification recommends both, and after
a compaction Claude Code keeps only the first 5,000 tokens
of an invoked skill (C9).

## F7 — File references *(script)*

- Paths are relative to the skill directory;
  `${CLAUDE_SKILL_DIR}/` in front also works in Claude
  Code. A skill does not name its own files through a
  project path such as `.claude/skills/<name>/…`: installed
  at user level or in a plugin, it would point to nothing.
- Every referenced file exists.
- References stay one level deep: `SKILL.md` points to a
  file, and that file does not send the reader on to a
  further document.
- Every file in the skill directory is named in `SKILL.md`;
  a file no line names is never read.
