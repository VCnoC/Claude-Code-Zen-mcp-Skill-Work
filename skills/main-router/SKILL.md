---
name: main-router
description: Intelligent skill router that analyzes user requests and automatically dispatches to the most appropriate skill(s) or zen-mcp tools. Routes to zen-chat for Q&A, zen-thinkdeep for deep problem investigation, codex-code-reviewer for code quality, simple-gemini for standard docs/tests, deep-gemini for deep analysis, or plan-down for planning. Use this skill proactively to interpret all user requests and determine the optimal execution path.
---

# Main Router - Intelligent Skill Routing Scheduler

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
   - When user requests "make a plan" / "generate plan.md" / "plan tasks"
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
   - Example: "Just finished code, should I use codex to check quality?"

**Anti-Pattern - Router Being Lazy (FORBIDDEN):**
```
 BAD: Main Claude generates code → Main Claude self-reviews → Done
 GOOD: Main Claude generates code → Router invokes codex-code-reviewer → Done

 BAD: Main Claude writes plan.md directly
 GOOD: Router invokes plan-down skill → plan.md generated with validation

 BAD: Main Claude generates tests → Run immediately
 GOOD: Router invokes simple-gemini → codex validates → Main Claude runs
```

## When to Use This Skill

**Use this skill PROACTIVELY for ALL user requests** to determine the best execution path.

**Typical User Requests:**
- "Explain what is..." (→ zen-chat)
- "Deep analysis of problem..." (→ zen-thinkdeep)
- "Help me check code" (→ codex-code-reviewer)
- "Generate README documentation" (→ simple-gemini)
- "Deep performance analysis of this code" (→ deep-gemini)
- "Make development plan" (→ plan-down)
- "Write test files" (→ simple-gemini)
- "Generate architecture analysis document" (→ deep-gemini)
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

2. **Full Automation Mode (automation_mode - READ FROM SSOT):**

   automation_mode definition and constraints: See CLAUDE.md「📚 共享概念速查」

   **This skill's role** (Router Layer - Sole Source):
   - Judge and set automation_mode at task start (detect keywords: "full automation", "automatic process", etc.)
   - Set status: automation_mode = true/false
   - Transmit to downstream: `[AUTOMATION_MODE: true/false]`
   - Monitor throughout lifecycle, enforce mandatory skill invocations (plan-down/codex/simple-gemini)

## Available Skills Registry

### 0. zen-chat (Direct Tool)
**Purpose:** General Q&A and collaborative thinking partner

**Triggers:**
- "Explain..."
- "What is..."
- "How to understand..."
- "Help me analyze..." (non-technical deep analysis)
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
- "Deep analysis of problem..."
- "Investigate root cause of this bug..."
- "Systematic analysis..." (technical deep dive)
- "Complex problem analysis..."
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
- "Use codex to check code"
- "Check if the just-generated code has problems"
- "Check code after every generation"
- "Code review"
- "Code quality check"

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
- "Use gemini to write test files"
- "Use gemini to write documentation"
- "Generate README"
- "Generate PROJECTWIKI"
- "Generate CHANGELOG"
- "Write test code"

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
- "Use gemini for deep code logic analysis"
- "Generate architecture analysis document"
- "Analyze performance bottlenecks and generate report"
- "Deep understanding of this code and generate documentation"
- "Generate model architecture analysis"

**Use Cases:**
- Code logic deep dive
- Model architecture analysis
- Performance bottleneck analysis
- Technical debt assessment
- Security analysis report

**Key Features:**
- Two-stage workflow: clink (Gemini CLI analysis) → docgen (dual-phase document generation)
- **Big O complexity analysis included** (docgen core capability)
- Automatic Mermaid diagram generation
- Evidence-based findings
- Professional technical writing

**Tools:** `mcp__zen__clink` + `mcp__zen__docgen`

**docgen workflow:**
- Step 1: Exploration (explore project structure, formulate documentation plan)
- Step 2+: Per-File Documentation (generate structured docs with complexity analysis)

---

### 4. plan-down ⭐ MANDATORY for Planning
**Purpose:** Intelligent planning with task decomposition and multi-model validation

