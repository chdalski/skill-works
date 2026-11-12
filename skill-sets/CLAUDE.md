# skill-sets

Each directory here is one skill set. These rules apply to
every set and every skill made in this repository: first
what holds for a set as a whole, then what holds for each
skill in it, then how skills and sets hand work on. Where a
rule leaves a choice, a table says which case gets which
answer; the set's design records the answer it took.

## The Set

### A set is self-contained

- A set brings everything its flow needs: its skills, the
  files they share, its agents, and its hand-over templates.
  It never refers to another set, so it works wherever it is
  installed, alone or next to any other set.
- A set ships as a plugin. Its skill text follows the Agent
  Skills specification and depends on no harness; what one
  harness needs lives in that harness's manifest. A set holds
  no harness code, such as hooks or extensions: a harness that
  lacks something the set needs is named in the skills'
  `compatibility` field, not patched.
- Every set carries its own `LICENSE.md` (MIT) and names the
  license in its manifest: a set is installed without this
  repository's root, and MIT requires the notice in every
  copy.

### Layout

```
<set>/
├── .claude-plugin/plugin.json   manifest: name, description, license
├── LICENSE.md                   the set's MIT license
├── skills/<skill>/              one directory per skill
├── shared/                      files two or more skills read
│   └── templates/               hand-over templates
└── agents/                      the set's own agents
```

- `shared/` holds what at least two skills of the set read.
  What only one skill reads stays in that skill's
  `references/` or `assets/`. A skill reaches a shared file
  only as `../../shared/<file>`, relative to its `SKILL.md`:
  one fixed path, which the form check knows.
- `shared/templates/` holds one template per hand-over: the
  shape of the file one skill writes and the next one reads.
  Both skills name the same template, so writer and reader
  cannot drift apart. A template for a result that only one
  skill produces, such as a final report, stays in that
  skill's `assets/`.
- `agents/` holds an agent for each kind of work a skill
  launches, such as an auditor or an advisor: one persona per
  file. A skill launches it by its full name,
  `<set>:<agent>`; the bare name is not found.

### Input and output

- A set states what it takes as input and what it leaves as
  its result. The input may be a file or only the
  conversation with the user.
- A set has an entry skill, the one a user or a seed starts
  first. The entry skill defines the set's input and, where
  the set offers one, asks for the run mode (see Hand-over).
- The entry skill checks its input. When the input is missing
  or unfit, it declines and asks the caller to complete it,
  instead of guessing what was meant.

### What a set leaves behind

Inside a set, skills work only with temporary files, or
extend a file handed in from outside the set. The set's
design decides for each output which kind it is:

| Output | Read by | Where | Removed |
|---|---|---|---|
| Scratch file of one run | the skill alone | new temp directory | when the run ends |
| State and hand-overs inside the set | skills of the set | temp directory with a fixed prefix | by the skill that hands it to no one |
| Lasting result: a design document, an ADR, a kept brief, a file for another machine | people, a team, other agents | where the project's instructions say, else where the user picks | never: it belongs to the project |
| Hand-over to another set | another set | defined by the seed | — |

A lasting result is worked out in the temp directory and
written to its place by a last step of its own; only there
does it become the skill's result, which its description
names.

## The Skill

### Three forms of a part

A part of a set's flow takes one of three forms:

| Form | When | Lives in | Started by | Afterwards |
|---|---|---|---|---|
| Chain link | it has its own input and result, and passes its work on | `skills/<skill>/` | the user, or the previous skill in run mode "straight through" | the caller has ended; the link hands over to the next one |
| Sub-skill | it has its own input and result, and another skill uses it inside its own flow | `skills/<skill>/` | another skill, through the skill tool; or the user, alone | it returns what it states to the caller, and starts nothing further |
| Phase | it has no input or result of its own | the `references/` of its skill | its skill, which reads it at the start of the phase | its skill goes on |

A part is a skill of its own when it would also be started
alone. Keep every skill directly under `skills/`: a
`SKILL.md` deeper inside another skill's directory is, if
read at all, only a file of that skill.

### Input and result

- Every skill states what it expects and what it creates.
  It checks its input when it starts and stops with a reason,
  or asks, when the input is missing or unfit.
- Its result is what its description says it produces or
  changes. Everything else it writes is temporary; where
  temporary files go is item I16 of the shared guideline
  (`sw-workshop/shared/instructions-skills.md`).

### Where state lives

| The procedure | Its state |
|---|---|
| runs once and ends with its result | may stay in the conversation |
| waits for the user between steps | a file in its temp directory |
| repeats steps for each file, task, or round | a file in its temp directory |
| runs until a condition holds | a file in its temp directory |

State kept only in the conversation is gone after a
compaction. A skill whose state lives in a file says how to
find it and go on after an interruption, a compaction, or in
a new session. The skill's design shows the choice in the
"Reads / writes" column of its procedure table.

### Writing a skill

Every skill is written with the skills of the workshop set
and checked against its guideline: the instruction items in
`sw-workshop/shared/` (`instructions.md`,
`instructions-skills.md`) and the form, coherence, and
shipped-content items of `sw-skill-audit`. What the guideline
says applies here; this file does not repeat it, so the two
cannot drift apart. The guideline ships with the workshop and
also governs the skills it makes in other projects.

## Hand-over

### How far a flow runs on its own

| Level | Decided by | When | Choices |
|---|---|---|---|
| Between the skills of a set | the user, for each run; a caller may pass it | at the start, by the entry skill | "step by step": each skill ends and names the next command with the hand-over directory; "straight through": each skill starts the next |
| Inside a skill: phases and sub-skills | the skill's design | when the skill is designed | automatic or by hand, for each hand-over |

- The run mode is stored in the hand-over directory, and
  every later skill reads it there. The user's gates hold in
  both modes; the mode decides only who starts the next
  skill.
- A skill that some mode starts automatically stays
  invocable by the model: a user-only skill cannot be
  started from another skill. A skill that no mode starts
  automatically may set the harness's field for user-only
  start, with the reason.
- Whether the model performs a start step is not guaranteed.
  Word it as a step that always runs in its mode, and keep
  the state in the hand-over directory, so a stopped chain
  can be resumed from it.

### Inside a set

- Chain links pass work on through a hand-over file. Its
  shape comes from the set's template in `shared/templates/`.
- In run mode "straight through", the last step of a chain
  link starts the next skill of the set, as `<set>:<skill>`,
  with the path of the hand-over directory.

### Checking hand-overs

- When a set chains skills or calls sub-skills, the audit of
  each skill checks its hand-overs: the file the sender
  writes is the file, in the place and shape, that the
  receiver reads, and every value the receiver needs is in it.
  A gap here breaks the chain silently, because each skill
  works on its own.

### Between sets

- Sets never start or name each other. A seed links them
  through what each set takes and leaves, and may chain them
  into one flow.
