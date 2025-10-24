---
name: deep-gemini
description: Deep technical documentation generation workflow using zen mcp's clink and docgen tools. First uses clink to launch gemini CLI in WSL for code analysis, then uses docgen for structured document generation with complexity analysis. Specializes in documents requiring deep understanding of code logic, model architecture, or performance bottleneck analysis. Use when user requests "使用gemini深度分析", "生成架构分析文档", "分析性能瓶颈", "深度理解代码逻辑", or similar deep analysis tasks. Default output is .md format.
---

# Deep Gemini - 深度技术文档生成

## Overview

This skill provides a two-stage deep analysis and documentation workflow:

**Stage 1 - Analysis (clink):** Launch gemini CLI in WSL to perform deep code/architecture/performance analysis
**Stage 2 - Documentation (docgen):** Generate structured technical documents with Big O complexity analysis

All operations leverage zen-mcp's workflow tools to ensure thorough analysis and professional documentation output.

**Technical Architecture:**
- **zen-mcp clink**: Bridge tool to launch gemini CLI in WSL environment for code analysis
- **zen-mcp docgen**: WorkflowTool for multi-step structured document generation with complexity analysis
- **gemini CLI session**: Opened via `gemini` command in WSL, where deep analysis is executed
- **Main Claude Model**: Context gathering, workflow orchestration, user interaction
- **User**: Provides analysis targets, reviews final documents

**Two-Stage Workflow:**
```
Main Claude → clink → Gemini CLI (分析) → docgen → 结构化文档 → User
     ↑                                                              ↓
     └──────────────────── User Approval ─────────────────────────┘
```

**Division of Responsibilities:**

**Stage 1 (Analysis via clink):**
- **Gemini CLI Session** (in WSL): Deep code/architecture/performance analysis, pattern identification
- **clink tool**: Bridges Zen MCP requests to CLI-executable commands, captures CLI output and metadata

**Stage 2 (Documentation via docgen):**
- **docgen tool**: Receives analysis results, executes multi-step document generation workflow, adds Big O complexity analysis
- **Main Claude Model**: Orchestrates both stages, manages user approvals, saves final documents

## When to Use This Skill

Trigger this skill when the user requests:
- "使用gemini深度分析代码逻辑"
- "生成架构分析文档"
- "分析性能瓶颈并生成报告"
- "深度理解这段代码并生成文档"
- "生成模型架构分析"
- "使用gemini进行深度分析"
- Any request requiring deep technical understanding and analysis documentation

**Distinction from simple-gemini:**
- **simple-gemini**: Standard documentation (PROJECTWIKI, README, CHANGELOG) and test code, uses clink only
- **deep-gemini**: Deep analysis documents with complexity analysis, uses clink + docgen two-stage workflow

## Supported Document Types

This skill specializes in generating the following types of deep analysis documents:

1. **代码逻辑深度分析** (Code Logic Deep Dive)
   - Control flow analysis
   - Data flow tracing
   - **Algorithm complexity analysis (Big O notation)**
   - Edge case identification
   - Performance characteristics

2. **模型架构分析** (Model Architecture Analysis)
   - Architecture design patterns
   - Component interaction diagrams
   - Layer-by-layer analysis
   - Design decision rationale
   - **Complexity evaluation of architectural choices**

3. **性能瓶颈分析** (Performance Bottleneck Analysis)
   - Profiling report interpretation
   - Hotspot identification
   - **Time/space complexity analysis**
   - Optimization recommendations
   - Resource usage analysis

4. **技术债务评估** (Technical Debt Assessment)
   - Code smell identification
   - Refactoring priorities
   - Risk assessment
   - **Complexity debt analysis**
   - Improvement roadmap

5. **安全分析报告** (Security Analysis Report)
   - Vulnerability assessment
   - Attack surface analysis
   - Security best practice compliance
   - Mitigation strategies
   - **Complexity of security mechanisms**

**Output Format:**
- Default: `.md` (Markdown)
- User can specify other formats per requirements

