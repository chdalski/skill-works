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

## I16 — Each file a skill writes has a defined place

Every file a skill writes is one of four kinds. A file whose
path is handed in is a handed-in file, whoever reads it; if
the description names it, it is also the result. For any
other file the test is: does a person read it or want to
keep it? Then it is the result or a work document, and it
stays. Does only a skill read it? Then it is temporary.

- **Result**: what the skill's description says it produces
  or changes, including the files in a directory the
  description names. Inside such a directory, a file that
  holds only the skill's working state, such as progress or
  a cache, is not part of the result unless the description
  names that file.
- **Work document**: a file the user reads, comments on, or
  accepts while the skill's flow runs, such as a brief or a
  draft. A file handed to the next skill of its plugin is a
  work document when a person reads it. Work documents go
  into the directory the project's instructions name for
  them; where they name none, a skill that receives no work
  document asks once, before it writes its first one, and a
  skill that receives one takes the directory of that work
  document.
- **Handed-in file**: a file whose path the request, the
  skill's arguments, or the project's instructions name. The
  skill may extend it.
- **Temporary file**: every other file.

The skill never deletes its result or a work document: they
belong to the user. At the end of its flow it names the work
documents that remain, so the user can keep, commit, or
delete them. A temporary file left behind stays after the
run, even one that Git ignores: nothing removes it when the
plugin is removed, and a later run may read it as current.

The skill says where its temporary files go, by kind, and
never as a fixed path such as `/tmp`: some systems lack it,
and a fixed path ignores a redirected `TMPDIR`.

- Scratch files for one run go into a new directory from the
  system's temp facility (`mktemp -d`; in Python
  `tempfile.mkdtemp()`) or into the scratch directory the
  harness names. The skill deletes the directory when the
  run ends.
- Helper files that must outlive one run but hold no state,
  such as a snapshot for a diff, go into a new directory from
  the system's temp facility with a fixed prefix and a random
  rest (`mktemp -d -t <skill>.XXXXXX`), not into the
  harness's scratch directory, which a new session does not
  see. A file in it names what it belongs to; the skill finds
  it again by listing the directories with that prefix and
  taking the one whose file names what the current run works
  on. The random rest keeps anyone from creating the
  directory in advance. Losing such a file costs only work: a
  reboot can empty the temp facility, so the skill says what
  it does when it finds none or more than one, and deletes
  the directory when it no longer needs it.

State that must survive a compaction or a new session (when a
procedure needs such state is C5) never lives in a temp
directory, not even as a copy: a reboot can empty it, and a
copy is a second place that sooner or later disagrees. It
lives in a work document, the result, or a handed-in file the
skill extends. Skills of a plugin hand each other these files,
not a temp directory, and the state of their flow stands in
the file that is handed on. The skill says how to find its
state again and what it does when it finds none or more than
one.

No temporary file goes into the skill directory: an update
replaces it, and an audit reads the file as part of the
skill. None goes into the project tree either, where it
shows up as a change and can be committed by mistake.

## I17 — Words the reader knows

Every term in a skill's text is common language, a term its
harness defines, or a term the skill or its plugin's shared
files define. A term from the repository the skill was made
in, such as a project's own names for its concepts or its
decision numbers, is defined in the skill or its plugin's
shared files, in one place (I8), or left out:
the project that runs the skill has never seen that
repository.
