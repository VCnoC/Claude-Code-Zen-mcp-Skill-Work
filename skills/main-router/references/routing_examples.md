## Routing Examples

### Example 1: General Q&A Request

**User:** "解释一下什么是机器学习中的过拟合？"

**Router Decision:**
```
Intent: General Q&A
Keywords: "解释一下", "什么是"
Target: Conceptual explanation
Output: Answer/explanation (no file operations)

→ Route to: zen-chat

Rationale:
- Pure conceptual question
- No file/code operations required
- Fast response with zen-chat is sufficient
- No need for complex analysis workflow
```

---

### Example 2: Deep Problem Investigation

**User:** "深度分析一下为什么训练时loss不下降的问题"

**Router Decision:**
```
Intent: Deep problem investigation
Keywords: "深度分析", "问题"
Target: Complex debugging/troubleshooting
Output: Multi-stage investigation report

→ Route to: zen-thinkdeep

Rationale:
- Requires systematic investigation
- Multi-stage hypothesis testing needed
- zen-thinkdeep provides evidence-based analysis
- Not a simple Q&A, requires deep reasoning
```

---

### Example 3: Simple Document Generation

**User:** "生成项目的 README 文档"

**Router Decision:**
```
Intent: Document generation
Document Type: README (standard)
Depth: Standard

→ Route to: simple-gemini

Rationale:
- README is a standard document type
- No deep analysis required
- simple-gemini handles README templates
```

---

### Example 4: Code Quality Check

**User:** "使用codex对代码进行检查"

**Router Decision:**
```
Intent: Code review
Explicit mention: "codex"

→ Route to: codex-code-reviewer

Rationale:
- User explicitly requested codex
- Clear intent for code quality check
- codex-code-reviewer is the designated tool
```

---

### Example 5: Deep Technical Analysis Request

**User:** "深度分析 model_training.py 的训练逻辑，包括复杂度"

**Router Decision:**
```
Intent: Deep analysis
Keywords: "深度分析", "复杂度"
Target: Specific code file
Output: Technical analysis document

→ Route to: deep-gemini

Rationale:
- "深度分析" signals need for comprehensive analysis
- "复杂度" requires Big O analysis (deep-gemini feature)
- Not a standard doc, requires clink + docgen workflow
```

---

### Example 6: Planning Request

**User:** "帮我制定一个用户认证功能的开发计划"

**Router Decision:**
```
Intent: Planning
Keywords: "制定", "计划"
Scope: Feature development
Output: plan.md

→ Route to: plan-down

Rationale:
- Clear planning intent
- Requires task decomposition
- plan-down uses four-path workflow: Phase 0 (chat judges method clarity) → [Conditional Phase 1] → Phase 2 (planner) → Phase 3 (plan.md)
```

---

### Example 7: Ambiguous Request

**User:** "生成一份文档"

**Router Decision:**
```
Intent: Document generation
Ambiguity: What type of document?

→ Action: Ask User for Clarification

Question to User:
"您想生成哪种类型的文档？

1. 标准项目文档（README, PROJECTWIKI, CHANGELOG）→ simple-gemini
2. 深度技术分析文档（架构分析, 性能分析）→ deep-gemini
3. 开发计划文档（plan.md）→ plan-down

请选择或说明文档类型。"
```

---

### Example 8: Multi-Skill Sequential

**User:** "先制定计划，然后生成 README"

**Router Decision:**
```
Intent: Multi-task sequential
Task 1: Planning → plan-down
Task 2: Document generation → simple-gemini
Execution: Sequential (Task 1 must complete before Task 2)

→ Execution Plan:
1. Invoke plan-down
2. Wait for completion
3. Invoke simple-gemini
4. Return combined results
```

---

### Example 9: Full Automation Mode - Correct Behavior

**User:** "全程自动化，帮我完成这个项目的开发流程：分析现有代码，制定优化计划，生成文档，检查代码质量"

