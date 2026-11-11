# Coherence

Whether a skill's procedure works as a whole: every step can
be reached, every path ends, and what one step hands on is
what the next one needs. Each part can read well while the
whole fails — a gate nobody can pass, a loop without an end,
state that no later session finds.

## Build the Model First

Before checking, write down the procedure as the skill
defines it, one row per step, phase, or loop. The report
includes this table, so the requester sees what the audit
understood.

| Step | Defined in | Entry | Exits | Reads / writes | Actor |
|---|---|---|---|---|---|

- **Entry** — the condition under which the step starts.
- **Exits** — every way the step can end and where each
  leads: the next step, another step, a stop, a question to
  the user.
- **Reads / writes** — files, state, arguments, tool and
  script output.
- **Actor** — the agent running the skill, a subagent, a
  script, the user.

Build the table from the text, not from what the procedure
probably means: a gap in the table is often the finding.

A skill without a procedure — background knowledge, a
reference — gets no table; check only C3 and C10 for it.

## C1 — Every step is reachable

Each step has an entry from the start or from another
step's exit. A step that no exit leads to never runs, and
a jump to a step that does not exist ("continue with step
7" in a six-step procedure) leaves the agent to guess.

## C2 — Every path ends

Each exit leads to a step, a stop, or a defined handover.
A loop names its end condition and what happens when a
limit is reached before the condition holds — "repeat until
the review passes" without a limit can run forever.

## C3 — Nothing contradicts

No two places — in `SKILL.md` or across its references —
prescribe different behavior for the same situation: a
different order, condition, gate, or output. The agent
follows whichever it read last.

## C4 — Gates are complete

Each gate states what passes it, who decides, and what
happens when it fails. Its approval covers the state that
is used afterwards: a change between the gate and the use
— a reformat, a last edit — leaves an approval of
something else.

## C5 — State lives in one place and survives

This applies to a procedure that spans more than one session
or must survive a compaction. It must survive one when
nothing bounds its length: it waits for the user between
steps, repeats steps for each file, task, or round, or runs
until a condition holds. Any other procedure may keep its
working state in the conversation.

Running state — progress, decisions, open items — lives in
exactly one place outside the conversation: a temp
directory as I16 describes, the skill's result, or a file
handed in from outside the set that the skill extends. The
skill says how to find that state again and continue from
it after an interruption or a compaction, and in a new
session if the procedure spans sessions. State kept
only in the conversation is gone after a compaction, and two
places holding it disagree sooner or later.

## C6 — Handoffs carry what the receiver needs

For every handoff — to a subagent, a script, the user, the
next skill — name what the receiver must know and check
that the handoff carries it. A subagent sees none of the
conversation; what it needs is in its prompt or in files it
is told to read. Each guarantee the procedure makes has one
owner: when two steps both "make sure" of the same thing,
each relies on the other.

## C7 — Failures have a defined path

Each step that can fail — a script errors, a tool or
interpreter is missing, an input is invalid, a check fails,
the user does not answer — has a defined reaction: retry,
fall back, stop, or ask. A question that times out is no
answer, and nothing that belongs to the user is decided in
its place. A file that ships in the skill directory or among
its set's shared files, and that the skill names by a fixed
path, is no such case when it is missing: a missing one
means a broken installation, not a step that failed (F7). A
bundled script that errors, and a file whose name a step
builds from an input, still need a reaction.

## C8 — Inputs are defined

The skill says what it expects as arguments and input
files, and what it does when one is missing or invalid. An
undefined input makes the agent guess — for an audit, which
skill to audit.

## C9 — The core survives a compaction

After a compaction Claude Code keeps only the first 5,000
tokens of an invoked skill. The steps, the gates, and where
the state lives stand at the top of `SKILL.md`; a procedure
that must survive a compaction (C5) reads each phase's file
again at the start of the phase instead of relying on what
was read before.

## C10 — Every reference resolves

Every skill, tool, section, term, and file outside the
skill directory that the procedure names exists under that
name. A rename that missed one reference leaves a step
pointing to nothing. Whether the skill's own files and its
set's shared files exist is part of the form check.

## C11 — Effects are stated

The skill states what it changes: files, commits, external
systems. A report-only skill changes no file it did not
create in this run. An action that cannot be undone —
deleting a file the skill did not create in this run,
pushing, sending — waits for the user's confirmation. A
temp directory that I16 has the skill delete counts as
created in this run.

## C12 — Done is defined

The skill says when it is finished and what it hands back.
Without that, the agent stops where the work looks done and
reports what it assumes.
