# 测试模式与最佳实践 (Test Patterns and Best Practices)

> 为测试代码生成提供标准模板和最佳实践，确保测试覆盖率和代码质量。

## 可用模式

| 文件名 | 用途 |
|--------|------|
| `unit_test_patterns.md` | 单元测试模式和示例（生成单元测试代码） |
| `integration_test_patterns.md` | 集成测试模式和示例（生成 API/服务集成测试） |
| `e2e_test_patterns.md` | E2E 测试模式和示例（生成端到端测试） |
| `test_best_practices.md` | 测试最佳实践和反模式（测试组织、Mock、数据管理） |

## 覆盖率目标（G9 合规）

- **默认目标**: 85% 语句覆盖率
- **最低阈值**: 70% 语句覆盖率
- **读取机制**: 从上下文读取 `[COVERAGE_TARGET: X%]`（由 main-router 设置）