**Key Feature - Complexity Analysis:**
All generated documents include Big O complexity analysis where applicable, providing developers with clear performance characteristics of analyzed code.

## Operation Mode (Based on Router's automation_mode)

**🚨 CRITICAL**: This skill **MUST read** the `automation_mode` status from the context set by main-router. **DO NOT** ask the user about automation preference or check for trigger phrases - this is handled exclusively by the router.

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

## Workflow: Two-Stage Deep Analysis Documentation Process

### Phase 1: Analysis Scope Definition

**Main Claude's Responsibilities:**

1. **Clarify Analysis Objectives:**
   - What aspect needs deep analysis? (code logic/architecture/performance/security)
   - What is the specific question or problem to solve?
   - What is the expected depth and breadth of analysis?
   - Is complexity analysis required?

2. **Gather Target Code Context:**
   - Identify files/modules/functions to analyze
   - Read relevant source code using Read tool
   - Collect supporting documentation (if exists)
   - Gather performance data/logs (if applicable)

3. **Define Scope:**
   ```
   分析目标：[明确分析对象]
   分析类型：[代码逻辑/架构/性能/安全]
   关键问题：[要回答的核心问题]
   分析深度：[表面/中等/深入]
   复杂度分析：[是/否]
   相关文件：[列出所有相关文件路径]
   ```

**Output:** Well-defined analysis scope and all necessary context files

### Phase 2: Deep Analysis via Gemini CLI (Stage 1 - clink)

**Main Claude's Action:**

Invoke gemini CLI session via clink for deep analysis:

```
Tool: mcp__zen__clink
Parameters:
- cli_name: "gemini"
- prompt: "请对以下代码/架构/性能数据进行深度分析：

  分析目标：[from Phase 1]
  分析类型：[from Phase 1]
  关键问题：[from Phase 1]

  请进行以下分析：
  1. [具体分析维度 1]
  2. [具体分析维度 2]
  3. [具体分析维度 3]
  4. 算法复杂度评估（时间复杂度、空间复杂度，使用 Big O 表示法）

  提供详细的分析结果，包括：
  - 核心发现
  - 关键洞察
  - 复杂度分析（Big O）
  - 潜在问题
  - 改进建议"

- files: [所有相关文件的绝对路径]
- role: "default"
- continuation_id: [首次调用时不提供]
```

**What Happens (clink bridges to Gemini CLI):**
1. clink receives Zen MCP request
2. clink launches gemini CLI session in WSL (via `gemini` command)
3. clink converts request into CLI-executable commands
4. Gemini CLI performs deep analysis inside WSL session environment
5. clink captures CLI output and metadata
6. Analysis results are returned to Main Claude
7. Session context is preserved via continuation_id

**Gemini CLI's Work (inside WSL session):**
- Read and comprehend all provided code/data
- Perform multi-dimensional analysis (logic, architecture, performance, security)
- Calculate algorithm complexity (time/space complexity in Big O notation)
- Identify patterns, anti-patterns, issues, opportunities
- Generate structured analysis findings with complexity metrics

**Output:** Comprehensive analysis findings with complexity data from gemini CLI

### Phase 3: Structured Document Generation (Stage 2 - docgen)

**Main Claude's Action:**

Invoke docgen tool to generate structured document based on analysis results.

**Step 1: Exploration Phase**

```
Tool: mcp__zen__docgen
Parameters:
  step: |
    探查分析项目，基于以下深度分析结果制定文档生成计划：

    分析结果：
    [从 Phase 2 获得的 Gemini CLI 分析结果]

    文档要求：
    1. 包含执行摘要
    2. 详细的方法论说明
    3. 核心发现（分层次、分维度）
    4. **算法复杂度分析章节**（Big O 表示法，包含时间和空间复杂度）
    5. 详细分析（每个发现的深入解释）
    6. 改进建议（优先级排序）
    7. 结论与下一步行动

    格式要求：
    - Markdown 格式
    - 使用 Mermaid 图表（架构图、流程图、时序图）
    - 代码示例带语法高亮
    - 复杂度分析使用表格呈现

  step_number: 1
  total_steps: 2
  next_step_required: true
  findings: ""
  num_files_documented: 0
  document_complexity: "medium"
```

