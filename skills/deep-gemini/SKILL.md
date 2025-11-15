---
name: deep-gemini
description: Deep technical documentation generation workflow using zen mcp's clink and docgen tools. First uses clink to launch gemini CLI in WSL for code analysis, then uses docgen for structured document generation with complexity analysis. Specializes in documents requiring deep understanding of code logic, model architecture, or performance bottleneck analysis. Use when user requests "use gemini for deep analysis", "generate architecture analysis document", "analyze performance bottlenecks", "deeply understand code logic", or similar deep analysis tasks. Default output is .md format.
---

# Deep Gemini - Deep Technical Documentation Generation

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
Main Claude → clink → Gemini CLI (Analysis) → docgen → Structured Doc → User
     ↑                                                                  ↓
     └──────────────────── User Approval ──────────────────────────────┘
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
- "Use gemini to deeply analyze code logic"
- "Generate architecture analysis document"
- "Analyze performance bottlenecks and generate report"
- "Deeply understand this code and generate documentation"
- "Generate model architecture analysis"
- "Use gemini for deep analysis"
- Any request requiring deep technical understanding and analysis documentation

**Distinction from simple-gemini:**
- **simple-gemini**: Standard documentation (PROJECTWIKI, README, CHANGELOG) and test code, uses clink only
- **deep-gemini**: Deep analysis documents with complexity analysis, uses clink + docgen two-stage workflow

## Supported Document Types

This skill specializes in generating the following types of deep analysis documents:

1. **Code Logic Deep Dive**
   - Control flow analysis
   - Data flow tracing
   - **Algorithm complexity analysis (Big O notation)**
   - Edge case identification
   - Performance characteristics

2. **Model Architecture Analysis**
   - Architecture design patterns
   - Component interaction diagrams
   - Layer-by-layer analysis
   - Design decision rationale
   - **Complexity evaluation of architectural choices**

3. **Performance Bottleneck Analysis**
   - Profiling report interpretation
   - Hotspot identification
   - **Time/space complexity analysis**
   - Optimization recommendations
   - Resource usage analysis

4. **Technical Debt Assessment**
   - Code smell identification
   - Refactoring priorities
   - Risk assessment
   - **Complexity debt analysis**
   - Improvement roadmap

5. **Security Analysis Report**
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

## Operation Mode (automation_mode - READ FROM SSOT)

automation_mode definition and constraints: See CLAUDE.md「📚 共享概念速查」

**This skill's role**: Skill Layer (read-only), read from context `[AUTOMATION_MODE: true/false]`
- `false` → Interactive: Show document, ask for approval
- `true` → Automated: Auto-save document, log to auto_log.md

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
   Analysis Target: [Specify analysis object]
   Analysis Type: [Code Logic/Architecture/Performance/Security]
   Key Questions: [Core questions to answer]
   Analysis Depth: [Surface/Medium/Deep]
   Complexity Analysis: [Yes/No]
   Relevant Files: [List all relevant file paths]
   ```

**Output:** Well-defined analysis scope and all necessary context files

### Phase 2: Deep Analysis via Gemini CLI (Stage 1 - clink)

**Main Claude's Action:**

Invoke gemini CLI session via clink for deep analysis:

```
Tool: mcp__zen__clink
Parameters:
- cli_name: "gemini"
- prompt: "Please perform deep analysis on the following code/architecture/performance data:

  Analysis Target: [from Phase 1]
  Analysis Type: [from Phase 1]
  Key Questions: [from Phase 1]

  Please perform the following analysis:
  1. [Specific analysis dimension 1]
  2. [Specific analysis dimension 2]
  3. [Specific analysis dimension 3]
  4. Algorithm complexity assessment (time complexity, space complexity, using Big O notation)

  Provide detailed analysis results, including:
  - Core findings
  - Key insights
  - Complexity analysis (Big O)
  - Potential issues
  - Improvement recommendations"

- files: [Absolute paths of all relevant files]
- role: "default"
- continuation_id: [Not provided for first call]
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
    Explore the analysis project and create a document generation plan based on the following deep analysis results:

    Analysis Results:
    [Gemini CLI analysis results obtained from Phase 2]

    Document Requirements:
    1. Include executive summary
    2. Detailed methodology description
    3. Core findings (hierarchical, multi-dimensional)
    4. **Algorithm complexity analysis section** (Big O notation, including time and space complexity)
    5. Detailed analysis (in-depth explanation of each finding)
    6. Improvement recommendations (priority-sorted)
    7. Conclusion and next steps

    Format Requirements:
    - Markdown format
    - Use Mermaid diagrams (architecture diagrams, flowcharts, sequence diagrams)
    - Code examples with syntax highlighting
    - Complexity analysis presented in tables

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
    Generate structured document for analysis results, including:
    - Executive summary
    - Complexity analysis (Big O notation)
    - Mermaid diagrams
    - Code examples
    - Improvement recommendations

  step_number: 2
  total_steps: 2
  next_step_required: false

  findings: |
    [Step 1 exploration results + Gemini CLI analysis results]

  num_files_documented: 0
  document_complexity: "medium"

  continuation_id: [Inherited from Step 1]
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
- **Big O complexity analysis integration**
- Structured document formatting
- Professional technical writing
- Automatic Mermaid diagram generation
- Code example formatting

