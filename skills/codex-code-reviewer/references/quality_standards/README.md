# 代码质量标准参考 (Code Quality Standards)

> 为 codex-code-reviewer 技能提供代码审查标准，确保代码质量、安全性、性能、架构和文档符合规范。

## 可用标准

| 文件名 | 用途 |
|--------|------|
| `global_rules.md` | 全局规则（G1-G8）：文档同步、安全合规、架构决策 |
| `core_principles.md` | 核心开发原则：伦理、可复现性、可解释性、模型选择 |
| `p3_constraints_and_quality.md` | P3执行方案约束 + 代码质量检查项：低风险判断、质量、安全、性能、架构 |
| `commit_and_quality_gates.md` | Conventional Commits规范 + 质量门槛：提交信息格式、测试覆盖率、性能指标 |
| `error_handling_and_usage.md` | 错误处理原则 + 使用建议：P4错误处理、问题归因、修复方案、检查优先级 |

## 质量检查维度（5大维度）

1. **代码质量** (25%) - 可读性、可维护性、复杂度
2. **安全性** (20%) - 敏感信息、输入验证、依赖安全
3. **性能** (15%) - 效率、资源使用、关键接口性能
4. **架构** (15%) - 模块化、耦合度、扩展性
5. **文档同步** (25%) - 代码注释、PROJECTWIKI、CHANGELOG
