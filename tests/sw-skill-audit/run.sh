#!/bin/sh
# Runs sw-skill-audit headless on every test object and writes one
# report per object to results/. Loads the set with --plugin-dir:
# a headless run does not load the project's local marketplace.
# Usage: tests/sw-skill-audit/run.sh [object ...]   (default: all)
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/../.." && pwd)"
cd "$root"
mkdir -p "$here/results"

objects="${*:-sw-skill-audit ensure-ai-dirs blueprint-audit broken-skill}"
for object in $objects; do
  if [ "$object" = sw-skill-audit ]; then
    path=skill-sets/sw-workshop/skills/sw-skill-audit
  else
    path=tests/sw-skill-audit/fixtures/$object
  fi
  echo "auditing $path"
  claude -p --model opus --plugin-dir skill-sets/sw-workshop \
    --allowedTools Agent Read Glob Grep "Bash(python3:*)" "Bash(ls:*)" "Bash(find:*)" \
    -- "/sw-workshop:sw-skill-audit $path" \
    > "$here/results/$object.md" 2>&1 &
done
wait
echo "reports in $here/results/"
