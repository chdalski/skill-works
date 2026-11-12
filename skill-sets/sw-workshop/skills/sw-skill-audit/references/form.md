# Form

What a skill must look like to load at all and to work in
every harness that reads the Agent Skills specification.
`scripts/check_form.py` checks the items marked *(script)*
and holds the same field lists and limits as this file;
change both together. Check the rest by reading.

## F1 — Layout *(script)*

A skill is a directory with a `SKILL.md`: YAML frontmatter
between two `---` lines, then a Markdown body. Optional
subdirectories are `scripts/` (code the agent runs),
`references/` (documents the agent reads to decide what to
do), and `assets/` (templates and data).

The frontmatter must parse as YAML. A plain, unquoted value
breaks the parse, and the harness then cannot load the
skill, when it:

- contains `: `;
- starts with a YAML indicator such as `*`, `&`, `!`, `%`,
  `@` or a backtick;
- starts with `[` or `{` but is not one complete flow list
  or map, as in `[Beta] Checks …`, or starts with `]`, `}`
  or `,`;
- starts with `- ` or `? `, which YAML reads as a list entry
  or a complex key.

A quote that never closes breaks it too, and a value that
starts with `#` is read as a comment, which leaves the field
empty. ` #` inside a plain value starts a comment as well:
`Triages issue #42 reports.` loads as `Triages issue` (a
`warn`). Such values are quoted or written as a block
scalar (`>`).

## F2 — `name` *(script)*

- 1–64 characters: lowercase letters, digits, and hyphens;
  no leading, trailing, or consecutive hyphens.
- Equal to the directory name. The harness finds a skill by
  its directory, and a mismatch can hide the skill without
  an error.
- Starts with the prefix the project requires, where the
  Input of `<audit-dir>/SKILL.md` calls for a prefix check.
- Free of the words `anthropic` and `claude`: the Claude
  API rejects such names.

## F3 — `description` limits *(script)*

- 1–1024 characters and no XML tags; the Claude API
  rejects descriptions with tags.
- Claude Code shows `description` and `when_to_use`
  together and cuts the entry at 1,536 characters.

## F4 — Specification fields *(script)*

The Agent Skills specification defines, besides `name` and
`description`:

- `license` — a license name or a bundled license file;
- `compatibility` — 1–500 characters on what the skill
  needs: the harness, system packages, network access;
- `metadata` — a map of string keys to string values; an
  unquoted number, boolean, or null is not a string, so
  such a value is quoted;
- `allowed-tools` — a space-separated string of
  pre-approved tools (experimental); in Claude Code, tools
  usable without a permission prompt during the invoking
  turn. As a specification field it needs no stated reason
  under F5.

## F5 — Harness fields *(script lists them, judge by reading)*

A skill uses the fields of the specification. A field that
only one harness knows changes nothing in another harness,
so a skill that relies on one behaves differently there. It
is allowed only where the skill cannot work without it, and
the skill states why — in its text or in `compatibility`,
which also names the harness. A harness field without a
stated reason is a `warn`. A key in neither list is a typo
or a field of another file type.

Claude Code fields:

| Field | Effect |
|---|---|
| `when_to_use` | Extra trigger text, shown with the description |
| `argument-hint` | Hint for the arguments in the `/` menu |
| `arguments` | Named arguments for `$name` substitution |
| `disable-model-invocation` | `true`: only the user can start the skill; the model cannot invoke it, not even from another skill |
| `user-invocable` | `false`: hidden from the `/` menu; only the model loads it |
| `disallowed-tools` | Tools removed while the skill is active |
| `model`, `effort` | Model and effort for the invoking turn |
| `context` | `fork`: runs the skill as a subagent that sees none of the conversation |
| `agent` | Subagent type for `context: fork` (default `general-purpose`) |
| `background` | With `context: fork`, `false` waits for the result in the invoking turn |
| `hooks` | Hooks registered when the skill is invoked |
| `paths` | Globs that limit automatic activation to matching files |
| `shell` | Shell for injected commands: `bash` or `powershell` |

## F6 — Size *(script)*

`SKILL.md` stays under 500 lines and its body under about
5,000 tokens. The specification recommends both, and after
a compaction Claude Code keeps only the first 5,000 tokens
of an invoked skill.

## F7 — File references *(script, partly by reading)*

The script follows Markdown links, paths under `scripts/`,
`references/`, `assets/`, `../../shared/`, and `../../agents/`, in links and
in plain text alike, and project paths that run through the
skill's own directory. A file named only by its bare name,
such as `plan-format.md` at the skill root, is checked by
reading.

- Paths are relative to the skill directory;
  `${CLAUDE_SKILL_DIR}/` in front also works in Claude
  Code. A skill does not name its own files through a
  project path such as `.claude/skills/<name>/…`: installed
  at user level or in a plugin, it would point to nothing.
- A skill in a plugin reads the files its plugin shares
  through `../../shared/<file>`, and names the definition of
  one of its plugin's agents through `../../agents/<file>`.
  A plugin ships as a whole, so these paths hold wherever it
  is installed. A shared file belongs to every skill that
  names it. An agent definition is read by the agent the
  skill starts, not by the skill: it must exist, and no other
  item applies to it.
- Every referenced file exists.
- References stay one level deep: `SKILL.md` points to a
  file, and that file does not send the reader on to a
  further document. This holds for shared files too.
- Every file in the skill directory is named in `SKILL.md`;
  a file no line names is never read (`warn`).
