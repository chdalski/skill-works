# D38: Skills in a set leave only their result

Status: amended by [D54](D54-files-by-reader.md)

## Decision

Inside a set, skills work only with temporary files as [D33](D33-temporary-files.md) describes, or they extend an artifact handed in from outside. A skill leaves for good only its result, for example the finished skill.

The draft of [D36](D36-skills-start-from-a-draft.md) is such a temporary file. `sw-skill-design` writes it, `sw-skill-create` reads it, `sw-skill-review` gives it to the auditor. After that it is deleted. After the run, the finished skill itself is the standard.

Accepted findings are kept in the same temp directory and apply only to this review cycle. A later cycle reports them again, and the user decides again.

Some artifacts must stay in the repository, because a seed passes them on between sets, for example from EGM (the elephant-goldfish-model) to a set that implements. We settle these when it is time; how a seed chains sets after an artifact is still open in the source.

The test bench in `tests/` ([D25](D25-the-test-bench-skill.md)) is not affected. It tests skills and passes nothing between them.

At first this decision gave a lasting place in `tests/<skill>/`. That contradicted [D33](D33-temporary-files.md).
