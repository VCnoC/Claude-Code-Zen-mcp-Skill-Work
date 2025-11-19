# Main Router - References 目录

本目录包含 main-router skill 的参考资料和示例文档。

## 目录结构

### routing_examples.md
包含14个完整的路由决策示例，展示了main-router在不同场景下的工作方式。

**示例列表：**
1. General Q&A Request - 一般问答请求
2. Deep Problem Investigation - 深度问题调查
3. Simple Document Generation - 简单文档生成
4. Code Quality Check - 代码质量检查
5. Deep Technical Analysis Request - 深度技术分析请求
6. Planning Request - 规划请求
7. Ambiguous Request - 模糊请求处理
8. Multi-Skill Sequential - 多技能顺序执行
9. Full Automation Mode - 全自动化模式
10. User Explicitly Mentions MCP Tools - 用户明确指定MCP工具
11. Complete Task Lifecycle with Active Monitoring - 完整任务生命周期监控
12. Frontend Development Request - 前端开发请求
13. Fullstack Project Detection - 全栈项目检测
14. Code + Review Workflow - 代码生成和审查工作流

## 设计原则

这个目录的创建遵循了**关注点分离（Separation of Concerns, SoC）**原则：

- **核心逻辑**（SKILL.md）：路由决策树、技能定义、工作流程
- **参考示例**（references/）：实际使用案例、最佳实践、模式示例

## 维护指南

当添加新的路由示例时：
1. 在 `routing_examples.md` 中添加新示例
2. 在 SKILL.md 的示例列表中添加对应条目
3. 确保示例包含完整的上下文和决策理由

## 历史

- **2025-11-19**: 从 SKILL.md（1842行）中提取示例到独立文件（892行），SKILL.md减少至1291行（30%优化）
