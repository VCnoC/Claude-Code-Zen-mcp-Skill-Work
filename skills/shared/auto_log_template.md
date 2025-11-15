# Auto_log 核心模板 (Core Template)

> **SSOT 声明**：本文件是 automation_mode=true 时生成 auto_log.md 的**唯一模板定义**。
> 详细规范见 `skills/shared/auto_log_detailed_spec.md`，示例见 `skills/shared/auto_log_examples.md`。

---

## 使用说明

### 触发条件
- ✅ automation_mode=true (全自动化模式)
- ✅ 任务完成后 (P3 执行完毕 或 P4 错误修复完毕)
- ✅ 由 main-router 调用 simple-gemini 统一生成

### 生成流程
1. **main-router** 在任务完成时检测到 automation_mode=true
2. **main-router** 调用 **simple-gemini** 并传递任务信息
3. **simple-gemini (gemini CLI)** 分析会话历史，提取决策信息，生成完整日志
4. **simple-gemini** 将日志写入项目根目录 `auto_log.md`

### 信息提取规则

从会话历史中提取以下标记：
- `[DECISION_LOG]...[/DECISION_LOG]` - 决策记录
- `[PHASE_TRANSITION]P1→P2[/PHASE_TRANSITION]` - 阶段转换
- `[AUTOMATION_MODE: true]` - 自动化模式确认
- `[COVERAGE_TARGET: X%]` - 测试覆盖率目标
- `[API_ERROR]...[/API_ERROR]` - API 错误记录
- TodoList 状态变化 (pending → in_progress → completed)

---

## 必选章节结构 (7 Sections)

### 1. 任务元信息 (Task Metadata)

```markdown
## 任务元信息

- **任务 ID**: [continuation_id 或生成的唯一 ID]
- **执行模式**: automation_mode=true
- **用户初始请求**: [原始用户请求完整文本]
- **开始时间**: YYYY-MM-DD HH:MM:SS
- **结束时间**: YYYY-MM-DD HH:MM:SS
- **总耗时**: [duration, 如 "45 分钟"]
```

### 2. 执行摘要 (Executive Summary)

```markdown
## 执行摘要

### 任务目标
- [目标 1]
- [目标 2]
- [目标 3]

### 最终结果
- **完成度**: [X]%
- **代码生成**: N files, M lines
- **测试覆盖率**: [实际]% (目标 [coverage_target]%)
- **文档更新**: [PROJECTWIKI.md / CHANGELOG.md / 其他]
- **质量检查**: [通过/部分通过/未通过]
```

### 3. 阶段流转表 (Phase Transitions)

```markdown
## 阶段流转表

| 阶段 | 状态 | 耗时 | 关键输出 | 说明 |
|------|------|------|---------|------|
| P1 分析问题 | ✅/⚠️/❌ | [duration] | [输出] | [简述] |
| P2 制定方案 | ✅/⚠️/❌ | [duration] | plan.md | [简述] |
| P3 执行方案 | ✅/⚠️/❌ | [duration] | [文件清单] | [简述] |
| P4 错误处理 | ⚠️未触发/✅已完成 | [duration] | [修复内容] | **[P4未触发必须说明原因]** |

### P4 未触发原因 (Required when P4 not entered)

**P4 未触发原因**（当 P4 状态为 ⚠️未触发 时必填）：
- [ ] P3 执行中所有问题已在过程中修复，无遗留错误
- [ ] 测试失败为测试代码问题而非业务逻辑问题，已在测试生成阶段修复
- [ ] 代码质量检查未发现 Critical/High 级别问题
- [ ] 其他原因：[具体说明]
```

### 4. 自动决策记录 (Automated Decisions)

```markdown
## 自动决策记录

使用以下格式循环记录每个决策：

### 决策 P{阶段}-{序号}

- **决策内容**: [具体决策描述]
- **决策时间**: [timestamp]
- **置信度**: certain / high / medium / low
- **决策依据**: [引用的规则编号/标准/上下文]
- **影响范围**: [受影响的模块/文件/配置]
- **备选方案**: [如有，说明为何未选择]

**示例**:

### 决策 P2-001
- **决策内容**: 使用 plan-down skill 生成 plan.md
- **决策时间**: 2025-01-15 10:23:45
- **置信度**: certain
- **决策依据**: G11 强制技能路由规则 - plan.md 必须用 plan-down
- **影响范围**: 项目根目录 plan.md
- **备选方案**: 主模型直接生成（已拒绝，违反 G11）
```

