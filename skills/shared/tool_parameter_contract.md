# Zen MCP Tools - Parameter Contract Reference

> ****: 1.0
> ****: 2025-11-13
> ****: zen-mcp-server/tools/

 Zen MCP Parameter Contract

---

##

1. [Simple Tools](#simple-tools)
   - [chat](#1-chat-chatrequest)
   - [challenge](#2-challenge-challengerequest)
   - [apilookup](#3-apilookup-lookuprequest)
2. [CLI CLI Bridge Tools](#cli-cli-bridge-tools)
   - [clink](#1-clink-clinkrequest)
3. [Workflow Tools](#workflow-tools)
   - [consensus](#1-consensus-consensusrequest)
   - [planner](#2-planner-plannerrequest)
   - [codereview](#3-codereview-codereviewrequest)
   - [debug](#4-debug-debuginvestigationrequest)
   - [thinkdeep](#5-thinkdeep-thinkdeepworkflowrequest)
4. [](#)
5. [](#)

---

## Simple Tools

 `ToolRequest`

### ToolRequest

```python
class ToolRequest(BaseModel):
    model: Optional[str]              #
    temperature: Optional[float]      #  [0.0, 1.0]
    thinking_mode: Optional[str]      # : minimal/low/medium/high/max
    continuation_id: Optional[str]    #  ID
    images: Optional[list[str]]       #  base64
```

---

### 1. chat (ChatRequest)

****: `mcp__zen__chat`
****: `ToolRequest`
****:

####

|  |  |  |  |
|--------|------|------|------|
| `prompt` | str |  |  |
| `working_directory_absolute_path` | str |  |  |
| `model` | str |  |  |
| `temperature` | float |  |  [0.0, 1.0] |
| `thinking_mode` | str |  |  |
| `continuation_id` | str |  |  ID |
| `absolute_file_paths` | list[str] |  |  |
| `images` | list[str] |  |  base64 |

####

```json
{
  "prompt": " Python ",
  "working_directory_absolute_path": "/mnt/d/project",
  "model": "gemini-2.5-pro",
  "temperature": 0.7,
  "thinking_mode": "high",
  "continuation_id": "conv-123"
}
```

---

### 2. challenge (ChallengeRequest)

****: `mcp__zen__challenge`
****: `ToolRequest`
****:

####

|  |  |  |  |
|--------|------|------|------|
| `prompt` | str |  |  |
| `model` | str |  |  |
| `temperature` | float |  |  [0.0, 1.0] |
| `thinking_mode` | str |  |  |
| `continuation_id` | str |  |  ID |
| `images` | list[str] |  |  base64 |

####

- `working_directory` / `working_directory_absolute_path`
- `absolute_file_paths`
- `args`

---

### 3. apilookup (LookupRequest)

****: `mcp__zen__apilookup`
****: `ToolRequest`
****: API/SDK

####

|  |  |  |  |
|--------|------|------|------|
| `prompt` | str |  |  API/SDK// |
| `model` | str |  |  |
| `temperature` | float |  |  [0.0, 1.0] |
| `thinking_mode` | str |  |  |
| `continuation_id` | str |  |  ID |
| `images` | list[str] |  |  base64 |

####

- `working_directory` / `working_directory_absolute_path`
- `absolute_file_paths`
- `args`

---

## CLI CLI Bridge Tools

CLI `BaseModel`**** `ToolRequest` `model``temperature``thinking_mode`

---

### 1. clink (CLinkRequest)

****: `mcp__zen__clink`
****: `BaseModel`
****: AI CLIcodex, gemini, claude

####

|  |  |  |  |
|--------|------|------|------|
| `prompt` | str |  | **** CLI  |
| `cli_name` | str |  | CLI "codex"/"gemini"/"claude" |
| `role` | str |  | "default"/"codereviewer"/"planner" |
| `absolute_file_paths` | list[str] |  |  |
| `images` | list[str] |  |  base64 |
| `continuation_id` | str |  |  ID |

#### CRITICAL

- `prompt` ****
- **** `working_directory` / `working_directory_absolute_path`clink
- **** `args`MCP `--skip-git-repo-check`
- **** `model``temperature``thinking_mode`clink ToolRequest

####

```json
{
  "prompt": "codex",
  "cli_name": "codex",
  "role": "codereviewer",
  "continuation_id": "conv-456"
}
```

####

```json
{
  "prompt": "",  //
  "working_directory": "/mnt/d/project",  //
  "args": "--skip-git-repo-check",  //  MCP
  "model": "gemini-2.5-pro",  //  clink  model
  "temperature": 0.8  //  clink  temperature
}
```

---

## Workflow Tools

 `WorkflowRequest`

### WorkflowRequest

```python
class WorkflowRequest(ToolRequest):
    #
    step: str                          #
    step_number: int                   #  1
    total_steps: int                   #
    next_step_required: bool           #

    #
    findings: str                      #
    files_checked: list[str]           #
    relevant_files: list[str]          #
    relevant_context: list[str]        # /
    issues_found: list[dict]           #
    confidence: str                    #
    hypothesis: Optional[str]          #
    use_assistant_model: Optional[bool] #
```

---

### 1. consensus (ConsensusRequest)

****: `mcp__zen__consensus`
****: `WorkflowRequest`
****:

####

|  |  |  |  |
|--------|------|------|------|
| `step` | str |  | Step 1: Steps 2+:  |
| `step_number` | int |  |  1  |
| `total_steps` | int |  |  |
| `next_step_required` | bool |  |  |
| `findings` | str |  | Step 1: Steps 2+:  |
| `models` | list[dict] |  (Step 1) |  2  |
| `relevant_files` | list[str] |  |  |
| `images` | list[str] |  |  base64 |
| `continuation_id` | str |  |  ID |
| `use_assistant_model` | bool |  |  true |
| `current_model_index` | int |  | 0-based |
| `model_responses` | list[dict] |  |  |

####

- `temperature`, `thinking_mode`, `files_checked`, `relevant_context`, `issues_found`, `hypothesis`, `confidence`

#### Step 1

- **** `models` 2
- `(model, stance)`

#### models

```json
{
  "models": [
    {
      "model": "gemini-2.5-pro",
      "stance": "for",  // "for" / "against" / "neutral"
      "stance_prompt": "Argue for GraphQL migration..."
    },
    {
      "model": "gemini-2.0-flash",
      "stance": "against",
      "stance_prompt": "Argue against migration..."
    }
  ]
}
```

---

### 2. planner (PlannerRequest)

****: `mcp__zen__planner`
****: `WorkflowRequest`
****:

####

|  |  |  |  |
|--------|------|------|------|
| `step` | str |  | Step 1: Later: // |
| `step_number` | int |  |  1  |
| `total_steps` | int |  |  |
| `next_step_required` | bool |  |  |
| `is_step_revision` | bool |  |  |
| `revises_step_number` | int |  |  |
| `is_branch_point` | bool |  |  |
| `branch_from_step` | int |  |  |
| `branch_id` | str |  |  |
| `more_steps_needed` | bool |  |  |
| `continuation_id` | str |  |  ID |
| `model` | str |  |  |
| `use_assistant_model` | bool |  |  false |

####

- `findings`, `files_checked`, `relevant_files`, `relevant_context`, `issues_found`, `confidence`, `hypothesis`, `temperature`, `thinking_mode`, `images`

####

- `is_step_revision=True` `revises_step_number`
- `is_branch_point=True` `branch_from_step` `branch_id`

---

### 3. codereview (CodeReviewRequest)

****: `mcp__zen__codereview`
****: `WorkflowRequest`
****:

####

|  |  |  |  |
|--------|------|------|------|
| `step` | str |  | Step 1: Later:  |
| `step_number` | int |  |  1  |
| `total_steps` | int |  | external: 2 internal: 1  |
| `next_step_required` | bool |  |  |
| `findings` | str |  | /// |
| `relevant_files` | list[str] |  (Step 1) | / |
| `files_checked` | list[str] |  |  |
| `relevant_context` | list[str] |  | / |
| `issues_found` | list[dict] |  |  |
| `images` | list[str] |  |  |
| `review_type` | str |  | "full"/"security"/"performance"/"quick" |
| `focus_on` | str |  |  |
| `standards` | str |  |  |
| `severity_filter` | str |  | "critical"/"high"/"medium"/"low"/"all" |
| `review_validation_type` | str |  | "external"/"internal" |
| `continuation_id` | str |  |  ID |
| `model` | str |  |  |
| `use_assistant_model` | bool |  |  true |

####

- `temperature`, `thinking_mode`, `confidence`

#### Step 1

- **** `relevant_files` /

---

### 4. debug (DebugInvestigationRequest)

****: `mcp__zen__debug`
****: `WorkflowRequest`
****:

####

|  |  |  |  |
|--------|------|------|------|
| `step` | str |  | Step 1: Later:  |
| `step_number` | int |  |  1  |
| `total_steps` | int |  |  |
| `next_step_required` | bool |  |  |
| `findings` | str |  |  |
| `files_checked` | list[str] |  |  |
| `relevant_files` | list[str] |  |  |
| `relevant_context` | list[str] |  | / |
| `hypothesis` | str |  |  |
| `confidence` | str |  | exploring/low/.../certain |
| `images` | list[str] |  | / |
| `continuation_id` | str |  |  ID |
| `model` | str |  |  |
| `use_assistant_model` | bool |  |  true |

####

- `temperature`, `thinking_mode`, `issues_found`

#### confidence

- ****: `"certain"`
- `"certain"`

---

### 5. thinkdeep (ThinkDeepWorkflowRequest)

****: `mcp__zen__thinkdeep`
****: `WorkflowRequest`
****:

####

|  |  |  |  |
|--------|------|------|------|
| `step` | str |  |  |
| `step_number` | int |  |  1  |
| `total_steps` | int |  |  |
| `next_step_required` | bool |  |  |
| `findings` | str |  |  |
| `files_checked` | list[str] |  |  |
| `relevant_files` | list[str] |  |  |
| `relevant_context` | list[str] |  | / |
| `hypothesis` | str |  |  |
| `confidence` | str |  |  |
| `issues_found` | list[dict] |  |  |
| `problem_context` | str |  | / |
| `focus_areas` | list[str] |  | // |
| `continuation_id` | str |  |  ID |
| `model` | str |  |  |
| `temperature` | float |  |  [0.0, 1.0] |
| `thinking_mode` | str |  |  |
| `use_assistant_model` | bool |  |  true |

####

- **thinkdeep `temperature` `thinking_mode` **

---

##

```
BaseModel
 CLinkRequest (clink)
   prompt, cli_name, role, absolute_file_paths, images, continuation_id

 ToolRequest
    model, temperature, thinking_mode, continuation_id, images

    ChatRequest (chat)
      + prompt, working_directory_absolute_path, absolute_file_paths

    ChallengeRequest (challenge)
      + prompt

    LookupRequest (apilookup)
      + prompt

    WorkflowRequest
       + step, step_number, total_steps, next_step_required
       + findings, files_checked, relevant_files, relevant_context
       + issues_found, confidence, hypothesis, use_assistant_model

       ConsensusRequest (consensus)
         + models, current_model_index, model_responses
         - temperature, thinking_mode, files_checked, relevant_context, issues_found, hypothesis, confidence

       PlannerRequest (planner)
         + is_step_revision, revises_step_number, is_branch_point, branch_from_step, branch_id, more_steps_needed
         - findings, files_checked, relevant_files, relevant_context, issues_found, confidence, hypothesis, temperature, thinking_mode, images

       CodeReviewRequest (codereview)
         + review_type, focus_on, standards, severity_filter, review_validation_type
         - temperature, thinking_mode, confidence

       DebugInvestigationRequest (debug)
         ( WorkflowRequest )
         - temperature, thinking_mode, issues_found

       ThinkDeepWorkflowRequest (thinkdeep)
          + problem_context, focus_areas
          ( temperature, thinking_mode - )
```

---

##

### 1: clink working_directory

```json
//
{
  "prompt": "codex",
  "working_directory": "/mnt/d/project"
}
```

****: clink `working_directory` `working_directory_absolute_path`

****:
```
 Remove 'working_directory' parameter.
clink tool does not support working directory configuration.
The CLI will run in the current directory automatically.
```

---

### 2: clink model/temperature

```json
//
{
  "prompt": "codex",
  "model": "gemini-2.5-pro",
  "temperature": 0.8
}
```

****: clink `CLinkRequest` `ToolRequest`

****:
```
 Remove 'model', 'temperature', 'thinking_mode' parameters.
clink uses CLinkRequest (not ToolRequest), these fields are not supported.
```

---

### 3: consensus Step 1 models

```json
//
{
  "step": "Evaluate API migration",
  "step_number": 1,
  "total_steps": 3,
  "next_step_required": true,
  "findings": "..."
  //  models
}
```

****: consensus Step 1 `models`

****:
```
 Add 'models' field in Step 1 with at least 2 model configurations.
Example:
models=[
  {'model':'gemini-2.5-pro','stance':'for'},
  {'model':'gemini-2.5-flash','stance':'against'}
]
```

---

### 4: clink prompt

```json
//
{
  "prompt": "",
  "cli_name": "codex"
}
```

****: clink `prompt`

****:
```
 'prompt' parameter must be a non-empty string.
Cannot pass empty string or null value.
Example: prompt="codex"
```

---

### 5: codereview Step 1 relevant_files

```json
//
{
  "step": "Review code quality",
  "step_number": 1,
  "total_steps": 2,
  "next_step_required": true,
  "findings": "..."
  //  relevant_files
}
```

****: codereview Step 1 `relevant_files`

****:
```
 Add 'relevant_files' field in Step 1 to specify code files or directories to review.
Example: relevant_files=["/mnt/d/project/src/api/router.py"]
```

---

##

- ****: `zen-mcp-server/tools/`
- ****: `zen-mcp-server/tools/shared/base_models.py`
- **Main Router SKILL**: `~/.claude/skills/main-router/SKILL.md`

---

****: 1.0
****: 2025-11-13
****: Claude Code Zen MCP Project
