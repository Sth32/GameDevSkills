#!/usr/bin/env python3
"""Read-only validation of skill packages and repository documentation links."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")
CORE_SKILLS = frozenset({
    "game-spec", "game-discovery", "game-tech-clarify", "game-config",
    "game-scaffold", "game-implement", "game-client-handoff", "game-review", "game-docs",
})
REQUIRED_REPO_FILES = (
    "README.md", "AGENTS.md", "docs/skill-development/principles.md",
    "docs/skill-development/design.md", "docs/skill-development/branch-workflow.md",
    "evals/branch-workflow.md", "evals/human-collaboration.md",
    "evals/stage-transition-gate.md", "evals/impact-propagation.md",
)
# These are smoke checks for specialized workflow coverage, not behavior tests.
TARGETED_MARKERS = {
    "game-tech-clarify": "**跨边界通信合同硬限制：",
    "game-scaffold": "**框架真实链路硬限制：",
    "game-implement": "**真实消费链验证硬限制：",
    "game-client-handoff": "**客户端合同可达性硬限制：",
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing YAML frontmatter delimiter") from exc
    result = {}
    for line in lines[1:end]:
        if not line or line.startswith((" ", "#")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("\"'")
    return result


def prose_only(text: str) -> str:
    """Ignore fenced examples, which can contain illustrative links."""
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def validate_links(path: Path, boundary: Path) -> list[str]:
    errors = []
    for match in LINK_RE.finditer(prose_only(path.read_text(encoding="utf-8"))):
        target = match[1].strip()
        target = target[1:target.index(">")] if target.startswith("<") and ">" in target else target.split()[0]
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            continue
        resolved = (path.parent / unquote(url.path)).resolve()
        if not resolved.is_relative_to(boundary.resolve()):
            errors.append(f"reference leaves package: {target}")
        elif not resolved.exists():
            errors.append(f"missing reference: {target}")
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    entry = skill_dir / "SKILL.md"
    if not entry.is_file():
        return ["missing SKILL.md"]
    errors = []
    try:
        fm = parse_frontmatter(entry)
    except ValueError as exc:
        return [str(exc)]
    name, description = fm.get("name", ""), fm.get("description", "")
    if name != skill_dir.name:
        errors.append(f"name '{name}' does not match directory '{skill_dir.name}'")
    if not NAME_RE.fullmatch(name) or not 1 <= len(name) <= 64:
        errors.append("name must be 1-64 lowercase letters, numbers and single hyphens")
    if not 1 <= len(description) <= 1024:
        errors.append("description length must be 1-1024 characters")
    text = entry.read_text(encoding="utf-8")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md exceeds 500 lines; move conditional details to references")
    for marker in ("人工协作", "文档更新", "结构性变更", "一致性", "00-工作流索引.md"):
        if marker not in text:
            errors.append(f"missing core workflow guidance: {marker}")
    targeted = TARGETED_MARKERS.get(name)
    if targeted and targeted not in text:
        errors.append("missing specialized runtime-chain guidance")
    if name == "game-spec" and "**需求分支硬限制：" not in text:
        errors.append("missing requirement-stage branching guidance")
    if name == "game-review":
        for marker in ("**独立 Review 硬限制：", "**整体 Review 硬限制：", "<Uxx>-07-<主题>-交叉评审.md"):
            if marker not in text:
                errors.append(f"missing review guidance: {marker}")
    elif name not in {"game-spec", "game-docs"}:
        if "**分支工作流硬限制：" not in text:
            errors.append("missing work-unit dependency guidance")
    for doc in sorted(skill_dir.rglob("*.md")):
        errors.extend(f"{doc.relative_to(skill_dir)}: {error}" for error in validate_links(doc, skill_dir))
    return errors


def main() -> int:
    errors = []
    for relative in REQUIRED_REPO_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    skill_dirs = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    found = {p.name for p in skill_dirs}
    for name in sorted(CORE_SKILLS - found):
        errors.append(f"missing core skill: {name}")
    for name in sorted(found - CORE_SKILLS):
        errors.append(f"skill outside project scope: {name}")
    for skill_dir in skill_dirs:
        skill_errors = validate_skill(skill_dir)
        errors.extend(f"{skill_dir.name}: {error}" for error in skill_errors)
        print(f"{'FAIL' if skill_errors else 'PASS'} {skill_dir.name}")
    documents = [ROOT / "README.md", ROOT / "AGENTS.md"]
    documents += sorted((ROOT / "docs").rglob("*.md"))
    documents += sorted((ROOT / "evals").glob("*.md"))
    for doc in documents:
        if doc.is_file():
            errors.extend(f"{doc.relative_to(ROOT)}: {error}" for error in validate_links(doc, ROOT))
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("All skills and documentation links passed static validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
