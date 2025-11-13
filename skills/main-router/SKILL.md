---
name: main-router
description: Intelligent skill router that analyzes user requests and automatically dispatches to the most appropriate skill(s) or zen-mcp tools. Routes to zen-chat for Q&A, zen-thinkdeep for deep problem investigation, codex-code-reviewer for code quality, simple-gemini for standard docs/tests, deep-gemini for deep analysis, or plan-down for planning. Use this skill proactively to interpret all user requests and determine the optimal execution path.
---

# Main Router - 智能技能路由调度器

## Overview

This skill serves as the **central intelligence hub** that analyzes user requests and automatically routes them to the most appropriate skill(s) for execution. It acts as a smart dispatcher, understanding user intent and orchestrating the right tools for the job.

**Core Capabilities:**
- Standards-based routing (follows CLAUDE.md)
- Intent analysis and classification
- Skill matching and selection
- Multi-skill orchestration (sequential or parallel)
- Conflict resolution and disambiguation
- Automatic routing without user intervention
- Full automation mode support (router makes decisions autonomously)

**Division of Responsibilities:**
- **Main Router**: Analyzes request → Reads standards → Determines skill(s) → Invokes skill(s) → Coordinates execution
- **Specialized Skills**: Execute their specific tasks when invoked by router

**Standards Compliance:**
- **MUST read** global and project CLAUDE.md before routing
- Apply standards hierarchy: Global CLAUDE.md > Project CLAUDE.md
- All routing decisions must align with documented rules and workflows

**Active Task Monitoring (CRITICAL - Router Must Not Be Lazy):**

Main Router MUST actively monitor the entire task lifecycle and proactively invoke appropriate skills at each stage. **Do NOT skip skill invocations to save time** - proper skill usage ensures quality and compliance.

**Mandatory Workflow Rules:**

1. **Planning Phase:**
   - When user requests "制定计划" / "生成 plan.md" / "规划任务"
   - **MUST use plan-down skill** (not Main Claude direct planning)
   - Rationale: plan-down provides multi-model validation and structured decomposition

2. **Code Generation → Quality Check Cycle:**
   - After Main Claude completes ANY code generation/modification
   - **MUST invoke codex-code-reviewer** to validate quality
   - Rationale: Ensures 5-dimension quality check (quality, security, performance, architecture, docs)

3. **Test Code Generation Workflow:**
   - When Main Claude needs test code
   - Step 1: **MUST invoke simple-gemini** to generate test files
   - Step 2: **MUST invoke codex-code-reviewer** to validate generated tests
   - Step 3: Return validated tests to Main Claude for execution
   - Rationale: Ensures test quality before execution

4. **Documentation Generation:**
   - Standard docs (README, PROJECTWIKI, CHANGELOG) → **simple-gemini**
   - Deep analysis docs (architecture, performance) → **deep-gemini**
   - Rationale: Specialized skills produce higher quality, standards-compliant docs

5. **Continuous Monitoring:**
   - Router monitors task progress throughout execution
   - Proactively suggests skill invocations when opportunities arise
   - Example: "刚完成代码,是否需要我使用 codex 检查质量?"

**Anti-Pattern - Router Being Lazy (FORBIDDEN):**
```
❌ BAD: Main Claude generates code → Main Claude self-reviews → Done
✅ GOOD: Main Claude generates code → Router invokes codex-code-reviewer → Done

❌ BAD: Main Claude writes plan.md directly
✅ GOOD: Router invokes plan-down skill → plan.md generated with validation

❌ BAD: Main Claude generates tests → Run immediately
✅ GOOD: Router invokes simple-gemini → codex validates → Main Claude runs
```

## When to Use This Skill

**Use this skill PROACTIVELY for ALL user requests** to determine the best execution path.

**Typical User Requests:**
- "解释一下什么是..." (→ zen-chat)
- "深度分析问题..." (→ zen-thinkdeep)
- "帮我检查代码" (→ codex-code-reviewer)
- "生成 README 文档" (→ simple-gemini)
- "深度分析这段代码的性能" (→ deep-gemini)
- "制定开发计划" (→ plan-down)
- "写测试文件" (→ simple-gemini)
- "生成架构分析文档" (→ deep-gemini)
- Any task-related request or Q&A

