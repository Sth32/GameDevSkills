# Game Development Skills

面向游戏服务端功能开发的 Agent Skills：把需求逐步收敛为可实现、可验证、可评审的工程结果，完成客户端对接，并沉淀长期功能文档。

## 核心流程

```text
01 原始需求 → 02 需求挖掘 → 03 程序实现澄清 → 04 配置规划
  → 05 框架实现 → 06 完整实现 → 客户端对接（按需）→ 07 Review
  → 长期功能文档
```

简单需求保持单线。复杂功能可从 `01` 起按真实边界拆成 `Uxx` 工作单元，各自按依赖推进、对接和 Review；所有目标单元完成后，仅在存在集成风险时执行整体 Review。用户可以调整顺序和确认节奏，文档始终保留真实状态与验证证据。

## Skills

| Skill | 主要产物 | 职责 |
|---|---|---|
| `game-spec` | `01-原始需求.md` | 无损整理需求，按需拆分工作单元 |
| `game-discovery` | `02-需求挖掘.md` | 收敛需要需求负责人决定的产品问题 |
| `game-tech-clarify` | `03-程序实现澄清.md` | 收敛高影响技术决策 |
| `game-config` | `04-配置规划.md` | 确认配置真源、值域和关键值，完成配表验证 |
| `game-scaffold` | `05-框架实现方案.md` + 骨架 | 建立数据、同步、持久化和调用链框架 |
| `game-implement` | `06-完整实现方案.md` + 代码 | 补齐行为、边界、兼容与验证 |
| `game-client-handoff` | 客户端对接文档 | 维护服务端—客户端真实合同 |
| `game-review` | `07-*-交叉评审.md` | 独立评审工作单元，按需检查整体集成 |
| `game-docs` | `docs/features/<feature>.md` | 提炼当前实现的长期权威文档 |

## 规范入口

- [长期准则](docs/skill-development/principles.md)：影响长期取舍的简短规则。
- [流程设计](docs/skill-development/design.md)：阶段职责、文档模型、协作与变更传播。
- [多分支规范](docs/skill-development/branch-workflow.md)：工作单元、依赖、命名和分支评审。
- 各 `skills/<skill-name>/SKILL.md`：执行规则与按需参考资料；每个技能可独立安装。

## 安装

```bash
npx skills@latest add Sth32/skills
```

也可以只复制需要的 `skills/<skill-name>/` 目录到 Agent 的 skills 目录。

## 验证

```bash
python scripts/validate_skills.py
python -m unittest discover -s scripts -p "test_*.py"
```

GitHub Actions 在 PR 和主分支推送时执行这些检查。`evals/` 保存核心技能、多分支、阶段衔接和人工协作的行为场景；静态检查通过不代表这些场景已经执行或通过。
