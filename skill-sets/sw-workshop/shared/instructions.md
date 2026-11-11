# Instruction Quality

How instruction files are written: a skill's `SKILL.md` and
its references, a rule, a `CLAUDE.md`, an agent definition.
An agent follows them under pressure to finish and fills
every gap with its own judgment; each item below closes a
gap of that kind. Report an item only where the file falls
short of it.

## I1 — Rationale where it changes behavior

A directive carries its reason when the reason changes how
an agent applies it: a failure mode the rule alone does not
predict, two principles that pull against each other, or a
step that looks skippable. A reason that restates the
directive in other words is filler.

Ask of each directive: would an agent apply it differently
if it knew why? Flag a missing reason where the answer is
yes, and filler where it is no.

## I2 — No decorative prose

Prose is decorative when removing it changes none of: which
actions the agent takes, their order, their conditions, or
the error handling. Echoes, closing summaries, preambles
such as "It is important to note that", and parentheses
that repeat the rule are candidates.

Four shapes look decorative but are not; do not flag them:

- a second statement of a rule that counters a different
  rationalization than the first;
- the first directive under a heading — it is the section's
  body, not a repeat of the heading;
- a clause that sets a precondition or an order, even when
  it reads like a reason;
- a "no exceptions" clause that blocks an exception the
  agent would otherwise grant itself.

Concrete failure citations ("a prior run did X and broke
Y") stay.

## I3 — Mandatory steps cannot be skipped

An early step that produces visible state — a file exists,
a key is set, a test passed — invites an agent to treat the
later steps as done. Where later steps must always run:

- the procedure says before its first step that every step
  runs;
- those steps use verbs that cannot be read as conditional
  ("always write", "run every time"), not "ensure",
  "verify", or "check", which read as "skip if done".

Steps that are genuinely conditional, or that consume an
earlier step's output, are not findings.

## I4 — Bright lines instead of judgment calls

Qualifiers such as trivial, simple, small, minor, obvious,
or mechanical, and category words such as configuration or
documentation, leave the boundary to the agent, and under
pressure it puts the boundary where the work is smallest.
Each one needs a definition or concrete examples. An
exception clause ("unless", "except", "when it's") is
scoped so narrowly that the main case cannot be argued into
it.

## I5 — One term per thing

The file uses one term for each action, role, and artifact.
An agent that reads two terms assumes two mechanisms. A file
written for one harness uses that harness's terms; in Claude
Code: *launch* a subagent (the Agent tool without a name),
*spawn* and *shut down* a teammate, *message* a teammate.

## I7 — No copied configuration

A value that a settings file owns — a directory, a path, a
mode — is read from that file, not copied into the
instructions. A copy goes stale without a sign when the
setting changes.

## I12 — Nothing dynamic in what loads at session start

Files that load at session start — `CLAUDE.md`, rules,
agent definitions — stay free of dates, counters, versions,
and running state: a change there breaks the prompt cache
for every turn after it. Instructions do not tell the agent
to write such content into them; running state belongs in a
file the procedure reads when it needs it.