**Router's Decision Process:**
```
User Request → Read Standards (CLAUDE.md) → Intent Analysis → Skill Matching → Auto/Manual Decision → Execution
```

**Operation Modes:**

1. **Interactive Mode (Default):**
   - Router asks user for clarification when ambiguous
   - User makes final decisions on skill selection
   - Router provides recommendations with rationale

2. **Full Automation Mode (Three-Layer Architecture - Router as Global Truth Source):**

   **🚨 CRITICAL - Router's Exclusive Role:**
   - **ONLY main-router** detects automation triggers in user's initial request
   - **ONLY main-router** sets `automation_mode = true/false` status
   - **Main-router MUST pass automation_mode** to all downstream skills via context
   - **Context Format**: `[AUTOMATION_MODE: true]` or `[AUTOMATION_MODE: false]`
   - **Downstream skills**: READ ONLY - never detect or modify automation_mode themselves

   **Automation Trigger Keywords:**
   - "全程自动化" / "full automation" / "自动化流程" / "全自动" / "自动化模式"

   **Behavior in Automation Mode:**
   - Router and Main Claude make all decisions autonomously
   - **DO NOT ask user for confirmation** ("是否继续？" is FORBIDDEN)
   - **DO NOT present choices** - auto-select best option based on confidence + standards
   - **Log all decisions to auto_log.md** with reason, confidence, standards
   - Only ask user in exceptional cases (blocking errors, security risks, data safety)

   **Decision Logging Template:**
   ```
   [自动决策记录]
   决策：[what was decided]
   理由：[why this decision was made]
   置信度：[low/medium/high/very_high]
   标准依据：[CLAUDE.md G1, P2要求, etc.]
   已记录到 auto_log.md
   ```

## Available Skills Registry

### 0. zen-chat (Direct Tool)
**Purpose:** General Q&A and collaborative thinking partner

**Triggers:**
- "解释一下..."
- "什么是..."
- "如何理解..."
- "帮我分析一下..." (non-technical deep analysis)
- General questions, brainstorming, explanations

**Use Cases:**
- Answer conceptual questions
- Explain programming concepts
- Brainstorming ideas
- Quick clarifications
- Thoughtful explanations

**Key Features:**
- Fast, direct responses
- No file operations needed
- Conversation-based
- Supports multi-turn discussions

**Tool:** `mcp__zen__chat` (direct invocation, not a packaged skill)

---

### 0.5. zen-thinkdeep (Direct Tool)
**Purpose:** Multi-stage investigation and reasoning for complex problem analysis

**Triggers:**
- "深度分析问题..."
- "调查这个bug的根因..."
- "系统性分析..." (technical deep dive)
- "复杂问题分析..."
- Architecture decisions, complex bugs, performance challenges

**Use Cases:**
- Complex bug investigation
- Architecture decision analysis
- Performance bottleneck deep dive
- Security analysis
- Systematic hypothesis testing

**Key Features:**
- Multi-stage investigation workflow
- Hypothesis-driven analysis
- Evidence-based findings
- Expert validation
- Comprehensive problem-solving

**Tool:** `mcp__zen__thinkdeep` (direct invocation, not a packaged skill)

---

### 1. codex-code-reviewer
**Purpose:** Code quality review with iterative fix-and-recheck cycles

**Triggers:**
- "使用codex对代码进行检查"
- "检查刚刚生成的代码是否存在问题"
- "每次生成完一次代码就要进行检查"
- "代码审查"
- "代码质量检查"

**Use Cases:**
- Post-development code quality validation
- Pre-commit code review
- Bug fix verification
- Refactoring quality assurance

**Key Features:**
- 5-dimension quality check (quality, security, performance, architecture, documentation)
- Iterative fix cycles (max 5 iterations)
- User approval required before fixes
- Based on CLAUDE.md standards