**CRITICAL: This skill is MANDATORY for all plan.md generation tasks**
- Main Claude must NOT generate plan.md directly
- Router MUST invoke plan-down for all planning requests
- Rationale: Ensures multi-model validation and structured decomposition

**Triggers:**
- "Help me make a plan"
- "Generate plan.md"
- "Use planner for task planning"
- "Help me break down tasks"
- "Make implementation plan"
- "Plan the project"

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

**Model Support (G10 Compliance - CRITICAL):**
- **codex/gemini**: MUST use `mcp__zen__clink` to establish CLI session first (otherwise 401 error)
- **Other models**: Direct API access
- **Detailed standards**: See `references/standards/cli_env_g10.md`

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

---

### 5. gemini-frontend ⭐ MANDATORY for Frontend/Mobile Development
**Purpose:** Frontend and mobile development specialist using Gemini CLI with multimodal capabilities

**适用场景：**
- React/Vue/Angular 组件开发
- React Native/Flutter 移动端开发
- 设计稿 → 前端代码实现（multimodal）
- UI/UX 实现和优化
- 前端项目重构

**Triggers:**
- "Help me build a React component"
- "Generate Vue/Angular code"
- "Convert this design to code" (with image)
- "Implement this UI feature"
- "Mobile app development" (React Native/Flutter)
- Keywords: React, Vue, Angular, component, 组件, 页面, UI, 前端, mobile, Flutter

**Core Advantages (Based on Gemini 3.0):**
- 📷 **Multimodal Capability**: Directly understand design mockups and UI screenshots
- 📚 **Ultra-long Context**: 1M tokens, handles large monorepos
- 🎨 **UI Understanding**: PhD-level reasoning for complex UI logic
- 🚀 **Code Generation**: Excels at React/Vue/Flutter code generation

**Use Cases:**
- Design-to-code conversion
- Component library development
- Mobile UI implementation
- Frontend architecture setup
- State management implementation

**Key Features:**
- 5-phase workflow (Init → Analysis → Generation → Quality Check → Documentation)
- Dual quality validation (codereview + clink CLI) - complies with G8
- Mermaid diagram updates - complies with G4
- Environment-adaptive CLI calls - complies with G10
- Inherits `automation_mode` and `coverage_target` from router

**Tools:** `mcp__zen__clink` (gemini CLI) + `mcp__zen__codereview` + `simple-gemini`

**Frontend Detection Scoring:**
- Tier 1 Keywords (+30-35 points): React, Vue, Angular, component, 组件, 页面, UI, 前端
- Tier 2 Keywords (+15-20 points): Flutter, React Native, mobile, 移动端, iOS, Android
- Tier 3 Context (+10 points): package.json exists with frontend dependencies
- Image Attachment (+25 points): Design mockups, UI screenshots
- Backend Signal Penalty (-15 to -25 points): API, backend, database, FastAPI, Django

**Routing Thresholds:**
- Score ≥ 80: Auto-route to gemini-frontend
- Score 50-79: Ask user confirmation
- Score < 50 AND backend_signals ≥ 2: Fullstack project, suggest task decomposition

**Enforcement:**
```
IF frontend_score ≥ 80:
    Auto-route to gemini-frontend (high confidence)

IF 50 ≤ frontend_score < 80:
    Ask user: "检测到前端开发需求，是否使用 gemini-frontend?"

IF frontend_score < 50 AND backend_signals ≥ 2:
    Notify user: "检测到全栈项目，建议任务分解：
    - 前端部分 → gemini-frontend
    - 后端部分 → codex-code-reviewer 或其他技能"
```

