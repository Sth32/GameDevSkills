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
| `game-review` | `07-交叉评审.md` / `Uxx-07-<主题>-交叉评审.md` | 独立评审工作单元，按需检查整体集成 |
| `game-docs` | `08-功能实现文档.md`（默认，与过程文档同目录） | 提炼当前实现的长期权威文档 |

## 文档位置

默认在使用技能的目标项目内直接写入 `Workbench/<YYMMDD><feature>/`，不增加 `requirements/` 或 `features/` 层。例如：

```text
Workbench/261030策牌Q4优化/01-原始需求.md
Workbench/261030策牌Q4优化/02-需求挖掘.md
Workbench/261030策牌Q4优化/07-交叉评审.md
Workbench/261030策牌Q4优化/08-功能实现文档.md
```

`YYMMDD` 是功能首次建档时的用户当地日期，与功能名直接相连；跨天或切换阶段仍使用原目录。按需生成的 `00`、Uxx、客户端对接和配表说明也直接放在同目录，不创建子目录。`08` 仅是长期文档的文件排序，不增加阶段状态。

分支文档按 `Uxx-阶段号-主题-阶段名.md` 命名，分支号与阶段号至少两位、补零，按文件名排序即可聚集同一分支。例如：

```text
U01-01-战斗-原始需求.md
U01-02-战斗-需求挖掘.md
U01-07-战斗-交叉评审.md
U02-01-奖励-原始需求.md
U02-02-奖励-需求挖掘.md
U02-07-奖励-交叉评审.md
```

分支配表说明使用 `Uxx-04-<主题>-策划配表说明.md`，客户端对接使用 `Uxx-06-<主题>-客户端对接文档.md`；对接的 `06` 只用于排序，合同稳定即可提前生成。单线文件、`00`、整体 `07` 和功能级 `08` 沿用原名。已有旧名按索引与实际引用续接，只有明确要求统一既有文件名时才同目录重命名并更新引用，不生成副本。

需要团队自定义时，在目标项目根目录创建可选的 `.game-dev-workbench.json` 并提交 Git：

```json
{
  "documentRoot": "Design/Workbench"
}
```

路径相对于目标项目根目录，只替换 `Workbench` 这一层，例如 `Design/Workbench/261030策牌Q4优化/`。该文件仅在相关技能执行时读取；不需要加入 AGENTS.md，也不支持环境变量覆盖。没有配置时直接使用 `Workbench/`，不自动创建配置文件。

先查找已有功能与同主题长期文档并沿用原位置，只有明确要求迁移才移动。确需新建时按“本次明确指定 → 配置文件 → 默认值”选择。对话直接指定功能目录或已带日期的目录名时原样使用，不重复追加日期、功能名或子路径；长期文档可单独指定文件。修改默认值不会生成第二套文档。详细规则见[文档位置](docs/skill-development/design.md#文档位置)。

## 规范入口

- [长期准则](docs/skill-development/principles.md)：影响长期取舍的简短规则。
- [流程设计](docs/skill-development/design.md)：阶段职责、文档模型、协作与变更传播。
- [多分支规范](docs/skill-development/branch-workflow.md)：工作单元、依赖、命名和分支评审。
- 各 `skills/<skill-name>/SKILL.md`：执行规则与按需参考资料；每个技能可独立安装。

## 安装

```bash
npx skills@latest add Sth32/GameDevSkills
```

也可以只复制需要的 `skills/<skill-name>/` 目录到 Agent 的 skills 目录。

## 验证

```bash
python scripts/validate_skills.py
python -m unittest discover -s scripts -p "test_*.py"
```

GitHub Actions 在 PR 和主分支推送时执行这些检查。`evals/` 保存核心技能、多分支、阶段衔接和人工协作的行为场景；静态检查通过不代表这些场景已经执行或通过。