**Step 2+: Per-File Documentation Phase**

```
Tool: mcp__zen__docgen
Parameters:
  step: |
    为分析结果生成结构化文档，包含：
    - 执行摘要
    - 复杂度分析（Big O 表示法）
    - Mermaid 图表
    - 代码示例
    - 改进建议

  step_number: 2
  total_steps: 2
  next_step_required: false

  findings: |
    [Step 1 探查结果 + Gemini CLI 分析结果]

  num_files_documented: 0
  document_complexity: "medium"

  continuation_id: [从 Step 1 继承]
```

**What Happens (docgen workflow execution):**

**Step 1 (Exploration):**
- docgen receives analysis results and document requirements
- Evaluates project structure and complexity
- Creates documentation plan
- Returns exploration findings with continuation_id

**Step 2+ (Per-File Documentation):**
- docgen generates structured document sections
- Includes **Big O complexity analysis** (key feature)
- Generates Mermaid diagrams automatically
- Formats code examples professionally
- Creates complexity metrics tables
- Returns complete document

**docgen's Specialized Capabilities:**
- Dual-phase workflow (exploration → documentation)
- **Big O complexity analysis integration** ✅
- Structured document formatting
- Professional technical writing
- Automatic Mermaid diagram generation
- Code example formatting

**Output:** Complete structured technical document with complexity analysis

### Phase 4: Review and Finalization

**Main Claude's Action:**

1. **🚨 First: Read automation_mode from Context**

   ```
   IF [AUTOMATION_MODE: false] → Interactive Mode (show document and ask for approval)
   IF [AUTOMATION_MODE: true] → Automated Mode (show document and auto-save)
   ```

2. **Present Document to User:**

   **A) Interactive Mode (automation_mode = false):**
   ```
   深度分析文档已生成：

   [显示文档内容摘要]

   文档统计：
   - 字数：[N]
   - 章节数：[N]
   - Mermaid 图表：[N]
   - 代码示例：[N]
   - 复杂度分析：[N 个函数/算法]

   关键发现：
   - [核心发现 1]
   - [核心发现 2]
   - [核心发现 3]

   复杂度摘要：
   - 最高时间复杂度：O(?)
   - 主要瓶颈：[描述]

   是否需要调整或补充？
   - 满意：保存文档
   - 需要修改：请说明修改要求
   ```

   **B) Automated Mode (automation_mode = true):**
   ```
   [全自动模式] 深度分析文档已生成并自动保存：

   [显示文档内容摘要]

   文档统计：
   - 字数：[N]
   - 章节数：[N]
   - Mermaid 图表：[N]
   - 代码示例：[N]
   - 复杂度分析：[N 个函数/算法]

   关键发现：
   - [核心发现 1]
   - [核心发现 2]
   - [核心发现 3]

   复杂度摘要：
   - 最高时间复杂度：O(?)
   - 主要瓶颈：[描述]

   [自动保存决策记录]
   决策：文档质量符合标准，自动保存
   置信度：high
   标准依据：包含所有必需章节（executive summary, complexity analysis, mermaid diagrams, recommendations）
   保存路径：docs/analysis/[analysis_type]_analysis_[timestamp].md

   已记录到 auto_log.md
   ```

2. **Handle Revisions (if requested):**

   **For Analysis Revision (use clink):**
   ```
   Tool: mcp__zen__clink
   Parameters:
   - cli_name: "gemini"
   - prompt: "请重新分析以下方面：

     [用户的修改要求]

     请提供更新的分析结果。"

   - continuation_id: [从 Phase 2 继承]
   ```

   **For Document Revision (use docgen):**
   ```
   Tool: mcp__zen__docgen
   Parameters:
     step: |
       请对文档进行以下修改：

       [用户的修改要求]

       请提供修订后的完整文档。

     step_number: 3  # 继续工作流
     total_steps: 3
     next_step_required: false

     findings: |
       [之前生成的文档内容 + 用户修改要求]

     num_files_documented: 1  # 已完成主文档
     document_complexity: "medium"

     continuation_id: [从 Phase 3 继承]
   ```

