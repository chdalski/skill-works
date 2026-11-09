# sw-skill-audit: Expected Results

What a correct audit reports for each test object. Written
before the audit runs, so a result is compared with an
expectation instead of explained after the fact. Item IDs
(F, I, C) refer to the guideline files in
`skill-sets/sw-workshop/skills/sw-skill-audit/references/`.

Each object lists:

- **Must report** — a finding the audit misses here counts
  as missed.
- **Must not report** — a finding here counts as a false
  alarm.
- **Open** — the guideline's answer is unclear; the user
  decides, then the item moves to one of the lists above.

One cause can yield findings under several items when each
item gives a different reason; each such finding counts.

Fixtures under `fixtures/` are frozen copies. `ensure-ai-dirs`
and `blueprint-audit` come from claude_orchestration at
commit `91a9341`; `broken-skill` was written for these
tests. A fixture is not a skill made in this repository, so
no fixture gets a prefix check (O11).

## sw-skill-audit (`skill-sets/sw-workshop/skills/sw-skill-audit`)

The audit judges itself by its own guidelines. Skills use the
fields of the Agent Skills specification; a harness field is
allowed only where the skill cannot work without it, with the
reason stated.

Run 1 found its Claude Code fields and real defects in its
script and procedure; those are fixed. It now asks for a
fresh subagent in its text instead of setting fields. Run 2
left 8 `warn`, run 3 left 6 `warn` and 2 `info`; each was
reviewed with the user and fixed, and by agreement no fourth
run followed. The next audit of this skill checks the
result.

Must report: nothing at `fail` or `warn`.

Must not report:
- F5 — it uses no harness field
- a missing `sw-` prefix — it carries one
- I9 — its deterministic checks run in its scripts
- C8 or C12 — input and end are defined

## ensure-ai-dirs (`fixtures/ensure-ai-dirs`)

A well-maintained skill with one known weakness.

Must report:
- F7 `warn`: names its own five files through the project
  path `.claude/skills/ensure-ai-dirs/…`
- I10 `warn`: the description is written as an instruction
  ("Ensure …"), not in the third person
- I6 `warn`: the text names "the lead" and "the plan review
  subagent", which ties the skill to one team structure
- I9 `warn`: comparing files and moving plans by their
  status line is deterministic work done by instructions,
  not by a script
- C7 `warn`: no reaction is defined for an unreadable
  `settings.json` or a `git mv` that fails on a tracked file
- I2 `warn`: lines 95–101 repeat the rule that step 2 is
  unconditional and explain the template's design without
  changing any action
- C5 `fail`: step 1 reads `plansDirectory` only from
  `settings.json` but writes it to `settings.local.json`, so
  every run writes it again and overwrites a value the user
  set there (found in run 1, confirmed by reading)
- C11 `warn`: step 2 overwrites existing files in the plans
  directory without asking
- A2 `warn`: the shipped `plan-format.md` and
  `plan-review-checklist.md` name `risk-assessment.md`,
  Security Engineer gates, and `no-silent-target-weakening`,
  none of which the skill ships or declares
- A3 `info`: `plan-review-checklist.md` says to skip
  sections without findings (line 13) but asks section 12 to
  note that it passed

Must not report:
- instruction or coherence items (I, C) against the content
  of the five shipped templates — they get A1–A3 only
- a `fail` other than C5
- I3 — its preamble makes every step mandatory, and step 3
  ("Ensure the backlog exists") is genuinely conditional
- I1 — the non-obvious steps carry their reasons
- F7 for `.claude/settings.json`, `.claude/settings.local.json`
  or `.ai/backlog.md` — these are project files the skill
  works on, not files of the skill
- a prefix finding

## blueprint-audit (`fixtures/blueprint-audit`)

A long, single-file audit of this toolkit's predecessor.

Must report:
- F6 `warn`: 649 lines and about 5,500 tokens, over both
  targets
- I8 `warn`: every check sits in `SKILL.md` instead of in
  `references/`. Same cause as F6, but a different reason:
  F6 is about the size limits, I8 about loading detail only
  when a step needs it. Both findings stay.
- I10 `warn`: the description is written as an instruction
  ("Audit a blueprint …")
- C8 `warn`: it asks which blueprint to audit, but no path
  is defined for an unknown name or an unanswered question
- C3 `fail`: Checks 8–12 ask for "None found" lines that the
  output format forbids, and Checks 10 and 11 prescribe their
  own entry shapes (found in run 1, confirmed by reading)
- C9 `warn`: the output format sits beyond the first 5,000
  tokens and is lost after a compaction

Must not report:
- C12 — the report format defines the end
- I11 recommending harness fields such as `context: fork` or
  `argument-hint`; a fresh context is asked for in the text
- a prefix finding
- C10 as `warn` or `fail` for paths of its home project
  (`blueprints/`, `/.claude/rules/…`): the copy runs outside
  that project, so their absence says nothing about the
  skill
- a finding against Check 12 for saying that `paths:` is no
  skill field: the Agent Skills specification has no
  `paths`, so the statement is correct

## broken-skill (`fixtures/broken-skill`)

Every error is planted.

Must report:
- F2 `fail`: the name breaks the format (uppercase, double
  hyphen) and does not match the directory
- F4 `fail`: `metadata` is a string, not a map
- F7 `fail`: `references/missing.md` and `scripts/run.sh` do
  not exist
- F3 `warn`: the description contains an XML tag
- F5 `warn`: unknown key `foo`
- F7 `warn`: `references/extra.md` points on to
  `references/more.md`
- I10 `warn`: the description says neither what nor when
- I4 `warn`: "looks good" leaves the end to judgment
- C1 `fail`: "continue with step 4" points to a step that
  does not exist
- C2 `fail`: "Repeat until …" has no limit and no action
  when a limit is reached

Must not report:
- a prefix finding
