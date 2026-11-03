# game-config 最小路径回归测试

输入：已授权将 YAML 真源的 `feature_enabled` 从 `false` 改为 `true`；无 Schema、生成物、多端输出或代码接线变化。

通过：直接修改目标键，保持其他内容；运行 YAML 解析与必要加载检查，用简短差异更新 `04`。不读取复杂管线指南、不建立 Schema/生成/输出矩阵，不因不存在的 Schema 阶段阻塞，也不能只写规划。
