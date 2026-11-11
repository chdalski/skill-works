# sw-skill-audit: Expected Results

What a correct audit reports for each test object. Written
before the audit runs, so a result is compared with an
expectation instead of explained after the fact. Item IDs
(F, C, A) refer to the guideline files in
`skill-sets/sw-workshop/skills/sw-skill-audit/references/`,
and I to those in `skill-sets/sw-workshop/shared/`.

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
tests. A fixture lies outside the project's skill
directories, so no fixture gets a prefix check (O11).

## sw-skill-audit (`skill-sets/sw-workshop/skills/sw-skill-audit`)

The audit judges itself by its own guidelines. Skills use the
fields of the Agent Skills specification; a harness field is
allowed only where the skill cannot work without it, with the
reason stated.

Run 1 found its Claude Code fields and real defects in its
script and procedure; those are fixed. It now asks for a
fresh subagent in its text instead of setting fields. Runs 2
to 6 were full audits and left 8, 6, 3, 1, and 3 `warn`;
each was reviewed with the user and fixed. Every run found
a different subset: a full audit does not converge on its
own, and one of run 6's findings came from a fix made after
run 5.

From run 7 on, the self-test follows a review cycle instead
of repeated full audits:

1. A full audit is the first pass; runs 1 to 6 were first
   passes.
2. Each `fail` and `warn` is fixed, or the user accepts it
   explicitly. An accepted finding moves to "Must not report"
   with its reason.
3. A follow-up pass gets the findings of the previous pass
   and the diff of the revision. It checks that the revision
   resolves them and contradicts nothing it leaves
   unchanged; it does not audit unchanged text again.
4. Steps 2 and 3 repeat until a follow-up pass reports no
   `fail` and no `warn`. `info` findings alone start no pass.
5. At the end, the user sees the `info` findings of the last
   pass, together with any finding that is disputed or whose
   fix needs a trade-off. What the user takes is applied and
   gets a follow-up pass on its diff; the rest is dropped.

Runs 7 to 9 were follow-up passes. Run 7 found one run 6
`warn` only partly fixed, one new `warn`, and two `info`, all
from the run 6 fixes; run 8 found no `fail` or `warn` and two
`info`, which the user took; run 9 confirmed both fixes and
found nothing new.

Step 5b moved the instruction guideline into the set's
`shared/` and added I13 to I16. Runs 10 to 13 were follow-up
passes on those changes, with the whole skill checked
against the new items. Run 10 found five `warn` and one
`info`. Four `warn` were fixed; the user accepted the I8
`warn` (below). The `info` said that step 5 has no reaction
to missing shared files; instead of that fix, C7 now states
that a missing file the set ships is no failure case. Run 12
found the first wording of that too wide; run 13 confirmed
the fix and found nothing new.

Step 5c then rewrote I16 and C5 so that skills inside a set
keep only temporary files. Runs 14 to 18 were follow-up
passes on that change: run 14 found one `fail` and four
`warn`, runs 15 to 17 each found one narrower `warn` in the
same paragraph of I16, and run 18 found nothing new. A
variant pass tested a simpler wording of that paragraph in a
copy; it left two `warn`, so the patched wording stayed.

Must report: nothing at `fail` or `warn` in the last
follow-up pass, apart from accepted findings.

Must not report:
- F5 — it uses no harness field
- a missing `sw-` prefix — it carries one
- I9 — its deterministic checks run in its scripts
- I15 — it does not ask: without a valid input it reports
  that and stops
- I16 — its scratch files go into a new temp directory that
  it deletes before the report
- C8 or C12 — input and end are defined
- I8 for `shared/instructions.md` and
  `shared/instructions-skills.md` — accepted by the user
  until `sw-skill-create` names them in step 5c: only this
  skill reads them so far, and the move was planned for the
  skills that follow

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
- I16 `warn`: step 1 writes `plansDirectory` into
  `.claude/settings.local.json`, a file the description does
  not name and nothing hands in. Same step as the C5 `fail`,
  but a different reason: C5 is about reading the value from
  one file and writing it to another, I16 about a file left
  behind outside the result. Both findings stay.
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
- I15 `warn`: step 1 asks which blueprint to audit, but
  nothing tells the agent how to ask; the fixture belongs to
  no set, so the fix is a guide for asking or a statement of
  what the question carries

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
