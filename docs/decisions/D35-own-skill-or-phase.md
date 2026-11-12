# D35: Own skill or phase

Status: amended by [D41](D41-run-modes.md)

## Decision

Inside a set, a part of a flow is a skill of its own when it has its own input and its own result, and one would also start it alone. Such a skill is a chain link.

In run mode "straight through", its last step always starts the next skill of the set (`<set>:<skill>`) with the file it hands over. In run mode "step by step", it names the command instead. So the user starts only the first skill. Each later skill can also be started alone with its input file, audited, and tested on the test bench.

A work step without its own input and result is not a skill of its own. It stays a phase in the references of a skill. The skill reads the phase again at the start of the phase (C9).

Whether the model carries out the hand-over is not guaranteed: the model decides whether it runs a start step from an instruction. So the start step is worded as unconditional (I3), and the state is in a file (C5). Step 5c tests whether the hand-over works reliably; the source gives no result.

Chained skills stay invocable by the model. Unlike in EGM (the elephant-goldfish-model repository), a person need not start each step. Between sets, the seed chains ([D3](D3-sets-never-refer-to-each-other.md)); how it does that is still open in the source.

What changed: this decision first said that the last step always starts the next skill. [D41](D41-run-modes.md) added the run modes, so this holds only in run mode "straight through".

## Reasons

`disable-model-invocation: true` stops every call by the model, also from another skill. In EGM a person starts the next skill, because its skills set this field.

## Consequences

- No hook fires when a skill is done. So inside a set the skills chain themselves.