### 5. 质量指标 (Quality Metrics)

```markdown
## 质量指标

### 测试覆盖率
- **目标值**: [coverage_target]%
- **实际值**: [actual]%
- **达标状态**: ✅ 达标 / ⚠️ 未达标 / ❌ 严重不足

### 代码质量 (5 维度简表)

| 维度 | 评分 | 问题数 | Critical/High | 状态 |
|------|------|--------|---------------|------|
| 质量 | [N/10] | [count] | [count] | ✅/⚠️/❌ |
| 安全 | [N/10] | [count] | [count] | ✅/⚠️/❌ |
| 性能 | [N/10] | [count] | [count] | ✅/⚠️/❌ |
| 架构 | [N/10] | [count] | [count] | ✅/⚠️/❌ |
| 文档 | [N/10] | [count] | [count] | ✅/⚠️/❌ |
| **总分** | **[N/50]** | **[total]** | **[total]** | ✅/⚠️/❌ |

### 测试执行结果
- **总测试数**: [total]
- **通过**: [passed] ✅
- **失败**: [failed] ❌
- **跳过**: [skipped] ⚠️
- **通过率**: [X]%
```

### 6. 文件清单 (File Inventory)

```markdown
## 文件清单

### 源代码
- 新增: [N] files, [M] lines
  - `path/to/file1.ext` (+X lines)
  - `path/to/file2.ext` (+Y lines)
- 修改: [N] files, [M] lines changed
  - `path/to/file3.ext` (+A/-B lines)

### 测试代码
- 新增: [N] files, [M] lines
  - `path/to/test1.ext` (+X lines)
- 修改: [N] files, [M] lines changed

### 文档
- 更新: PROJECTWIKI.md ([章节列表])
- 更新: CHANGELOG.md ([版本号/Unreleased])
- 新增: [其他文档]

### 配置
- 修改: [配置文件列表]
```

### 7. 结论与建议 (Conclusion)

```markdown
## 结论与建议

### 任务完成情况
- **完成度**: [X]%
- **未完成项**: [如有，列出原因]
- **偏差说明**: [如有，说明与原计划的偏差及原因]

### 自动化效果评估
- **决策准确性**: [评估自动决策的准确性]
- **效率提升**: [相比交互模式的效率提升]
- **质量保障**: [质量检查的有效性]

### 后续建议
- [建议 1]
- [建议 2]
- [如无，填写"无"]

### 遗留问题
- [问题 1]
- [问题 2]
- [如无，填写"无遗留问题"]
```

---

## 可选章节 (Optional Sections)

### API/工具失败记录 (API/Tool Failures)

仅当发生 API 错误或工具调用失败时包含此章节：

```markdown
## API/工具失败记录

### 失败 {序号}
- **时间**: [timestamp]
- **工具**: [tool_name]
- **错误**: [error_message]
- **应对**: [如何处理的]
- **影响**: [对任务的影响]
```

---

## 生成质量检查清单

生成 auto_log.md 后，必须完成以下核心检查：

- [ ] **必选章节完整** (7/7)：任务元信息、执行摘要、阶段流转表、自动决策记录、质量指标、文件清单、结论与建议
- [ ] **P4未触发说明**：当P4状态为⚠️未触发时，必须说明原因
- [ ] **决策记录规范**：所有决策有ID（P{阶段}-{序号}）、置信度、依据
- [ ] **数据准确性**：覆盖率有目标vs实际对比、文件统计准确
- [ ] **格式一致性**：Markdown格式正确、时间戳统一、状态图标统一

> **详细检查清单**（35项）见 `skills/shared/auto_log_detailed_spec.md` → 质量检查清单章节

---

**版本**: 2025-01-15 (核心模板 v1.1 - 精简版)
**详细规范**: `skills/shared/auto_log_detailed_spec.md`（信息提取规则、完整检查清单、FAQ）
**示例库**: `skills/shared/auto_log_examples.md`（完整示例、决策树可视化）