**Tool:** `mcp__zen__codereview`

---

### 2. simple-gemini
**Purpose:** Standard documentation and test code generation

**Triggers:**
- "使用gemini来编写测试文件"
- "使用gemini来编写文档"
- "生成README"
- "生成PROJECTWIKI"
- "生成CHANGELOG"
- "写测试代码"

**Use Cases:**
- Generate standard project documentation (PROJECTWIKI, README, CHANGELOG, ADR)
- Write test code files
- Create project templates
- Standard documentation maintenance

**Key Features:**
- Two modes: Interactive (default) and Automated
- Document types: PROJECTWIKI, README, CHANGELOG, ADR, plan.md
- Test code generation with codex validation
- Follows CLAUDE.md standards

**Tool:** `mcp__zen__clink` (launches gemini CLI in WSL)

---

### 3. deep-gemini
**Purpose:** Deep technical analysis documents with complexity evaluation

**Triggers:**
- "使用gemini深度分析代码逻辑"
- "生成架构分析文档"
- "分析性能瓶颈并生成报告"
- "深度理解这段代码并生成文档"
- "生成模型架构分析"

**Use Cases:**
- Code logic deep dive
- Model architecture analysis
- Performance bottleneck analysis
- Technical debt assessment
- Security analysis report

**Key Features:**
- Two-stage workflow: clink (Gemini CLI analysis) → docgen (dual-phase document generation)
- **Big O complexity analysis included** (docgen 核心能力)
- Automatic Mermaid diagram generation
- Evidence-based findings
- Professional technical writing

**Tools:** `mcp__zen__clink` + `mcp__zen__docgen`

**docgen 工作流程:**
- Step 1: Exploration (探查项目结构，制定文档计划)
- Step 2+: Per-File Documentation (生成结构化文档，包含复杂度分析)

---

### 4. plan-down ⭐ MANDATORY for Planning
**Purpose:** Intelligent planning with task decomposition and multi-model validation

**CRITICAL: This skill is MANDATORY for all plan.md generation tasks**
- Main Claude must NOT generate plan.md directly
- Router MUST invoke plan-down for all planning requests
- Rationale: Ensures multi-model validation and structured decomposition

**Triggers:**
- "帮我制定计划"
- "生成 plan.md"
- "使用 planner 进行任务规划"
- "帮我做任务分解"
- "制定实施方案"
- "规划项目"

**Use Cases:**
- Feature development planning
- Project implementation roadmaps
- Refactoring strategies
- Migration plans
- Complex task breakdown

**Key Features:**
- Two-stage workflow: planner (decomposition) → consensus (validation)
- Multi-model evaluation (codex, gemini, gpt-5)
- Standards-based planning (CLAUDE.md)
- Mermaid dependency graphs
- Risk assessment tables

**Tools:** `mcp__zen__chat` (Phase 0 method clarity judgment) + `mcp__zen__planner` + `mcp__zen__consensus` (conditional - only for Automatic + Unclear path) + `mcp__zen__clink` (when using consensus with codex/gemini)

**Model Support (CRITICAL - Follow G10 Rules):**
- **For codex/gemini models in consensus**: MUST launch CLI via `mcp__zen__clink` BEFORE calling consensus
  - Step 1: Use `mcp__zen__clink` to start codex/gemini CLI session
  - Step 2: Use `mcp__zen__consensus` which will use the established CLI session
  - Rationale: codex/gemini require CLI session, direct API calls will fail (401 error)
- **For other models** (gpt-5-pro, claude, etc.): Direct API access via consensus
- **Best Practice**: If using mixed models (codex + gpt-5-pro), start CLI first for safety

**Enforcement:**
```
IF user requests planning OR plan.md generation:
    MUST route to plan-down
    NEVER allow Main Claude to create plan.md directly

Reason: plan-down provides superior planning quality through:
- Multi-stage interactive planning
- Multi-model consensus validation
- Standards compliance verification
- Risk assessment and dependency analysis
```

## Routing Decision Logic

### Phase 0: Standards Reading & MCP Discovery (CRITICAL - First Step)

