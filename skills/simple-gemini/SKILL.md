---
name: simple-gemini
description: Collaborative documentation and test code writing workflow using zen mcp's clink to launch gemini CLI session in WSL (via 'gemini' command) where all writing operations are executed. Use this skill when the user requests "使用gemini来编写测试文件", "使用gemini来编写文档", "生成相关测试文件", "生成一份解释文档", or similar document/test writing tasks. The gemini CLI session acts as the specialist writer, working with the main Claude model for context gathering, outline approval, and final review. For test code, codex CLI (also launched via clink) validates quality after gemini completes writing.
---

# Gemini Documentation & Test Writer

## Overview

This skill provides a collaborative writing workflow where gemini CLI (launched via zen mcp's clink tool as a WSL command `gemini`) serves as a specialist writer for markdown documentation and test code. All writing operations are executed within the gemini CLI session environment, while the main Claude model handles context gathering, user interaction, and test execution. For test code, codex CLI (also launched via clink as WSL command `codex`) performs quality validation after gemini completes the initial writing.

**Technical Architecture:**
- **zen-mcp clink**: Acts as the bridge to launch CLI tools in WSL environment
- **gemini CLI session**: Opened via `gemini` command in WSL, where all document/test writing happens
- **codex CLI session**: Opened via `codex` command in WSL for code review tasks
- **Conversation context**: Maintained via `continuation_id` across CLI sessions

**Division of Responsibilities:**
- **Gemini CLI Session** (in WSL): Specialist writer for .md documents and test code, all writing executed inside this CLI environment
- **Main Claude Model**: Context gathering, CLI invocation orchestration, outline approval, test execution, final review
- **Codex CLI Session** (in WSL): Test code quality validation and correction, review executed inside this CLI environment
- **User**: Approval of outlines and final review (in Interactive Mode) or information recipient (in Automated Mode)

## When to Use This Skill

Trigger this skill when the user or main model requests:
- "使用gemini来编写测试文件"
- "使用gemini来编写文档"
- "生成相关测试文件"
- "生成一份解释文档"
- Commands from Claude or codex to write documentation
- Any request to create .md documentation or test code files

## Operation Mode (Based on Router's automation_mode)

**🚨 CRITICAL**: This skill **MUST read** the `automation_mode` status from the context set by main-router. **DO NOT** ask the user about automation preference or check for trigger phrases - this is handled exclusively by the router.

This skill supports two operation modes based on the `automation_mode` state:

### 1. Interactive Mode (automation_mode=false, Default)

**Triggered When:** Router sets `automation_mode=false` (default)

**User Approval Required:**
- Outline approval before full document writing
- Final document review before saving
- Test code correction approval
- All major decisions require user confirmation

**When to Use:**
- User wants control over the process
- Important or sensitive documents
- First-time document generation
- Learning and understanding the workflow

### 2. Automated Mode (automation_mode=true)

**Triggered When:** Router detects automation keywords in initial request and sets `automation_mode=true`

**Main Claude Makes Decisions:**
- Main Claude reviews and approves outlines autonomously
- Main Claude validates final documents against standards
- Main Claude approves test code corrections automatically
- Only final results are presented to user for information
- **All decisions are logged to auto_log.md**

**Main Claude's Autonomous Decision Criteria:**
- **Outline**: Check completeness, structure alignment with templates
- **Document**: Verify adherence to standards (CLAUDE.md)
- **Test Code**: Ensure quality meets requirements (coverage ≥ 70%)
- **Only escalate to user** if critical issues or ambiguities are detected

### Mode Detection (READ ONLY - Three-Layer Architecture)

**Layer 1: Router (Global Truth Source)**
- Only the main-router judges and sets `automation_mode` based on initial request
- Status is set once at task start and remains unchanged throughout lifecycle

**Layer 2: Transmission**
- Router passes `automation_mode` status to this skill via context
- Format: `[AUTOMATION_MODE: true]` or `[AUTOMATION_MODE: false]`

**Layer 3: Skill (READ ONLY - This Skill)**

**✅ MUST DO:**
- Read `automation_mode` from context passed by router
- Adjust behavior based on the status:
  - `automation_mode=true` → Auto-approve all decisions, log to auto_log.md
  - `automation_mode=false` → Interactive confirmation required

**❌ ABSOLUTELY FORBIDDEN:**
- ❌ Ask user "是否需要自动化执行？"
- ❌ Check user's initial request for automation keywords
- ❌ Modify the automation_mode status set by router
- ❌ Re-detect automation triggers during execution

## Workflow Decision Tree

```
User Request
    │
    ├─→ Document Writing? ──→ Document Writing Workflow
    │
    └─→ Test Code Writing? ──→ Test Code Writing Workflow
```

## Document Writing Workflow

### Phase 1: Preparation & Context Gathering (Main Claude)

**Main Claude's Responsibility:**

1. **Understand the Documentation Need:**
   - What type of document? (README, PROJECTWIKI, ADR, CHANGELOG, technical spec, etc.)
   - What is the purpose and audience?
   - What scope should be covered?

2. **Gather Context:**
   - Read relevant code files if needed
   - Check existing documentation structure
   - Identify project standards from CLAUDE.md
   - **Context File Selection:**
     - **Interactive Mode (automation_mode = false)**: Ask user: "Do you need me to reference existing code/files for this document?"
     - **Automated Mode (automation_mode = true)**: Auto-analyze project structure and select relevant files, log decision to auto_log.md

3. **Identify Document Requirements:**
   - For CLAUDE.md mandated documents (PROJECTWIKI.md, CHANGELOG.md, ADRs):
     - Apply standards from `references/doc_templates.md`
     - Follow CLAUDE.md 项目知识库内容结构与生成规则统一模板
   - For other documents:
     - Determine appropriate structure
     - Identify key sections needed

### Phase 2: Outline Generation (Gemini CLI Session)

**Invoke Gemini CLI Session via `mcp__zen__clink`:**

```
Tool: mcp__zen__clink
Parameters:
- cli_name: "gemini"  # Launches 'gemini' command in WSL
- prompt: "Generate a detailed outline for [document type] covering [scope].
          Context: [provide all gathered context]
          Requirements: [standards from CLAUDE.md if applicable]
          Purpose: [document purpose]
          Audience: [target readers]"
- files: [list of relevant file paths for context - absolute paths]
- role: "default" (or "planner" for complex planning tasks)
- continuation_id: [if continuing from previous gemini CLI session]
```

**What Happens:**
1. zen-mcp clink opens a gemini CLI session in WSL
2. The prompt and files are passed into the gemini CLI environment
3. All outline generation work is executed inside the gemini CLI session
4. The gemini CLI session returns the completed outline
5. The session context is preserved via continuation_id for future calls

**Gemini CLI Session Output:** Detailed outline with:
- Main sections and subsections
- Key points to cover in each section
- Special considerations (diagrams, code examples, etc.)

### Phase 3: Outline Review & Approval (Main Claude + User)

**Main Claude's Responsibility:**

**🚨 First: Read automation_mode from context**
```
IF [AUTOMATION_MODE: false] → Interactive Mode
IF [AUTOMATION_MODE: true] → Automated Mode
```

#### Interactive Mode (automation_mode=false, Default)

1. **Present Outline to User:**
   ```
   Gemini CLI 已生成文档大纲：

   [显示大纲]

   是否批准此大纲？
   - 是：继续编写
   - 否：请提供修改意见
   - 修改：[具体修改建议]
   ```

2. **Wait for User Approval** - Do NOT proceed without confirmation

3. **Iterate if Needed:** If user requests changes, provide feedback to gemini and regenerate outline

#### Automated Mode (automation_mode=true)

1. **Main Claude Reviews Outline Autonomously (based on automation_mode=true):**
   - Check completeness: All required sections present?
   - Check structure: Follows template requirements?
   - Check scope: Covers all identified needs?
   - Check standards: Aligns with CLAUDE.md?

2. **Decision Logic (based on automation_mode=true from router):**
   ```
   IF outline is complete AND well-structured AND meets standards:
       → Auto-approve, proceed to Phase 4
       → Log to auto_log.md: "大纲已自动审批通过 (automation_mode=true)"
       → Record: decision reason, confidence, standards met
   ELSE:
       → Provide feedback to Gemini CLI, regenerate outline
       → Retry up to 2 times
       → Log each retry to auto_log.md
       → If still not meeting standards, escalate to user
   ```

3. **Present Decision to User (Information Only):**
   ```
   ✅ 大纲已自动审批（自动化模式）

   [显示大纲摘要]

   审批原因：
   - ✅ 结构完整
   - ✅ 符合模板要求
   - ✅ 覆盖所有需求

   继续编写完整文档...
   ```

### Phase 4: Document Writing (Gemini CLI Session)

**After Outline Approval, Invoke Gemini CLI Session:**

```
Tool: mcp__zen__clink
Parameters:
- cli_name: "gemini"  # Reuses the same gemini CLI session in WSL
- prompt: "Write the complete [document type] based on this approved outline:
          [outline]

          Writing Guidelines:
          - Follow the outline structure exactly
          - For PROJECTWIKI.md/CHANGELOG.md/ADR: strictly follow templates in references/doc_templates.md
          - Use Mermaid diagrams where appropriate (```mermaid blocks)
          - Write in clear, professional Chinese (or English if specified)
          - Include code examples where helpful
          - Ensure consistency with CLAUDE.md standards

          Context: [all gathered context]
          Referenced files: [files to reference]"
