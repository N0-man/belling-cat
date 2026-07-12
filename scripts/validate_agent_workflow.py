#!/usr/bin/env python3
"""Static consistency checks for this repository's OpenCode workflow."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")
SKILL_REFERENCE_RE = re.compile(
    r"`([a-z0-9]+(?:-[a-z0-9]+)*)`\s+skills?\b", re.IGNORECASE
)
FORMAT_FILE_RE = re.compile(r"`([A-Z][A-Z0-9_-]*-FORMAT\.md)`")
AGENT_REFERENCE_RE = re.compile(
    r"`([a-z0-9]+(?:-[a-z0-9]+)*)`\s+subagents?\b", re.IGNORECASE
)
COMMAND_TABLE_ROW_RE = re.compile(
    r"^\|\s*`/([a-z0-9]+(?:-[a-z0-9]+)*)`\s*\|\s*`([a-z0-9-]+)`\s*\|\s*([^|]+)\|",
    re.MULTILINE,
)
NAMED_TABLE_ROW_RE = re.compile(
    r"^\|\s*`([a-z0-9]+(?:-[a-z0-9]+)*)`\s*\|", re.MULTILINE
)

ALLOWED_SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata"}
ALLOWED_COMMAND_KEYS = {"description", "agent", "model", "variant", "subtask"}
ALLOWED_AGENT_KEYS = {
    "description",
    "mode",
    "model",
    "variant",
    "temperature",
    "top_p",
    "steps",
    "disable",
    "prompt",
    "permission",
    "hidden",
    "color",
    "options",
    "tools",
    "maxSteps",
}
BUILTIN_AGENTS = {"build", "plan", "general", "explore", "scout"}
INTERNAL_AGENT_SUFFIXES = ("reviewer", "auditor")
REQUIRED_README_HEADINGS = {
    "## How OpenCode pieces fit together",
    "## Primary agents",
    "## Internal subagents",
    "## Skills and their normal callers",
    "## Commands and who normally triggers them",
}
REQUIRED_MAKE_TARGETS = {
    "install",
    "test",
    "lint",
    "lint-fix",
    "format",
    "format-check",
    "typecheck",
    "workflow-lint",
    "preflight",
}
DEV_ONLY_DEPENDENCIES = {"pytest", "pytest-asyncio", "ruff", "mypy"}
MAX_AGENTS_LINES = 140
WORKFLOW_VERSION = "5"


@dataclass
class Result:
    errors: list[str]
    warnings: list[str]

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def split_frontmatter(path: Path, result: Result) -> tuple[dict[str, str], str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        result.error(f"{path}: cannot read: {exc}")
        return {}, "", ""

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        result.error(f"{path}: missing opening YAML frontmatter delimiter")
        return {}, "", text

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        result.error(f"{path}: missing closing YAML frontmatter delimiter")
        return {}, "", text

    raw_frontmatter = "\n".join(lines[1:end])
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = TOP_LEVEL_KEY_RE.match(line)
        if not match:
            result.error(f"{path}: malformed top-level frontmatter line: {line!r}")
            continue
        values[match.group(1)] = (match.group(2) or "").strip().strip("\"'")

    body = "\n".join(lines[end + 1 :])
    return values, raw_frontmatter, body


def discover_files(root: Path, pattern: str) -> list[Path]:
    return sorted(root.glob(pattern))


def validate_skills(root: Path, result: Result) -> set[str]:
    skill_paths = discover_files(root, ".opencode/skills/*/SKILL.md")
    if not skill_paths:
        result.error("no skills found under .opencode/skills/*/SKILL.md")
        return set()

    names: set[str] = set()
    for path in skill_paths:
        fields, _raw, body = split_frontmatter(path, result)
        unknown = set(fields) - ALLOWED_SKILL_KEYS
        if unknown:
            result.error(
                f"{path}: unsupported OpenCode skill frontmatter keys: {sorted(unknown)}"
            )

        name = fields.get("name", "")
        description = fields.get("description", "")
        dirname = path.parent.name

        if not name:
            result.error(f"{path}: missing skill name")
        elif not SKILL_NAME_RE.fullmatch(name):
            result.error(f"{path}: invalid skill name {name!r}")
        elif name != dirname:
            result.error(
                f"{path}: skill name {name!r} does not match directory {dirname!r}"
            )
        elif name in names:
            result.error(f"{path}: duplicate skill name {name!r}")
        else:
            names.add(name)

        if not description:
            result.error(f"{path}: missing skill description")
        elif len(description) > 1024:
            result.error(f"{path}: skill description exceeds 1024 characters")

        for filename in FORMAT_FILE_RE.findall(body):
            referenced = path.parent / filename
            if not referenced.exists():
                result.error(
                    f"{path}: referenced format file does not exist: {filename}"
                )

        text = path.read_text(encoding="utf-8")
        if "disable-model-invocation:" in text:
            result.error(
                f"{path}: disable-model-invocation is ignored by OpenCode skills"
            )
        if "user-invocable:" in text:
            result.error(
                f"{path}: user-invocable is not recognized OpenCode skill frontmatter"
            )

    return names


def validate_agents(root: Path, result: Result) -> set[str]:
    agent_paths = discover_files(root, ".opencode/agents/*.md")
    names: set[str] = set()

    for path in agent_paths:
        fields, raw, _body = split_frontmatter(path, result)
        name = path.stem
        if name in names:
            result.error(f"{path}: duplicate agent name {name!r}")
        names.add(name)

        unknown = set(fields) - ALLOWED_AGENT_KEYS
        if unknown:
            result.error(
                f"{path}: unsupported agent frontmatter keys: {sorted(unknown)}"
            )
        if "tools" in fields:
            result.error(
                f"{path}: deprecated agent key 'tools'; use permission instead"
            )
        if "maxSteps" in fields:
            result.error(f"{path}: deprecated agent key 'maxSteps'; use steps instead")
        if not fields.get("description"):
            result.error(f"{path}: missing agent description")
        if fields.get("mode") not in {"subagent", "primary", "all"}:
            result.error(f"{path}: missing or invalid agent mode")

        if name.endswith(INTERNAL_AGENT_SUFFIXES):
            checks = {
                r"(?m)^hidden:\s*true\s*$": "must be hidden",
                r"(?m)^\s{2}edit:\s*deny\s*$": "must explicitly deny edit",
                r'(?m)^\s{4}"\*":\s*deny\s*$': "must deny arbitrary bash",
                r"(?m)^\s{2}task:\s*deny\s*$": "must deny nested task invocation",
                r"(?m)^\s{2}skill:\s*deny\s*$": "must deny skill loading",
                r"(?m)^\s{2}question:\s*deny\s*$": "must deny direct user questioning",
                r"(?m)^\s{2}external_directory:\s*deny\s*$": "must deny external-directory access",
                r"(?m)^\s{2}webfetch:\s*deny\s*$": "must deny webfetch",
                r"(?m)^\s{2}websearch:\s*deny\s*$": "must deny websearch",
            }
            for pattern, message in checks.items():
                if not re.search(pattern, raw):
                    result.error(f"{path}: internal review/audit agent {message}")

    return names


def command_skill_references(body: str) -> set[str]:
    """Return backticked names explicitly followed by ``skill`` or ``skills``."""
    return set(SKILL_REFERENCE_RE.findall(body))


def validate_commands(
    root: Path,
    skill_names: set[str],
    agent_names: set[str],
    result: Result,
) -> tuple[set[str], dict[str, str]]:
    command_paths = discover_files(root, ".opencode/commands/*.md")
    names: set[str] = set()
    owners: dict[str, str] = {}
    known_agents = BUILTIN_AGENTS | agent_names

    for path in command_paths:
        fields, _raw, body = split_frontmatter(path, result)
        name = path.stem
        if name in names:
            result.error(f"{path}: duplicate command name {name!r}")
        names.add(name)

        unknown = set(fields) - ALLOWED_COMMAND_KEYS
        if unknown:
            result.error(
                f"{path}: unsupported command frontmatter keys: {sorted(unknown)}"
            )
        if not fields.get("description"):
            result.error(f"{path}: missing command description")

        agent = fields.get("agent", "")
        if not agent:
            result.error(f"{path}: command must declare its primary agent")
        elif agent not in known_agents:
            result.error(f"{path}: command references unknown agent {agent!r}")
        else:
            owners[name] = agent

        for ref in sorted(command_skill_references(body)):
            if ref not in skill_names:
                result.error(f"{path}: command references missing skill {ref!r}")

    return names, owners


def validate_cross_references(
    root: Path, skill_names: set[str], agent_names: set[str], result: Result
) -> None:
    """Validate explicit skill and internal-agent references in active workflow files."""
    active_paths = [
        *discover_files(root, ".opencode/skills/*/SKILL.md"),
        *discover_files(root, ".opencode/commands/*.md"),
    ]
    for path in active_paths:
        _fields, _raw, body = split_frontmatter(path, result)
        for ref in sorted(set(SKILL_REFERENCE_RE.findall(body))):
            if ref not in skill_names:
                result.error(f"{path}: references missing skill {ref!r}")
        for ref in sorted(set(AGENT_REFERENCE_RE.findall(body))):
            if ref not in agent_names:
                result.error(f"{path}: references missing internal agent {ref!r}")


def validate_config(root: Path, agent_names: set[str], result: Result) -> None:
    config_path = root / "opencode.json"
    if not config_path.exists():
        result.error("opencode.json is missing")
        return

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result.error(f"{config_path}: invalid JSON: {exc}")
        return

    if config.get("$schema") != "https://opencode.ai/config.json":
        result.error(f"{config_path}: missing canonical OpenCode schema URL")

    configured_agents = set(config.get("agent", {}))
    known_agents = BUILTIN_AGENTS | agent_names | configured_agents
    for primary in ("build", "plan"):
        if primary not in configured_agents:
            result.error(f"{config_path}: missing configured primary agent {primary!r}")

    build_task = (
        config.get("agent", {}).get("build", {}).get("permission", {}).get("task")
    )
    if not isinstance(build_task, dict):
        result.error(f"{config_path}: build agent must use granular task permissions")
    else:
        if build_task.get("*") != "deny":
            result.error(
                f"{config_path}: build task permissions must deny wildcard first"
            )
        for agent in sorted(agent_names):
            if build_task.get(agent) != "allow":
                result.error(
                    f"{config_path}: build agent must explicitly allow subagent {agent!r}"
                )

    plan_task = (
        config.get("agent", {}).get("plan", {}).get("permission", {}).get("task")
    )
    if plan_task != "deny":
        result.error(f"{config_path}: plan agent task permission must be deny")

    for owner, agent_config in config.get("agent", {}).items():
        task_rules = agent_config.get("permission", {}).get("task")
        if not isinstance(task_rules, dict):
            continue
        for target in task_rules:
            if target == "*":
                continue
            if target not in known_agents:
                result.error(
                    f"{config_path}: agent {owner!r} grants task permission to unknown agent {target!r}"
                )


def validate_documentation(
    root: Path,
    command_names: set[str],
    command_owners: dict[str, str],
    skill_names: set[str],
    agent_names: set[str],
    result: Result,
) -> None:
    readme = root / "README.md"
    agents = root / "AGENTS.md"
    if not readme.exists():
        result.error("README.md is missing")
        return
    if not agents.exists():
        result.error("AGENTS.md is missing")
        return

    readme_text = readme.read_text(encoding="utf-8")
    agents_text = agents.read_text(encoding="utf-8")

    missing_headings = sorted(REQUIRED_README_HEADINGS - set(readme_text.splitlines()))
    for heading in missing_headings:
        result.error(f"README.md: missing human-guide section {heading!r}")

    command_rows: dict[str, list[tuple[str, str]]] = {}
    for command, owner, trigger in COMMAND_TABLE_ROW_RE.findall(readme_text):
        command_rows.setdefault(command, []).append((owner, trigger.strip()))

    for command in sorted(command_names):
        rows = command_rows.get(command, [])
        if not rows:
            result.error(
                f"README.md: command /{command} is not documented in the ownership table"
            )
            continue
        if len(rows) > 1:
            result.error(f"README.md: command /{command} has duplicate ownership rows")
            continue
        owner, trigger = rows[0]
        if owner != command_owners.get(command):
            result.error(
                f"README.md: command /{command} owner {owner!r} does not match frontmatter "
                f"{command_owners.get(command)!r}"
            )
        if not trigger:
            result.error(
                f"README.md: command /{command} has no normal trigger documented"
            )

    named_rows = set(NAMED_TABLE_ROW_RE.findall(readme_text))
    for skill in sorted(skill_names):
        if skill not in named_rows:
            result.error(
                f"README.md: skill {skill!r} is not documented in the skill table"
            )
    for agent in sorted(agent_names):
        if agent not in named_rows:
            result.error(
                f"README.md: internal agent {agent!r} is not documented in a table"
            )

    line_count = len(agents_text.splitlines())
    if line_count > MAX_AGENTS_LINES:
        result.error(
            f"AGENTS.md: {line_count} lines exceeds the {MAX_AGENTS_LINES}-line base-context limit"
        )
    if "detailed procedures live in `.opencode/skills/`" not in agents_text:
        result.error("AGENTS.md: must delegate detailed procedures to skills")


def parse_make_targets(text: str) -> dict[str, str]:
    targets: dict[str, str] = {}
    lines = text.splitlines()
    current: str | None = None
    buffer: list[str] = []
    for line in lines:
        match = re.match(r"^([A-Za-z0-9_.-]+):(?:\s*(.*))?$", line)
        if match and not line.startswith("\t"):
            if current is not None:
                targets[current] = "\n".join(buffer)
            current = match.group(1)
            buffer = [match.group(2) or ""]
        elif current is not None:
            buffer.append(line)
    if current is not None:
        targets[current] = "\n".join(buffer)
    return targets


def validate_build_files(root: Path, result: Result) -> None:
    makefile = root / "Makefile"
    pyproject = root / "pyproject.toml"
    gitignore = root / ".gitignore"
    lockfile = root / "uv.lock"

    for path in (makefile, pyproject, gitignore, lockfile):
        if not path.exists():
            result.error(f"{path.name} is missing")

    if makefile.exists():
        text = makefile.read_text(encoding="utf-8")
        targets = parse_make_targets(text)
        missing = REQUIRED_MAKE_TARGETS - set(targets)
        for target in sorted(missing):
            result.error(f"Makefile: missing target {target!r}")

        preflight_header = next(
            (line for line in text.splitlines() if line.startswith("preflight:")), ""
        )
        required_deps = {"workflow-lint", "lint", "format-check", "typecheck", "test"}
        for dep in sorted(required_deps):
            if dep not in preflight_header.split()[1:]:
                result.error(f"Makefile: preflight is missing dependency {dep!r}")
        for mutating in ("lint-fix", "format"):
            if mutating in preflight_header.split()[1:]:
                result.error(
                    f"Makefile: preflight must not depend on mutating target {mutating!r}"
                )

        for target in (
            "test",
            "lint",
            "format-check",
            "typecheck",
            "lint-fix",
            "format",
        ):
            if target in targets and "uv run --locked" not in targets[target]:
                result.error(f"Makefile: target {target!r} must use 'uv run --locked'")

    if pyproject.exists():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            result.error(f"pyproject.toml: invalid TOML: {exc}")
        else:
            runtime = {
                re.split(r"[<>=!~\[]", dep, maxsplit=1)[0].strip().lower()
                for dep in data.get("project", {}).get("dependencies", [])
            }
            misplaced = sorted(runtime & DEV_ONLY_DEPENDENCIES)
            if misplaced:
                result.error(
                    f"pyproject.toml: development tools are in runtime dependencies: {misplaced}"
                )
            dev = {
                re.split(r"[<>=!~\[]", dep, maxsplit=1)[0].strip().lower()
                for dep in data.get("dependency-groups", {}).get("dev", [])
            }
            missing_dev = sorted(DEV_ONLY_DEPENDENCIES - dev)
            if missing_dev:
                result.error(f"pyproject.toml: dev group is missing {missing_dev}")

    if gitignore.exists():
        ignore = set(gitignore.read_text(encoding="utf-8").splitlines())
        for pattern in (".venv/", ".session/", ".reports/"):
            if pattern not in ignore:
                result.error(f".gitignore: missing local-state pattern {pattern!r}")
            if ".scratch/" in ignore:
                result.error(
                    ".gitignore: .scratch/ is important, and should not be ignored"
                )


def validate_known_drift(root: Path, result: Result) -> None:
    active_paths = [
        *discover_files(root, ".opencode/**/*.md"),
        root / "AGENTS.md",
        root / "README.md",
        root / "Makefile",
    ]
    all_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in active_paths
        if path.exists()
    )
    obsolete = {
        "git diff main...HEAD": "guessed review range",
        "git diff HEAD~1": "guessed review range",
        "git add .": "broad staging",
        "git add -A": "broad staging",
        "create and approve the INVEST-oriented backlog": "agent-owned backlog approval wording",
    }
    for marker, label in obsolete.items():
        if marker in all_text:
            result.error(f"workflow contains obsolete {label}: {marker!r}")

    handoff_format = root / ".opencode/skills/handoff/HANDOFF-FORMAT.md"
    if (
        handoff_format.exists()
        and f"workflow_version: {WORKFLOW_VERSION}"
        not in handoff_format.read_text(encoding="utf-8")
    ):
        result.error(f"{handoff_format}: workflow_version must be {WORKFLOW_VERSION}")


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    result = Result(errors=[], warnings=[])

    skill_names = validate_skills(root, result)
    agent_names = validate_agents(root, result)
    command_names, command_owners = validate_commands(
        root, skill_names, agent_names, result
    )
    validate_cross_references(root, skill_names, agent_names, result)
    validate_config(root, agent_names, result)
    validate_documentation(
        root, command_names, command_owners, skill_names, agent_names, result
    )
    validate_build_files(root, result)
    validate_known_drift(root, result)

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")

    print(
        f"workflow-lint: {len(skill_names)} skills, {len(command_names)} commands, "
        f"{len(agent_names)} agents, {len(result.warnings)} warnings, {len(result.errors)} errors"
    )
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