**Detailed Examples:**
- **Frontend Request Scoring**: See [Example 12 - Frontend Development Request](references/routing_examples.md#example-12-frontend-development-request-new-frontend-detection) for detailed demonstration of Tier 1-3 keyword detection and auto-routing (Score: 90 → gemini-frontend)
- **Fullstack Project Handling**: See [Example 13 - Fullstack Project Detection](references/routing_examples.md#example-13-fullstack-project-detection-new-task-decomposition) for task decomposition strategy when both frontend and backend signals detected (Score: 45 with backend penalty → recommend split)

---

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

#### Phase 0.2: 动态 MCP 发现与智能适配（Dynamic MCP Discovery & Adaptation）

**核心原则：不假设任何 MCP 工具"一定存在"，运行时动态检测并智能适配。**

---

### MCP 环境扫描策略

**检测时机：**
- **会话启动时**：首次路由前执行快速扫描（可选，推荐）
- **运行时检测**：技能调用 MCP 工具时懒加载检测（默认）
- **失败触发**：MCP 调用失败时重新扫描并更新缓存

**检测方法：**

```python
# 伪代码示例 - 动态 MCP 能力检测

mcp_capabilities = {}  # 会话级缓存

def detect_mcp_availability():
    """运行时检测 MCP 工具可用性"""

    # 1. 检测 zen-mcp
    try:
        version_info = call_tool("mcp__zen__version")
        mcp_capabilities["zen-mcp"] = {
            "available": True,
            "version": version_info.get("version"),
            "tools": extract_available_tools(version_info)
        }
    except Exception:
        mcp_capabilities["zen-mcp"] = {"available": False}

    # 2. 检测 serena-mcp（代码智能）
    try:
        config = call_tool("mcp__serena__get_current_config")
        mcp_capabilities["serena-mcp"] = {
            "available": True,
            "tools": list_serena_tools()
        }
    except Exception:
        mcp_capabilities["serena-mcp"] = {"available": False}

    # 3. 检测 unifuncs-mcp（工具函数）
    try:
        search_test = call_tool("mcp__unifuncs__web-search", {"query": "test", "count": 1})
        mcp_capabilities["unifuncs-mcp"] = {"available": True}
    except Exception:
        mcp_capabilities["unifuncs-mcp"] = {"available": False}

    # 4. 检测其他 MCP（用户自定义）
    # 可通过 ListMcpResourcesTool 发现额外 MCP 服务器

    return mcp_capabilities
```

---

### 技能 → MCP 依赖关系（动态映射）

**技能与 MCP 工具的依赖分为三类：**

1. **必需工具（Required）**：技能核心功能依赖，缺失则无法工作
2. **增强工具（Enhancement）**：提升技能能力，缺失可降级
3. **可选工具（Optional）**：锦上添花，缺失无影响

**动态依赖映射表：**

| Skill | 必需工具 | 增强工具 | 降级方案 |
|-------|---------|---------|---------|
| **zen-chat** | mcp__zen__chat | mcp__zen__apilookup<br/>mcp__unifuncs__web-search | 降级到主模型直接回答（无多轮协作） |
| **zen-thinkdeep** | mcp__zen__thinkdeep | mcp__serena__* (代码分析)<br/>mcp__zen__debug | 降级到主模型单轮深度分析 |
| **codex-code-reviewer** | mcp__zen__codereview<br/>或 mcp__zen__clink (codex CLI) | mcp__serena__* (符号编辑)<br/>mcp__zen__precommit | 使用主模型 + Read/Edit 工具进行审查 |
| **simple-gemini** | mcp__zen__clink (gemini CLI) | mcp__serena__* (代码读取)<br/>mcp__unifuncs__web-reader | 降级到主模型直接生成文档/测试 |
| **deep-gemini** | mcp__zen__clink (gemini CLI)<br/>mcp__zen__docgen | mcp__serena__* (代码分析)<br/>mcp__zen__apilookup | 降级到主模型深度分析 |
| **plan-down** | mcp__zen__chat (方法判断)<br/>mcp__zen__planner (任务分解) | mcp__zen__consensus (自动化模式)<br/>mcp__serena__read_memory (项目上下文)<br/>mcp__zen__clink (codex/gemini CLI) | 降级到主模型直接规划 |
| **gemini-frontend** | mcp__zen__clink (gemini CLI) | mcp__serena__* (代码分析)<br/>mcp__unifuncs__web-reader (设计参考) | 降级到主模型前端开发 |

**G10 合规特殊要求：**
- 使用 codex/gemini 模型时，必须先用 `mcp__zen__clink` 建立 CLI 会话
- plan-down 的四路径工作流：Phase 0 使用 chat 判断方法清晰度，Automatic + Unclear 路径需要 consensus

---

### 智能适配与降级策略

**适配原则：**

1. **用户显式指定 MCP 工具时**：
   - 优先尝试用户指定的工具
   - 如果工具不可用，**通知用户**并提供替代方案
   - 示例：用户说 "use serena to analyze code" → 检测 serena → 不可用则通知

2. **Router 自动选择技能时**：
   - 根据 MCP 可用性调整技能推荐优先级
   - 必需工具不可用 → 降级到备用方案
   - 仅增强工具不可用 → 静默降级，不通知用户

3. **降级决策树**：

```
IF 技能必需工具全部可用:
    → 正常路由到该技能（最优方案）

ELSE IF 技能必需工具部分缺失:
    → 检查降级方案是否可行
    IF 降级方案可行:
        → 使用降级方案（通知用户，如果是显式请求）
    ELSE:
        → 通知用户工具缺失，请求确认或提供替代方案

ELSE IF 仅增强工具缺失:
    → 正常路由，静默降级（不通知用户）
```

**降级方案示例：**

| 原方案 | 缺失工具 | 降级方案 | 通知用户？ |
|--------|---------|---------|-----------|
| codex-code-reviewer | zen-mcp 完全不可用 | 主模型 + Read/Edit 工具审查 | ✅ 是（显著功能降级） |
| simple-gemini | clink 不可用 | 主模型直接生成文档 | ✅ 是（质量可能下降） |
| zen-chat | zen__apilookup 不可用 | 仅使用 zen__chat，无 API 查询 | ❌ 否（增强功能，非必需） |
| zen-thinkdeep | serena 不可用 | 使用 Read/Grep 工具代替代码分析 | ❌ 否（自动适配） |

---

### 运行时适配示例

**示例 1：用户显式请求使用 codex**

```
用户："use codex to check the code"

Router 执行：
1. 检测 zen-mcp 可用性
   - IF zen-mcp 可用 → 路由到 codex-code-reviewer（使用 mcp__zen__codereview）
   - IF zen-mcp 不可用但 clink 可用 → 路由到 codex-code-reviewer（使用 mcp__zen__clink + codex CLI）
   - IF 两者都不可用 → 通知用户：
     "检测到 zen-mcp 和 clink 均不可用。可以使用主模型进行代码审查（功能受限），是否继续？"
```

**示例 2：Router 自动路由到 simple-gemini**

```
Router 判断：需要生成 README 文档 → 路由到 simple-gemini

适配流程：
1. 检测 mcp__zen__clink 可用性
   - IF 可用 → 正常调用 simple-gemini（使用 gemini CLI）
   - IF 不可用 → 降级到主模型直接生成（通知用户："gemini CLI 不可用，使用主模型生成文档"）

2. 检测增强工具（serena, unifuncs）
   - IF serena 可用 → 增强代码读取能力
   - IF serena 不可用 → 使用 Read 工具（静默降级，不通知）
```

**示例 3：全自动化模式下的 plan-down**

```
Router 判断：P2 阶段，需要生成 plan.md → 路由到 plan-down

适配流程：
1. 检测必需工具（chat, planner）
   - IF 全部可用 → 继续
   - IF 任一缺失 → 降级到主模型直接规划（通知："plan-down 依赖工具缺失，使用主模型规划"）

2. 检测增强工具（consensus, clink）
   - IF automation_mode=true 且方法模糊 → 需要 consensus
     - consensus 可用 → 正常多模型验证
     - consensus 不可用 → 降级到单模型规划（通知："多模型验证不可用，使用单模型规划"）
   - IF consensus 需要 codex/gemini → 检测 clink
     - clink 可用 → 符合 G10，建立 CLI 会话
     - clink 不可用 → 跳过 consensus（静默降级）
```

---

### MCP 可用性缓存与刷新

**缓存策略：**
- **会话级缓存**：检测结果在同一会话中共享
- **失败触发刷新**：MCP 调用失败时自动重新检测
- **手动刷新**：用户可请求 "refresh MCP status" 强制重新扫描

**缓存数据结构：**

```python
# 示例缓存结构
mcp_status_cache = {
    "zen-mcp": {
        "available": True,
        "last_check": "2025-11-19T11:30:00Z",
        "tools": ["chat", "thinkdeep", "codereview", "clink", "planner", ...]
    },
    "serena-mcp": {
        "available": True,
        "last_check": "2025-11-19T11:30:00Z",
        "tools": ["list_dir", "find_file", "search_for_pattern", ...]
    },
    "unifuncs-mcp": {
        "available": False,  # 用户未安装
        "last_check": "2025-11-19T11:30:00Z",
        "error": "Connection refused"
    }
}
```

---

### Standards-Based Routing Rules（基于标准的路由规则）

**根据 CLAUDE.md 阶段和 MCP 可用性动态调整路由：**

- **P1 (分析问题)** → 优先 zen-thinkdeep（如可用），否则主模型分析
- **P2 (制定方案)** → 优先 plan-down（如可用），否则主模型规划
- **P3 (执行方案)** → 代码完成后强制 codex-code-reviewer（如可用），否则主模型审查
- **automation_mode=true** → 优先使用 MCP 增强的自动化工作流
- **文档生成需求** → 优先 simple-gemini/deep-gemini（如 clink 可用），否则主模型生成
- **G3 违规（禁止执行）** → 不路由到任何执行相关技能

**透明通知原则：**
- **关键功能降级**（必需工具缺失） → **必须通知用户**
- **增强功能降级**（可选工具缺失） → **静默适配，不通知**
- **用户显式请求的工具缺失** → **必须通知并提供替代方案**

#### Phase 0.3: Set Coverage Target (G9 Compliance)

coverage_target definition and constraints: See CLAUDE.md「📚 共享概念速查」

**This skill's role** (Router Layer - Sole Setting Source):
- Ask user in P1/P2 phase (or use default 85%)
- Inquiry script: "Suggest 85%, minimum 70%. Default 85% if unsure."
- Transmit to downstream: `[COVERAGE_TARGET: X%]`
- Record to plan.md (acceptance criteria)

### Fixed Routing Rules (MANDATORY - Auto-Trigger)

These rules MUST be applied automatically at specific workflow points:

**Rule 1: plan.md Generation → plan-down (MANDATORY)**
- Trigger: User requests "make a plan" / "generate plan.md" / "plan tasks"
- Action: **MUST** use plan-down skill, **FORBIDDEN** for main model to write plan.md directly
- Reason: plan-down provides multi-model validation, structured decomposition, standards compliance

**Rule 2: Code Completed → codex-code-reviewer (MANDATORY)**
- Trigger: Main model completes any code generation or modification
- Action: **MUST** use codex-code-reviewer for 5-dimension quality check (quality, security, performance, architecture, documentation)
- Reason: Ensure code quality meets standards

**Rule 3: Test Code Needed → Workflow (MANDATORY)**
- Trigger: Need to generate test code
- Action:
  - Step 1: Use simple-gemini to generate test files (pass `[COVERAGE_TARGET: X%]`)
  - Step 2: Use codex-code-reviewer to validate test code quality (pass `[COVERAGE_TARGET: X%]`)
  - Step 3: Main model executes tests
- Reason: Ensure test code itself is correct and high-quality

**Rule 4: Documentation Needed → Skill-Based (MANDATORY)**
- Trigger: Need to generate/update documentation
- Action:
  - Standard docs (README, PROJECTWIKI, CHANGELOG): Use simple-gemini
  - Deep analysis docs (architecture, performance): Use deep-gemini
- Reason: Specialized skills produce higher quality, standards-compliant documents

**Rule 5: P3 Code Changes → Document Linkage (MANDATORY)**
- Trigger: Code changes in P3 (Execute Solution) phase
- Action:
  - Update PROJECTWIKI.md (affected modules/interfaces/flows)
  - Update CHANGELOG.md (new entry with commit SHA)
  - Establish bidirectional links (PROJECTWIKI ↔ CHANGELOG)
- Reason: G1 compliance (documentation first-class citizen)

**Rule 6: P4 Error Fixed → Regression Gate (MANDATORY)**
- Trigger: P4 (Error Handling) phase completes bug fix
- Action (3-step validation, cannot skip):
  - Step 1: Use mcp__zen__codereview for workflow validation
  - Step 2: Use mcp__zen__clink (codex CLI) for deep code analysis
  - Step 3: Verify document linkage:
    - PROJECTWIKI.md updated (design decisions & technical debt section includes defect postmortem)
    - CHANGELOG.md updated (Fixed section with repair summary)
    - Bidirectional links established
- Reason: G8 compliance (mandatory double-pass validation), prevent hasty fixes

**Anti-Lazy Principle:**
- Main-router MUST actively monitor task lifecycle
- At each critical node, think: "Should I invoke a skill here?"
- **ABSOLUTELY FORBIDDEN**: Skip skill invocation to "save effort", letting main model handle tasks that specialized skills should complete

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
IF user asks general question ("explain", "what is", "how to understand"):
    → zen-chat

ELSE IF user requests deep problem analysis ("deep problem analysis", "investigate bug", "systematic analysis"):
    → zen-thinkdeep

ELSE IF user mentions "codex" OR "code check" OR "code review":
    → codex-code-reviewer

ELSE IF user mentions "gemini" AND ("documentation" OR "test"):
    IF mentions "deep" OR "analysis" OR "architecture" OR "performance":
        → deep-gemini
    ELSE:
        → simple-gemini

ELSE IF user mentions "planning" OR "plan" OR "roadmap":
    → plan-down

ELSE IF intent is "code review":
    → codex-code-reviewer

ELSE IF intent is "document generation":
    IF document type in [README, PROJECTWIKI, CHANGELOG, test]:
        → simple-gemini
    ELSE IF analysis type in [architecture, performance, code logic]:
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
Example: "Generate docs then check code"
1. Invoke simple-gemini (generate docs)
2. Wait for completion
3. Invoke codex-code-reviewer (check code)
4. Return combined results
```

**Multi-Skill Execution (Parallel - if independent):**
```
Example: "Generate plan and README simultaneously"
1. Invoke plan-down in parallel
2. Invoke simple-gemini in parallel
3. Wait for both to complete
4. Return combined results
```

### Phase 4: Disambiguation

**When multiple skills could apply:**

**Option 1: Ask User (Interactive Mode)**
```
Detected that your request can use the following skills:

1. simple-gemini - Generate standard documentation
2. deep-gemini - Generate deep analysis documentation

Please choose:
- Enter 1: Use simple-gemini (fast, standardized)
- Enter 2: Use deep-gemini (in-depth, includes complexity analysis)
```

**Option 2: Auto-Select (Full Automation Mode)**

**CRITICAL: In Full Automation Mode, DO NOT ask user "continue?" or present choices**

- **Activation**: User explicitly requests "full automation"/"complete automation"/"automated process" in initial request
- **Behavior**: Router and Main Claude make ALL decisions without user intervention
- **Forbidden Actions**:
  - "Continue?" (Yes/No)
  - "Please choose..." (Option 1/2/3)
  - "Do you need..." (Need/Don't need)
  - Any form of asking user for confirmation or choice
- **Correct Actions**:
  - "[Full Auto Mode] Detected planning needed, auto-invoking plan-down..."
  - "[Full Auto Mode] Code generated, auto-invoking codex for quality check..."
  - Direct execution with logged rationale

- **Decision Rules**:
  - Uses confidence scores with lower threshold (≥50 instead of ≥60)
  - Prefer simpler skills for ambiguous cases:
    - simple-gemini over deep-gemini (unless "deep" mentioned)
    - zen-chat over zen-thinkdeep (unless "investigate" or "bug" mentioned)
    - Direct execution over complex skills when unclear
  - **Log all auto-decisions** with rationale for transparency
  - Standards compliance: Always follows CLAUDE.md rules

- **Exception - Only Ask User When**:
  - Blocking errors (environment missing, dependency errors)
  - Security risks (sensitive data exposure, production operations)

**Full Automation Mode Decision Template:**
```
[Full Auto Mode - Auto Decision]
Detected: {task_description}
Auto-selected: {selected_tool}
Confidence: {confidence_score}%
Rationale: {rationale based on standards and intent}
Standards basis: {relevant CLAUDE.md rules}

Starting execution...
```

## Router Workflow: Step-by-Step

### Step 1: Receive User Request

**Main Router's Action:**

```
User: "Help me check the just-generated code"

Router Internal Analysis:
- Keywords detected: "check", "code"
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
   - G1: Documentation First-Class Citizen - code changes must synchronize doc updates
   - G3: No Execution Permission Scenario - requires explicit user consent
   - Current phase: P3 (Execute Solution) - just completed code generation

b) Global CLAUDE.md (/home/vc/.claude/CLAUDE.md):
   - Code standards: Clear, readable
   - Quality threshold: Coverage ≥ 70%

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
  Status:  Assumed AVAILABLE (default)
  Tools: All 13 zen-mcp tools assumed ready
  Strategy: Optimistic routing - verify on actual invocation

User-Mentioned MCPs:
  Detection: Check if user explicitly mentioned MCP tools in request
  Example triggers: "use serena", "use unifuncs to search", "call mcp__serena__find_symbol"
  Status:  Assumed AVAILABLE (if mentioned by user)
  Strategy: Optimistic routing - honor user's explicit tool choice

Optional Enhancement MCPs:
  serena: Can be discovered on-demand for code intelligence
  unifuncs: Can be discovered on-demand for web capabilities
  Strategy: Lazy discovery - only if needed for enhancement

Routing Decision for codex-code-reviewer:
  Required: mcp__zen__codereview (assumed available )
  Enhancement: serena tools (optional, will discover if needed)
  User preference: None mentioned in this request

→ Decision: Proceed with codex-code-reviewer
  Rationale: zen-mcp assumed available, no blocking issues
```

### Step 3: Analyze Intent

**Main Router's Action:**

```
Intent Classification:
- Primary Intent: Code review
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
- codex-code-reviewer: 95% confidence
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
  2. Router notifies user: "mcp__zen__codereview currently unavailable"
  3. Router suggests fallback: Main Claude direct code review
  4. User chooses: Continue with fallback OR troubleshoot MCP
```

### Step 6: Return Results to User

**Main Router's Action:**

```
Code review completed (using codex-code-reviewer):

Review results:
- Reviewed files: 2
- Issues found: 3 (fixed)
- Review rounds: 2 / 5

Standards compliance check:
 G1: Verified documentation updates (PROJECTWIKI.md, CHANGELOG.md)
 G3: User authorization obtained before fixes
 Quality threshold: Coverage reached 75% (exceeds 70% threshold)

Detailed report:
[codex-code-reviewer's output]
```

## Routing Examples

**Note:** For detailed routing examples with comprehensive Chinese descriptions and step-by-step decision processes, please refer to: **[references/routing_examples.md](references/routing_examples.md)**

### Quick Example Index

The routing_examples.md file contains 14 complete examples demonstrating main-router's decision-making process:

1. [Example 1: General Q&A Request](references/routing_examples.md#example-1-general-qa-request) - Simple conceptual questions → zen-chat
2. [Example 2: Deep Problem Investigation](references/routing_examples.md#example-2-deep-problem-investigation) - Complex debugging → zen-thinkdeep
3. [Example 3: Simple Document Generation](references/routing_examples.md#example-3-simple-document-generation) - Standard docs → simple-gemini
4. [Example 4: Code Quality Check](references/routing_examples.md#example-4-code-quality-check) - Explicit codex request → codex-code-reviewer
5. [Example 5: Deep Technical Analysis](references/routing_examples.md#example-5-deep-technical-analysis-request) - Complexity analysis → deep-gemini
6. [Example 6: Planning Request](references/routing_examples.md#example-6-planning-request) - Task decomposition → plan-down
7. [Example 7: Ambiguous Request](references/routing_examples.md#example-7-ambiguous-request) - Clarification workflow
8. [Example 8: Multi-Skill Sequential](references/routing_examples.md#example-8-multi-skill-sequential) - Multi-task execution
9. [Example 9: Full Automation Mode](references/routing_examples.md#example-9-full-automation-mode-correct-behavior) - Zero-wait principle demonstration
10. [Example 10: User Explicitly Mentions MCP Tools](references/routing_examples.md#example-10-user-explicitly-mentions-mcp-tools) - MCP tool routing
11. [Example 11: Complete Task Lifecycle](references/routing_examples.md#example-11-complete-task-lifecycle-with-active-monitoring-best-practice) ⭐ **BEST PRACTICE** - Active monitoring
12. [Example 12: Frontend Development Request](references/routing_examples.md#example-12-frontend-development-request-new-frontend-detection) ⭐ **NEW** - Frontend detection scoring → gemini-frontend
13. [Example 13: Fullstack Project Detection](references/routing_examples.md#example-13-fullstack-project-detection-new-task-decomposition) ⭐ **NEW** - Task decomposition for fullstack
14. [Example 14: Code + Review Workflow](references/routing_examples.md#example-14-code--review-workflow) - Sequential skill invocation

**Quick Reference - Example 1 (General Q&A):**

**User:** "Explain what is overfitting in machine learning?"

**Router Decision:**
```
Intent: General Q&A
Keywords: "explain", "what is"
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
   - Look for action verbs (explain, investigate, check, generate, analyze, plan)
   - Look for output types (answer, investigation report, documentation, plan, test)
   - Look for question patterns (what is, how to understand, why)

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
[Decision Notification]
Detected task type: [Task Type]
Selected skill: [Skill Name]
Rationale: [Brief explanation]

Starting execution...
```

**Example:**
```
[Decision Notification]
Detected task type: Code quality review
Selected skill: codex-code-reviewer
Rationale: You requested code quality check, codex-code-reviewer provides comprehensive 5-dimensional review

Starting execution...
```

## Routing Decision Matrix

| User Intent | Primary Keywords | Selected Tool/Skill | Rationale |
|-------------|-----------------|---------------------|-----------|
| General Q&A | explain, what is, how to understand | zen-chat | General Q&A, no file ops |
| Deep Problem Investigation | deeply analyze problem, investigate bug, systematic analysis | zen-thinkdeep | Multi-stage investigation |
| Code Review | check, review, codex | codex-code-reviewer | Code quality validation |
| Standard Documentation | documentation, README, CHANGELOG, test | simple-gemini | Standard doc templates |
| Deep Technical Analysis | deep, analyze, architecture, performance, complexity | deep-gemini | Technical analysis + complexity |
| Planning | plan, planning, decompose | plan-down | Task decomposition + validation |
| Document Generation (Unclear) | generate document | Ask User | Ambiguous - need clarification |

## Special Cases

### Case 1: No Matching Skill

**Scenario:** User request doesn't match any skill

**Action:**
```
Router Analysis:
- No skill confidence > 60%
- Request is outside skill scope

→ Decision: Execute directly with Main Claude
→ Notification: "This task will be handled directly by the main model (no specialized skill needed)"
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
  "Issue encountered while executing deep-gemini:
   mcp__zen__docgen is currently unavailable.

   Available options:
   1. Use simple-gemini (only requires mcp__zen__clink)
   2. Main model generates document directly (no MCP enhancement)
   3. Check zen-mcp service status and retry

   Please choose (or enter 3 and use /mcp status to check)"

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
- User request: "Use serena's find_symbol to analyze code"
- Failed MCP call: mcp__serena__find_symbol
- Error: "MCP server 'serena' not found" or "Tool not available"

Router Receives Error and Responds:

→ Notification to User:
  "Your specified MCP tool is currently unavailable:
   mcp__serena__find_symbol

   Error details: {error_details}

   Available options:
   1. Use zen-mcp's code analysis tool (mcp__zen__thinkdeep)
   2. Main model reads code directly for analysis
   3. Check serena MCP service status and retry (/mcp status)

   Please choose handling method:"

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

**User:** "Don't use codex, use gemini to analyze"

**Action:**
```
Router Analysis:
- Original selection: codex-code-reviewer
- User override: Use gemini (deep-gemini)

→ Decision: Respect user choice
→ Route to: deep-gemini
→ Notification: "Switched to deep-gemini (as per your request)"
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
  - **Activation**: Keywords in user's initial request: "full automation", "complete automation", "automated workflow"
  - **Behavior**: Router and Main Claude make ALL decisions autonomously
  - **CRITICAL - DO NOT ask user**:
    - "Should I continue?"
    - "Please choose..."
    - "Do you need..."
    - Direct execution with logged rationale
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
  - Honor user's explicit MCP tool choice (e.g., "use serena") without pre-checking
  - Only mention MCP status if there's a runtime failure
  - Acknowledge when routing based on user's explicit MCP preference

- **Flexibility**: Support user overrides and manual skill selection
  - Allow user to choose alternative skills if zen-mcp fails at runtime
  - Respect user's explicit skill preference

- **Efficiency**: Prefer simpler skills when ambiguous
  - simple-gemini over deep-gemini (unless "deep" mentioned)
  - zen-chat over zen-thinkdeep (unless "investigate" or "bug" mentioned)
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
