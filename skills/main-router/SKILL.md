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
- If user explicitly mentions using specific MCP tools (e.g., "use serena to analyze code", "use unifuncs to search"), those tools are assumed available
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
- If user is in **P1 (Analyze Problem)** phase → May route to zen-thinkdeep for deep analysis
- If user is in **P2 (Formulate Solution)** phase → May route to plan-down for planning
- If user is in **P3 (Execute Solution)** phase → May route to codex-code-reviewer after code changes
- If user mentions **"full automation"** → Enable Full Automation Mode
- If standards require documentation → Auto-route to simple-gemini or deep-gemini
- If standards forbid execution (G3 violation) → Do NOT route to execution-related skills

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

### Example 1: General Q&A Request

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

### Example 2: Deep Problem Investigation

**User:** "Deeply analyze why the loss doesn't decrease during training"

**Router Decision:**
```
Intent: Deep problem investigation
Keywords: "deeply analyze", "problem"
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

**User:** "Generate the project's README document"

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

**User:** "Use codex to check the code"

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

**User:** "Deeply analyze the training logic of model_training.py, including complexity"

**Router Decision:**
```
Intent: Deep analysis
Keywords: "deeply analyze", "complexity"
Target: Specific code file
Output: Technical analysis document

→ Route to: deep-gemini

Rationale:
- "deeply analyze" signals need for comprehensive analysis
- "complexity" requires Big O analysis (deep-gemini feature)
- Not a standard doc, requires clink + docgen workflow
```

---

### Example 6: Planning Request

**User:** "Help me create a development plan for user authentication feature"

**Router Decision:**
```
Intent: Planning
Keywords: "create", "plan"
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

**User:** "Generate a document"

**Router Decision:**
```
Intent: Document generation
Ambiguity: What type of document?

→ Action: Ask User for Clarification

Question to User:
"What type of document do you want to generate?

1. Standard project documentation (README, PROJECTWIKI, CHANGELOG) → simple-gemini
2. Deep technical analysis documentation (architecture analysis, performance analysis) → deep-gemini
3. Development plan documentation (plan.md) → plan-down

Please select or specify the document type."
```

---

### Example 8: Multi-Skill Sequential

**User:** "First create a plan, then generate README"

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

**User:** "Full automation, help me complete this project's development workflow: analyze existing code, create optimization plan, generate documentation, check code quality"

**Router Response (CORRECT - No Questions Asked):**
```
[Full Automation Mode] Detected user request "full automation", initiating full automation workflow.

Step 0: Standards Loading
- Read Global CLAUDE.md: P1→P2→P3 workflow, G1 Documentation First-Class Citizen
- Read Global CLAUDE.md: Model Development Principles
- Read Project CLAUDE.md: [Project-specific rules]

Step 1: Intent Analysis
- Detected multi-task sequential workflow
- Task sequence: Analysis → Planning → Documentation → Review

Step 2: Auto-Routing Execution (NO USER CONFIRMATION)

[Full Automation Mode - Task 1: Analyze Existing Code]
Auto-selected: zen-thinkdeep
Confidence: 75%
Rationale: Requires deep analysis, meets P1 phase requirements
Standards basis: CLAUDE.md P1 - Problem Analysis
→ Immediately execute zen-thinkdeep...

[Full Automation Mode - Task 2: Create Optimization Plan]
Auto-selected: plan-down
Confidence: 90%
Rationale: Clear planning intent, meets P2 phase requirements
Standards basis: CLAUDE.md P2 - Solution Planning, G11 mandatory use of plan-down
→ Immediately execute plan-down...

Auto-selected: simple-gemini
Confidence: 65%
Rationale: Standard document generation, choose simple over deep when ambiguous
Standards basis: G1 - Documentation First-Class Citizen
→ Immediately execute simple-gemini...

[Full Automation Mode - Task 4: Check Code Quality]
Auto-selected: codex-code-reviewer
Confidence: 95%
Rationale: Clear code review intent, meets P3 phase requirements
Standards basis: CLAUDE.md P3 - Review after execution, G11 mandatory use of codex
→ Immediately execute codex-code-reviewer...

[Full Automation Mode - Execution Plan]
Execution mode: Sequential
1. zen-thinkdeep → Analyze existing code structure and issues
2. plan-down → Create optimization plan based on analysis results
3. simple-gemini → Generate PROJECTWIKI.md and README.md
4. codex-code-reviewer → Comprehensive code quality review

Standards basis: CLAUDE.md (P1→P2→P3), CLAUDE.md (Quality Principles)
Average confidence: 81.25%

✅ Note: No user confirmation needed throughout, automatically execute all steps.

[Full Automation Mode - Task Completion]
All tasks completed.
→ Generate decision log auto_log.md...
→ Use simple-gemini to record complete decision-making process
```