**Router Response (CORRECT - No Questions Asked):**
```
[全自动模式] 检测到用户请求"全程自动化"，启动全自动工作流。

Step 0: Standards Loading
- 读取 Global AGENTS.md: P1→P2→P3 workflow, G1 文档一等公民
- 读取 Global CLAUDE.md: 模型开发原则
- 读取 Project AGENTS.md: [项目特定规则]

Step 1: Intent Analysis
- 检测到多任务顺序工作流
- 任务序列: 分析 → 规划 → 文档 → 审查

Step 2: Auto-Routing Execution (NO USER CONFIRMATION)

[全自动模式 - 任务 1: 分析现有代码]
自动选择: zen-thinkdeep
置信度: 75%
理由: 需要深度分析，符合 P1 阶段要求
标准依据: AGENTS.md P1 - 分析问题
→ 立即执行 zen-thinkdeep...

[全自动模式 - 任务 2: 制定优化计划]
自动选择: plan-down
置信度: 90%
理由: 明确规划意图，符合 P2 阶段要求
标准依据: AGENTS.md P2 - 制定方案，G11 强制使用 plan-down
→ 立即执行 plan-down...

自动选择: simple-gemini
置信度: 65%
理由: 标准文档生成，ambiguous 时选择 simple over deep
标准依据: G1 - 文档一等公民
→ 立即执行 simple-gemini...

[全自动模式 - 任务 4: 检查代码质量]
自动选择: codex-code-reviewer
置信度: 95%
理由: 明确代码审查意图，符合 P3 阶段要求
标准依据: AGENTS.md P3 - 执行方案后需审查，G11 强制使用 codex
→ 立即执行 codex-code-reviewer...

[全自动模式 - 执行计划]
执行方式：顺序执行（Sequential）
1. zen-thinkdeep → 分析现有代码结构和问题
2. plan-down → 基于分析结果制定优化计划
3. simple-gemini → 生成 PROJECTWIKI.md 和 README.md
4. codex-code-reviewer → 全面代码质量审查

标准依据: AGENTS.md (P1→P2→P3), CLAUDE.md (质量原则)
平均置信度: 81.25%

⚠️ 注意：全程无需用户确认，自动执行所有步骤。

[全自动模式 - 任务完成]
所有任务执行完毕。
→ 生成决策日志 auto_log.md...
→ 使用 simple-gemini 记录完整决策过程
```

**Final Step - Auto Log Generation (MANDATORY):**
```
After all tasks complete in Full Automation Mode:

Tool: simple-gemini (or invoke directly via skill)
Task: Generate auto_log.md
Content Requirements:
  - 完整决策时间线（每个阶段的时间戳）
  - 所有自动决策的选择理由和标准依据
  - 调用的技能/工具列表及参数
  - 置信度评分和风险评估
  - 遇到的问题和解决方案
  - 最终结果和输出文件清单
  - 决策树可视化（Mermaid）

Template Structure for auto_log.md:
---
# 全自动化执行日志 (Auto Execution Log)
生成时间: {timestamp}

## 执行摘要 (Executive Summary)
- 用户初始请求: {original_request}
- 执行模式: 全自动化
- 总任务数: {task_count}
- 成功/失败: {success_count}/{failure_count}
- 总耗时: {duration}

## 决策时间线 (Decision Timeline)
{chronological list of all decisions}

## 技能调用记录 (Skills Invoked)
{list of all skills with parameters and results}

## 自动决策详情 (Auto-Decision Details)
{detailed rationale for each auto-decision}

## 遇到的问题 (Issues Encountered)
{any errors or blockers, and how they were resolved}

## 输出文件清单 (Output Files)
{list of all generated files}
---

Purpose: Provide complete transparency to user
```

**Anti-Pattern - WRONG Full Automation Behavior:**
```
❌ WRONG:
"由于当前是全自动化模式，我将自动进入 P2 阶段并调用 plan-down 生成详细方案。
 是否继续？（全自动模式下默认继续，如需调整技术栈请告知）"

Why Wrong:
- 询问"是否继续？" - 违反全自动化原则
- "如需调整技术栈请告知" - 不应提示用户干预
- 应该直接执行，而非询问

✅ CORRECT:
"[全自动模式] 检测到需要制定方案，自动进入 P2 阶段。
 调用 plan-down skill 生成详细方案...
 （决策依据：用户初始请求包含'全程自动化'，当前阶段 P1→P2，标准依据 G11）"
```

---

### Example 10: User Explicitly Mentions MCP Tools

**User:** "使用 serena 的 find_symbol 工具来分析代码结构，然后生成文档"