- files: [relevant files - absolute paths]
- role: "default"
- continuation_id: [reuse from outline generation - maintains session context]
```

**What Happens:**
1. zen-mcp clink reconnects to the existing gemini CLI session using continuation_id
2. The session has context from the previous outline generation
3. The full document writing work is executed inside the gemini CLI session
4. The gemini CLI session returns the completed markdown document

**Gemini CLI Session Output:** Complete markdown document

### Phase 5: Review & Finalization (Main Claude + User)

**Main Claude's Responsibility:**

**🚨 First: Read automation_mode from context**
```
IF [AUTOMATION_MODE: false] → Interactive Mode
IF [AUTOMATION_MODE: true] → Automated Mode
```

#### Interactive Mode (automation_mode=false, Default)

1. **Present Document:**
   ```
   Gemini CLI 已完成文档编写：

   文档类型：[type]
   文件路径：[proposed path]

   [显示文档内容或摘要]

   请审核此文档：
   - ✅ 批准并保存
   - 🔄 需要修改：[请说明修改内容]
   - ❌ 重新生成
   ```

2. **Handle Feedback:**
   - If approved: Write the document to the file system
   - If modifications needed: Provide feedback to gemini for revision
   - If regeneration needed: Return to Phase 2

3. **Finalize:**
   - Save document to appropriate location
   - Update CHANGELOG.md if this is a significant documentation change
   - Confirm completion with user

#### Automated Mode (automation_mode=true)

1. **Main Claude Validates Document Autonomously (based on automation_mode=true):**
   - **For PROJECTWIKI/CHANGELOG/ADR**: Check against `references/doc_templates.md`
     - All required sections present?
     - Mermaid diagrams included?
     - Links are valid?
     - Consistent with CLAUDE.md standards?
   - **For other documents**: Check completeness, clarity, and consistency

2. **Decision Logic (based on automation_mode=true from router):**
   ```
   IF document meets all quality standards:
       → Auto-approve and save
       → Update CHANGELOG.md if needed
       → Log to auto_log.md: "文档已自动审批并保存 (automation_mode=true)"
       → Record: validation checklist, quality metrics, decision reason
   ELSE:
       → Provide feedback to Gemini CLI for revision
       → Retry up to 2 times
       → Log each retry and reason to auto_log.md
       → If still not meeting standards, escalate to user
   ```

3. **Present Final Result to User (Information Only):**
   ```
   ✅ 文档已自动完成并保存（自动化模式）

   文档类型：[type]
   文件路径：[actual path]

   质量检查：
   - ✅ 结构完整
   - ✅ 符合标准
   - ✅ 格式正确
   - ✅ 链接有效

   [显示文档摘要或关键章节]

   已自动更新 CHANGELOG.md
   ```

## Test Code Writing Workflow

### Phase 1: Preparation & Context Gathering (Main Claude)

**Main Claude's Responsibility:**

1. **Understand Testing Need:**
   - What code/module needs testing?
   - Test type: unit, integration, or E2E?
   - Testing framework: pytest, unittest, jest, etc.?
   - Coverage requirements (default ≥ 70%)

2. **Gather Context:**
   - Read the code to be tested
   - Identify key functions/classes/modules
   - Check existing test structure
   - Review testing standards from CLAUDE.md

3. **Identify Test Requirements:**
   - Key functionality to test
   - Edge cases and boundary conditions
   - Error handling scenarios
   - Performance considerations if applicable

### Phase 2: Test Code Generation (Gemini CLI Session)

**Invoke Gemini CLI Session via `mcp__zen__clink`:**

```
Tool: mcp__zen__clink
Parameters:
- cli_name: "gemini"  # Launches 'gemini' command in WSL
- prompt: "Generate comprehensive test code for [module/function].

          Code to Test:
          [code content or file references]

          Test Requirements:
          - Framework: [pytest/unittest/etc.]
          - Test types: [unit/integration/E2E]
          - Coverage target: ≥ 70%
          - Include: normal cases, edge cases, error handling, boundary conditions

          Standards:
          - Follow best practices from references/test_patterns.md
          - Clear test names and assertions
          - Proper setup/teardown
          - Mock external dependencies
          - Document complex test logic

          Context: [project structure, existing tests, conventions]"