**Final Step - Auto Log Generation (MANDATORY):**
```
After all tasks complete in Full Automation Mode:

Tool: simple-gemini (or invoke directly via skill)
Task: Generate auto_log.md
Content Requirements:
  - Complete decision timeline (timestamps for each phase)
  - All auto-decision rationales and standards basis
  - Skills/tools invoked list and parameters
  - Confidence scores and risk assessment
  - Issues encountered and solutions
  - Final results and output files list
  - Decision tree visualization (Mermaid)

Template Structure for auto_log.md:
---
# Full Automation Execution Log (Auto Execution Log)
Generated at: {timestamp}

## Executive Summary (Executive Summary)
- User initial request: {original_request}
- Execution mode: Full automation
- Total tasks: {task_count}
- Success/Failure: {success_count}/{failure_count}
- Total duration: {duration}

## Decision Timeline (Decision Timeline)
{chronological list of all decisions}

## Skills Invoked (Skills Invoked)
{list of all skills with parameters and results}

## Auto-Decision Details (Auto-Decision Details)
{detailed rationale for each auto-decision}

## Issues Encountered (Issues Encountered)
{any errors or blockers, and how they were resolved}

## Output Files (Output Files)
{list of all generated files}
---

Purpose: Provide complete transparency to user
```

**Anti-Pattern - WRONG Full Automation Behavior:**
```
❌ WRONG:
"Because current mode is full automation, I will automatically enter P2 phase and call plan-down to generate detailed plan.
 Should I continue? (Default to continue in automation mode, please let me know if tech stack needs adjustment)"

Why Wrong:
- Asking "Should I continue?" - Violates full automation principle
- "please let me know if tech stack needs adjustment" - Should not prompt user intervention
- Should execute directly, not ask

✅ CORRECT:
"[Full Automation Mode] Detected need for planning, automatically entering P2 phase.
 Calling plan-down skill to generate detailed plan...
 (Decision basis: User initial request contains 'full automation', current phase P1→P2, standards basis G11)"
```

---

### Example 10: User Explicitly Mentions MCP Tools

**User:** "Use serena's find_symbol tool to analyze code structure, then generate documentation"

**Router Decision:**
```
Intent: Multi-task sequential with explicit MCP tool preference
User-Mentioned MCP: serena (specifically mcp__serena__find_symbol)
Task 1: Code structure analysis (using serena)
Task 2: Document generation

Step 0.2: MCP Assumptions
→ zen-mcp: Assumed AVAILABLE (default)
→ serena: Assumed AVAILABLE (user explicitly mentioned)
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
  → Notify user: "serena tool is currently unavailable"
  → Fallback: Use zen-mcp code analysis tools or manual code reading
  → User choice: Continue with fallback OR troubleshoot serena MCP
```

---

### Example 11: Complete Task Lifecycle with Active Monitoring ⭐ BEST PRACTICE

**User:** "Help me develop a user login feature"

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
1. plan-down → plan.md generated
2. Main Claude → login.py generated
3. codex-code-reviewer → login.py validated
4. simple-gemini → test_login.py generated
5. codex-code-reviewer → test_login.py validated
6. Main Claude → tests executed
7. simple-gemini → PROJECTWIKI.md updated
8. codex-code-reviewer → final validation

Router's Active Role:
- Monitored entire lifecycle (5 phases)
- Invoked skills 6 times proactively
- Did NOT allow Main Claude to skip quality checks
- Ensured proper skill usage at each stage
```

**Key Takeaway:** Router actively monitors and intervenes, ensuring proper skill usage throughout the task lifecycle. **No lazy shortcuts allowed.**

---

### Example 12: Code + Review Workflow

**User:** "Generate test files then check code quality"

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