**Router Decision:**
```
Intent: Multi-task sequential with explicit MCP tool preference
User-Mentioned MCP: serena (specifically mcp__serena__find_symbol)
Task 1: Code structure analysis (using serena)
Task 2: Document generation

Step 0.2: MCP Assumptions
→ zen-mcp: Assumed AVAILABLE (default) ✅
→ serena: Assumed AVAILABLE (user explicitly mentioned) ✅
→ No pre-check needed for either

Step 1: Intent Analysis
→ User wants to use serena for code analysis
→ Then generate documentation based on analysis

Step 2: Routing Decision

Task 1: Code Analysis with serena
→ Tool: Main Claude with mcp__serena__find_symbol
Rationale: User explicitly requested serena tool
Strategy: Direct invocation, verify lazily at runtime

Task 2: Generate Documentation
→ Route to: simple-gemini (confidence: 70%)
Rationale: Standard documentation generation after analysis
Note: Can leverage serena findings from Task 1

→ Execution Plan (Sequential):
1. Main Claude invokes mcp__serena__find_symbol for code analysis
2. Collect structure findings
3. Invoke simple-gemini for documentation (can reference serena findings)
4. Return combined results

Error Handling:
If mcp__serena__find_symbol fails at runtime:
  → Notify user: "serena 工具当前不可用"
  → Fallback: Use zen-mcp code analysis tools or manual code reading
  → User choice: Continue with fallback OR troubleshoot serena MCP
```

---

### Example 11: Complete Task Lifecycle with Active Monitoring ⭐ BEST PRACTICE

**User:** "帮我开发一个用户登录功能"

**Router Active Monitoring Workflow:**

```
Phase 1: Planning
→ Router detects: User requests feature development
→ Action: MUST invoke plan-down (not Main Claude direct planning)
→ Tool: plan-down skill
→ Output: plan.md with multi-model validated task breakdown

Phase 2: Code Generation (Main Claude executes)
→ Router monitors: Main Claude generates login.py
→ Router detects: Code generation completed
→ Action: MUST invoke codex-code-reviewer for quality check
→ Tool: codex-code-reviewer
→ Output: Quality report + potential fixes

Phase 3: Test Code Generation
→ Router detects: Need test code for login.py
→ Action 1: MUST invoke simple-gemini to generate test_login.py
→ Action 2: MUST invoke codex-code-reviewer to validate test code
→ Tool: simple-gemini → codex-code-reviewer
→ Output: Validated test_login.py ready for Main Claude to execute

Phase 4: Documentation
→ Router detects: Need to update PROJECTWIKI.md
→ Action: MUST invoke simple-gemini for doc generation
→ Tool: simple-gemini
→ Output: Updated PROJECTWIKI.md with login feature docs

Phase 5: Final Validation
→ Router detects: All components completed
→ Action: MUST invoke codex-code-reviewer for final review
→ Tool: codex-code-reviewer
→ Output: Comprehensive quality report

Full Execution Log:
1. plan-down → plan.md generated ✅
2. Main Claude → login.py generated
3. codex-code-reviewer → login.py validated ✅
4. simple-gemini → test_login.py generated
5. codex-code-reviewer → test_login.py validated ✅
6. Main Claude → tests executed ✅
7. simple-gemini → PROJECTWIKI.md updated ✅
8. codex-code-reviewer → final validation ✅

Router's Active Role:
- Monitored entire lifecycle (5 phases)
- Invoked skills 6 times proactively
- Did NOT allow Main Claude to skip quality checks
- Ensured proper skill usage at each stage
```

**Key Takeaway:** Router actively monitors and intervenes, ensuring proper skill usage throughout the task lifecycle. **No lazy shortcuts allowed.**

---

### Example 12: Frontend Development Request ⭐ NEW - Frontend Detection

**User:** "帮我开发一个 React 组件,实现用户登录页面"