**Main Router's Action:**

Before ANY routing decision, **MUST complete** the following two sub-phases:

#### Phase 0.1: Read Standards

Read the following files to understand project-specific rules and workflows:

**a) Read Global Standards:**
- **Global CLAUDE.md**: `/home/vc/.claude/CLAUDE.md`
  - Extract: Global rules (G1-G11), phase requirements (P1-P4), routing mechanism, core principles
  - Key focus: Which phase user is in, execution permissions, documentation requirements
  - Extract: Model development workflow, ethics principles, reproducibility requirements

**b) Read Project-Specific Standards (if exist):**
- **Project CLAUDE.md**: `./CLAUDE.md` (current directory)
  - Extract: Project-specific rules, custom workflows, overrides

**Standards Priority Hierarchy (when conflicts):**
1. Global CLAUDE.md (highest priority)
2. Project CLAUDE.md (overrides global)
3. PROJECTWIKI.md (lowest priority)

#### Phase 0.2: MCP Capability Reference (Optional Discovery)

**Default MCP Assumptions:**

**zen-mcp is assumed AVAILABLE by default** - No pre-check required.
- All zen-mcp tools are treated as available unless proven otherwise during execution
- Verification happens lazily when skills actually invoke zen-mcp tools
- Only communicate with user if tools fail at runtime

**User-Mentioned MCP Tools are assumed AVAILABLE** - No pre-check required.
- If user explicitly mentions using specific MCP tools (e.g., "使用 serena 来分析代码", "用 unifuncs 搜索"), those tools are assumed available
- Router will route optimistically based on user's explicit MCP tool preference
- Verification happens lazily when those tools are actually invoked
- Only notify user if the explicitly mentioned tools fail at runtime

**Optional MCP Discovery (for non-zen MCPs):**

Optionally use `ListMcpResourcesTool` to discover additional MCP servers:
- serena (Serena Code Intelligence) - if available, provides code intelligence enhancements
- unifuncs (Utility Functions) - if available, provides web search/reading
- Other MCP servers - discovered on-demand

**MCP Capability Reference Map:**

Built-in knowledge of MCP tools available for skill enhancement:

**zen-mcp tools:**
- `mcp__zen__chat` - General Q&A, collaborative thinking
- `mcp__zen__thinkdeep` - Multi-stage investigation, hypothesis testing
- `mcp__zen__codereview` - Code quality review (used by codex-code-reviewer)
- `mcp__zen__planner` - Interactive sequential planning (used by plan-down)
- `mcp__zen__consensus` - Multi-model consensus building (used by plan-down)
- `mcp__zen__clink` - Launch CLI tools in WSL (used by simple-gemini, deep-gemini)
- `mcp__zen__docgen` - Structured document generation (used by deep-gemini)
- `mcp__zen__precommit` - Git changes validation (optional enhancement)
- `mcp__zen__debug` - Systematic debugging (optional enhancement)
- `mcp__zen__challenge` - Critical thinking tool (optional enhancement)
- `mcp__zen__apilookup` - API documentation lookup (optional enhancement)
- `mcp__zen__listmodels` - Available AI models query (used by all skills)
- `mcp__zen__version` - Server version and config (diagnostic)

**serena-mcp tools (Code Intelligence):**
- `mcp__serena__list_dir` - List directory contents (non-gitignored)
- `mcp__serena__find_file` - Find files by pattern
- `mcp__serena__search_for_pattern` - Flexible pattern search in codebase
- `mcp__serena__get_symbols_overview` - High-level code structure overview
- `mcp__serena__find_symbol` - Locate code symbols (classes, methods, etc.)
- `mcp__serena__find_referencing_symbols` - Find references to symbols
- `mcp__serena__replace_symbol_body` - Edit symbol definitions
- `mcp__serena__insert_after_symbol` - Insert code after symbols
- `mcp__serena__insert_before_symbol` - Insert code before symbols
- `mcp__serena__write_memory` - Store project knowledge
- `mcp__serena__read_memory` - Retrieve project knowledge
- `mcp__serena__list_memories` - List available memories
- `mcp__serena__delete_memory` - Remove memory files
- `mcp__serena__activate_project` - Switch between projects
- `mcp__serena__get_current_config` - Get agent configuration
- `mcp__serena__check_onboarding_performed` - Check project onboarding status
- `mcp__serena__onboarding` - Project onboarding workflow
- `mcp__serena__think_about_collected_information` - Reflect on gathered info
- `mcp__serena__think_about_task_adherence` - Verify task alignment
- `mcp__serena__think_about_whether_you_are_done` - Completion check

