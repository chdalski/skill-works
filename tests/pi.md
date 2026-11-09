# Testing Sets in pi

pi is a test harness here, not a target: running a set in pi
shows that its skills do not depend on Claude Code. Seeds
target Claude Code only, so nothing in this repository adds
what pi lacks.

## Before You Start

- pi needs a model provider with an API key. A Claude Pro or
  Max subscription must not be used in pi; Anthropic allows
  it only in its own apps.
- pi has no subagent tool in its core. A skill that needs one,
  such as `sw-skill-audit`, says so in its `compatibility`
  field and stops without it. Install a subagent extension
  yourself; pi's example subagent extension works.

## Load a Set

Install the repository as a project package. pi writes the
entry to `.pi/settings.json` and clones the repository into
`.pi/git/`:

```sh
pi install git:github.com/chdalski/skill-works --local
```

Narrow the package to the sets under test in
`.pi/settings.json`; the root `package.json` declares the
skills of every set:

```json
{
  "packages": [
    {
      "source": "git:github.com/chdalski/skill-works",
      "skills": ["skill-sets/sw-workshop/**"]
    }
  ]
}
```

Keep `.pi/git/` out of version control.

## Run a Skill

pi shows skills without the plugin namespace:
`/skill:sw-skill-audit <path>`.

## Update After a Push

```sh
pi update --extensions --approve
```

Without `--approve`, pi skips the packages in
`.pi/settings.json`, yet still reports "Updated packages".
It does this even with `defaultProjectTrust: always`. Plain
`pi update` updates only pi itself.