**Router Decision with Frontend Detection:**
```
Step 0: Standards Reading
- Read AGENTS.md/CLAUDE.md for phase requirements and rules

Step 1: Frontend Detection Scoring
Keywords detected:
- "React" → Tier 1: +35 points
- "组件" → Tier 1: +30 points
- "页面" → Tier 1: +25 points
- "登录" → Neutral (no points)

Context signals:
- No package.json found → +0 (no Tier 3 bonus)
- No backend signals detected → +0

Total frontend_score: 90 points ✅
Backend signal count: 0

Decision Threshold Analysis:
- Score ≥ 80 → Auto-route to gemini-frontend
- High confidence for frontend task

Step 2: Intent Analysis
→ Primary Intent: Frontend component development
→ Framework: React (explicitly mentioned)
→ Task: Implement login page UI
→ Expected Output: Working React component

Step 3: Routing Decision
→ Route to: gemini-frontend (Confidence: 90%)

Rationale:
- High frontend score (90 ≥ 80 threshold)
- React framework explicitly mentioned
- Component development matches gemini-frontend use cases
- Leverages Gemini 3.0's multimodal + long context capabilities

Step 4: Execution Plan (gemini-frontend Workflow)
Phase 1: Initialize Gemini CLI
  → Tool: mcp__zen__clink (cli_name="gemini")
  → Session established

Phase 2: Analyze Requirements
  → Parse user requirements: Login page with React
  → Identify components needed: Form, Input fields, Button, Validation
  → Check project context (if any existing code)

Phase 3: Generate Frontend Code
  → Generate LoginPage.jsx component
  → Include: useState for form state, validation logic, styling
  → Follow React best practices (hooks, functional components)

Phase 4: Dual Quality Checking
  Round 1: mcp__zen__codereview (workflow validation)
    → Check: Code quality, security (input validation), performance
    → Quality score: 88% ✅

  Round 2: mcp__zen__clink (cli_name="codex", deep analysis)
    → Deep analysis: React patterns, accessibility, edge cases
    → Final quality score: 92% ✅

Phase 5: Documentation Update
  → Tool: simple-gemini
  → Update: PROJECTWIKI.md with component documentation
  → Update: CHANGELOG.md with new feature entry

Fallback Strategy (if Gemini unavailable):
  → Notify user: "Gemini CLI 当前不可用"
  → Fallback option: codex-code-reviewer (general code generation)
  → User choice: Continue with fallback OR wait for Gemini

→ Final Output:
  - LoginPage.jsx (React component with validation)
  - Updated PROJECTWIKI.md (component API docs)
  - Updated CHANGELOG.md (feature entry)
  - Quality report (92% score, passed all checks)
```

**Key Takeaway:** Frontend detection scoring system accurately identifies React component development and routes to gemini-frontend for optimal code generation with multimodal capabilities.

---

### Example 13: Fullstack Project Detection ⭐ NEW - Task Decomposition

**User:** "开发一个用户管理系统，包括 React 前端和 FastAPI 后端"

**Router Decision with Fullstack Detection:**
```
Step 1: Frontend Detection Scoring
Keywords detected:
- "React" → Tier 1: +35 points
- "前端" → Tier 1: +30 points
- "FastAPI" → Backend signal: -20 points
- "后端" → Backend signal: -25 points

Total frontend_score: 45 points (after cancellation: 35 + 30 - 20 - 25)
Backend signal count: 2 ✅

Decision Threshold Analysis:
- Score = 45 < 50 → Below fuzzy zone
- Backend signals ≥ 2 → Fullstack detected

Step 2: Fullstack Handling
→ Detected: Fullstack project (frontend + backend)
→ Recommendation: Task decomposition approach

Step 3: User Notification
"检测到全栈项目开发需求，建议进行任务分解：

**前端部分** (React):
  → 推荐技能: gemini-frontend
  → 优势: Gemini 3.0 的长上下文和 multimodal 能力
  → 包含: 组件开发、UI实现、状态管理

**后端部分** (FastAPI):
  → 推荐技能: codex-code-reviewer (代码生成 + 质量检查)
  → 包含: API endpoints、数据模型、业务逻辑

是否接受此建议？
A) 是 - 分阶段执行（先前端后后端，或先后端后前端）
B) 否 - 使用通用开发流程
C) 自定义 - 告诉我您希望如何安排"

Step 4: User Choice Handling
IF user选择 A (分阶段执行):
  IF user选择 "先前端":
    1. Invoke gemini-frontend (React 部分)
    2. Wait for completion
    3. Invoke codex-code-reviewer (FastAPI 部分)
    4. Final integration and testing
  ELSE IF user选择 "先后端":
    1. Invoke Main Claude + codex-code-reviewer (FastAPI 部分)
    2. Wait for completion
    3. Invoke gemini-frontend (React 部分)
    4. Frontend-backend integration testing

ELSE IF user选择 B (通用流程):
  → Route to Main Claude (direct execution without specialized skills)

ELSE IF user选择 C (自定义):
  → Ask user to specify custom workflow
  → Adapt routing based on user's preference
```