**unifuncs-mcp tools (Utility Functions):**
- `mcp__unifuncs__web-search` - Web search capability
- `mcp__unifuncs__web-reader` - Read web page content

**MCP-Skill Capability Matrix:**

| Skill | Required MCP Tools | Optional Enhancement Tools | Special Requirements |
|-------|-------------------|---------------------------|---------------------|
| zen-chat | mcp__zen__chat | mcp__zen__apilookup, mcp__unifuncs__web-search | - |
| zen-thinkdeep | mcp__zen__thinkdeep | mcp__serena__* (code analysis), mcp__zen__debug | - |
| codex-code-reviewer | mcp__zen__codereview | mcp__serena__* (symbol editing), mcp__zen__precommit | - |
| simple-gemini | mcp__zen__clink | mcp__serena__* (code reading), mcp__unifuncs__web-reader | - |
| deep-gemini | mcp__zen__clink, mcp__zen__docgen | mcp__serena__* (code analysis), mcp__zen__apilookup | - |
| plan-down | mcp__zen__chat, mcp__zen__planner, mcp__zen__consensus (conditional), mcp__zen__clink (for codex/gemini) | mcp__serena__read_memory (project context) | **G10 Compliance**: codex/gemini require clink to establish CLI session before consensus. Four-path workflow: Phase 0 uses chat to judge method clarity, then routes to appropriate path. |

**MCP Availability Strategy:**

**Optimistic Routing (Default):**
- **Assume zen-mcp tools are available** - Route to skills without pre-checking
- Skills will attempt to use zen-mcp tools directly
- Only intervene if tool invocation fails at runtime

**Lazy Verification (On-Demand):**
- Verification happens when skills actually invoke MCP tools
- If tool fails → Skill reports error back to router
- Router then communicates with user and suggests fallback

**Optional Enhancement Discovery:**
- serena/unifuncs MCPs can be discovered on-demand using `ListMcpResourcesTool`
- If discovered → Pass as enhancement options to skills
- If not discovered → Skills proceed with zen-mcp only (no user notification)

**Standards-Based Routing Rules:**
- If user is in **P1 (分析问题)** phase → May route to zen-thinkdeep for deep analysis
- If user is in **P2 (制定方案)** phase → May route to plan-down for planning
- If user is in **P3 (执行方案)** phase → May route to codex-code-reviewer after code changes
- If user mentions **"全程自动化"** → Enable Full Automation Mode
- If standards require documentation → Auto-route to simple-gemini or deep-gemini
- If standards forbid execution (G3 violation) → Do NOT route to execution-related skills

### Phase 1: Intent Classification

**Main Router's Action:**

Analyze the user request to identify:

1. **Primary Intent:**
   - General Q&A / explanations → **zen-chat**
   - Complex problem investigation → **zen-thinkdeep**
   - Code review / quality check → **codex-code-reviewer**
   - Standard documentation → **simple-gemini**
   - Deep technical analysis → **deep-gemini**
   - Planning / task breakdown → **plan-down**
   - Other (direct execution by Main Claude)

2. **Request Characteristics:**
   - **Target:** What is the subject? (code files, documentation, architecture, plan)
   - **Action:** What needs to be done? (check, generate, analyze, plan)
   - **Depth:** Surface-level or deep analysis?
   - **Output:** What is expected? (report, document, plan, fixed code)

3. **Context Signals:**
   - Keywords in user message
   - Recently modified files (git status)
   - Existing project state (has plan.md? has PROJECTWIKI.md?)
   - User's workflow stage (development, review, planning)

