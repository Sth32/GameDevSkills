# Game Development Skills

面向游戏服务端的 Agent Skills：从需求整理到实现、客户端对接、Review 和长期文档。默认按下表顺序推进；用户可调整协作节奏。简单需求保持单线，独立范围可从 `01` 拆为 Uxx；仅有集成风险时追加整体 Review。

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

## 安装

```bash
npx skills@latest add /path/to/GameDevSkills
```

将 `/path/to/GameDevSkills` 替换为本地仓库路径。

也可将所需 `skills/<skill-name>/` 整个目录复制到 Agent 的 skills 目录。每个技能独立安装，入口与随包 `references/` 一起使用。

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
