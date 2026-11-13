# User Decisions

Step 7 of the review. Ask about the open entries under Sorted:
`info`, disputed, trade-off, and agreed. Open with the number
of items and one line on each. Ask the acceptance question
(Acceptance) only when no entry under Sorted is open or marked
taken; the sections below say when. Every answer goes under Decisions, with the pass
count, before you act on it.

## Nothing to decide

The guard above allows the acceptance question as this step
starts → tell the user the last pass was clean, and go to
Acceptance.

## When the loop stopped with agreed entries open

The pass count reached `stop-at`, or the last pass named
churn. First ask one question that names the open agreed
entries and why the loop stopped (from Passes):

- **go on fixing all** → mark them taken;
- **decide each** → they join the questions below;
- **back to sw-skill-design** → see Hand-back; offer it only
  when `draft` names a file.

Skip this question when Decisions already holds one of these
three answers at the current pass count; that answer then
applies.

## One question per item

Each with the finding, the proposed fix, and a
recommendation:

- `info`: take or drop;
- disputed, trade-off, or an agreed entry to decide: take, or
  accept with a reason (the entry then goes under Accepted
  with the item, the quoted place, and the reason).

Then: something taken → set `stop-at` to the pass count + 5,
under Decisions, and go to step 5; nothing taken →
Acceptance.

## Acceptance

Ask once whether the user accepts the reviewed skill, with the
passes run, the fixes, and the accepted findings in one line
each:

- **accept** → step 8;
- **not yet** → ask what is missing, and, when `draft` names
  a file, offer back to sw-skill-design (see Hand-back) as an
  option of that question. Each point named becomes a taken
  entry under Sorted, written as
  `pass <n>, user, "<the point>": trade-off — the user's point — taken`,
  and the run goes to step 5 with `stop-at` set to the pass
  count + 5. No point named → ask the acceptance question
  again.

## At any question

- **pause** → give the resume command and stop;
- **abandon** → confirm first, naming the files that will be
  deleted (a "no" returns to the question); then delete the
  review directory and the cycle's work documents as step 8
  does, and stop.

## Hand-back

1. Delete the review directory, and the record this record
   names as `reason` if it lies in the workspace: this record
   now carries the flow.
2. Write under Final state "handed back to sw-skill-design"
   with the command that starts it with this record (in
   Claude Code: `/sw-workshop:sw-skill-design <record>`), what
   is open, and how to see the changes, and
   `status: handed-back`. The record, the draft and the brief
   stay: the flow goes on in sw-skill-design.
3. Print that command.
4. When the draft's header has the run mode "straight
   through", start `sw-workshop:sw-skill-design` with the
   record's path with your harness's skill tool. Stop.

The review does not track whether design received the
record: if that start stops, the user runs the command from
the record.