- files: [code files to test + existing test examples - absolute paths]
- role: "default"
- continuation_id: [if continuing from previous gemini CLI session]
```

**What Happens:**
1. zen-mcp clink opens a gemini CLI session in WSL
2. Source code and test examples are passed into the gemini CLI environment
3. All test code generation work is executed inside the gemini CLI session
4. The gemini CLI session returns the completed test code file(s)

**Gemini CLI Session Output:** Complete test code file(s)

### Phase 3: Test Code Validation (Codex)

**Main Claude invokes Codex via `mcp__zen__codereview`:**

```
Tool: mcp__zen__codereview
Parameters:
- step: "Review the test code generated by gemini for quality, completeness, and adherence to testing standards.

        Focus Areas:
        - Test coverage adequacy
        - Assertion completeness
        - Edge case handling
        - Code quality (readability, maintainability)
        - Framework best practices
        - Mock/fixture usage
        - Error handling in tests"
- step_number: 1
- total_steps: 2-3
- next_step_required: true
- findings: ""
- relevant_files: [absolute paths to generated test files]
- review_type: "full"
- model: "codex"
- review_validation_type: "external"
- confidence: "exploring"
- files_checked: [test file paths]
```

**Codex Output:** Review findings with identified issues (if any)

### Phase 4: Test Code Correction (If Needed - Codex CLI)

**If Codex CLI Identifies Issues:**

**🚨 First: Read automation_mode from context**
```
IF [AUTOMATION_MODE: false] → Interactive Mode
IF [AUTOMATION_MODE: true] → Automated Mode
```

#### Interactive Mode (automation_mode=false, Default)

Main Claude presents findings to user:
```
Codex CLI 检查发现以下问题：