**Output:** Complete structured technical document with complexity analysis

### Phase 4: Review and Finalization

**Main Claude's Action:**

1. ** automation_mode check**: `[AUTOMATION_MODE: false]` → Interactive (show + ask) / `true` → Automated (show + auto-save)

2. **Present Document to User:**

   **A) Interactive Mode (automation_mode = false):**
   ```
   Deep analysis document has been generated:

   [Display document content summary]

   Stats: [N] words, [N] sections, [N] diagrams, [N] examples, [N] complexity analyses
   Findings: [Core finding 1], [Core finding 2], [Core finding 3]
   Complexity: Highest O(?), Bottleneck: [Description]

   Do you need adjustments or additions?
   - Satisfied: Save document
   - Need modifications: Please specify modification requirements
   ```

   **B) Automated Mode (automation_mode = true):**
   ```
   [Fully Automated Mode] Deep analysis document has been generated and automatically saved:

   [Display document content summary]

   Stats: [N] words, [N] sections, [N] diagrams, [N] examples, [N] complexity analyses
   Findings: [Core finding 1], [Core finding 2], [Core finding 3]
   Complexity: Highest O(?), Bottleneck: [Description]

   [Automated Save Decision Record]
   Decision: Document quality meets standards, automatically saved
   Confidence: high
   Standards basis: Contains all required sections (executive summary, complexity analysis, mermaid diagrams, recommendations)
   Save path: docs/analysis/[analysis_type]_analysis_[timestamp].md

   Recorded in auto_log.md
   ```

2. **Handle Revisions (if requested):**

   **For Analysis Revision (use clink):**
   ```
   Tool: mcp__zen__clink
   Parameters:
   - cli_name: "gemini"
   - prompt: "Please re-analyze the following aspects:

     [User's modification requirements]

     Please provide updated analysis results."

   - continuation_id: [Inherited from Phase 2]
   ```

   **For Document Revision (use docgen):**
   ```
   Tool: mcp__zen__docgen
   Parameters:
     step: |
       Please make the following modifications to the document:

       [User's modification requirements]

       Please provide the revised complete document.

     step_number: 3  # Continue workflow
     total_steps: 3
     next_step_required: false

     findings: |
       [Previously generated document content + user modification requirements]

     num_files_documented: 1  # Main document completed
     document_complexity: "medium"

     continuation_id: [Inherited from Phase 3]
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
# Required Parameters (Workflow Fields)
step: |             # Description and requirements of the current step
  [Detailed instructions for document generation]
  [Must include complexity analysis requirements]

step_number: 1      # Current step number
total_steps: 2      # Estimated total steps
next_step_required: true   # Whether next step is required

findings: |         # Accumulated findings and information
  [Previous findings + Analysis results]

# Required Parameters (docgen-specific)
num_files_documented: 0    # Number of files documented
document_complexity: "medium"  # Document complexity (low/medium/high)

# Optional Parameters
continuation_id:    # Continuation session ID

# Unsupported Parameters (will be rejected)
# prompt - Not accepted
# files - Not accepted
# model - Explicitly excluded
# temperature - Explicitly excluded
# thinking_mode - Explicitly excluded
# images - Explicitly excluded
# working_directory - Does not exist
```

**Specialized Capabilities:**
- Dual-phase workflow (exploration → per-file documentation)
- **Big O complexity analysis integration**
- Professional technical writing
- Automatic Mermaid diagram generation
- Code example formatting
- Structured document organization

**Output:**
- Complete markdown document with:
  - Executive summary
  - Methodology description
  - Findings with evidence
  - **Complexity analysis section (Big O notation)**
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
## Algorithm Complexity Analysis

| Function/Algorithm | Time Complexity | Space Complexity | Description |
|-------------------|----------------|------------------|-------------|
| train_model() | O(n²) | O(n) | Nested loops cause quadratic complexity |
| predict() | O(n log n) | O(1) | Sorting operations dominate |
| preprocess() | O(n) | O(n) | Linear scan, additional storage |
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

**User:** "Use gemini to deeply analyze the training logic in src/model_training.py, including complexity analysis"

