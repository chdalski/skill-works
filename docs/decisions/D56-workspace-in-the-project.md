# D56: A workspace for the sets in the project

Status: accepted

## Decision

Every file a set writes and does not hand on as its result goes into one workspace in the project:

```
.skill-works.json   settings, committed; for now one key:
                    { "directory": ".skill-works" }
.skill-works/       the workspace; its name comes from "directory"
  .gitignore        "*": nothing in the workspace is committed
  work/             work documents: the files the user reads
                    while a flow runs (brief, draft, review record)
  temp/             temporary files: the files only skills read
                    (scratch, diff, snapshot)
```

The first skill that needs the workspace creates whatever of it is missing: `.skill-works.json` with the default, the directory, its `.gitignore`, `work/` and `temp/`. Every skill uses it, also one that only reports.

A set writes three kinds of files:

| Kind | Read by | Lives in | Deleted |
|---|---|---|---|
| Result (lasting) | the user, other people and agents, after the flow | where the project's instructions say; else where the user picks | never by a skill |
| Work document (flow-scoped) | the user, while the flow runs | `work/` | by the skill that ends the flow, after the user's acceptance; earlier by any skill of the flow, once a later work document replaces it or the user confirms abandoning the flow |
| Temporary file | only skills | `temp/` | by the skill, as soon as nothing needs it |

The place decides which rule holds: a skill deletes its own work documents and temporary files only inside the workspace. A file outside it that the user, the project's instructions, or a seed hands to a skill is a handed-in file: the skill may change or extend it, and deletes or moves it only where that is the skill's task and the user confirms. Work documents that the skills of a flow hand each other stay work documents. The user's acceptance is an explicit question at the end of a flow, such as the one `sw-skill-review` asks before it deletes.

A flow that is abandoned and never resumed leaves its files in the workspace; they are a few kilobytes and ignored by Git.

One script in each set does the work: it reads the settings, creates the workspace, names new files, lists open work documents, and deletes only inside the workspace. Skill text names the script, not the rules.

## Reasons

Work documents must survive a reboot while the flow runs: a reboot emptied `/tmp` and took a draft that waited for the user's acceptance. After the user's acceptance they have no use left: the result, such as the finished skill, is the reference from then on. So they live in the project for as long as the flow runs, and the skill that ends the flow deletes them.

Temporary files in the system's temp facility cost a permission prompt for every write outside the project in Claude Code, and a fixed `/tmp` does not exist on Windows. Inside the project, the workspace's own `.gitignore` keeps them out of `git status` without touching the project's `.gitignore`.

A settings file at the root is read the same way by every harness and by scripts; a line in `CLAUDE.md` or `AGENTS.md`, as the elephant-goldfish-model repository uses for its artifact directory, depends on the harness and is prose.

Known cost: because sets never refer to each other ([D3](D3-sets-never-refer-to-each-other.md)), every set carries the script and the rules. A change reaches existing sets only when they are updated. A seed may later take this over for all sets of a project.

## Consequences

- Replaces [D54](D54-files-by-reader.md) and [D33](D33-temporary-files.md).
- [D55](D55-no-flow-directory.md), [D36](D36-skills-start-from-a-draft.md), [D45](D45-where-the-state-lives.md) and [D32](D32-the-review-cycle.md) name `work/` as the place of work documents.
- Guideline item I16, and coherence items C5 and C11, follow this decision; a follow-up pass on `sw-skill-audit` checks the change.
- The glossary, `skill-sets/CLAUDE.md`, and the plugin's `shared/terms.md` and `shared/harness-phrases.md` follow it.
- The shared script `shared/scripts/workspace.py` does the workspace work; `sw-skill-audit` and `sw-skill-review` use it.
- The drafts of `sw-skill-review` and `sw-skill-brainstorm` and the skill `sw-skill-review` follow it.
- skill-works keeps its own work documents in its workspace `.skill-works/work/`.
