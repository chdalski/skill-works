# D2: Sets do not depend on a harness

Status: accepted

## Decision

A skill set does not depend on a harness. It has one skill text for all harnesses. Each harness gets a manifest and thin adapters.

## Reasons

EGM (the elephant-goldfish-model repository) is the model. EGM has one skill text for all harnesses. Each harness finds its manifest at the path it expects. Agents get a thin adapter for each harness, with tools and isolation; the model stays `inherit`.