**Main Claude:**
```
Okay, I will use gemini to perform deep analysis on the training logic, including algorithm complexity assessment.

[Phase 1: Gathering Context]
Reading src/model_training.py and related dependencies...

[Phase 2: Using clink to invoke Gemini CLI for analysis]
Performing deep analysis...
- Control flow analysis
- Data flow tracing
- Algorithm complexity calculation
- Bottleneck identification

[Phase 3: Using docgen to generate structured document]
Generating complete document with complexity analysis...

[Phase 4: Presenting Results]
Reading context: [AUTOMATION_MODE: false]

Deep analysis document has been generated!

Document Statistics:
- Word count: 4,200
- Section count: 7
- Mermaid diagrams: 4
- Code examples: 10
- Complexity analysis: 8 functions

Key Findings:
- Training loop has O(n²) complexity (nested iteration)
- Data preprocessing can be optimized to O(n log n)
- Memory usage peak occurs during batch processing stage

Complexity Summary:
| Function | Time Complexity | Space Complexity | Optimization Potential |
|----------|----------------|------------------|----------------------|
| train_epoch() | O(n²) | O(n) | High - Can reduce to O(n log n) |
| validate() | O(n) | O(1) | Low |
| save_checkpoint() | O(n) | O(n) | Medium |

Saved to: docs/analysis/model_training_analysis_20251021.md

[Interactive Mode] Do you need further optimization recommendations?
```

### Scenario 2: Performance Bottleneck Analysis

**User:** "Analyze performance bottlenecks and generate a report, profiling data is in logs/profile.txt, need complexity analysis"

**Main Claude:**
```
Okay, I will analyze performance bottlenecks and assess complexity.

[Phase 1: Gathering Context]
- Profiling data: logs/profile.txt
- Hotspot code: [Auto-identified source files]

[Phase 2: clink → Gemini CLI Analysis]
Analyzing profiling data and corresponding code...
- Identifying hotspot functions
- Calculating theoretical complexity
- Comparing with actual performance

[Phase 3: docgen Generating Structured Report]
Generating performance analysis report (with complexity assessment)...

[Phase 4: Result Presentation]
Performance bottleneck analysis report is complete!

Top 3 Bottlenecks:
1. data_loader.load_batch() - O(n²) actual, should be O(n)
   → Root cause: Repeated file reads
   → Expected improvement after optimization: 10x performance gain

2. feature_extractor.transform() - O(n log n) already optimized
   → No significant optimization potential

3. model.predict_batch() - O(n) theoretical, actually O(n²)
   → Root cause: Implicit nested loops
   → Expected improvement after optimization: 5x performance gain

Saved to: docs/analysis/performance_bottleneck_20251021.md
```

### Scenario 3: Architecture Deep Dive with Complexity Evaluation

**User:** "Use gemini to generate an architecture analysis document for the entire data processing flow, assess design complexity"

**Main Claude:**
```
I will generate an architecture analysis document for the data processing flow, including complexity assessment.

[Phase 1: Defining Scope]
- Data processing related modules: [List modules]
- Analysis focus: Component interaction, data flow, design complexity

[Phase 2: clink → Gemini CLI Architecture Analysis]
Executing architecture-level analysis...
- Component dependencies
- Data flow path complexity
- Interaction pattern assessment

[Phase 3: docgen Generating Architecture Document]
Generating structured architecture document...

[Phase 4: Results]
Architecture analysis document has been generated!

Architecture Complexity Assessment:
- Component coupling: Medium (6/10)
- Data flow complexity: O(n) - Linear pipeline
- Deepest call stack: 5 levels
- Circular dependencies: 0 (Good)

Key Architecture Findings:
- Pipeline pattern adopted, complexity well controlled
- Suggest introducing cache layer to reduce I/O complexity
- Asynchronous processing can improve throughput by 3x

Document Contains:
- High-level architecture diagram (Mermaid)
- Data flow diagram (Mermaid)
- Sequence diagram (Mermaid)
- Complexity analysis table
- Optimization recommendation roadmap

Saved to: docs/analysis/architecture_analysis_20251021.md
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
- **Compatibility**: Works with CLAUDE.md standards for documentation quality
- **WSL Integration**: clink serves as the bridge between Main Claude and gemini CLI in WSL; docgen operates in Zen MCP environment
- **Tool Separation**: clink = analysis bridge, docgen = document generation workflow - each has distinct responsibilities
- **automation_mode & auto_log (READ FROM SSOT)**:
  - Definitions and constraints: See CLAUDE.md「📚 共享概念速查」
  - This skill: Skill Layer (read-only), outputs `[Automated Save Decision Record]` fragments when automation_mode=true
  - auto_log template: See `skills/shared/auto_log_template.md`
