# Skill 文档重构模板（Skill Refactoring Template）

> **用途**：为所有 skill 文档提供统一的重构模板，确保与全局规则/标准的关系清晰明确。
> **原则**：技能文档只描述"如何使用标准"，不重复定义标准本身（SSOT）。

---

## 使用说明

在每个 skill 文档中，添加或替换以下章节：

---

## 与全局规则/标准的关系（建议位置：文档开头或"工作流程"之前）

### automation_mode（自动化模式）

- **本 skill 的角色**：Skill 层（只读取，不判断）
- **状态来源**：从 main-router 传递的上下文中读取 `[AUTOMATION_MODE: true/false]`
- **行为约束**：
  - ❌ 禁止检查用户初始请求中的关键词（"全程自动化"等）
  - ❌ 禁止修改 router 设置的 automation_mode 状态
  - ✅ 根据状态调整行为：
    - `automation_mode=true`：不询问用户，自动选择参数，决策记录到片段输出
    - `automation_mode=false`：在关键节点询问用户确认
- **详细规范**：见 CLAUDE.md「📚 共享概念速查 → automation_mode」及 G11 三层架构

### auto_log（自动化决策日志）

> **触发条件、职责分工、生成机制以 CLAUDE.md「📚 共享概念速查 → auto_log」为准**

- **本 skill 的职责（Skill 层）**：当 automation_mode=true 时，输出 `[自动决策记录]` 片段
  - 记录内容：模型选择、参数配置、自动决策及理由、跳过的问题及原因
  - 不负责汇总或文件生成（由 router 和 simple-gemini 完成）
- **模板格式**：`skills/shared/auto_log_template.md`

### CLI 调用（G10 标准）

*（仅当本 skill 需要启动 CLI 时包含此节）*

- **本 skill 的职责**：当需要启动 [codex/gemini/claude] CLI 时，调用 `mcp__zen__clink` 工具
- **参数传递**：
  ```yaml
  Tool: mcp__zen__clink
  Parameters:
    prompt: "[codex/gemini/claude]"
    cli_name: "[codex/gemini/claude]"
    # 其他参数（role / files / continuation_id）根据任务需要传递
  ```
- **禁止行为**：
  - ❌ 不得自行检测操作系统环境
  - ❌ 不得手动拼接 PowerShell / WSL 命令
  - ❌ 不得传递不支持的参数（args / working_directory）
- **详细规范**：见 `references/standards/cli_env_g10.md`（环境检测方法、参数合同、完成条件）

### coverage_target（测试覆盖率目标）

*（仅当本 skill 涉及测试生成或验证时包含此节）*

- **本 skill 的角色**：Skill 层（只读取，不询问）
- **状态来源**：从上下文中读取 `[COVERAGE_TARGET: X%]`
- **行为约束**：
  - 生成测试时确保覆盖率 ≥ coverage_target
  - 生成后标注预期覆盖率
  - 如果实际覆盖率 < coverage_target：触发补测（automation_mode=true）或询问用户（automation_mode=false）
- **详细规范**：见 CLAUDE.md「📚 共享概念速查 → coverage_target」及 G9 三层架构

### P4 质量验证（回归闸门）

*（仅当本 skill 参与 P4 回归验证时包含此节）*

- **本 skill 的职责**：在 P4 回归闸门中承担 [具体验证步骤]
- **验证范围**：
  - 例如：codex-code-reviewer 负责第 1 轮工作流验证 + 第 2 轮 CLI 深度分析
  - 例如：simple-gemini 负责文档联动验证中的文档生成/更新
- **完成条件**：[本 skill 的验证通过标准]
- **详细规范**：见 `references/standards/p4_final_validation.md`（完整 3 步验证流程）

---

## 重构示例：simple-gemini skill

以下是一个完整的重构示例，展示如何应用上述模板：

---

## simple-gemini Skill 文档（重构后示例）

### 与全局规则/标准的关系

#### automation_mode（自动化模式）

- **本 skill 的角色**：Skill 层（只读取，不判断）
- **状态来源**：从 main-router 传递的上下文中读取 `[AUTOMATION_MODE: true/false]`
- **行为约束**：
  - ❌ 禁止检查用户初始请求中的关键词（"全程自动化"等）
  - ❌ 禁止修改 router 设置的 automation_mode 状态
  - ✅ 根据状态调整行为：
    - `automation_mode=true`：
      - 自动选择最佳模型（gemini-2.5-pro / gemini-2.5-flash）
      - 自动确定文档结构和内容组织
      - 不询问用户"是否使用此模板？"等问题
      - 决策记录到 `[自动决策记录]` 片段
    - `automation_mode=false`：
      - 在选择模型时询问用户偏好
      - 在生成文档大纲后询问用户确认