[严重] 测试文件A:行B - 缺少边界条件测试
[中等] 测试文件A:行C - 断言不够具体
...

是否批准 Codex CLI 自动修正这些问题？
- 是：继续修正
- 否：手动修改
```

After approval, codex CLI applies corrections (following codex-code-reviewer workflow).

#### Automated Mode (automation_mode=true)

Main Claude reviews issues and decides autonomously (based on automation_mode=true):

1. **Evaluate Issue Severity:**
   - Critical/High severity: Always fix
   - Medium severity: Fix if straightforward
   - Low severity: Fix if no risk

2. **Decision Logic (based on automation_mode=true from router):**
   ```
   IF issues are fixable AND low risk:
       → Auto-approve codex corrections
       → Log to auto_log.md: "测试代码问题已自动修正 (automation_mode=true)"
       → Record: issue list, fix decisions, severity levels, risk assessment
   ELSE IF issues are complex or high risk:
       → Escalate to user for decision
       → Log escalation reason to auto_log.md
   ```

3. **Present Decision to User (Information Only):**
   ```
   ✅ 测试代码问题已自动修正（自动化模式）
   [automation_mode=true 由 router 设置]

   修正的问题：
   - ✅ [严重] 已添加边界条件测试
   - ✅ [中等] 已完善断言说明
   - ✅ [低] 已优化测试命名

   决策依据：automation_mode=true，所有问题可安全修复
   已记录到 auto_log.md

   继续运行测试...
   ```

### Phase 5: Test Execution & Review (Main Claude + User)

**Main Claude's Responsibility:**

**🚨 First: Read automation_mode from context**
```
IF [AUTOMATION_MODE: false] → Interactive Mode
IF [AUTOMATION_MODE: true] → Automated Mode
```

1. **Execute Tests:**
   - Run the test suite using appropriate commands
   - Capture output and results
   - Analyze failures if any

#### Interactive Mode (automation_mode=false, Default)

2. **Present Results to User:**
   ```
   Gemini CLI 已完成测试代码编写，Codex CLI 已验证质量。

   测试文件：[file paths]
   覆盖率：[percentage]

   测试运行结果：

   ✅ 通过：X 个
   ❌ 失败：Y 个
   ⚠️  跳过：Z 个

   [详细结果]

   是否满意？需要调整吗？
   - ✅ 批准并保存
   - 🔄 需要调整
   - ❌ 重新生成
   ```

3. **Iterate if Needed:**
   - If tests fail due to test code issues: Provide feedback to gemini/codex for correction
   - If tests reveal bugs in source code: Handle separately (not this skill's responsibility)

#### Automated Mode (automation_mode=true)

2. **Main Claude Evaluates Test Results Autonomously (based on automation_mode=true):**
   - **Success Criteria:**
     - All tests pass (or only expected skips)
     - Coverage ≥ 70%
     - No critical failures

3. **Decision Logic (based on automation_mode=true from router):**
   ```
   IF all tests pass AND coverage >= 70%:
       → Auto-approve and save test files
       → Log to auto_log.md: "测试已自动完成并保存 (automation_mode=true)"
       → Record: test results, coverage metrics, decision reason
   ELSE IF some tests fail:
       → Analyze failure reasons
       → If fixable: Provide feedback to Gemini/Codex, retry (max 2 times)
       → Log retry attempts and reasons to auto_log.md
       → If source code bugs: Report to user, save tests anyway, log findings
       → If persistent test issues: Escalate to user, log escalation reason
   ```

4. **Present Final Result to User (Information Only):**
   ```
   ✅ 测试已自动完成（自动化模式）

   测试文件：[file paths]

   测试运行结果：
   - ✅ 通过：X 个 (100%)
   - 覆盖率：78%

   质量检查：
   - ✅ 所有测试通过
   - ✅ 覆盖率达标（≥ 70%）
   - ✅ 测试结构清晰
   - ✅ 断言完整

   测试文件已保存
   ```

## Collaboration Guidelines

### Main Claude's Role

- **Context Provider**: Gather all necessary context for gemini
- **User Interface**: Handle all user interactions and approvals
- **Executor**: Run tests, validate results
- **Quality Gate**: Final review before delivery
- **Feedback Loop**: Provide structured feedback to gemini/codex for iterations

### Gemini CLI Session's Role (in WSL)

- **Specialist Writer**: Focus purely on high-quality writing within the CLI session environment
- **Standard Adherent**: Strictly follow templates and standards provided in the prompt
- **Context Consumer**: Access and use files passed into the CLI session environment
- **Session-based Processing**: All writing work happens inside the WSL CLI session
- **Responsive**: Accept feedback and iterate within the same session via continuation_id
- **Independent Execution**: Operates independently in WSL, not relying on Main Claude's capabilities

### Codex's Role

- **Test Validator**: Ensure test code quality
- **Best Practice Enforcer**: Apply testing standards
- **Corrector**: Fix identified issues
- **Quality Reporter**: Provide clear findings to main Claude

## Document Type Standards

### CLAUDE.md Mandated Documents

For these documents, **strictly follow** templates in `references/doc_templates.md`:

1. **PROJECTWIKI.md**
   - Follow 项目知识库内容结构与生成规则统一模板
   - Include all 12 required sections
   - Use Mermaid diagrams
   - Ensure traceability links

2. **CHANGELOG.md**
   - Follow Keep a Changelog format
   - Semantic Versioning
   - Link to commits and PRs

3. **ADR (Architecture Decision Records)**
   - Use MADR template
   - Format: `YYYYMMDD-title.md`
   - Include context, alternatives, decision, consequences

4. **plan.md**
   - Detailed implementation plan
   - Checkable task list
   - Review section for summary

See `references/doc_templates.md` for complete templates.

### Other Documents

For general documentation:
- Follow project conventions
- Use clear structure
- Include examples where helpful
- Maintain consistency with existing docs

## Test Code Standards

Follow patterns from `references/test_patterns.md`:

1. **Test Organization:**
   - One test file per source file (convention: `test_<module>.py` or `<module>_test.py`)
   - Group related tests in classes
   - Clear, descriptive test names

2. **Coverage Requirements:**
   - Minimum 70% line coverage
   - Test all public APIs
   - Cover edge cases and error conditions

3. **Best Practices:**
   - AAA pattern (Arrange-Act-Assert)
   - Use fixtures for setup/teardown
   - Mock external dependencies
   - Avoid test interdependencies
   - Clear assertions with helpful messages

## Tool Parameters Reference

### mcp__zen__clink (Launch CLI Tools in WSL)

**Purpose:** Bridge tool to launch and interact with CLI tools (gemini, codex) in WSL environment.

**How It Works:**
1. clink launches the specified CLI tool as a command in WSL (e.g., `gemini` command)
2. Opens an interactive CLI session for that tool
3. Passes prompt and files into the CLI session environment
4. All processing happens inside the CLI tool's session
5. Returns the CLI session's output to Main Claude
6. Maintains session context via continuation_id for multi-turn conversations

**Key parameters for launching Gemini CLI:**
- `cli_name`: "gemini" (required - launches `gemini` command in WSL)
- `prompt`: The writing request with full context and requirements (required)
- `files`: List of relevant files for context - absolute paths (optional)
  - These files are accessible within the gemini CLI session
- `images`: List of image paths for visual context - absolute paths (optional)
- `role`: "default", "codereviewer", or "planner" (optional, default: "default")
  - Determines the gemini CLI's behavior/persona within the session
- `continuation_id`: Reuse to maintain the same gemini CLI session across multiple calls (optional)
  - Enables multi-turn conversations within the same CLI environment
  - Example: outline generation → full document writing uses same session

**Available Roles for Gemini CLI Session:**
- `default`: General-purpose writing within CLI
- `planner`: Planning and outlining tasks within CLI
- `codereviewer`: Code-related documentation within CLI

**Example Flow:**
```
Call 1 with continuation_id=None:
  → Launches: gemini command in WSL
  → Session: New gemini CLI session starts
  → Returns: Outline + continuation_id="abc123"

