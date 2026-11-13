# Harness Phrases

Phrases for actions that many skills need, worded so that
every harness that reads the Agent Skills specification can
run them. A skill that needs one of these actions uses the
phrase as given; a skill made for another project copies the
phrase into its own text, since it cannot refer to this file.

Each entry gives the action, the phrase, and the evidence:
where it was tested and how. An entry without evidence is
untested; a skill may use it, and its first run in each
harness is its test.

## Start a fresh subagent

Phrase: "Start a fresh subagent that does not inherit this
conversation, with your harness's subagent tool (in Claude
Code: the Agent tool with the type `<plugin>:<agent>`; if the
harness does not know that type, a fresh general subagent told
to read the agent definition at `<path>` first). Never use a
fork, which carries the conversation along. If your harness
has no subagent tool, say so and <what the skill does then>."

Evidence: Claude Code — `sw-skill-audit` runs 1 to 29 started
their auditor this way; a test plugin's agent started as
`<plugin>:<agent>` got its own text, and its bare name failed
with "Agent type not found". pi — the audit ran end to end
with pi's example subagent extension; without it, pi has no
subagent tool.

## Refer to the skill's own directory

Phrase: "Below, `<skill-dir>` is the directory of this file:
in Claude Code `${CLAUDE_SKILL_DIR}`; in another harness, or
if the previous word shows no absolute path, the directory
you read this file from." Files of the plugin are then
`<skill-dir>/../../shared/<file>` and
`<skill-dir>/../../agents/<file>`.

Evidence: Claude Code and pi — `sw-skill-audit` found its
scripts and references this way in both.

## Use the workspace

Phrase: "Run
`python3 <skill-dir>/../../shared/scripts/workspace.py --root <project> path work`
(or `path temp`): it creates the workspace when it is missing
and prints the directory to use; `new-temp <name>` makes a
new directory in `temp/`. When it says `created <path>` on
stderr, tell the user that the settings file was created and
is meant to be committed. Delete work documents and the
directories you made in `temp/` only with its `delete`
command." A skill made
for another project copies the script into its own plugin.

Evidence: untested as a phrase; the script runs with Python 3
on every system.

## Start a sub-skill

Phrase: "Start the skill `<plugin>:<skill>` with your
harness's skill tool (in Claude Code: the Skill tool), with
<arguments>. It returns its result to you; go on with the
next step when it has."

Evidence: Claude Code — an agent of a test plugin started the
plugin's skill `<plugin>:<skill>` this way. That a calling
skill goes on after the sub-skill returns is untested.

## Hand over to the next skill

Phrase: "In run mode 'straight through', start the skill
`<plugin>:<skill>` with your harness's skill tool, with the
path of <work document>, as your last action. In both run
modes, first print the command that starts it (in Claude
Code: `/<plugin>:<skill> <path>`), so the user can start it
by hand if the start stops."

Evidence: untested.

## Give a resume command

Phrase: "Tell the user the command that resumes this skill
with <work document> (in Claude Code:
`/<plugin>:<skill> <path>`)."

Evidence: untested.

## Ask the user

Phrase: "Read `<skill-dir>/../../shared/asking.md`, then ask
the user with your harness's question tool, or in plain text
if it has none, and wait for the answer."

Evidence: untested.

## Recognize an installed copy

Phrase: "A path inside the copy of a plugin that the harness
installed (in Claude Code under `~/.claude/plugins/`) is no
place to change a skill: an update replaces it. Ask for the
skill's source in the repository."

Evidence: untested.
