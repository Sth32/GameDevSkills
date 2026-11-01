# 文档位置行为场景

这些场景验证文档落点、跨阶段续接和配置加载范围。通过静态校验不代表场景已执行；执行时观察实际读取和写入路径，不执行真实项目迁移。

| 场景与输入 | 期望可观察行为 | 失败信号 |
|---|---|---|
| 目标项目为 `Game/`，没有配置；用 game-spec 整理新功能“背包” | 新建 `Game/Workbench/requirements/背包/01-原始需求.md`；不生成配置文件 | 写入技能安装目录、终端当前目录或旧默认目录 |
| `Game/.sth32-game-skills.json` 为 `{"documentRoot":"Design/Workbench"}`；新建“背包” | 过程文档落在 `Game/Design/Workbench/requirements/背包/`；game-docs 新建在 `Game/Design/Workbench/features/背包.md` | 仍使用默认 Workbench，或把配置路径当成具体功能目录 |
| 配置为 `Design/Workbench`；本次说“文档根目录用 TempDocs” | 本次新建的两类文档分别位于 `TempDocs/requirements/` 与 `TempDocs/features/`；不改项目配置 | 临时覆盖自动写回配置，或只对部分阶段生效 |
| 配置为 `Design/Workbench`；本次说“背包需求放在 Design/背包评审材料/” | 直接使用该功能目录；其后阶段、Uxx 和对接在同目录续接；新建长期文档仍按配置的 features 目录 | 再追加 requirements/背包，或将过程目录隐式当成所有文档的根目录 |
| 用户只给出既有 `Game/docs/requirements/背包/02-需求挖掘.md`，要求继续技术澄清；配置已改成 Workbench | 在旧功能目录新建或更新 03；通过适用阶段引用或 00 定位依赖 | 在 Workbench 再建立同一功能，或自动搬迁旧文档 |
| 新建默认已改成 Workbench；已有 `Game/docs/features/背包.md` | game-docs 原位更新既有长期文档 | 在 Workbench/features 再创建同主题权威文档 |
| 用户明确要求把旧功能迁移到 Workbench/requirements/背包 | 移动该范围内文档并更新真实引用，保持一份权威内容；不顺带迁移其他功能 | 复制后保留两套有效文档，或移动无关目录 |
| 仅独立安装 game-review，目标项目已有自定义目录与 00 | 根据用户提供路径或配置定位功能，检查当前 Uxx 的真实依赖与 Review；不依赖其他技能安装目录 | 必须读取本技能包外的配置说明才能决定路径 |
| 当前终端在 Game/Server/，用户目标项目为 Game/ | 从 Game 根目录解析配置，路径也相对于 Game | 生成 Game/Server/Workbench 或读取全局技能目录配置 |
| 环境变量指向 TempDocs，项目配置指向 Design/Workbench | 新建使用项目配置；不读取环境变量作为文档位置来源 | 环境变量或个人配置覆盖项目约定 |
| 配置文件不存在或为 `{}` | 新建使用 Workbench，不要求先建配置 | 把缺配置当阻塞，或自动生成配置文件 |
| 需依赖的配置不是合法 JSON，或 documentRoot 为空、数字、绝对路径 | 说明具体配置问题，停止依赖它的新建写入；不静默换目录 | 默默回退 Workbench 或在错误位置写入 |
| 同一功能在旧目录和新目录都有候选权威文档 | 核对用户指向及现有引用；归属仍不明确时请用户选择 | 任取一份覆盖，或生成第三套文档 |
| 用户明确说“本次长期文档写在 Knowledge/背包.md” | game-docs 使用指定文件；不改动过程目录或项目配置 | 仍强制写入 features，或连带搬迁整个功能 |

无关对话不应被技能说明要求读取此配置；本仓库不通过 AGENTS.md 注入文档位置设置。
