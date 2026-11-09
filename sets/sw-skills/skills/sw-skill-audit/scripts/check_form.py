#!/usr/bin/env python3
"""Check the form of an agent skill (references/form.md, items marked "script").

Usage: check_form.py <skill-dir> [--prefix <name-prefix>]

Prints one line per finding: "<severity> <item> <path>[:<line>] <message>",
then a summary line. Severity is fail, warn, or info.
Exit code: 0 without fail findings, 1 with fail findings, 2 on usage errors.
Standard library only; the frontmatter parser covers the YAML subset that
skill frontmatter uses (scalars, quoted scalars, block scalars, one level of
nested mappings and lists).
"""

import os
import re
import sys

SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
CLAUDE_CODE_KEYS = {
    "when_to_use", "argument-hint", "arguments", "disable-model-invocation",
    "user-invocable", "disallowed-tools", "model", "effort", "context", "agent",
    "background", "hooks", "paths", "shell",
}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PATH_RE = re.compile(r"(?:\$\{CLAUDE_SKILL_DIR\}/)?((?:scripts|references|assets)/[A-Za-z0-9._/-]+)")
SKILL_LINE_LIMIT = 500
BODY_TOKEN_LIMIT = 5000
LISTING_CHAR_LIMIT = 1536

findings = []


def report(severity, item, path, message, line=None):
    location = f"{path}:{line}" if line else path
    findings.append((severity, item, location, message))


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return re.sub(r"\s+#.*$", "", value)


def parse_frontmatter(lines):
    """Return (data, key_lines, body_start) or raise ValueError."""
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md does not start with a '---' frontmatter line")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("frontmatter has no closing '---' line")
    data, key_lines = {}, {}
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s+(.*))?$", line)
        if not match:
            raise ValueError(f"line {i + 1}: cannot parse frontmatter line {line.strip()!r}")
        key, rest = match.group(1), (match.group(2) or "").strip()
        key_lines[key] = i + 1
        i += 1
        block = []
        while i < end and (not lines[i].strip() or lines[i][:1] in (" ", "\t")):
            block.append(lines[i])
            i += 1
        while block and not block[-1].strip():
            block.pop()
        if rest[:1] in ("|", ">"):
            stripped = [b.strip() for b in block]
            if rest[0] == "|":
                data[key] = "\n".join(stripped)
            else:
                paragraphs, current = [], []
                for text in stripped + [""]:
                    if text:
                        current.append(text)
                    elif current:
                        paragraphs.append(" ".join(current))
                        current = []
                data[key] = "\n".join(paragraphs)
        elif rest:
            data[key] = " ".join([unquote(rest)] + [b.strip() for b in block if b.strip()])
        elif all(b.strip().startswith("- ") or not b.strip() for b in block):
            data[key] = [unquote(b.strip()[2:]) for b in block if b.strip()]
        else:
            mapping = {}
            for b in block:
                if b.strip():
                    k, _, v = b.strip().partition(":")
                    mapping[k.strip()] = v.strip()
            data[key] = mapping
    return data, key_lines, end + 1


def check_name(data, key_lines, skill_dir, prefix):
    name = data.get("name")
    line = key_lines.get("name")
    if not isinstance(name, str) or not name:
        report("fail", "F2", "SKILL.md", "name is missing or empty", line)
        return
    if len(name) > 64:
        report("fail", "F2", "SKILL.md", f"name has {len(name)} characters; the limit is 64", line)
    if not NAME_RE.match(name):
        report("fail", "F2", "SKILL.md",
               f"name {name!r} must be lowercase letters, digits and single hyphens, "
               "without a leading or trailing hyphen", line)
    dir_name = os.path.basename(os.path.normpath(skill_dir))
    if name != dir_name:
        report("fail", "F2", "SKILL.md", f"name {name!r} does not match the directory name {dir_name!r}", line)
    if prefix and not name.startswith(prefix):
        report("fail", "F2", "SKILL.md", f"name {name!r} lacks the project prefix {prefix!r}", line)
    if "anthropic" in name or "claude" in name:
        report("warn", "F2", "SKILL.md", "name contains 'anthropic' or 'claude'; the Claude API rejects such names", line)


def check_description(data, key_lines):
    description = data.get("description")
    line = key_lines.get("description")
    if not isinstance(description, str) or not description.strip():
        report("fail", "F3", "SKILL.md", "description is missing or empty", line)
        return
    if len(description) > 1024:
        report("fail", "F3", "SKILL.md", f"description has {len(description)} characters; the limit is 1024", line)
    if re.search(r"<[A-Za-z/][^>]*>", description):
        report("warn", "F3", "SKILL.md", "description contains an XML tag; the Claude API rejects it", line)
    when = data.get("when_to_use")
    if isinstance(when, str) and len(description) + len(when) > LISTING_CHAR_LIMIT:
        report("warn", "F3", "SKILL.md",
               f"description and when_to_use have {len(description) + len(when)} characters together; "
               f"Claude Code cuts the listing entry at {LISTING_CHAR_LIMIT}", line)


