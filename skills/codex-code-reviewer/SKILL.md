---
name: codex-code-reviewer
description: Systematic code review workflow using zen mcp's codex tool. Use this skill when the user explicitly requests "使用codex对代码进行检查", "检查刚刚生成的代码是否存在问题", or "每次生成完一次代码就要进行检查". The skill performs iterative review cycles - checking code quality, presenting issues to the user for approval, applying fixes, and re-checking until no issues remain or maximum iterations (5) are reached.
---

# Codex Code Reviewer

## Overview

This skill provides a systematic, iterative code review workflow powered by zen mcp's codex tool. It automatically checks recently modified code files against project standards (AGENTS.md and CLAUDE.md requirements), presents identified issues to users for approval, applies fixes, and re-validates until code quality standards are met or the maximum iteration limit is reached.

**Operation Modes:**
- **Interactive Mode (Default)**: Present issues to user, wait for approval before applying fixes
- **Full Automation Mode**: Automatically select and apply all suggested fixes without user approval (activated when user initially requests "全程自动化" or "full automation")

## When to Use This Skill

Trigger this skill when the user says:
- "使用codex对代码进行检查"
- "请你帮我检查刚刚生成的代码是否存在问题"
- "每次生成完一次代码就要进行检查"
- Similar requests for code quality validation using codex

## Workflow: Iterative Code Review Cycle

### Prerequisites

Before starting the review cycle:

1. **🚨 Read Operation Mode from Context (Three-Layer Architecture):**
   - **MUST** read `automation_mode` from the context passed by main-router
   - **Context Format**: `[AUTOMATION_MODE: true]` or `[AUTOMATION_MODE: false]`
   - **READ ONLY**: This skill MUST NOT detect/judge automation mode itself
   - **Behavior**:
     - If `automation_mode = true`: Enable **Full Automation Mode** (auto-apply fixes based on severity)
     - If `automation_mode = false`: Use **Interactive Mode** (require user approval)
   - **❌ FORBIDDEN**: Do NOT check user's initial request for keywords like "全程自动化"

2. **Identify Files to Review:**
   - Use `git status` or similar to identify recently modified files
   - **Interactive Mode (automation_mode = false)**: Confirm with user which files should be reviewed
   - **Automated Mode (automation_mode = true)**: Auto-select all recently modified files, log decision to auto_log.md

3. Initialize iteration counter: `current_iteration = 1`
4. Set maximum iterations: `max_iterations = 5`
5. Initialize review tool tracker: `first_review_done = false`
6. **Detect Review Context:**
   - Check if this is **final quality validation** (项目结束/最终验证)
   - If YES: Enable **Final Validation Mode** (requires minimum 2 passes: codereview + clink)
   - If NO: Use **Standard Review Mode**

### Review Cycle Loop

Execute the following loop until termination conditions are met:

#### Step 1: Select and Invoke Appropriate Review Tool

**Tool Selection Logic:**

```python
if current_iteration == 1 and not first_review_done:
    # First review: Use mcp__zen__codereview
    review_tool = "mcp__zen__codereview"
    first_review_done = True
else:
    # Second and subsequent reviews: Use mcp__zen__clink with codex CLI
    review_tool = "mcp__zen__clink"
```

**A) First Review: Call `mcp__zen__codereview`**

```
Tool: mcp__zen__codereview
Parameters:
- step: Detailed review request (e.g., "Review the following files for code quality, security, performance, and adherence to project standards...")
- step_number: current_iteration
- total_steps: Estimate based on findings (start with 2-3)
- next_step_required: true (initially)
- findings: Document all discovered issues
- relevant_files: [list of recently modified file paths - MUST be absolute full paths]
- review_type: "full" (covers quality, security, performance, architecture)
- model: "codex" (or user-specified model)
- review_validation_type: "external" (for expert validation)
- confidence: Start with "exploring", increase as understanding grows
```

**Important**:
- Always use **absolute full paths** for `relevant_files`
- Follow zen mcp's codereview workflow (typically 2-3 steps for external validation)
- Reference `references/code_quality_standards.md` for quality criteria