### Phase 2: Skill Matching

**Decision Tree:**

```
IF user asks general question ("解释", "什么是", "如何理解"):
    → zen-chat

ELSE IF user requests deep problem analysis ("深度分析问题", "调查bug", "系统性分析"):
    → zen-thinkdeep

ELSE IF user mentions "codex" OR "代码检查" OR "代码审查":
    → codex-code-reviewer

ELSE IF user mentions "gemini" AND ("文档" OR "测试"):
    IF mentions "深度" OR "分析" OR "架构" OR "性能":
        → deep-gemini
    ELSE:
        → simple-gemini

ELSE IF user mentions "计划" OR "plan" OR "规划":
    → plan-down

ELSE IF intent is "code review":
    → codex-code-reviewer

ELSE IF intent is "document generation":
    IF document type in [README, PROJECTWIKI, CHANGELOG, 测试]:
        → simple-gemini
    ELSE IF analysis type in [架构, 性能, 代码逻辑]:
        → deep-gemini

ELSE IF intent is "planning":
    → plan-down

ELSE IF intent is "Q&A" (no code/file operations):
    → zen-chat

ELSE:
    → Main Claude (direct execution, no skill routing)
```

**Confidence Scoring:**

For each tool/skill, calculate confidence score (0-100):

```python
confidence_scores = {
    "zen-chat": calculate_qa_confidence(request),
    "zen-thinkdeep": calculate_deep_investigation_confidence(request),
    "codex-code-reviewer": calculate_code_review_confidence(request),
    "simple-gemini": calculate_simple_doc_confidence(request),
    "deep-gemini": calculate_deep_analysis_confidence(request),
    "plan-down": calculate_planning_confidence(request)
}

# Interactive Mode (Default)
if max(confidence_scores.values()) >= 60:
    selected_tool = max(confidence_scores, key=confidence_scores.get)
else:
    # Ambiguous - ask user for clarification
    ask_user_to_clarify()

# Full Automation Mode (if user requested)
if automation_mode_enabled:
    if max(confidence_scores.values()) >= 50:  # Lower threshold
        selected_tool = max(confidence_scores, key=confidence_scores.get)
        log_auto_decision(selected_tool, confidence_scores)
    else:
        # Fallback to Main Claude
        selected_tool = "main_claude"
```

### Phase 3: Execution Strategy

**Single Skill Execution:**
```
User Request → Analyze → Match to Skill X → Invoke Skill X → Return Result
```

**Multi-Skill Execution (Sequential):**
```
Example: "生成文档然后检查代码"
1. Invoke simple-gemini (generate docs)
2. Wait for completion
3. Invoke codex-code-reviewer (check code)
4. Return combined results
```

**Multi-Skill Execution (Parallel - if independent):**
```
Example: "同时生成计划和README"
1. Invoke plan-down in parallel
2. Invoke simple-gemini in parallel
3. Wait for both to complete
4. Return combined results
```

### Phase 4: Disambiguation

**When multiple skills could apply:**

**Option 1: Ask User (Interactive Mode)**
```
检测到您的请求可以使用以下技能：

1. simple-gemini - 生成标准文档
2. deep-gemini - 生成深度分析文档

请选择：
- 输入 1: 使用 simple-gemini（快速、标准化）
- 输入 2: 使用 deep-gemini（深入、包含复杂度分析）
```

**Option 2: Auto-Select (Full Automation Mode)**

**CRITICAL: In Full Automation Mode, DO NOT ask user "是否继续？" or present choices**

- **Activation**: User explicitly requests "全程自动化"/"full automation"/"自动化流程" in initial request
- **Behavior**: Router and Main Claude make ALL decisions without user intervention
- **Forbidden Actions**:
  - ❌ "是否继续？" (是/否)
  - ❌ "请选择..." (选项 1/2/3)
  - ❌ "是否需要..." (需要/不需要)
  - ❌ Any form of asking user for confirmation or choice