3. **Save Final Document:**
   - Use Write tool to save document to specified path
   - Default filename: `{analysis_type}_analysis_{timestamp}.md`
   - User can specify custom filename and format

**Output:** Final document saved to file system

### Phase 5: Post-Generation Actions (Optional)

**Main Claude's Action (if requested by user):**

1. **Generate Summary:**
   - Extract key findings into a one-page summary
   - Include complexity summary table
   - Suitable for executive presentation

2. **Create Presentation Slides:**
   - Convert document into slide deck outline
   - Highlight key diagrams and complexity findings

3. **Integration with Project Wiki:**
   - Add generated document link to PROJECTWIKI.md
   - Update relevant sections with key insights and complexity metrics

## Tool Parameters Reference

### mcp__zen__clink Tool

**Purpose:** Bridge Zen MCP requests to Gemini CLI in WSL for code analysis

**Key Parameters:**

```yaml
cli_name: "gemini"  # Launches 'gemini' command in WSL
prompt: |           # Analysis task for gemini CLI session
  [Detailed analysis instructions including complexity analysis requirements]
files:              # Absolute paths to context files
  - /absolute/path/to/file1.py
  - /absolute/path/to/file2.py
role: "default"     # Role preset for gemini CLI
continuation_id:    # Session ID to continue previous gemini CLI session
```

**Responsibilities:**
- Launch gemini CLI in WSL environment
- Convert Zen MCP requests to CLI commands
- Capture CLI output and metadata
- Maintain session continuity via continuation_id

### mcp__zen__docgen Tool

**Purpose:** Multi-step structured document generation with complexity analysis

**Key Parameters (Workflow Required):**

```yaml
# 必填参数（工作流字段）
step: |             # 当前步骤的描述和要求
  [Detailed instructions for document generation]
  [Must include complexity analysis requirements]

step_number: 1      # 当前步骤编号
total_steps: 2      # 预计总步骤数
next_step_required: true   # 是否需要下一步

findings: |         # 累积的发现和信息
  [Previous findings + Analysis results]

# 必填参数（docgen 特定）
num_files_documented: 0    # 已记录的文件数量
document_complexity: "medium"  # 文档复杂度（low/medium/high）

# 可选参数
continuation_id:    # 继续会话 ID

# ❌ 不支持的参数（会被拒绝）
# prompt - 不接受
# files - 不接受
# model - 显式排除
# temperature - 显式排除
# thinking_mode - 显式排除
# images - 显式排除
# working_directory - 不存在
```

**Specialized Capabilities:**
- Dual-phase workflow (exploration → per-file documentation)
- **Big O complexity analysis integration** ✅
- Professional technical writing
- Automatic Mermaid diagram generation
- Code example formatting
- Structured document organization

**Output:**
- Complete markdown document with:
  - Executive summary
  - Methodology description
  - Findings with evidence
  - **Complexity analysis section (Big O notation)** ✅
  - Mermaid diagrams
  - Code examples
  - Recommendations
  - Conclusion

### Typical Tool Flow

```
Phase 1: Main Claude gathers context
    ↓
Phase 2: clink → Gemini CLI (analysis + complexity evaluation)
    ↓ [analysis results with complexity data]
Phase 3: docgen (dual-phase workflow)
    Step 1: Exploration
        - Evaluate project structure
        - Create documentation plan
        → Returns continuation_id
    Step 2: Per-File Documentation
        - Generate structured document
        - Include Big O complexity analysis
        - Generate Mermaid diagrams
        → Returns complete document
    ↓ [complete document]
Phase 4: Main Claude → User (review)
    ↓ [approval or revision request]
Phase 5: Save document (Main Claude)
```

## Best Practices