Call 2 with continuation_id="abc123":
  → Reconnects: To existing gemini CLI session "abc123"
  → Session: Same gemini CLI with previous context
  → Returns: Full document + same continuation_id
```

### mcp__zen__codereview (Codex CLI)

Key parameters for test validation:
- `model`: "codex"
- `review_type`: "full"
- `review_validation_type`: "external"
- `relevant_files`: Absolute paths to test files
- Follow codex-code-reviewer skill standards

## Error Handling

### If Gemini CLI Fails
- Main Claude: Notify user of the CLI invocation failure
- Offer to retry with adjusted parameters or write manually
- Check if continuation_id needs to be reset
- Provide more specific instructions and context
- Consider breaking down into smaller tasks

### If Codex Validation Fails
- Main Claude: Present issues to user
- Offer manual correction or codex automatic correction
- Maximum 3 correction iterations to prevent loops

### If User Rejects Output
- Gather specific feedback
- Provide detailed feedback to gemini CLI via new clink invocation
- Maintain continuation_id for context continuity
- Regenerate with improvements

## Resources

### references/doc_templates.md

Complete templates for CLAUDE.md mandated documents. Load when:
- Writing PROJECTWIKI.md, CHANGELOG.md, ADR, or plan.md
- User asks about document structure standards
- Need to verify format compliance

### references/test_patterns.md

Testing best practices and code patterns. Load when:
- Writing test code
- User asks about testing standards
- Need test structure examples

## Example Usage Scenarios

### Example 1: Writing ADR (Interactive Mode)

**User**: "使用gemini来编写文档，我需要记录数据库选择决策的ADR"

**Main Claude**:
```
好的,我来协调 Gemini CLI 为您编写 ADR 文档。