**Key Takeaway:** Backend signal cancellation prevents false positives for fullstack projects, and task decomposition ensures each part uses the most suitable skill.

---

### Example 14: Code + Review Workflow

**User:** "生成测试文件然后检查代码质量"

**Router Decision:**
```
Intent: Multi-task sequential
Task 1: Generate tests → simple-gemini
Task 2: Code review → codex-code-reviewer
Execution: Sequential

→ Execution Plan:
1. Invoke simple-gemini (test code generation)
2. Wait for test files to be created
3. Invoke codex-code-reviewer (review all code including new tests)
4. Return results
```

## Best Practices

### For Effective Routing

1. **Active Monitoring (CRITICAL - Anti-Lazy Principle):**
   - Router MUST monitor task lifecycle continuously
   - Proactively invoke skills at appropriate stages
   - NEVER allow Main Claude to skip quality checks
   - Mandatory interventions:
     - plan.md generation → MUST use plan-down
     - Code generation complete → MUST use codex-code-reviewer
     - Test code needed → MUST use simple-gemini → codex validation
     - Documentation needed → MUST use simple-gemini/deep-gemini
   - Think: "What skill should be used at this stage?"

2. **Keyword Detection:**
   - Look for explicit skill/tool names (chat, thinkdeep, codex, gemini, planner)
   - Look for action verbs (解释, 调查, 检查, 生成, 分析, 规划)
   - Look for output types (答案, 调查报告, 文档, 计划, 测试)
   - Look for question patterns (什么是, 如何理解, 为什么)

3. **Context Awareness:**
   - Check git status for recently modified files
   - Check for existing artifacts (plan.md, PROJECTWIKI.md)
   - Consider user's recent interactions
   - Note project phase (planning, development, review)

4. **Confidence Thresholds:**
   - High confidence (≥80): Auto-route
   - Medium confidence (60-79): Auto-route with notification
   - Low confidence (<60): Ask user for clarification

5. **User Communication:**
   - Always inform user which skill was selected
   - Provide rationale for skill selection
   - Allow user to override router's decision

6. **Error Handling:**
   - If selected skill fails, offer fallback options
   - If no skill matches, execute directly with Main Claude
   - If user request is unclear, ask clarifying questions

### Router Communication Template

**Format:**
```
[决策通知]
检测到任务类型：[任务类型]
选择技能：[技能名称]
理由：[简短说明]

开始执行...
```

**Example:**
```
[决策通知]
检测到任务类型：代码质量审查
选择技能：codex-code-reviewer
理由：您请求检查代码质量，codex-code-reviewer 提供全面的 5 维度审查

开始执行...
```

## Routing Decision Matrix

| User Intent | Primary Keywords | Selected Tool/Skill | Rationale |
|-------------|-----------------|---------------------|-----------|
| **前端开发 (NEW)** | React, Vue, Angular, component, 组件, 页面, UI, 前端 | gemini-frontend | Frontend/mobile dev with multimodal + long context |
| **移动端开发 (NEW)** | React Native, Flutter, Swift, Kotlin, iOS, Android, 移动端 | gemini-frontend | Mobile app dev with specialized support |
| **设计转代码 (NEW)** | design-to-code, 设计稿, UI设计, Figma, 界面 | gemini-frontend | Multimodal design understanding |
| **全栈项目 (NEW)** | 前端+后端 keywords, fullstack, 全栈 | Task Decomposition | Frontend → gemini-frontend, Backend → others |
| 一般问答 | 解释, 什么是, 如何理解 | zen-chat | General Q&A, no file ops |
| 深度问题调查 | 深度分析问题, 调查bug, 系统性分析 | zen-thinkdeep | Multi-stage investigation |
| 代码审查 | 检查, 审查, codex | codex-code-reviewer | Code quality validation |
| 标准文档 | 文档, README, CHANGELOG, 测试 | simple-gemini | Standard doc templates |
| 深度技术分析 | 深度, 分析, 架构, 性能, 复杂度 | deep-gemini | Technical analysis + complexity |
| 规划制定 | 计划, plan, 规划, 分解 | plan-down | Task decomposition + validation |
| 文档生成（不明确） | 生成文档 | Ask User | Ambiguous - need clarification |