- **详细规范**：见 CLAUDE.md「📚 共享概念速查 → automation_mode」及 G11 三层架构

#### auto_log（自动化决策日志）

- **触发条件**：仅当 automation_mode=true 时，本 skill 输出 `[自动决策记录]` 片段
- **职责分工**：
  - 本 skill：生成结构化的决策片段，包含：
    - 选择的模型及理由（例如：gemini-2.5-pro，因为需要生成长文档）
    - 文档结构决策（例如：使用 3 级标题结构，包含 5 个主要章节）
    - 模板选择（例如：使用 doc_templates/technical_spec.md）
    - 跳过的选项及原因（例如：跳过 FAQ 章节，因为项目处于早期阶段）
  - main-router：汇总所有 skill 的片段
  - simple-gemini（最终阶段）：基于统一模板生成 `auto_log.md` 文件
- **模板位置**：`skills/shared/auto_log_template.md`
- **详细规范**：见 CLAUDE.md「📚 共享概念速查 → auto_log」

#### CLI 调用（G10 标准）

- **本 skill 的职责**：当需要启动 gemini CLI 时，调用 `mcp__zen__clink` 工具
- **参数传递**：
  ```yaml
  Tool: mcp__zen__clink
  Parameters:
    prompt: "gemini"
    cli_name: "gemini"
    role: "default"  # 或 "codereviewer" / "planner" 根据任务选择
    files: [相关文件路径列表]  # 可选
    continuation_id: [会话延续 ID]  # 可选
  ```
- **禁止行为**：
  - ❌ 不得自行检测操作系统环境
  - ❌ 不得手动拼接 PowerShell / WSL 命令
  - ❌ 不得传递不支持的参数（args / working_directory）
- **详细规范**：见 `references/standards/cli_env_g10.md`（环境检测方法、参数合同、完成条件）

#### P4 质量验证（回归闸门）

- **本 skill 的职责**：在 P4 回归闸门中承担文档联动验证中的文档生成/更新任务
- **验证范围**：
  - 当检测到 PROJECTWIKI.md 缺失"设计决策 & 技术债务"中的缺陷复盘章节时，自动生成
  - 当检测到 CHANGELOG.md 未记录 P4 修复变更时，自动补充
- **完成条件**：
  - ✅ PROJECTWIKI.md 包含完整的缺陷复盘（根因、修复、影响、预防）
  - ✅ CHANGELOG.md 在 `[Unreleased]` 或对应版本的 Fixed 分区中记录修复变更
  - ✅ 双向链接有效（PROJECTWIKI ↔ CHANGELOG）
- **详细规范**：见 `references/standards/p4_final_validation.md`（完整 3 步验证流程）

---

## 应用到其他 skill 的通用步骤

对于任意 skill，按以下步骤填写模板：

1. **automation_mode**：
   - 明确本 skill 在 automation_mode=true 时自动做哪些决策？
   - 明确在 automation_mode=false 时询问用户哪些问题？

2. **auto_log**（如果 automation_mode=true）：
   - 列出本 skill 输出的决策片段包含哪些字段？
   - 示例字段：模型选择、参数配置、跳过的选项及原因、执行结果

3. **CLI 调用**（如果需要）：
   - 明确本 skill 调用哪个 CLI？（codex / gemini / claude）
   - 列出需要传递的参数（prompt / cli_name / role / files / continuation_id）

4. **coverage_target**（如果涉及测试）：
   - 明确本 skill 如何确保覆盖率达标？
   - 明确未达标时如何处理？（自动补测 vs 询问用户）

5. **P4 质量验证**（如果参与）：
   - 明确本 skill 在 3 步验证流程中承担哪些职责？
   - 明确完成条件是什么？

---

## 重构后的文档结构建议

重构后的 skill 文档建议按以下结构组织：

```markdown
# [Skill Name] Skill

> **简介**：[1-2 句话概括本 skill 的用途]

## 与全局规则/标准的关系

[按上述模板填写]

## 触发条件

[什么场景下 main-router 会调用本 skill]

## 工作流程

[本 skill 的核心执行步骤，3-5 个阶段]

## 输入/输出

- **输入**：[需要的参数、上下文、文件等]
- **输出**：[生成的文件、返回的数据结构等]

## 示例用法

[1-2 个典型场景的完整示例]

## 与其他 skill 的协作

[如何与 main-router / codex / simple-gemini 等其他 skill 协作]

## 注意事项

[常见陷阱、限制、已知问题等]
```

---

## 维护说明

- 当全局规则（G1-G11）或标准文档（G10, P4 等）发生变更时，检查所有 skill 文档是否需要同步更新
- 优先更新"与全局规则/标准的关系"章节，确保引用正确
- 避免在 skill 文档中重复定义已在 CLAUDE.md 或标准文档中定义的概念
