# D3: Sets never refer to each other

Status: accepted

## Decision

Skill sets never refer to each other. Each set states what it takes as input and what it leaves as its result. The input can also be only the conversation with the user, for example when a set takes up a first document.

A seed links sets through these statements. In this way a seed can chain sets into an automatic flow. Example: create an artifact with the user; after acceptance, implement it without a further question.

Before step 5 of the plan, this decision said only "Only a seed links sets". The statements of input and result were added then.