### For Effective Deep Analysis

1. **Scope Management:**
   - Start with narrow, focused scope
   - Expand gradually if needed
   - Clearly specify if complexity analysis is required
   - Avoid analyzing entire large codebases at once

2. **Context Quality:**
   - Provide relevant files only (not entire project)
   - Include documentation and comments
   - Add performance data/logs if analyzing performance
   - Ensure code is well-formatted for complexity analysis

3. **Analysis Depth:**
   - Match depth to user's actual needs
   - For complexity analysis, identify critical paths only
   - Don't over-analyze simple utility functions
   - Justify deep dives with clear objectives

4. **Complexity Analysis:**
   - Focus on algorithms and critical paths
   - Provide Big O notation for time and space complexity
   - Explain complexity in context (why it matters)
   - Compare with alternative approaches if relevant

### Document Quality Standards

**Must Include:**
- Executive summary (2-3 paragraphs with complexity highlights)
- Clear methodology description
- Evidence-based findings (not speculation)
- **Complexity analysis section:**
  - Time complexity (Big O)
  - Space complexity (Big O)
  - Bottleneck identification
  - Comparison with optimal complexity
- Actionable recommendations
- At least 2 Mermaid diagrams (for architecture/flow analysis)
- Code examples with proper syntax highlighting
- Conclusion with next steps

**Complexity Analysis Format:**

Use tables for clarity:

```markdown
## 算法复杂度分析

| 函数/算法 | 时间复杂度 | 空间复杂度 | 说明 |
|----------|-----------|-----------|------|
| train_model() | O(n²) | O(n) | 嵌套循环导致二次复杂度 |
| predict() | O(n log n) | O(1) | 排序操作主导 |
| preprocess() | O(n) | O(n) | 线性扫描，额外存储 |
```

**Mermaid Diagram Types:**
- `flowchart TD/LR`: Control flow, decision trees, complexity paths
- `sequenceDiagram`: Interaction patterns, call sequences
- `classDiagram`: Class relationships, inheritance
- `graph TD/LR`: Dependency graphs, component relationships

**Formatting:**
- Use tables for complexity metrics and comparisons
- Use blockquotes for important complexity insights
- Use code blocks with language tags
- Use ordered lists for sequential steps
- Use unordered lists for features/findings

## Example Usage Scenarios

### Scenario 1: Code Logic Deep Dive with Complexity Analysis

**User:** "使用gemini深度分析 src/model_training.py 的训练逻辑，包括复杂度分析"

**Main Claude:**
```
好的，我将使用 gemini 对训练逻辑进行深度分析，包括算法复杂度评估。

[Phase 1: 收集上下文]
读取 src/model_training.py 及相关依赖...

[Phase 2: 使用 clink 调用 Gemini CLI 分析]
正在进行深度分析...
- 控制流分析
- 数据流追踪
- 算法复杂度计算
- 瓶颈识别

[Phase 3: 使用 docgen 生成结构化文档]
生成带复杂度分析的完整文档...

[Phase 4: 呈现结果]
读取上下文: [AUTOMATION_MODE: false]

深度分析文档已生成！

文档统计：
- 字数：4,200
- 章节数：7
- Mermaid 图表：4
- 代码示例：10
- 复杂度分析：8 个函数

关键发现：
- 训练循环存在 O(n²) 复杂度（嵌套迭代）
- 数据预处理可优化为 O(n log n)
- 内存使用峰值出现在批处理阶段

复杂度摘要：
| 函数 | 时间复杂度 | 空间复杂度 | 优化潜力 |
|------|-----------|-----------|---------|
| train_epoch() | O(n²) | O(n) | 高 - 可降至 O(n log n) |
| validate() | O(n) | O(1) | 低 |
| save_checkpoint() | O(n) | O(n) | 中 |

已保存至：docs/analysis/model_training_analysis_20251021.md

[Interactive Mode] 是否需要进一步优化建议？
```

### Scenario 2: Performance Bottleneck Analysis