def check_fields(data, key_lines):
    for key in data:
        if key not in SPEC_KEYS and key not in CLAUDE_CODE_KEYS:
            report("warn", "F5", "SKILL.md",
                   f"key {key!r} is neither in the Agent Skills spec nor a Claude Code skill field", key_lines[key])
    compatibility = data.get("compatibility")
    if compatibility is not None and not (isinstance(compatibility, str) and 1 <= len(compatibility) <= 500):
        report("fail", "F4", "SKILL.md", "compatibility must be a string of 1-500 characters", key_lines["compatibility"])
    metadata = data.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        report("fail", "F4", "SKILL.md", "metadata must be a map of string keys to string values", key_lines["metadata"])
    if isinstance(data.get("allowed-tools"), list):
        report("warn", "F4", "SKILL.md",
               "allowed-tools is a list; the spec defines a space-separated string", key_lines["allowed-tools"])
    harness_keys = sorted(k for k in data if k in CLAUDE_CODE_KEYS)
    if harness_keys and "claude code" not in str(compatibility or "").lower():
        report("info", "F5", "SKILL.md",
               f"uses Claude Code fields ({', '.join(harness_keys)}) without naming Claude Code in compatibility")


def check_size(lines, body_start):
    if len(lines) > SKILL_LINE_LIMIT:
        report("warn", "F6", "SKILL.md", f"SKILL.md has {len(lines)} lines; the target is under {SKILL_LINE_LIMIT}")
    body_tokens = len("\n".join(lines[body_start:])) // 4
    if body_tokens > BODY_TOKEN_LIMIT:
        report("warn", "F6", "SKILL.md",
               f"body is about {body_tokens} tokens; the target is under {BODY_TOKEN_LIMIT}")
    report("info", "F6", "SKILL.md", f"{len(lines)} lines, body about {body_tokens} tokens (characters / 4)")


def referenced_paths(text):
    refs = []
    for number, line in enumerate(text.splitlines(), start=1):
        targets = [t.split("#")[0] for t in LINK_RE.findall(line) if not re.match(r"^[a-z]+:|^#|^/", t)]
        targets += [t.rstrip(".,:;)") for t in PATH_RE.findall(line)]
        for target in dict.fromkeys(targets):
            refs.append((target, number))
    return refs


def check_references(skill_dir, skill_text):
    skill_root = os.path.abspath(skill_dir)
    dir_name = os.path.basename(os.path.normpath(skill_dir))
    from_skill = set()
    for target, number in referenced_paths(skill_text):
        from_skill.add(os.path.normpath(target))
        if not os.path.exists(os.path.join(skill_root, target)):
            report("fail", "F7", "SKILL.md", f"references {target!r}, which does not exist", number)
    own_path = re.compile(r"\.claude/skills/" + re.escape(dir_name) + r"/([A-Za-z0-9._/-]+)")
    for number, line in enumerate(skill_text.splitlines(), start=1):
        for target in dict.fromkeys(t.rstrip(".,:;)") for t in own_path.findall(line)):
            from_skill.add(os.path.normpath(target))
            if not os.path.exists(os.path.join(skill_root, target)):
                report("fail", "F7", "SKILL.md", f"references {target!r}, which does not exist", number)
            report("warn", "F7", "SKILL.md",
                   f"names its own file {target!r} through a project path; a path relative to the skill "
                   "directory keeps working wherever the skill is installed", number)
    for directory, _, files in os.walk(skill_root):
        for file_name in files:
            path = os.path.relpath(os.path.join(directory, file_name), skill_root)
            if path == "SKILL.md":
                continue
            if file_name.endswith(".md"):
                with open(os.path.join(skill_root, path), encoding="utf-8") as handle:
                    for target, number in referenced_paths(handle.read()):
                        resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
                        sibling = os.path.normpath(target)
                        if not (os.path.exists(os.path.join(skill_root, resolved))
                                or os.path.exists(os.path.join(skill_root, sibling))):
                            report("fail", "F7", path, f"references {target!r}, which does not exist", number)
                        elif sibling.endswith(".md") and sibling != path:
                            report("warn", "F7", path,
                                   f"points on to {target!r}; keep references one level deep from SKILL.md",
                                   number)
            named = (path in from_skill
                     or any(path.startswith(r.rstrip("/") + "/") for r in from_skill)
                     or re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(file_name) + r"(?![A-Za-z0-9_-])", skill_text))
            if not named:
                report("info", "F7", path, "no line in SKILL.md names this file")


def main(argv):
    args = list(argv)
    prefix = None
    if "--prefix" in args:
        index = args.index("--prefix")
        if index + 1 >= len(args):
            print("usage: check_form.py <skill-dir> [--prefix <name-prefix>]", file=sys.stderr)
            return 2
        prefix = args[index + 1]
        del args[index:index + 2]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print("usage: check_form.py <skill-dir> [--prefix <name-prefix>]", file=sys.stderr)
        return 2
    skill_dir = args[0]
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        report("fail", "F1", skill_dir, "the directory has no SKILL.md")
    else:
        with open(skill_md, encoding="utf-8") as handle:
            text = handle.read()
        lines = text.splitlines()
        try:
            data, key_lines, body_start = parse_frontmatter(lines)
        except ValueError as error:
            report("fail", "F1", "SKILL.md", str(error))
        else:
            check_name(data, key_lines, skill_dir, prefix)
            check_description(data, key_lines)
            check_fields(data, key_lines)
            check_size(lines, body_start)
            check_references(skill_dir, text)
    for severity, item, location, message in findings:
        print(f"{severity} {item} {location} {message}")
    counts = {s: sum(1 for f in findings if f[0] == s) for s in ("fail", "warn", "info")}
    print(f"summary: {counts['fail']} fail, {counts['warn']} warn, {counts['info']} info")
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