**B) Second and Subsequent Reviews: Call `mcp__zen__clink` with codex CLI**

```
Tool: mcp__zen__clink
Parameters:
- prompt: |
    请对以下文件进行代码审查，检查代码质量、安全性、性能和架构设计：

    [列出文件路径及其上下文]

    审查维度：
    1. 代码质量：可读性、可维护性、复杂度
    2. 安全性：漏洞、敏感信息处理
    3. 性能：效率、资源使用
    4. 架构：设计模式、模块化
    5. 文档：注释完整性

    请按严重程度（critical/high/medium/low）分类问题，
    并提供具体的文件位置、行号和修复建议。
- cli_name: "codex"
- role: "code_reviewer"
- files: [list of recently modified file paths - MUST be absolute full paths]
- continuation_id: [optional, for context continuity across reviews]
```

**Important**:
- Always use **absolute full paths** for `files`
- Use `continuation_id` to maintain context across multiple clink review iterations
- clink directly interacts with codex CLI for detailed code analysis
- Supported parameters: `prompt` (required), `cli_name`, `role`, `files`, `images`, `continuation_id`

#### Step 2: Present Findings and Decision Making

After codex returns the review results:

1. **Summarize Issues Clearly:**
   - Group by severity (critical/high/medium/low)
   - Provide specific file locations and line numbers
   - Explain the impact of each issue

2. **🚨 First: Read automation_mode from Context**

   ```
   IF [AUTOMATION_MODE: false] → Interactive Mode (see A below)
   IF [AUTOMATION_MODE: true] → Automated Mode (see B below)
   ```

   **Decision Making Based on Mode:**

   **A) Interactive Mode (automation_mode = false):**
   ```
   发现 X 个问题需要修复：

   [严重] 文件A:行B - 问题描述
   [中等] 文件C:行D - 问题描述
   ...

   是否批准修复这些问题？
   - 是：继续修复
   - 否：终止审查
   - 部分：请指定要修复的问题
   ```
   **Wait for User Response** - Do NOT proceed without explicit approval

   **B) Full Automation Mode (automation_mode = true):**
   ```
   [全自动模式] 发现 X 个问题，自动选择修复策略：

   [严重] 文件A:行B - 问题描述 → ✅ 自动修复
   [中等] 文件C:行D - 问题描述 → ✅ 自动修复
   ...

   决策依据：
   - 所有 critical/high 级别问题：强制修复
   - medium 级别问题：如果修复安全且不影响业务逻辑 → 修复
   - low 级别问题：如果是代码风格问题 → 修复

   立即执行修复...
   ```
   **Automatic Decision** - No user approval needed, proceed directly to Step 3

3. **Automation Mode Decision Logic:**
   ```python
   if automation_mode:
       for issue in issues_found:
           if issue.severity in ["critical", "high"]:
               # Always fix critical and high severity issues
               apply_fix(issue)
           elif issue.severity == "medium":
               # Fix if safe and doesn't change business logic
               if is_safe_fix(issue) and not affects_business_logic(issue):
                   apply_fix(issue)
           elif issue.severity == "low":
               # Fix if it's a style/formatting issue
               if is_style_issue(issue):
                   apply_fix(issue)

       # Log all auto-decisions to auto_log.md for transparency
       log_to_auto_log_md(fixed_issues, skipped_issues, rationale, confidence, standards_met)
   ```

#### Step 3: Apply Fixes

**Interactive Mode**: If user approves
**Automation Mode**: Proceed directly based on auto-decision logic

1. Apply fixes to the identified issues
2. Use appropriate tools (Edit, Write, etc.) to modify code
3. Follow project coding standards from AGENTS.md and CLAUDE.md
4. Document changes made

