# Instruction Quality for Skills

Items that apply to skills only, on top of the items for
every instruction file. Report an item only where the skill
falls short of it.

Here a plugin is the package a skill ships in, with the other
skills it ships with and the files they share. A skill outside
any plugin counts its own directory as its plugin. A flow is
the work that one or more skills of a plugin do, from the
first skill that runs, whoever starts it, to the last one
that hands nothing on.

## I6 — Inputs and outputs, not team structure

A skill names what it receives and what it returns, not who
sends or receives it: "the requester" and "the implementor"
instead of named roles. It does not branch on the workflow
that called it. A skill that names its teammates breaks in
the first setup with a different team.

## I8 — Core first, details on demand

`SKILL.md` holds the procedure. What goes where is decided by
the paths through the skill: what every path needs stays in
`SKILL.md` as far as its size limit allows (F6), and detail
of a step that every path passes through may go into a
reference read at that step; what only some paths reach goes into
`references/`, or into the plugin's shared files when
several of its skills need it. Each reference is named at
the step that reads it, together with when to read it. A
file no step points to is never read.

Each concept has one home: its definition, rules, and limits
stand in one place, under one heading. Another place that
needs the concept points to that home instead of restating
it: two homes drift apart, and the agent follows whichever it
read last.

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
tasks and specific enough to fire on the intended ones. The
description is in the context of every session, so:

- its leading words say what the skill does;
- each situation that should start the skill gets one
  phrase, not a list of synonyms;
- it leaves out what the body carries, such as how the skill
  works; a sentence stays when it changes whether the agent
  loads the skill, such as "reports only";
- a skill that only the user starts gets a short description
  for people, without triggers: the agent never decides to
  load it.

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

## I15 — Questions follow a guide for asking

A skill asks the user when it waits for an answer before it
goes on: a decision, a confirmation, a missing input. A
skill that only reports a missing input and stops does not
ask. A skill that asks reads a guide for asking at the step
where it asks: the one its plugin ships, such as a shared
`asking.md`. Without a guide the agent asks in its own style,
and a question cut short leaves the user unable to decide. If
its plugin has no such guide, the fix is to add one to the
plugin, or to state in the skill what each question carries:
what is to decide, an example, the options, and a
recommendation.

## I16 — Each file a skill writes has a place and an end

Every file a skill creates for its work is one of three kinds,
and the skill says for each file where it goes and when it is
deleted:

- **Result**: what the skill's description says it produces
  or changes, including the files in a directory the
  description names. Inside such a directory, a file that
  holds only working state, such as progress or a cache, is
  not part of the result unless the description names it. A
  work document the skill hands on within its flow, such as a
  brief, stays a work document even when the description
  names it. A result stays; no skill deletes it.
- **Work document**: a file the user reads, comments on, or
  accepts while the skill's flow runs, such as a brief, a
  draft, or a review record, also one the skills of a plugin
  hand each other. It must survive a reboot while the flow
  runs, and it has no use after the user's acceptance: the
  skill that ends the flow deletes it then. Any skill of the
  flow may delete it earlier, once a later work document of
  the same flow replaces it, or when the user confirms
  abandoning the flow or replacing the cycle it belongs to,
  such as a review cycle. A flow that is
  abandoned and never resumed may leave it behind.
- **Temporary file**: a file only skills read, such as a
  scratch file, a diff, or a snapshot. The skill deletes it as
  soon as nothing needs it. Losing it costs only work; the
  skill says what it does when it is gone.

Work documents and temporary files go into a **workspace**: a
directory inside the project that version control ignores,
with one place for work documents and one for temporary
files, which the skill or its plugin names and creates when
it is missing. A settings file that names the workspace sits
at the top of the project and is meant to be committed; it is
no work document or temporary file and stays, and the skill
tells the user when it creates it. A skill deletes its work
documents and temporary files only inside its workspace, or,
without one, in the place it names for them; deleting other
files, where that is the skill's task, follows C11. A skill whose plugin has no workspace may put the
scratch files of one run into a new directory from the
system's temp facility (`mktemp -d`; in Python
`tempfile.mkdtemp()`) and delete it when the run ends; never
a fixed path such as `/tmp`, which some systems lack and which
ignores a redirected `TMPDIR`. Its work documents still need
a place in the project that survives a reboot, and the skill
names it; having no workspace is no finding by itself.

A **handed-in file** is a file outside the workspace whose
path the request, the skill's arguments, or the project's
instructions name. The skill may change or extend
it, but not delete or move it unless that is its task and the
user confirms (C11); if the description names it, it is also
the result.

State that must survive a compaction or a new session (when a
procedure needs such state is C5) lives in a work document,
the result, or a handed-in file the skill extends, never in a
temporary file, not even as a copy: a copy is a second place
that sooner or later disagrees. Skills of a plugin hand each
other these files, and the state of their flow stands in the
file that is handed on. The skill says how to find its state
again and what it does when it finds none or more than one.

No work document or temporary file goes into a skill
directory: an update replaces it, and an audit reads the file
as part of the skill. A file left
in the project outside an ignored workspace shows up as a
change and can be committed by mistake.

## I17 — Words the reader knows

Every term in a skill's text is common language, a term its
harness defines, or a term the skill or its plugin's shared
files define. A term from the repository the skill was made
in, such as a project's own names for its concepts or its
decision numbers, is defined in the skill or its plugin's
shared files, in one place (I8), or left out:
the project that runs the skill has never seen that
repository.
