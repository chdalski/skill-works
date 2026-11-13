# Open the Cycle

Step 2 of the review, when no open record was given. Work
through the parts in this order, and ask a question only when
its case occurs.

`workspace.py` and `<root>` are as under The Record in
`SKILL.md`.

## Open records of this skill

List them with
`workspace.py open review review --field skill-path=<absolute skill path>`.
A record that another open record's header lists under
`closes` is being closed: finish deleting it (see Closing)
and leave it out.

**Handed a draft:**

- an open record that names this draft and has no report
  under Passes → it is this cycle: resume it as the table
  under Resume in `SKILL.md` says;
- other open records → ask once: delete them and start a new
  cycle; resume the one that names this draft (offer this
  only when exactly one does, and say its findings may be
  stale if the draft changed since); or stop (end, and give
  the command that hands the draft in again);
- none → New cycle.

**A skill path without `--new`:**

- none → Version control;
- one → resume it as the table under Resume in `SKILL.md`
  says; tell the user which record it is and that `--new`
  starts a new cycle;
- more than one → list them and ask which one goes on, and
  say that the others will be deleted; delete them with the
  answer, as in Closing; then resume the chosen one as the table under Resume in
  `SKILL.md` says.

**A skill path with `--new`:** open records → ask to confirm
deleting them (a "no" ends the run) → Version control; none
→ Version control.

## Version control

Only for a new cycle started on a skill path. The skill's
directory, or a shared file its `SKILL.md` names, has
uncommitted changes, or is not under version control → ask:
go on (the review's fixes then mix with those changes), or
stop to commit first (end; nothing has changed yet).

## New cycle

1. Take the values to carry over: from a handed-in draft, its
   path and its header's `root` and reason; with `--new` and
   exactly one record to close, that record's `draft` and
   `reason`; else
   none, and with two or more records to close tell the user
   that the new cycle runs without a draft.
2. Write the new record from the template, with the name from
   `workspace.py next-name <skill> review`: `skill-path`; `root` from the
   draft's header, else `<root>`; `draft`; `reason`; `closes`
   (the records this cycle replaces); `stop-at: none`;
   `status: review:auditing 1`.
3. Delete each record that `closes` lists (see Closing).
4. Give the user the record's path and the resume command.

## Closing

To close another cycle: delete with `workspace.py delete` its
review directory (see Helper Files in `SKILL.md`), then its
record, and tell the user which record went. Its draft, brief
and reason record stay: the new cycle takes them over when it
names the same draft; otherwise name them to the user as left
where they are. A crash
between the two leaves the record, so the next run finishes
the closing.

## When a script fails

As under Helper Files in `SKILL.md`.