首先让我了解一些信息：
1. 数据库选择的背景是什么？
2. 考虑了哪些数据库选项？
3. 最终选择了哪个数据库？
4. 主要决策因素是什么？

[收集信息后...]

现在让 Gemini CLI 生成 ADR 大纲...
[调用 mcp__zen__clink with cli_name="gemini"]

Gemini CLI 生成的大纲如下：
[显示大纲]

是否批准？
```

**User**: "是"

**Main Claude**:
```
[调用 mcp__zen__clink 完整编写，使用 continuation_id]

Gemini CLI 已完成 ADR 编写：

文件：docs/adr/20251020-select-postgresql.md

[显示内容]

是否批准保存？
```

### Example 2: Writing Test Code (Interactive Mode)

**User**: "使用gemini来编写测试文件，测试 src/features.py"

**Main Claude**:
```
好的，让我先分析 src/features.py 的代码...

[读取代码]

发现需要测试的关键函数：
- create_features()
- validate_data()
- transform_features()

测试框架：pytest
目标覆盖率：≥ 70%

现在让 Gemini CLI 编写测试代码...
[调用 mcp__zen__clink with cli_name="gemini"]

测试代码已生成。现在让 Codex CLI 验证质量...
[调用 mcp__zen__codereview with model="codex"]