- **Correct Actions**:
  - ✅ "[全自动模式] 检测到需要规划，自动调用 plan-down..."
  - ✅ "[全自动模式] 代码已生成，自动调用 codex 检查质量..."
  - ✅ Direct execution with logged rationale

- **Decision Rules**:
  - Uses confidence scores with lower threshold (≥50 instead of ≥60)
  - Prefer simpler skills for ambiguous cases:
    - simple-gemini over deep-gemini (unless "深度" mentioned)
    - zen-chat over zen-thinkdeep (unless "调查" or "bug" mentioned)
    - Direct execution over complex skills when unclear
  - **Log all auto-decisions** with rationale for transparency
  - Standards compliance: Always follows CLAUDE.md rules

- **Exception - Only Ask User When**:
  - Blocking errors (environment missing, dependency errors)
  - Security risks (sensitive data exposure, production operations)

**Full Automation Mode Decision Template:**
```
[全自动模式 - 自动决策]
检测到：{task_description}
自动选择：{selected_tool}
置信度：{confidence_score}%
理由：{rationale based on standards and intent}
标准依据：{relevant CLAUDE.md rules}

开始执行...
```

## Router Workflow: Step-by-Step

### Step 1: Receive User Request

**Main Router's Action:**

```
User: "帮我检查刚刚生成的代码"

Router Internal Analysis:
- Keywords detected: "检查", "代码"
- Intent: Code review
- Target: Recently generated code
- Expected output: Quality report + fixes
```

### Step 2: Read Standards & Discover MCPs (CRITICAL)

**Main Router's Action:**

**Part A: Standards Reading**
```
Standards Reading:
a) Global CLAUDE.md (/home/vc/.claude/CLAUDE.md):
   - G1: 文档一等公民 - 代码变更必须同步更新文档
   - G3: 无执行许可场景 - 需要用户明确同意
   - Current phase: P3 (执行方案) - just completed code generation

b) Global CLAUDE.md (/home/vc/.claude/CLAUDE.md):
   - 代码规范：清晰、可读
   - 质量门槛：覆盖率 ≥ 70%

c) Project CLAUDE.md (./CLAUDE.md): [If exists]
   - Project-specific rules

d) Project CLAUDE.md (./CLAUDE.md): [If exists]
   - Model-specific requirements

Standards-Based Decision:
- P3 phase → Code review recommended after code changes (CLAUDE.md requirement)
- G1 rule → Must check if documentation was updated
- User approval needed before fixes (G3)
```

**Part B: MCP Capability Reference (No Pre-check)**
```
MCP Assumptions:

zen-mcp:
  Status: ✅ Assumed AVAILABLE (default)
  Tools: All 13 zen-mcp tools assumed ready
  Strategy: Optimistic routing - verify on actual invocation

User-Mentioned MCPs:
  Detection: Check if user explicitly mentioned MCP tools in request
  Example triggers: "使用 serena", "用 unifuncs 搜索", "调用 mcp__serena__find_symbol"
  Status: ✅ Assumed AVAILABLE (if mentioned by user)
  Strategy: Optimistic routing - honor user's explicit tool choice

Optional Enhancement MCPs:
  serena: Can be discovered on-demand for code intelligence
  unifuncs: Can be discovered on-demand for web capabilities
  Strategy: Lazy discovery - only if needed for enhancement

Routing Decision for codex-code-reviewer:
  Required: mcp__zen__codereview (assumed available ✅)
  Enhancement: serena tools (optional, will discover if needed)
  User preference: None mentioned in this request

→ Decision: Proceed with codex-code-reviewer
  Rationale: zen-mcp assumed available, no blocking issues
```

### Step 3: Analyze Intent

**Main Router's Action:**

```
Intent Classification:
- Primary Intent: Code review ✅
- Secondary Intent: None
- Complexity: Standard (not deep analysis)
- Urgency: Normal

Context Signals:
- Git status shows modified files: src/features.py, src/model_training.py
- No explicit skill mentioned by user
- Recent activity: Code generation just completed

Standards Alignment:
- Matches P3 phase requirement for post-code-change review
- Aligns with G1 (need to verify doc updates)
```

