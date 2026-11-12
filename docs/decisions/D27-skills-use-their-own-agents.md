# D27: Skills use their own agents

Status: accepted

## Decision

When a skill needs an agent, it gets its own agent, made for it, as an agent file in the plugin. There is one persona for each file and one thin adapter for each harness ([D2](D2-harness-independent-sets.md)). Skills do not use a general subagent.

The change started with a test: does the agent tool accept `<plugin>:<agent>` as the agent type, and what do plugin agents ignore. The test passed in step 5c. The agent tool accepted the full name `<plugin>:<agent>` and the agent got its own text. The bare name failed with "Agent type 'probe' not found". Plugin agents ignore `hooks`, `mcpServers`, and `permissionMode`.

Because the test passed:

- The auditor of `sw-skill-audit` and the advisors of [D31](D31-seeds-draft-advice-acceptance.md) move into agents of their own.
- The instruction from step 3 to launch a fresh general subagent goes away.
- `sw-skill-audit` learns to check the agents of a set.

pi has no agent format in its core. There, users adapt themselves ([D14](D14-no-missing-harness-capabilities.md)).

## Reasons

EGM (the elephant-goldfish-model repository) is the model: agents get a thin adapter for each harness, with tools and isolation.

## Consequences

- A skill always launches its agent by the full name, for example `sw-workshop:<agent>`.
- An agent that needs `hooks`, `mcpServers`, or `permissionMode` does not fit in a set.