**Automation Mode Transparency (Log to auto_log.md):**
- Log all applied fixes with rationale, confidence, and standards met
- Log skipped fixes with reasons (e.g., "affects business logic", "unclear impact")
- All automated decisions MUST be recorded in `auto_log.md`
- Example log format:
  ```
  [自动修复记录]
  ✅ 已修复：3 个严重问题，2 个中等问题，1 个代码风格问题
  ⏭️ 已跳过：1 个中等问题（可能影响业务逻辑）

  详细决策：
  1. security-issue-001 (critical) → 修复 (SQL注入风险)
  2. performance-issue-002 (medium) → 修复 (N+1查询，安全修复)
  3. style-issue-003 (low) → 修复 (变量命名不规范)
  4. logic-change-004 (medium) → 跳过 (需要理解业务逻辑才能修复)
  ```

#### Step 4: Increment and Validate

```
current_iteration = current_iteration + 1
```

Check termination conditions:

**Standard Review Mode:**
- **Success**: Review tool reports no issues → Exit loop, report success
- **Max iterations reached**: current_iteration > max_iterations → Exit loop, report remaining issues
- **User cancellation**: User declined fixes → Exit loop
- **Continue**: Issues remain and iterations < max_iterations → Go to Step 1

**Final Validation Mode (项目结束/最终验证):**
- **Minimum Pass Requirement**: MUST complete at least 2 passes
  - Pass 1: mcp__zen__codereview (first_review_done = true)
  - Pass 2: mcp__zen__clink with codex CLI
- **Early Exit Prevention**:
  - If current_iteration < 2 → MUST continue to Step 1 (even if no issues found)
  - If current_iteration >= 2 AND no issues found in both passes → Exit loop, report success
- **Max iterations reached**: current_iteration > max_iterations → Exit loop, report remaining issues
- **User cancellation**: User declined fixes → Exit loop
- **Continue**: Issues remain OR minimum passes not met → Go to Step 1

### Termination and Reporting

When the cycle terminates, provide a final report:

```
代码审查完成报告：

审查轮次：X / 5
审查文件：[列出文件]

使用工具：
- 第 1 轮：mcp__zen__codereview (codex workflow validation)
- 第 2 轮：mcp__zen__clink (codex CLI direct analysis)
- 第 3+ 轮：mcp__zen__clink (continued)

最终状态：
- ✅ 所有问题已修复 / ⚠️ 达到最大审查次数 / ❌ 用户取消
- [Final Validation Mode] ✅ 已完成最少 2 轮验证 / ⚠️ 未满足最少 2 轮要求

修复摘要：
- 已修复问题：X 个
- 剩余问题：Y 个（如果有）

建议：[下一步建议]
```

## Code Quality Standards

This skill enforces standards defined in:
- **AGENTS.md**: Global rules (G1-G8), phase-specific requirements (P1-P4)
- **CLAUDE.md**: Model development workflow, ethics, reproducibility, explainability
- **Project-specific**: PROJECTWIKI.md architecture decisions and conventions

Key quality dimensions checked:
1. **Code Quality**: Readability, maintainability, complexity
2. **Security**: Vulnerabilities, sensitive data handling
3. **Performance**: Efficiency, resource usage
4. **Architecture**: Adherence to documented design decisions
5. **Documentation**: Code comments, PROJECTWIKI.md alignment

See `references/code_quality_standards.md` for detailed criteria.

## Best Practices

### For Effective Reviews

1. **Scope Control**: Review recently modified files only (use git diff/status)
2. **Context Preservation**: Maintain continuation_id across review cycles for context continuity
3. **Incremental Fixes**: Address high-severity issues first, then iterate for lower-priority ones
4. **User Communication**: Always explain WHY an issue matters and HOW the fix improves code

### Error Handling

- **Tool Errors**: If `mcp__zen__codereview` fails, report to user and offer manual review
- **Ambiguous Issues**: When codex findings are unclear, seek user clarification before fixing
- **Conflicting Standards**: If AGENTS.md and CLAUDE.md conflict, prioritize AGENTS.md (global rules)

## Resources

### references/code_quality_standards.md

