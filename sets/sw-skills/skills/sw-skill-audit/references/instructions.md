# Instruction Quality

How a skill's instructions are written. An agent follows a
skill under pressure to finish and fills every gap with its
own judgment; each item below closes a gap of that kind.
Report an item only where the skill falls short of it.

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

The skill uses one term for each action, role, and
artifact, and the harness's own terms where they exist. An
agent that reads two terms assumes two mechanisms. In
Claude Code: *launch* a subagent (the Agent tool without a
name), *spawn* and *shut down* a teammate, *message* a
teammate.

## I6 — Inputs and outputs, not team structure

A skill names what it receives and what it returns, not who
sends or receives it: "the requester" and "the implementor"
instead of named roles. It does not branch on the workflow
that called it. A skill that names its teammates breaks in
the first setup with a different team.

## I7 — No copied configuration

A value that a settings file owns — a directory, a path, a
mode — is read from that file, not written into the skill.
A copy goes stale without a sign when the setting changes.

## I8 — Core first, details on demand

`SKILL.md` holds the procedure. Detail that only some steps
need lives in `references/` and is named at the step that
needs it, together with when to read it. A file no step
points to is never read.

## I9 — Scripts for deterministic work

Counting, parsing, and checking that files exist belong in
a script, not in instructions: an agent miscounts and
assumes where a script measures. The script prints only
what the agent needs, and `SKILL.md` says what to do when
the script or its interpreter is missing.

## I10 — The description triggers correctly

The description is all an agent sees before it decides to
load the skill. It says what the skill does and when to use
it, in the third person, with the words a request or task
would contain. It is narrow enough not to fire on unrelated
tasks and specific enough to fire on the intended ones.

## I11 — Invocation is chosen deliberately

- A skill with side effects, or a long procedure that
  should start only on request, can be started by the user
  only.
- A skill that another skill or an agent must call stays
  invocable by the model — a user-only skill cannot be
  called from another skill.
- Background knowledge that the user never calls directly
  is hidden from the user's command list.
- A skill runs in a fresh context when it must judge
  without the conversation's bias or would flood the
  conversation with intermediate output; it runs in the
  conversation when it needs what was said there.

F5 lists the fields that implement these choices.

## I12 — Nothing dynamic in what loads at session start

Files that load at session start — `CLAUDE.md`, rules,
agent definitions — stay free of dates, counters, versions,
and running state: a change there breaks the prompt cache
for every turn after it. A skill does not write such
content into them; running state belongs in a file the
procedure reads when it needs it. A skill body enters the
conversation as a message, so output injected into it may
change; keep it under 2,000 characters.