**User:** "分析性能瓶颈并生成报告，profiling 数据在 logs/profile.txt，需要复杂度分析"

**Main Claude:**
```
好的，我将分析性能瓶颈并评估复杂度。

[Phase 1: 收集上下文]
- profiling 数据：logs/profile.txt
- 热点代码：[自动识别的源文件]

[Phase 2: clink → Gemini CLI 分析]
分析 profiling 数据和对应代码...
- 识别热点函数
- 计算理论复杂度
- 对比实际性能

[Phase 3: docgen 生成结构化报告]
生成性能分析报告（含复杂度评估）...

[Phase 4: 结果呈现]
性能瓶颈分析报告已完成！

Top 3 瓶颈：
1. data_loader.load_batch() - O(n²) 实际，应为 O(n)
   → 根因：重复文件读取
   → 优化后预期：10x 性能提升

2. feature_extractor.transform() - O(n log n) 已优化
   → 无明显优化空间

3. model.predict_batch() - O(n) 理论，实际 O(n²)
   → 根因：隐式的嵌套循环
   → 优化后预期：5x 性能提升

已保存至：docs/analysis/performance_bottleneck_20251021.md
```

### Scenario 3: Architecture Deep Dive with Complexity Evaluation

**User:** "使用gemini生成整个数据处理流程的架构分析文档，评估设计复杂度"

**Main Claude:**
```
我将为数据处理流程生成架构分析文档，包括复杂度评估。

[Phase 1: 定义范围]
- 数据处理相关模块：[列出模块]
- 分析重点：组件交互、数据流、设计复杂度

[Phase 2: clink → Gemini CLI 架构分析]
执行架构级别分析...
- 组件依赖关系
- 数据流路径复杂度
- 交互模式评估

[Phase 3: docgen 生成架构文档]
生成结构化架构文档...

[Phase 4: 结果]
架构分析文档已生成！

架构复杂度评估：
- 组件耦合度：中等（6/10）
- 数据流复杂度：O(n) - 线性流水线
- 最深调用栈：5 层
- 循环依赖：0（良好）

关键架构发现：
- 采用管道模式，复杂度控制良好
- 建议引入缓存层降低 I/O 复杂度
- 异步处理可将吞吐量提升 3x

文档包含：
- 高层架构图（Mermaid）
- 数据流图（Mermaid）
- 时序图（Mermaid）
- 复杂度分析表
- 优化建议路线图

已保存至：docs/analysis/architecture_analysis_20251021.md
```

## Collaboration Guidelines

### Main Claude Model's Role

**Pre-Analysis Phase:**
- Clarify user's analysis objectives and questions
- Determine if complexity analysis is required
- Identify target code/modules/data for analysis
- Read all relevant source files using Read tool
- Gather supporting documentation and data
- Define clear scope and depth

**During Analysis Phase (clink):**
- Invoke gemini CLI via mcp__zen__clink
- Pass all necessary context files to gemini CLI session
- Request complexity analysis if applicable
- Capture analysis results with complexity metrics

**During Documentation Phase (docgen):**
- Invoke docgen via mcp__zen__docgen
- Pass analysis results to docgen workflow
- Ensure complexity analysis is included in document structure
- Monitor multi-step workflow execution

**Post-Documentation Phase:**
- Receive complete document from docgen
- Present to user with complexity highlights
- Save document to file system using Write tool
- Integrate with project documentation if requested
- Handle any user-requested revisions

**What Main Claude Does NOT Do:**
- Perform deep analysis directly (delegated to Gemini CLI via clink)
- Calculate complexity directly (delegated to analysis tools)
- Write the detailed analysis document directly (delegated to docgen)
- Generate complex Mermaid diagrams directly (delegated to docgen)

### clink Tool's Role

**Bridging Function:**
- Receive Zen MCP analysis requests
- Launch gemini CLI in WSL environment (via `gemini` command)
- Convert requests into CLI-executable commands
- Pass context files to CLI session
- Capture CLI output and metadata
- Return analysis results to Main Claude
- Maintain session continuity via continuation_id