Detailed quality standards extracted from AGENTS.md and CLAUDE.md. Load this reference when:
- Detailed quality criteria are needed
- User questions specific standards
- Ambiguous quality issues require clarification

Use grep patterns to search: `G1|G2|核心原则|伦理|可复现`

## Example Usage

### Example 1: Interactive Mode (Default)

**User**: "使用codex对代码进行检查"

**Assistant**:
```
好的，我将使用 codex 对最近修改的代码进行系统审查。

首先，让我识别最近修改的文件...
[运行 git status]

发现以下文件有修改：
- src/features.py
- src/model_training.py

读取上下文: [AUTOMATION_MODE: false]
模式：交互式审查（需要用户批准修复）

开始第 1 轮审查...
[调用 mcp__zen__codereview]

审查结果：
发现 3 个问题：
[严重] src/features.py:45 - 潜在的空指针引用
[中等] src/model_training.py:120 - 缺少异常处理
[低] src/features.py:30 - 变量命名不符合规范

是否批准修复这些问题？
```

**User**: "是"

**Assistant**:
```
开始修复问题...
[应用修复]

修复完成。开始第 2 轮审查...
[调用 mcp__zen__clink with codex CLI]

审查结果：✅ 未发现新问题

代码审查完成！
审查轮次：2 / 5
使用工具：
- 第 1 轮：mcp__zen__codereview
- 第 2 轮：mcp__zen__clink (codex CLI)
所有问题已成功修复。
```

---

### Example 2: Full Automation Mode ⭐

**User Initial Request**: "全程自动化，帮我开发登录功能，代码完成后自动检查质量"

**Main Router**: Detects "全程自动化" → Sets automation_mode = true

**After code generation, Main Claude invokes codex-code-reviewer with automation_mode = true:**

**Assistant**:
```
好的，我将使用 codex 对刚生成的代码进行系统审查。

首先，让我识别最近修改的文件...
[运行 git status]

发现以下文件有修改：
- src/auth/login.py
- src/auth/session.py
- tests/test_login.py

读取上下文: [AUTOMATION_MODE: true]
模式：全自动审查（自动选择并应用修复）

开始第 1 轮审查...
[调用 mcp__zen__codereview]

审查结果：
发现 5 个问题：
[严重] src/auth/login.py:45 - SQL注入风险 (critical)
[严重] src/auth/session.py:23 - 明文存储密码 (critical)
[中等] src/auth/login.py:78 - 缺少异常处理 (medium)
[中等] src/auth/session.py:56 - 性能问题：N+1查询 (medium)
[低] tests/test_login.py:12 - 测试命名不规范 (low)

[全自动模式] 自动选择修复策略：

决策分析：
✅ SQL注入风险 (critical) → 自动修复（安全问题强制修复）
✅ 明文存储密码 (critical) → 自动修复（安全问题强制修复）
✅ 缺少异常处理 (medium) → 自动修复（标准异常处理，不影响业务逻辑）
✅ N+1查询问题 (medium) → 自动修复（使用 select_related，安全优化）
✅ 测试命名不规范 (low) → 自动修复（代码风格问题）

立即执行修复...
[自动应用所有修复]

[自动修复记录]
✅ 已修复：2 个严重问题，2 个中等问题，1 个代码风格问题

详细修复：
1. SQL注入风险 → 使用参数化查询替换字符串拼接
2. 明文密码 → 使用 bcrypt 加密存储
3. 异常处理 → 添加 try-except 块和错误日志
4. N+1查询 → 使用 select_related('user') 优化查询
5. 测试命名 → 重命名为 test_login_with_valid_credentials

修复完成。开始第 2 轮审查...
[调用 mcp__zen__clink with codex CLI]

审查结果：✅ 未发现新问题

代码审查完成！
审查轮次：2 / 5
使用工具：
- 第 1 轮：mcp__zen__codereview
- 第 2 轮：mcp__zen__clink (codex CLI)
全自动模式：自动修复 5 个问题，跳过 0 个问题
所有问题已成功修复，无需用户干预。
```

