# Shipped Content and Data

Files a skill carries but does not follow itself. They get a
short check of their own, not the instruction and coherence
items: they are written for other readers, later.

## Which Files These Are

Sort every file of the skill by how `SKILL.md` uses it:
the files in the skill directory, and the files outside it
that `SKILL.md` names by a path relative to the skill
directory, such as its set's shared files under
`../../shared/`. Project files the skill works on are not
files of the skill.

- **Reference** — the agent reads it to decide what to do.
  It is part of the skill's instructions and gets every
  instruction and coherence item.
- **Script** — code the agent runs. What `SKILL.md` says
  about it — how to call it, what it prints, and what
  happens when it fails — is checked with the rest of the
  instructions, against the script's documented usage and
  output;
  the code itself gets none of the items here.
- **Shipped content** — the skill copies or writes it into a
  project: a template, a format guide, a checklist other
  agents read there.
- **Data** — a script or the agent reads it as data: a
  lookup table, a schema, a reference copy to compare with.
- **Other** — neither the agent nor a script uses it: a
  license, a README, an image for human readers. F7 covers
  it; no further item applies.

`references/` usually holds references and `assets/` shipped
content or data, but the use decides, not the directory.

A1 applies to shipped content and data; A2 and A3 apply to
shipped content only, since data is not written for a
reader.

## A1 — Present and named

Every shipped file and data file exists and is named in
`SKILL.md` at the step that uses it. References and scripts
are covered by the form and instruction checks instead.

## A2 — No hidden dependency (`warn`)

Every file, rule, tool, or role a shipped file names either
comes with the same skill set or is named as a requirement
in the skill's `compatibility` field. For a skill that
belongs to no set, such as a fixture, the set is the skill
directory itself. A template that refers to a rule outside
its set works only in a setup that happens to have that
rule, and nothing tells the project it needs it.

## A3 — No contradiction inside a shipped file (`info`)

A shipped file does not tell its later reader two different
things for the same situation.
