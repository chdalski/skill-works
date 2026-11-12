# D43: Hand-over templates

Status: accepted

## Decision

A template that two skills name, because one writes and one reads, goes in `shared/templates/`. Examples: `brief.md` (brainstorm → design) and `draft.md` (design → create, review, audit).

A template for a result that only one skill produces goes in that skill's `assets/`. Example: the final report of `sw-skill-review`.

This is [D23](D23-shared-files-in-shared.md), applied to templates.

At hand-overs, the audit checks that writer and reader name the same template.

## Reasons

In EGM (the elephant-goldfish-model repository), the writing skill brings the shape: the brief is in the text of `egm-brainstorm`, and `egm-draft` knows the shape without saying so. A renamed heading there would lose content without notice ("has no other source for them").
