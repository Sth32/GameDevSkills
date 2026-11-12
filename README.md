# GameWorkbenchSkills · 需求工作台

面向游戏功能需求的 Agent Skills：从需求整理、关键决策到实现、Review 和长期文档，按真实任务需要推进。当前实现相关 Skill 主要面向游戏服务端场景；用户可调整协作节奏，简单需求保持单线，独立范围可拆为 Uxx，只有集成风险时才追加整体 Review。

| Skill | 主要产物 | 职责 |
|---|---|---|
| `game-spec` | `01-原始需求.md` | 无损整理需求 |
| `game-discovery` | `02-需求挖掘.md` | 收敛产品决策 |
| `game-tech-clarify` | `03-程序实现澄清.md` | 收敛高影响技术决策 |
| `game-config` | `04-配置规划.md` | 确认配置真源、值域和关键值，验证配表 |
| `game-scaffold` | `05-框架实现方案.md` + 骨架 | 建立数据、同步、持久化和调用链 |
| `game-implement` | `06-完整实现方案.md` + 代码 | 完成行为、兼容与验证 |
| `game-client-handoff` | 客户端对接文档（按需） | 维护服务端—客户端真实合同 |
| `game-review` | `07-交叉评审.md` | 独立评审，按需检查整体集成 |
| `game-docs` | `08-功能实现文档.md` | 提炼当前实现的长期权威文档 |

文档与回归场景使用《原神》主题的虚构示例；代码符号、配置值和服务端机制仅用于演示，不代表原神实际实现或任何团队的内部项目。

## 新需求的轻量入口

遇到需要跨需求梳理、设计、实现等阶段推进的**新功能需求**时，Agent 应在初步理解目标后、实质建档或大量编码前适时询问一次：

> 这个需求适合用「需求工作台」推进。是否使用？我可以协助需求梳理、关键问题确认、技术方案、功能实现和交叉 Review。
>
> **使用工作台 / 直接处理**

选择使用后，按当前需求和既有授权进入适用的 Skill，后续由 Agent 负责阶段衔接；关键决策才询问用户。选择直接处理后，该需求不再重复推荐。局部修复、解释、单独评审、可行性咨询、明确点名某个 Skill 或继续已有工作台任务，均不弹出此询问。**选择工作台不等于授予额外代码修改权限，也不等于完成验收。**

## 安装

```bash
npx skills@latest add /path/to/GameWorkbenchSkills
```

将 `/path/to/GameWorkbenchSkills` 替换为本地仓库路径。

也可将所需 `skills/<skill-name>/` 整个目录复制到 Agent 的 skills 目录。每个技能独立安装，入口与随包 `references/` 一起使用。

前置询问由 `game-spec` 的 Skill 描述与规则承载，**依赖使用方的 Agent 能发现并自动选择该 Skill**。如果仅安装其他 Skill，或客户端不会隐式触发 Skill，README 本身不能让询问生效。需要稳定覆盖这类环境时，可在**实际开发项目**的 Agent 常驻规则（如 `AGENTS.md`）添加：

> 对新的、需要多阶段推进的游戏功能需求，如果用户未明确选择工作台，在大量工作前适时询问一次是否使用「需求工作台」；局部任务和已有流程不问，用户拒绝后同一需求不再询问。启用后依实际文档与授权选择相应 Skill，关键决策才向用户确认。

## 文档位置

默认写入目标项目的 `Workbench/<YYMMDD><功能名>/`，日期取首次建档时的用户当地日期。例如 `Workbench/261030七圣召唤优化/01-原始需求.md`。所有阶段与分支文件放在同目录；已有功能原位续写。

团队可在目标项目根目录创建并提交 `.game-dev-workbench.json`：

```json
{"documentRoot": "Design/Workbench"}
```

新建根目录按“本次指定 → 项目配置 → Workbench”选择。配置只在技能执行时读取，不自动创建；只影响新建目录。完整路径、旧文档续接与命名规则见[流程设计](docs/skill-development/design.md#文档位置)。

## 规范与验证

- [长期准则](docs/skill-development/principles.md)：持续适用的设计取舍。
- [流程设计](docs/skill-development/design.md)：文档、阶段、协作和变更传播。
- [多分支规范](docs/skill-development/branch-workflow.md)：拆分、依赖和分支评审。

```bash
python scripts/validate_skills.py
python -m unittest discover -s scripts -p "test_*.py"
```

PR 和主分支推送执行上述静态检查；`evals/` 中的行为场景需另行执行，不能由静态通过推定通过。

## CNB 自动同步

GitHub Actions 的 `Sync to CNB` 在推送时将 GitHub 当前全部分支和标签同步到 [CNB 仓库](https://cnb.cool/qun-org/GameDevSkills)，也支持在 Actions 页面手动运行。工作流使用仓库 Secret `CNB_TOKEN`（需要目标仓库 Git 推送权限），凭据不进入代码或远端 URL。

同步采用原子推送，不强制覆盖分叉历史，也不删除 CNB 独有分支或标签。失败详情见 Actions 日志；修复凭据或冲突后可手动重试。旧分支若尚未包含此工作流，其单独推送不会触发同步，但下一次工作流运行会一并同步。仅同步 Git 历史，不同步 Issue、PR 或 Release 附件。