**Key Differences in Full Automation Mode:**
- ✅ No user approval step - proceeds directly to fixing
- ✅ Automatic decision logic based on severity and safety
- ✅ Transparent logging of all auto-decisions
- ✅ Rationale provided for each fix/skip decision
- ✅ Maintains same quality standards as interactive mode

---

### Example 3: Final Validation Mode (项目结束/最终质量验证) ⭐⭐

**User**: "项目已完成,请进行最终质量验证"

**Assistant**:
```
好的,我将进行最终质量验证。

读取上下文: [AUTOMATION_MODE: false] (默认交互模式)
检测到：项目结束/最终验证阶段
启用：Final Validation Mode（最少 2 轮验证）

首先，让我识别项目文件...
[运行 git status 或分析项目结构]

发现以下核心文件：
- src/features.py
- src/model_training.py
- src/utils.py
- tests/test_features.py
- tests/test_model.py

开始第 1 轮审查（使用 mcp__zen__codereview）...
[调用 mcp__zen__codereview]

审查结果：
发现 2 个问题：
[中等] src/utils.py:67 - 缺少输入验证
[低] tests/test_features.py:23 - 测试覆盖率不足

是否批准修复这些问题？
```

**User**: "是"

**Assistant**:
```
开始修复问题...
[应用修复]

修复完成。开始第 2 轮审查（使用 mcp__zen__clink with codex CLI）...
[调用 mcp__zen__clink]
Parameters:
- prompt: "请对以下文件进行深度代码审查..."
- cli_name: "codex"
- role: "code_reviewer"
- files: [所有核心文件的绝对路径]

审查结果：✅ 未发现新问题

代码审查完成！
审查轮次：2 / 5

使用工具：
- 第 1 轮：mcp__zen__codereview (codex workflow validation)
- 第 2 轮：mcp__zen__clink (codex CLI direct analysis)

最终状态：
- ✅ 所有问题已修复
- ✅ 已完成最少 2 轮验证要求

修复摘要：
- 已修复问题：2 个
- 剩余问题：0 个

质量验证通过！项目已达到发布标准。
```

**Key Features in Final Validation Mode:**
- ✅ **Mandatory minimum 2 passes**: Cannot exit before completing both codereview and clink checks
- ✅ **Dual-tool verification**: First pass uses codereview workflow, second pass uses codex CLI directly
- ✅ **Early exit prevention**: Even if first pass finds no issues, must proceed to second pass
- ✅ **Comprehensive coverage**: Ensures thorough quality validation before project completion

---

## Notes

- This skill uses **dual-tool approach** for comprehensive code review:
  - **First review (iteration 1)**: `mcp__zen__codereview` for workflow-based validation
  - **Subsequent reviews (iteration 2+)**: `mcp__zen__clink` with codex CLI for direct analysis
- Maximum 5 iterations prevents infinite loops while allowing thorough review
- **Interactive Mode (Default)**: Always prioritize user consent before applying code changes
- **Full Automation Mode**: Auto-apply fixes based on severity and safety analysis, with full transparency
- **Final Validation Mode**: Enforces minimum 2 passes (codereview + clink) for project completion
- Maintains compatibility with AGENTS.md workflow (P3: 执行方案, P4: 错误处理)
- **🚨 CRITICAL - automation_mode Management**:
  - **Three-Layer Architecture**: This skill follows the global automation_mode architecture
  - **Router (Layer 1)**: Only main-router judges and sets `automation_mode` based on user's initial request
  - **Transmission (Layer 2)**: Router passes automation_mode to this skill via context `[AUTOMATION_MODE: true/false]`
  - **Skill (Layer 3 - READ ONLY)**: This skill ONLY reads automation_mode, never judges or modifies it
  - **❌ FORBIDDEN**: Do NOT ask user "是否需要自动化执行?" or check for automation keywords
  - **Automated Mode (automation_mode=true)**: All decisions logged to `auto_log.md` with reason, confidence, standards
- Final validation mode activated when user mentions "项目结束" / "最终验证" / "最终质量验证"
