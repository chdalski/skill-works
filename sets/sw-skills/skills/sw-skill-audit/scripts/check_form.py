#!/usr/bin/env python3
"""Check the form of an agent skill: the items in references/form.md marked "script".

Usage: check_form.py <skill-dir> [--prefix <name-prefix>]

Prints one line per finding: "<severity> <item> <path>[:<line>] <message>",
then a final line "summary: N fail, N warn, N info". The severity is a
proposal; the audit grades each finding by its own severity definitions.

Exit code: 0 without fail findings, 1 with fail findings, 2 when the script
could not run (usage error, unreadable directory). Exit 1 is a result, not an
error. If the frontmatter cannot be parsed, the name, description and field
checks are skipped and reported as skipped; the size and reference checks
still run.

Standard library only. The frontmatter parser covers the YAML subset skill
frontmatter uses: plain, quoted and block scalars, flow maps and lists, and
one level of nested mappings and lists. It also flags plain values that a
full YAML parser rejects.
"""

import os
import re
import sys

# Field lists and limits mirror references/form.md (F4, F5, F6). Change both together.
SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
CLAUDE_CODE_KEYS = {
    "when_to_use", "argument-hint", "arguments", "disable-model-invocation",
    "user-invocable", "disallowed-tools", "model", "effort", "context", "agent",
    "background", "hooks", "paths", "shell",
}
SKILL_LINE_LIMIT = 500
BODY_TOKEN_LIMIT = 5000
LISTING_CHAR_LIMIT = 1536

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# A skill-relative path starts a token: at line start, after a space, quote or
# bracket, or after ${CLAUDE_SKILL_DIR}/ or a <placeholder>/ such as <audit-dir>/.
# "docs/references/x.md" is a project path and does not match.
PATH_RE = re.compile(
    r"(?<![\w./-])(?:\$\{CLAUDE_SKILL_DIR\}/|<[a-z-]+>/)?((?:scripts|references|assets)/[A-Za-z0-9._/-]+)")
YAML_INDICATORS = "*&!%@`"
# Unquoted values a YAML parser turns into a number, boolean or null instead of a string.
YAML_TYPED_RE = re.compile(
    r"^(?:[-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?|0x[0-9a-fA-F]+|true|false|yes|no|on|off|null|~)$", re.IGNORECASE)

findings = []
typed_values = []  # (top-level key, nested key, line) of unquoted values YAML does not read as strings


def report(severity, item, path, message, line=None):
    location = f"{path}:{line}" if line else path
    findings.append((severity, item, location, message))


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return re.sub(r"\s+#.*$", "", value)


def is_quoted(value):
    value = value.strip()
    return len(value) >= 2 and value[0] == value[-1] and value[0] in "'\""


def parse_flow(value, top_key, line):
    """Parse a one-line flow map {a: b, c: d} or flow list [a, b]."""
    inner = value[1:-1].strip()
    items = [part.strip() for part in inner.split(",") if part.strip()] if inner else []
    if value.startswith("["):
        return [unquote(item) for item in items]
    mapping = {}
    for item in items:
        key, _, val = item.partition(":")
        if YAML_TYPED_RE.match(val.strip()):
            typed_values.append((top_key, unquote(key), line))
        mapping[unquote(key)] = unquote(val)
    return mapping


def frontmatter_end(lines):
    if not lines or lines[0].strip() != "---":
        return None
    return next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)


