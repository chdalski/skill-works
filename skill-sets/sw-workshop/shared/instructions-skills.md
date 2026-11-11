# Instruction Quality for Skills

Items that apply to skills only, on top of the items for
every instruction file. Report an item only where the skill
falls short of it.

## I6 — Inputs and outputs, not team structure

A skill names what it receives and what it returns, not who
sends or receives it: "the requester" and "the implementor"
instead of named roles. It does not branch on the workflow
that called it. A skill that names its teammates breaks in
the first setup with a different team.

## I8 — Core first, details on demand

`SKILL.md` holds the procedure. Detail that only some steps
need lives in `references/`, or in the set's shared files
when several skills of the set need it, and is named at the
step that needs it, together with when to read it. A file
no step points to is never read.

## I9 — Scripts for deterministic work

Counting, parsing, and checking that files exist belong in
a script, not in instructions: an agent miscounts and
assumes where a script measures. The script prints only
what the agent needs. What happens when the script fails is
a failure path like any other.

## I10 — The description triggers correctly

The description is all an agent sees before it decides to
load the skill. It says what the skill does and when to use
it, in the third person, with the words a request or task
would contain. It is narrow enough not to fire on unrelated
tasks and specific enough to fire on the intended ones.

## I11 — Invocation and context are chosen deliberately

The specification has no fields for these choices, so the
skill makes them in its text first; a harness field is the
last resort.

- A skill with side effects, or a long procedure that
  should start only on request, says so in its description
  and text. Only where that is not enough may it use the
  harness's field for user-only start, with the reason.
- A skill that another skill or an agent must call stays
  invocable by the model: a user-only skill cannot be
  called from another skill.
- A skill that must judge without the conversation's bias,
  or would flood the conversation with intermediate output,
  tells the agent to run the work in a fresh subagent,
  started with the harness's subagent tool, and says what
  to do when the harness has none. Fresh means it does not
  inherit the conversation: a fork that carries the
  conversation along brings the bias back. It runs in the
  conversation when it needs what was said there.

## I13 — Neutral terms in a skill for several harnesses

A skill is written for several harnesses unless its
`compatibility` field or its text says it runs in one
harness only. Such a skill keeps one neutral term per
action, such as *start a subagent*, and names a harness's
tool together with the harness where it helps: in Claude
Code, the Agent tool. Such a hint does not make the skill
single-harness. A term of one harness alone reads as a step
that the other harnesses cannot run.

## I14 — Injected output stays small

Command output injected into a skill body may change from
run to run, unlike the files I12 keeps static: the body
enters the conversation as a message, not the cached
prefix. Keep that output under 2,000 characters, since it
lands in the conversation on every invocation.

## I15 — Questions follow the set's guide for asking

A skill asks the user when it waits for an answer before it
goes on: a decision, a confirmation, a missing input. A
skill that only reports a missing input and stops does not
ask. A skill that asks reads its set's guide for asking at
the step where it asks; in a skill-works set that is the
shared `asking.md`. Without the guide the agent asks
in its own style, and a question cut short leaves the user
unable to decide. If the set has no such guide, the fix is
to add one to the set, or to state in the skill what each
question carries: what is to decide, an example, the
options, and a recommendation.

## I16 — Temporary files have a defined place

A skill that writes files outside its result says where
they go, by kind, and never as a fixed path such as `/tmp`:
some systems lack it, and a fixed path ignores a redirected
`TMPDIR`.

- Scratch files for one run go into a new directory from
  the system's temp facility (`mktemp -d`; in Python
  `tempfile.mkdtemp()`) or into the scratch directory the
  harness names. The skill deletes the directory when the
  run ends.
- State that must survive a compaction goes into such a
  directory with a fixed prefix and a random rest
  (`mktemp -d -t <skill>.XXXXXX`), and a file in it names
  what the state belongs to. The skill says how to find it
  again: list the directories with that prefix and take the
  one whose file names the current target. The random rest
  keeps anyone from creating the directory in advance.
- What must outlast the session is not temporary: it lives
  in the project, in a place the skill names.

None of these goes into the skill directory: an update
replaces it, and an audit reads the file as part of the
skill. Scratch files stay out of the project tree, where
they show up as changes and can be committed by mistake.