## Special Cases

### Case 1: No Matching Skill

**Scenario:** User request doesn't match any skill

**Action:**
```
Router Analysis:
- No skill confidence > 60%
- Request is outside skill scope

→ Decision: Execute directly with Main Claude
→ Notification: "此任务将由主模型直接处理（无需专用技能）"
```

---

### Case 2: Conflicting Skills

**Scenario:** Multiple skills have similar confidence scores

**Action:**
```
Router Analysis:
- simple-gemini: 75%
- deep-gemini: 73%
- Difference < 10% → Ambiguous

→ Decision: Ask user to choose
→ Present both options with pros/cons
```

---

### Case 3: Runtime MCP Tool Failure

**Scenario A:** zen-mcp tool fails during skill execution (discovered at runtime)

**Action:**
```
Skill Execution Error:
- Skill: deep-gemini
- Failed MCP call: mcp__zen__docgen
- Error: "MCP tool not available" or "Connection failed"

Router Receives Error and Responds:

→ Notification to User:
  "在执行 deep-gemini 时遇到问题：
   mcp__zen__docgen 当前不可用。

   可选方案：
   1. 使用 simple-gemini（仅需 mcp__zen__clink）
   2. 主模型直接生成文档（无 MCP 增强）
   3. 检查 zen-mcp 服务状态后重试

   请选择（或输入 3 后使用 /mcp status 检查）"

User Choice Handling:
- Choice 1 → Route to simple-gemini
- Choice 2 → Main Claude direct execution
- Choice 3 → Wait for user to troubleshoot, then retry

Note: This only happens when zen-mcp actually fails at runtime,
      not during routing phase (optimistic assumption).
```

**Scenario B:** User-mentioned MCP tool fails at runtime

**Action:**
```
Direct MCP Invocation Error:
- User request: "使用 serena 的 find_symbol 分析代码"
- Failed MCP call: mcp__serena__find_symbol
- Error: "MCP server 'serena' not found" or "Tool not available"

Router Receives Error and Responds:

→ Notification to User:
  "您指定的 MCP 工具当前不可用：
   mcp__serena__find_symbol

   错误信息：{error_details}

   可选方案：
   1. 使用 zen-mcp 的代码分析工具（mcp__zen__thinkdeep）
   2. 主模型直接读取代码进行分析
   3. 检查 serena MCP 服务状态后重试（/mcp status）

   请选择处理方式："

User Choice Handling:
- Choice 1 → Route to zen-thinkdeep (alternative analysis)
- Choice 2 → Main Claude manual code reading
- Choice 3 → Wait for user to troubleshoot, then retry original request

Note: User-mentioned MCP tools are assumed available (optimistic),
      but must provide clear error feedback if they fail at runtime.
```

---

### Case 4: User Override

**Scenario:** User explicitly requests a different skill

**User:** "不用 codex，用 gemini 来分析"

**Action:**
```
Router Analysis:
- Original selection: codex-code-reviewer
- User override: Use gemini (deep-gemini)

→ Decision: Respect user choice
→ Route to: deep-gemini
→ Notification: "已切换到 deep-gemini（根据您的要求）"
```

## Notes

### Core Principles

- **Active Task Monitoring (HIGHEST PRIORITY - Anti-Lazy Principle)**:
  - Router MUST continuously monitor task lifecycle
  - Proactively invoke skills at critical stages
  - Mandatory skill usage rules (NEVER skip):
    - plan.md → **plan-down** (MANDATORY)
    - Code complete → **codex-code-reviewer** (MANDATORY)
    - Test code → **simple-gemini** + **codex** validation (MANDATORY)
    - Documentation → **simple-gemini** or **deep-gemini** (MANDATORY)
  - Think at each stage: "Should I invoke a skill here?"
  - **Being lazy is FORBIDDEN** - always use proper skills

- **Standards-First Approach**: ALWAYS read AGENTS.md/CLAUDE.md before routing decisions
  - Global AGENTS.md: `/home/vc/.claude/AGENTS.md`
  - Global CLAUDE.md: `/home/vc/.claude/CLAUDE.md`
  - Project AGENTS.md: `./AGENTS.md` (if exists)
  - Project CLAUDE.md: `./CLAUDE.md` (if exists)