def parse_frontmatter(lines):
    """Return (data, key_lines) or raise ValueError."""
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md does not start with a '---' frontmatter line")
    end = frontmatter_end(lines)
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
        elif rest[:1] in ("{", "[") and rest[-1:] in ("}", "]"):
            data[key] = parse_flow(rest, key, key_lines[key])
        elif rest[:1] == "#":
            report("fail", "F1", "SKILL.md",
                   f"the value of {key!r} starts with '#', which YAML reads as a comment, so the value is empty; "
                   "quote it", key_lines[key])
            data[key] = None
        elif rest[:1] in ("'", '"') and not is_quoted(" ".join([rest] + [b.strip() for b in block if b.strip()])):
            report("fail", "F1", "SKILL.md",
                   f"the value of {key!r} opens a quote it never closes, which YAML parsers reject",
                   key_lines[key])
            data[key] = rest
        elif rest:
            continuation = [b.strip() for b in block if b.strip()]
            if rest[:1] not in ("'", '"'):
                for text in [rest] + continuation:
                    if ": " in text or text[:1] in YAML_INDICATORS:
                        report("fail", "F1", "SKILL.md",
                               f"the plain value of {key!r} contains ': ' or starts with a YAML indicator, "
                               "which YAML parsers reject; quote the value or use a block scalar (>)",
                               key_lines[key])
                        break
            data[key] = " ".join([unquote(rest)] + continuation)
        elif all(b.strip().startswith("- ") or not b.strip() for b in block):
            data[key] = [unquote(b.strip()[2:]) for b in block if b.strip()]
        else:
            mapping = {}
            offset = key_lines[key]
            for number, b in enumerate(block, start=offset + 1):
                if b.strip():
                    k, _, v = b.strip().partition(":")
                    if YAML_TYPED_RE.match(v.strip()):
                        typed_values.append((key, k.strip(), number))
                    mapping[k.strip()] = unquote(v)
            data[key] = mapping
    return data, key_lines


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
    if metadata is not None and not (isinstance(metadata, dict)
                                     and all(isinstance(v, str) for v in metadata.values())):
        report("fail", "F4", "SKILL.md", "metadata must be a map of string keys to string values", key_lines["metadata"])
    for top_key, nested_key, line in typed_values:
        if top_key == "metadata":
            report("fail", "F4", "SKILL.md",
                   f"metadata value {nested_key!r} is unquoted, so YAML reads it as a number, boolean or null, "
                   "not a string; quote it", line)
    if isinstance(data.get("allowed-tools"), list):
        report("warn", "F4", "SKILL.md",
               "allowed-tools is a list; the spec defines a space-separated string", key_lines["allowed-tools"])
    for key in sorted(k for k in data if k in CLAUDE_CODE_KEYS):
        report("info", "F5", "SKILL.md",
               f"{key!r} is a Claude Code field, not a spec field: allowed only where the skill cannot work "
               "without it, with the reason stated (judge by reading)", key_lines[key])


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
    # Any project path that runs through the skill's own directory name, such as
    # .claude/skills/<name>/x or skill-sets/<set>/skills/<name>/x.
    own_path = re.compile(r"(?<![\w.-])(?:[\w.-]+/)+" + re.escape(dir_name) + r"/([A-Za-z0-9._/-]+)")
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
            if file_name.endswith(".md") and not path.startswith("assets" + os.sep):
                try:
                    with open(os.path.join(skill_root, path), encoding="utf-8") as handle:
                        content = handle.read()
                except UnicodeDecodeError:
                    report("warn", "F7", path, "is not UTF-8 text; its references were not checked")
                    content = ""
                if content:
                    for target, number in referenced_paths(content):
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
                report("warn", "F7", path, "no line in SKILL.md names this file, so nothing ever reads it")


def main(argv):
    usage = "usage: check_form.py <skill-dir> [--prefix <name-prefix>]"
    args = list(argv)
    prefix = None
    if "--prefix" in args:
        index = args.index("--prefix")
        if index + 1 >= len(args):
            print(usage, file=sys.stderr)
            return 2
        prefix = args[index + 1]
        del args[index:index + 2]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print(usage, file=sys.stderr)
        return 2
    skill_dir = args[0]
    skill_md = os.path.join(skill_dir, "SKILL.md")
    text = None
    if not os.path.isfile(skill_md):
        report("fail", "F1", skill_dir, "the directory has no SKILL.md")
    else:
        try:
            with open(skill_md, encoding="utf-8") as handle:
                text = handle.read()
        except OSError as error:
            print(f"cannot read {skill_md}: {error}", file=sys.stderr)
            return 2
        except UnicodeDecodeError:
            report("fail", "F1", "SKILL.md", "is not UTF-8 text, so no harness can read it; no further checks ran")
    if text is not None:
        lines = text.splitlines()
        try:
            data, key_lines = parse_frontmatter(lines)
        except ValueError as error:
            report("fail", "F1", "SKILL.md", str(error))
            report("info", "F1", "SKILL.md",
                   "skipped the name, description and field checks (F2-F5) because the frontmatter "
                   "could not be parsed; check them by reading")
        else:
            check_name(data, key_lines, skill_dir, prefix)
            check_description(data, key_lines)
            check_fields(data, key_lines)
        end = frontmatter_end(lines)
        check_size(lines, end + 1 if end is not None else 0)
        check_references(skill_dir, text)
    for severity, item, location, message in findings:
        print(f"{severity} {item} {location} {message}")
    counts = {s: sum(1 for f in findings if f[0] == s) for s in ("fail", "warn", "info")}
    print(f"summary: {counts['fail']} fail, {counts['warn']} warn, {counts['info']} info")
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as error:  # noqa: BLE001 - any crash must end without a summary line
        print(f"check_form.py stopped: {type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(2)
