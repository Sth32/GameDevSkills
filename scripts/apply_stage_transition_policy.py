#!/usr/bin/env python3
"""Distribute human collaboration guidance and formal stage checks."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"
COLLABORATION_SOURCE = ROOT / "docs" / "skill-development" / "human-collaboration.md"

COLLABORATION_RULE = (
    "**人工协作优先：以下门禁、确认点和文档时序均为默认方式；用户可跳步、合并确认、按显式假设继续或延后 Review，已有适用授权无需重复确认。"
    "执行前说明实际缺口与影响，按约定范围继续，不把未验证写成已通过；真实操作权限仍须满足。遇到暂停、上游回写或交接时，按"
    "[协作约定](references/协作约定.md)处理；该约定也适用于下文模板。**"
)
COLLABORATION_RULE_RE = re.compile(r"\*\*人工协作优先：.*?\*\*", re.DOTALL)

LIGHTWEIGHT_SKILLS = frozenset(
    {
        "game-bugfix",
        "game-small-change",
        "game-refactor",
        "game-light-review",
        "game-hotfix",
    }
)

MAINTENANCE_ENTRY_SKILLS = frozenset(
    {
        "game-discovery",
        "game-tech-clarify",
        "game-config",
        "game-scaffold",
        "game-implement",
        "game-review",
    }
)

MAINTENANCE_ENTRY_RULE = (
    "**维护升级入口硬限制：本 skill 允许从轻量维护独立进入。若本次任务没有适用的完整前序阶段文档，先用用户已确认目标、"
    "当前代码/配置、稳定合同与验证证据建立升级基线，并检查本阶段真正需要的产品、技术、配置或框架事实。已由证据覆盖的前序阶段"
    "不补建文档、不伪造完成状态；首次进入时在当前阶段唯一文档记录入口、范围、代码基线、证据位置、必要的已确认结论与实际未决项，"
    "后续阶段引用这一基线。下文文档职责、输入、上游回写和完成条件中的缺失文档按该基线承接：新确认事实原位归入基线，已有适用正式文档仍按原规则维护。"
    "若仍缺少会改变本阶段工作的产品/技术决策或运行证据，返回最早必要 skill 解决，不得把未知当成已确认。已有且适用于本次任务的上游"
    "文档仍保留真实状态；用户可按协作约定接受显式假设、先行实现或延后检查，不把这些决定当作前置已通过。该入口不自动创建 Uxx。**"
)

DOCS_TRANSITION_RULE = (
    "**阶段切换门禁硬限制：生成或更新长期功能文档前，必须读取本次范围适用的单线或分支 Review 顶部状态；需要整体 Review 时也检查其状态。"
    "未达到可交付终态时说明具体缺口；用户要求先整理时可从已验证的稳定事实编写草稿，在交接说明中保留 Review 覆盖限制，不替上游补写通过状态。长期文档自身不是阶段过程文档，"
    "不写阶段状态、未解决计数或当前步骤，也不要求模板定义终态；完成时核对稳定契约、更新最后核对版本并重新读取确认内容已落盘。**"
)

STAGE_TRANSITION_RULE = (
    "**阶段切换门禁硬限制：默认读取当前范围真实上游的状态与证据，达到本阶段条件后写入原有终态并核对落盘。"
    "缺文件、状态滞后或检查未完成时，先说明缺口及影响；用户可按协作约定跳步、并行、采用暂定假设或延后检查，"
    "也可预先授权连续执行多个 Step，Agent 按约定范围继续，不重复索要同一确认。继续决定与验证结论分开："
    "保留未完成/待验证事实，在当前文档按需记录继续范围、依据或假设、待补项与复核点，不新增审批文档。"
    "只有未授权的高后果实际操作或缺少工具权限才暂停该动作；不因形式状态单独阻塞其他已授权工作。**"
)

CONSISTENCY_RULE_RE = re.compile(r"\*\*阶段完成一致性硬限制：.*?\*\*", re.DOTALL)
TRANSITION_RULE_RE = re.compile(r"\*\*阶段切换门禁硬限制：.*?\*\*", re.DOTALL)
MAINTENANCE_ENTRY_RULE_RE = re.compile(r"\*\*维护升级入口硬限制：.*?\*\*", re.DOTALL)
VERSION_RE = re.compile(r'(\n\s*version:\s*")(\d+)\.(\d+)\.(\d+)("\s*\n)')
README_SECTION_RE = re.compile(r"## 阶段切换门禁\n.*?(?=## [^#]|\Z)", re.DOTALL)

README_SECTION = f"""## 阶段切换门禁

{STAGE_TRANSITION_RULE}

正常可移交终态以各阶段模板为准。当前主流程为：