- **MCP-Aware Routing**: Optimistic assumption with lazy verification
  - **zen-mcp assumed available by default** - No pre-check required
  - **User-mentioned MCP tools assumed available** - Honor user's explicit tool choice
  - Route to skills immediately without MCP verification
  - Verify MCP availability lazily (on actual tool invocation)
  - Only communicate with user if MCP tools fail at runtime
  - Optional: Discover serena/unifuncs MCPs on-demand for enhancements
  - Provide fallback options when MCP tools actually fail

- **Proactive Usage**: Main Router should be invoked for ALL task-related user requests

- **Standards Compliance**: All routing decisions must align with documented rules
  - Respect phase requirements (P1→P2→P3)
  - Follow global rules (G1-G8)
  - Apply project-specific overrides when applicable

### Operation Modes

- **Interactive Mode (Default)**:
  - Ask user for clarification when ambiguous
  - Confidence threshold: ≥60%
  - User makes final decisions
  - Provide recommendations with rationale

- **Full Automation Mode**:
  - **Activation**: Keywords in user's initial request: "全程自动化", "full automation", "自动化流程"
  - **Behavior**: Router and Main Claude make ALL decisions autonomously
  - **CRITICAL - DO NOT ask user**:
    - ❌ "是否继续？"
    - ❌ "请选择..."
    - ❌ "是否需要..."
    - ✅ Direct execution with logged rationale
  - **Decision Rules**:
    - Lower confidence threshold: ≥50%
    - Auto-select best option (no user choice)
    - Log all auto-decisions with rationale
    - Standards-based decision making (no guessing)
  - **Exception**: Only ask when blocking errors or security risks occur
  - **Mandatory Final Step**: After all tasks complete, generate `auto_log.md` using simple-gemini
    - Purpose: Complete transparency and audit trail
    - Content: Decision timeline, skills invoked, rationale, results
    - Format: Structured Markdown with timestamps and decision tree
  - Prefer simpler skills when ambiguous

### Best Practices

- **Transparency**: Always inform user which skill/tool was selected and why
  - Focus on intent match and standards alignment in routing notification
  - Honor user's explicit MCP tool choice (e.g., "使用 serena") without pre-checking
  - Only mention MCP status if there's a runtime failure
  - Acknowledge when routing based on user's explicit MCP preference

- **Flexibility**: Support user overrides and manual skill selection
  - Allow user to choose alternative skills if zen-mcp fails at runtime
  - Respect user's explicit skill preference

- **Efficiency**: Prefer simpler skills when ambiguous
  - simple-gemini over deep-gemini (unless "深度" mentioned)
  - zen-chat over zen-thinkdeep (unless "调查" or "bug" mentioned)
  - Direct execution over complex skills when unclear

- **Context-Aware**: Consider project state, recent activity, git status, and AGENTS.md phase
  - Leverage serena memory tools for project context (if discovered)
  - Use git status to inform routing decisions

- **Multi-Skill Support**: Handle sequential and parallel skill execution
  - Route to multiple skills when user requests multi-task workflows
  - Execute skills independently or sequentially as needed

- **Fallback Strategy**: Graceful degradation on runtime failures
  - zen-mcp fails → Notify user and suggest alternative skill or Main Claude
  - Provide actionable troubleshooting steps (e.g., "/mcp status")
  - Allow user to retry after troubleshooting

- **Continuous Improvement**: Learn from user corrections and overrides
  - Track skill selection patterns for future optimization
  - Log runtime MCP failures for debugging

- **No Redundancy**: Don't invoke router for meta-requests about the router itself

## Router Self-Awareness

**The router should NOT route these requests:**
- "What skills are available?" → Direct answer
- "How does routing work?" → Direct answer
- "Explain the router" → Direct answer
- General questions about Claude Code or skills → Direct answer

**The router SHOULD route these requests:**
- General Q&A and explanations → zen-chat
- Deep problem investigation → zen-thinkdeep
- Any task-specific request (code review, docs, planning, analysis)
- Requests with explicit skill/tool names
- Requests with clear intent (review, generate, analyze, plan, explain, investigate)
