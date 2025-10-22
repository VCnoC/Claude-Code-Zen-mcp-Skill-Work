# 变更日志（Changelog）

所有重要变更均记录于此文件。

本文件格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，并遵循 [语义化版本号](https://semver.org/lang/zh-CN/) 规范。

## [Unreleased]

### Added（新增）
- 重写 README.md 文档（精简版）
- 添加项目架构流程图（使用 Mermaid）
- 添加 5 个核心技能简介
- 添加快速开始指南
- 创建 PROJECTWIKI.md 项目知识库
- 创建 CHANGELOG.md 变更日志

### Changed（变更）
- 将 readme.md 重构为 README.md，精简为约 120 行
- 优化文档结构，保留核心信息

### Removed（移除）
- 移除旧版 readme.md 文件

---

## [1.0.0] - 2025-10-22

### Added（新增）
- 初始化项目结构
- 添加 5 个核心技能包：
  - main-router（智能路由）
  - plan-down（智能规划）
  - codex-code-reviewer（代码审查）
  - simple-gemini（标准文档生成）
  - deep-gemini（深度分析）
- 添加 AGENTS.md 全局规则（版本 2025-10-11.4）
- 添加 CLAUDE.md 项目配置

---

<!-- 比对链接（将 <REPO_URL> 替换为实际仓库地址） -->
[Unreleased]: <REPO_URL>/compare/v1.0.0...HEAD
[1.0.0]: <REPO_URL>/releases/tag/v1.0.0

<!-- 归类指引（Conventional Commits → Changelog 分区）
feat: Added（新增）
fix: Fixed（修复）
perf / refactor / style / chore / docs / test: Changed（变更）或按需归类
deprecate: Deprecated（弃用）
remove / breaking: Removed（移除）并标注 BREAKING
security: Security（安全）
-->