**Does NOT:**
- Generate documents (docgen's responsibility)
- Format output (docgen's responsibility)
- Perform complexity calculations (Gemini CLI's responsibility)

### docgen Tool's Role

**Document Generation Workflow:**
- Receive analysis results from clink stage
- Execute multi-step document generation workflow:
  1. Structure outline
  2. Write executive summary
  3. Elaborate findings
  4. **Generate complexity analysis section (Big O notation)**
  5. Create Mermaid diagrams
  6. Format code examples
  7. Formulate recommendations
  8. Write conclusion
- Perform professional technical writing
- Ensure structured, readable output
- Return complete document

**Specialized Capabilities:**
- Big O complexity analysis integration
- Multi-step workflow orchestration
- Automatic diagram generation
- Professional formatting
- Complexity metrics presentation

**Does NOT:**
- Perform code analysis (clink + Gemini CLI's responsibility)
- Execute code (Main Claude's responsibility if needed)
- Save files to disk (Main Claude's responsibility)

### Gemini CLI Session's Role (via clink)

**Inside the gemini CLI environment in WSL:**
- Read and deeply comprehend provided code/data
- Perform multi-dimensional analysis (logic, architecture, performance, security)
- **Calculate algorithm complexity (time/space complexity in Big O notation)**
- Identify patterns, anti-patterns, issues, opportunities
- Evaluate performance characteristics
- Generate structured analysis findings with complexity metrics
- Maintain context across multiple prompts via continuation_id
- Return comprehensive analysis results to clink

**Does NOT:**
- Generate final documents (docgen's responsibility)
- Format documents professionally (docgen's responsibility)
- Save files (Main Claude's responsibility)

### User's Role

**Provide:**
- Clear analysis objectives and questions
- Target code/modules/data for analysis
- **Specify if complexity analysis is required**
- Desired depth and scope of analysis
- Output format preference (if not .md)

**Review and Approve:**
- Analysis results before document generation
- Final document before saving
- Complexity analysis accuracy (if domain expert)
- Revision requests if needed

**Optional:**
- Request integration with existing documentation
- Request summary or presentation versions
- Specify custom filename and location
- Provide additional context for complexity optimization

## Notes

- **Two-Stage Architecture**: clink for analysis (Gemini CLI in WSL) → docgen for document generation (workflow tool)
- **Complexity Analysis**: Key differentiator - all documents include Big O complexity analysis where applicable
- **Session Continuity**: Both clink and docgen support continuation_id for multi-turn workflows
- **Context Loading**: Files are loaded into gemini CLI session (via clink), then passed to docgen for document generation
- **Output Quality**: Deep analysis documents are evidence-based, well-structured, actionable, and include complexity metrics
- **Mermaid Diagrams**: Strongly encouraged for architecture and flow analysis - docgen automates diagram generation
- **Scope Control**: Start narrow and expand as needed - complexity analysis is resource-intensive
- **Compatibility**: Works with AGENTS.md and CLAUDE.md standards for documentation quality
- **WSL Integration**: clink serves as the bridge between Main Claude and gemini CLI in WSL; docgen operates in Zen MCP environment
- **Tool Separation**: clink = analysis bridge, docgen = document generation workflow - each has distinct responsibilities
- **🚨 CRITICAL - automation_mode Management**:
  - **Three-Layer Architecture**: This skill follows the global automation_mode architecture
  - **Router (Layer 1)**: Only main-router judges and sets `automation_mode` based on user's initial request
  - **Transmission (Layer 2)**: Router passes automation_mode to this skill via context `[AUTOMATION_MODE: true/false]`
  - **Skill (Layer 3 - READ ONLY)**: This skill ONLY reads automation_mode, never judges or modifies it
  - **❌ FORBIDDEN**: Do NOT ask user "是否需要自动化执行?" or check for automation keywords
  - **Automated Mode (automation_mode=true)**: All decisions (document approval, save) auto-approved and logged to `auto_log.md` with reason, confidence, standards