Codex CLI 检查结果：
✅ 测试覆盖完整
✅ 断言清晰
⚠️ 建议增加边界条件测试

是否批准 Codex CLI 自动补充边界条件测试？
```

**User**: "是"

**Main Claude**:
```
[Codex CLI 修正]

测试代码已完善。现在运行测试...
[执行测试]

测试结果：
✅ 所有测试通过
覆盖率：78%

测试文件已保存：tests/test_features.py
```

### Example 3: Writing ADR (Automated Mode)

**User**: "使用gemini来编写文档，记录数据库选择决策的ADR。自动化执行，不需要我确认"

**Router**: Sets `automation_mode=true` (detects "自动化执行，不需要我确认")

**Main Claude** (reads automation_mode=true from context):
```
[automation_mode=true] 检测到自动化模式，将自主审批并完成文档。

首先让我了解一些信息：
1. 数据库选择的背景是什么？
2. 考虑了哪些数据库选项？
3. 最终选择了哪个数据库？
4. 主要决策因素是什么？

[收集信息后...]

正在生成 ADR 大纲...
[调用 mcp__zen__clink with cli_name="gemini"]

✅ 大纲已自动审批（自动化模式）

大纲摘要：
1. 背景与问题陈述
2. 决策驱动因素
3. 考虑的方案（PostgreSQL, MongoDB, MySQL）
4. 决策结果
5. 实施计划
6. 验证方式

审批原因：
- ✅ 结构完整（符合 MADR 模板）
- ✅ 覆盖所有需求
- ✅ 符合标准

继续编写完整文档...
[调用 mcp__zen__clink with continuation_id]

✅ 文档已自动完成并保存（自动化模式）

文档类型：ADR
文件路径：docs/adr/20251020-select-postgresql.md

质量检查：
- ✅ 结构完整（所有 MADR 章节）
- ✅ 符合 CLAUDE.md 标准
- ✅ 格式正确
- ✅ 无失效链接

文档摘要：
- 决策：选择 PostgreSQL
- 理由：性能优秀、功能完整、团队有经验
- 影响：查询性能提升 3-5 倍，需 1-2 周迁移

已自动更新 CHANGELOG.md

ADR 编写完成！
```

### Example 4: Writing Test Code (Automated Mode)

**User**: "使用gemini来编写测试文件，测试 src/features.py，自动化完成"

**Router**: Sets `automation_mode=true` (detects "自动化完成")

**Main Claude** (reads automation_mode=true from context):
```
[automation_mode=true] 检测到自动化模式，将自主完成测试代码编写。