### Step 4: Match to Skill(s) (Optimistic Routing)

**Main Router's Action:**

```
Skill Matching:
- codex-code-reviewer: 95% confidence ✅
  - Reason: Intent is code review, has modified files
  - Standards support: P3 phase requirement
  - zen-mcp: Assumed available (optimistic)
- simple-gemini: 10%
  - zen-mcp: Assumed available
- deep-gemini: 15%
  - zen-mcp: Assumed available
- plan-down: 5%
  - zen-mcp: Assumed available

Decision: Route to codex-code-reviewer
Rationale: Highest confidence + Standards alignment
Note: zen-mcp availability assumed, will verify during execution
```

### Step 5: Invoke Selected Skill (Optimistic Execution)

**Main Router's Action:**

```
Invoking: codex-code-reviewer

Parameters:
- Files to review: [src/features.py, src/model_training.py]
- Review type: full
- User approval: required

MCP Strategy:
  Primary tools: zen-mcp (assumed available, no pre-check)
  Enhancement tools: serena/unifuncs (can discover on-demand if needed)

Execution:
[codex-code-reviewer executes workflow using zen-mcp tools]

Error Handling (if zen-mcp fails):
  1. Skill reports error to router
  2. Router notifies user: "mcp__zen__codereview 当前不可用"
  3. Router suggests fallback: Main Claude direct code review
  4. User chooses: Continue with fallback OR troubleshoot MCP
```

### Step 6: Return Results to User

**Main Router's Action:**

```
代码审查已完成（使用 codex-code-reviewer）：

审查结果：
- 审查文件：2 个
- 发现问题：3 个（已修复）
- 审查轮次：2 / 5

标准合规性检查：
✅ G1: 已验证文档更新（PROJECTWIKI.md, CHANGELOG.md）
✅ G3: 修复前已获得用户授权
✅ 质量门槛：覆盖率达到 75%（超过 70% 阈值）

详细报告：
[codex-code-reviewer's output]
```

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
- 读取 Global CLAUDE.md: P1→P2→P3 workflow, G1 文档一等公民
- 读取 Global CLAUDE.md: 模型开发原则
- 读取 Project CLAUDE.md: [项目特定规则]

Step 1: Intent Analysis
- 检测到多任务顺序工作流
- 任务序列: 分析 → 规划 → 文档 → 审查

Step 2: Auto-Routing Execution (NO USER CONFIRMATION)

[全自动模式 - 任务 1: 分析现有代码]
自动选择: zen-thinkdeep
置信度: 75%
理由: 需要深度分析，符合 P1 阶段要求
标准依据: CLAUDE.md P1 - 分析问题
→ 立即执行 zen-thinkdeep...

[全自动模式 - 任务 2: 制定优化计划]
自动选择: plan-down
置信度: 90%
理由: 明确规划意图，符合 P2 阶段要求
标准依据: CLAUDE.md P2 - 制定方案，G11 强制使用 plan-down
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
标准依据: CLAUDE.md P3 - 执行方案后需审查，G11 强制使用 codex
→ 立即执行 codex-code-reviewer...

[全自动模式 - 执行计划]
执行方式：顺序执行（Sequential）
1. zen-thinkdeep → 分析现有代码结构和问题
2. plan-down → 基于分析结果制定优化计划
3. simple-gemini → 生成 PROJECTWIKI.md 和 README.md
4. codex-code-reviewer → 全面代码质量审查

标准依据: CLAUDE.md (P1→P2→P3), CLAUDE.md (质量原则)
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

### Example 12: Code + Review Workflow

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

- **Standards-First Approach**: ALWAYS read CLAUDE.md before routing decisions
  - Global CLAUDE.md: `/home/vc/.claude/CLAUDE.md`
  - Global CLAUDE.md: `/home/vc/.claude/CLAUDE.md`
  - Project CLAUDE.md: `./CLAUDE.md` (if exists)
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

- **Context-Aware**: Consider project state, recent activity, git status, and CLAUDE.md phase
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