| 阶段 | 权威文档 | 正常可移交终态 |
|---|---|---|
| 01 原始需求 | 未分支 `01-原始需求.md`；分支 `01-Uxx-<主题>-原始需求.md` | 叶文档 `整理完成`；父文档可为 `已拆分` |
| 02 需求挖掘 | `02-需求挖掘.md` | `已收敛` |
| 03 程序实现澄清 | `03-程序实现澄清.md` | `已收敛` |
| 04 配置规划 | `04-配置规划.md` | `已完成` |
| 05 框架实现 | `05-框架实现方案.md` | `骨架已完成` |
| 06 完整实现 | `06-完整实现方案.md` | `已完成` |
| 07 交叉评审 | 未分支/整体 `07-交叉评审.md`；分支 `07-Uxx-<主题>-交叉评审.md` | `通过`；`有条件通过` 仅按已明确接受的条件继续 |

顶部状态只表达**当前阶段自身**是否闭环。下游依赖必须留在事项内，例如配置阶段已经完成但仍有代码接入工作时，`04` 顶部应为 `已完成`，代码依赖写在对应配置事项中，而不是把阶段状态写成“待代码接入”。

"""


def bump_patch_version(text: str) -> str:
    match = VERSION_RE.search(text)
    if not match:
        raise ValueError("missing semantic metadata version")
    major, minor, patch = map(int, match.group(2, 3, 4))
    replacement = f'{match.group(1)}{major}.{minor}.{patch + 1}{match.group(5)}'
    return text[: match.start()] + replacement + text[match.end() :]


def patch_skill(text: str, path: Path) -> str:
    skill_name = path.parent.name
    if COLLABORATION_RULE_RE.search(text):
        new_text = COLLABORATION_RULE_RE.sub(COLLABORATION_RULE, text, count=1)
    else:
        title = re.search(r"^# .+$", text, re.MULTILINE)
        if not title:
            raise ValueError(f"{path}: missing skill title anchor")
        new_text = text[:title.end()] + "\n\n" + COLLABORATION_RULE + text[title.end():]
    if skill_name in LIGHTWEIGHT_SKILLS:
        return bump_patch_version(new_text) if new_text != text else text

    rule = DOCS_TRANSITION_RULE if skill_name == "game-docs" else STAGE_TRANSITION_RULE
    if TRANSITION_RULE_RE.search(new_text):
        new_text = TRANSITION_RULE_RE.sub(rule, new_text, count=1)
    else:
        consistency = CONSISTENCY_RULE_RE.search(new_text)
        if not consistency:
            raise ValueError(f"{path}: missing stage completion consistency rule anchor")
        new_text = new_text[: consistency.end()] + "\n\n" + rule + new_text[consistency.end() :]

    if skill_name in MAINTENANCE_ENTRY_SKILLS:
        if MAINTENANCE_ENTRY_RULE_RE.search(new_text):
            new_text = MAINTENANCE_ENTRY_RULE_RE.sub(MAINTENANCE_ENTRY_RULE, new_text, count=1)
        else:
            transition = TRANSITION_RULE_RE.search(new_text)
            assert transition is not None
            new_text = new_text[: transition.start()] + MAINTENANCE_ENTRY_RULE + "\n\n" + new_text[transition.start() :]

    return bump_patch_version(new_text) if new_text != text else text


def patch_readme(text: str) -> str:
    # README is only a navigation entry. If a legacy stage-gate section exists,
    # keep it canonical; otherwise do not inject detailed formal-flow policy.
    if README_SECTION_RE.search(text):
        return README_SECTION_RE.sub(README_SECTION, text, count=1)
    return text


def write_if_changed(path: Path, new_text: str, *, check: bool) -> bool:
    old_text = path.read_text(encoding="utf-8") if path.exists() else None
    if old_text == new_text:
        return False
    if not check:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    changed: list[Path] = []
    try:
        collaboration = COLLABORATION_SOURCE.read_text(encoding="utf-8")
        # The package copy must not refer to repository-only maintenance paths.
        collaboration = collaboration.split("\n## 维护方式\n", 1)[0].rstrip() + "\n"
        for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            old = skill_file.read_text(encoding="utf-8")
            new = patch_skill(old, skill_file)
            if write_if_changed(skill_file, new, check=args.check):
                changed.append(skill_file)
            reference = skill_file.parent / "references" / "协作约定.md"
            if write_if_changed(reference, collaboration, check=args.check):
                changed.append(reference)

        old_readme = README.read_text(encoding="utf-8")
        if write_if_changed(README, patch_readme(old_readme), check=args.check):
            changed.append(README)
    except (OSError, ValueError) as exc:
        print(f"stage transition policy application failed: {exc}", file=sys.stderr)
        return 2

    if changed:
        prefix = "NEEDS UPDATE" if args.check else "UPDATED"
        for path in changed:
            print(f"{prefix} {path.relative_to(ROOT)}")
        return 1 if args.check else 0

    print("Stage transition policy is up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
