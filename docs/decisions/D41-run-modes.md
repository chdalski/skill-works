# D41: Run modes

Status: accepted

## Decision

How automatically a flow runs is set on two levels.

Between the skills of a set, the user chooses a run mode for each run, where the set offers one:

- "step by step": each skill ends and names the next command with the work document it hands on;
- "straight through": each skill starts the next one itself.

The entry skill asks for the run mode. A caller, for example a seed, can pass it as an argument. It is stored in the header of the work document that carries the flow ([D55](D55-no-flow-directory.md)), and each later skill reads it there; a document that does not carry the flow, such as a review record, names the one that does. The user's gates apply in both modes.

Inside a skill (phases, sub-skills), the design fixes for each hand-over whether it runs automatically or by hand. The draft records this.

A skill that no mode starts automatically may set `disable-model-invocation`, with a reason (F5). A skill that can be started automatically may not, because that field stops every call by the model, also from another skill.

For `sw-workshop`:

- The run mode is set at the start of `sw-skill-brainstorm`.
- The contrarian pass, the advisor passes, and the audit loop of the review always run automatically.
- The decisions at the end of the review are always made by hand.

This decision changes [D35](D35-own-skill-or-phase.md).

## Reasons

EGM (the elephant-goldfish-model repository) is the model. There, the user chooses a preset in `egm-review`: "interactive", with a gate after each stage, or "uninterrupted", without a stop. `egm-review-loop` and `egm-resolve` always run along in the same conversation.
