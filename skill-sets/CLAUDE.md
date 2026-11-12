# skill-sets

Each directory here is one skill set. These rules apply to
every set and every skill made in this repository: first
what holds for a set as a whole, then what holds for each
skill in it, then how skills and sets hand work on.

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
  cannot drift apart.
- `agents/` holds an agent for each kind of work a skill
  launches, such as an auditor or an advisor: one persona per
  file. A skill launches it by its full name,
  `<set>:<agent>`; the bare name is not found.

### Input and output

- A set states what it takes as input and what it leaves as
  its result. The input may be a file or only the
  conversation with the user.
- A set has an entry skill, the one a user or a seed starts
  first. The entry skill defines the set's input.
- The entry skill checks its input. When the input is missing
  or unfit, it declines and asks the caller to complete it,
  instead of guessing what was meant.

### Files inside a set

- Skills inside a set work only with temporary files, or
  extend a file handed in from outside the set. A set leaves
  nothing behind but its result.
- Lasting files that pass from one set to another are the
  seed's to define, not the set's.

## The Skill

### Belongs to one set

- A skill belongs to exactly one set and ships only with it.
  Skills of one set may depend on each other.
- A part of a flow is a skill of its own when it has its own
  input and its own result and would also be started alone.
  A step without its own input and result stays a phase, in
  the `references/` of the skill it belongs to.

### Input and result

- Every skill states what it expects and what it creates.
  It checks its input when it starts and stops with a reason,
  or asks, when the input is missing or unfit.
- Its result is what its description says it produces or
  changes. Everything else it writes is temporary.

### Writing a skill

- Use the fields of the Agent Skills specification. A field
  of one harness only where the skill cannot work without it,
  with the reason in the text or in `compatibility`.
- Keep the core procedure — steps, gates, where state lives —
  in the first 5,000 tokens of `SKILL.md`: after a compaction
  Claude Code keeps only that much of an invoked skill.
- A skill that asks the user reads `../../shared/asking.md`
  at the step where it asks.
- A skill that needs a judgment free of the conversation's
  bias runs it in a fresh agent of its set, never in a fork
  of the conversation.

### Temporary files

- Scratch files for one run go into a new directory from the
  system's temp facility (`mktemp -d`, `tempfile.mkdtemp()`)
  or into the scratch directory the harness names, and are
  deleted when the run ends.
- State that must survive a compaction or a new session, and
  every hand-over, goes into a new directory from the
  system's temp facility with a fixed prefix
  (`mktemp -d -t <skill>.XXXXXX`) and a file that names its
  target. Never into the harness's scratch directory, which a
  new session does not see.
- Never into the skill's directory, which an update replaces
  and an audit reads as part of the skill, and never into the
  project tree, where it shows up as a change.
- The skill that hands the directory to no one deletes it.

## Hand-over

### Inside a set

- Skills that form a chain (a starts b, b starts c) pass work
  on through a hand-over file. Its shape comes from the set's
  template in `shared/templates/`.
- The last step of a skill with a successor always starts the
  next skill of the set, as `<set>:<skill>`, with the path of
  the hand-over. The user starts only the entry skill.
- A skill that another skill starts stays invocable by the
  model: a user-only skill cannot be started from another
  skill.
- Whether the model performs the start step is not
  guaranteed. Word it as a step that always runs, and keep the
  state in the hand-over directory, so a stopped chain can be
  resumed from it.

### Checking hand-overs

- When a set chains skills that start each other, the audit
  of each skill checks its hand-overs: the file the sender
  writes is the file, in the place and shape, that the
  receiver reads, and every value the receiver needs is in it.
  A gap here breaks the chain silently, because each skill
  works on its own.

### Between sets

- Sets never start or name each other. A seed links them
  through what each set takes and leaves, and may chain them
  into one flow.