正在分析代码...
[读取代码]

发现需要测试的关键函数：
- create_features()
- validate_data()
- transform_features()

测试框架：pytest
目标覆盖率：≥ 70%

正在生成测试代码...
[调用 mcp__zen__clink with cli_name="gemini"]

正在进行质量验证...
[调用 mcp__zen__codereview with model="codex"]

Codex CLI 发现 3 个改进点：
- [中等] 建议增加边界条件测试
- [低] 优化测试命名
- [低] 增加注释说明

✅ 测试代码问题已自动修正（自动化模式）

修正的问题：
- ✅ [中等] 已添加边界条件测试（空列表、None、极值）
- ✅ [低] 已优化测试命名（更具描述性）
- ✅ [低] 已增加复杂逻辑的注释

正在运行测试...
[执行 pytest --cov=src tests/]

✅ 测试已自动完成（自动化模式）

测试文件：tests/test_features.py

测试运行结果：
- ✅ 通过：15 个 (100%)
- 覆盖率：82%

质量检查：
- ✅ 所有测试通过
- ✅ 覆盖率达标（≥ 70%）
- ✅ 测试结构清晰（AAA 模式）
- ✅ 断言完整（含错误消息）
- ✅ Mock 使用正确

详细结果：
- test_create_features_normal: ✅
- test_create_features_empty_input: ✅
- test_create_features_none_input: ✅
- test_validate_data_valid: ✅
- test_validate_data_invalid: ✅
- test_transform_features_basic: ✅
- ... (共 15 个测试)

测试文件已保存，测试代码编写完成！
```

## Notes

- **CLI Session Architecture**: zen-mcp clink launches actual CLI tools (`gemini` and `codex` commands) in WSL environment
- **Execution Location**: All writing operations happen inside the gemini CLI session in WSL, not in the main Claude model
- **Context Preservation**: continuation_id maintains the same CLI session across multiple calls, enabling multi-turn conversations within the CLI environment
- Gemini CLI session excels at understanding context and producing well-structured writing
- Main Claude acts as orchestrator and bridge, not the actual writer

**🚨 CRITICAL - automation_mode Management:**
- **Three-Layer Architecture**: This skill follows the global automation_mode architecture
  - **Router (Layer 1)**: Only main-router judges and sets `automation_mode` based on user's initial request
  - **Transmission (Layer 2)**: Router passes automation_mode to this skill via context
  - **Skill (Layer 3 - READ ONLY)**: This skill ONLY reads automation_mode, never judges or modifies it
- **Automated Mode (automation_mode=true)**: Main Claude autonomously reviews and approves based on objective quality criteria, significantly speeding up the workflow
  - **All decisions logged via output sections**: Every auto-approval is recorded in output (see auto_log mechanism below)
  - Triggered when router sets automation_mode=true (detects keywords like "自动化" / "全自动" / "不需要确认")
- **Interactive Mode (automation_mode=false, Default)**: User approval gates ensure quality and alignment, suitable for important or sensitive tasks
- **Mode Detection**: This skill MUST read automation_mode from context, NEVER ask user or check for keywords
- **Status Consistency**: All behavior must align with the automation_mode status set by router

**CRITICAL - auto_log.md Generation Mechanism:**
- This skill **DOES NOT** directly write to `auto_log.md` file
- In automation_mode=true, outputs decision records in structured format within the response text
- main-router collects all decision records at task completion and uses simple-gemini itself to generate unified `auto_log.md`
- File location: Project root directory `auto_log.md` (runtime audit log, not version controlled)
- Output format: Include decision type, rationale, confidence, and standards met in structured sections
- See `references/auto_log_template.md` for complete log structure and examples

- Codex CLI session (also in WSL) ensures test code meets engineering standards
- This workflow separates concerns:
  - **Context gathering**: Main Claude
  - **Writing**: Gemini CLI session in WSL
  - **Validation**: Codex CLI session in WSL
  - **Execution & Review**: Main Claude
  - **Mode management**: main-router (sets automation_mode)
- The clink tool provides seamless integration with external CLI tools while maintaining conversation context
- **WSL Integration**: All CLI tools run in WSL, ensuring compatibility with Linux-based tools and commands
