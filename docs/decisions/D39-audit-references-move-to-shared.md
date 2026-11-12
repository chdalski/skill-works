# D39: The audit references move to `shared/`

Status: accepted

## Decision

`form.md`, `coherence.md`, and `shipped.md` move to `shared/`, in the same commit as the skills of step 5c that read them.

- `coherence.md` is also read by `sw-skill-design` and its advisor, because the draft has the shape of the procedure model. `sw-skill-create` reads it too.
- `form.md` and `shipped.md` are also read by `sw-skill-create`.

So each file in `shared/` has at least two readers from the start ([D23](D23-shared-files-in-shared.md)), and the accepted I8 finding from step 5b is settled.

`form.md` then names the audit's script without a path, as the form check of `sw-skill-audit`.

## Reasons

From another skill, the path `scripts/check_form.py` pointed to nothing.
