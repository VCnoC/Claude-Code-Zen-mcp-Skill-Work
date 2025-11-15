# G10｜环境自适应 CLI 调用标准（Environment-Adaptive CLI Invocation）

> **文档性质**：从 CLAUDE.md 中抽取的复杂操作规范，因步骤复杂且易错而独立成文。
> **原文档位置**：CLAUDE.md → 全局规则 → G10
> **版本号**：v1.0.0
> **最后更新**：2025-01-14
> **依赖**：无

---

## 何时使用（触发条件）

当需要调用以下 CLI 工具时，**必须**先使用本标准进行环境检测和 CLI 启动：

- **codex CLI**：代码审查、质量检查时
- **gemini CLI**：文档生成、测试生成、深度分析时
- **claude CLI**：其他需要 Claude CLI 能力时

**关键场景**：
- 调用 `mcp__zen__consensus` 工具（需要 codex/gemini 模型）时
- plan-down skill（Automatic + Unclear 路径）需要启动 gemini CLI 时
- codex-code-reviewer skill 需要调用 codex CLI 时
- simple-gemini / deep-gemini skills 需要调用 gemini CLI 时

---

## 核心原则

**在使用任何 CLI 工具（codex, gemini）前，必须先检测操作系统环境，根据环境选择正确的调用方式。**

---

## 环境检测方法

使用以下命令检测当前操作系统环境：

```bash
# 检测方法 1：查看 uname
uname -a

# 检测方法 2：检查 WSL 环境变量
echo $WSL_DISTRO_NAME

# 检测方法 3：检查平台信息
python3 -c "import platform; print(platform.system())"
```

---

## 环境判定规则

### 1. WSL 环境
- **判定条件**：`uname -a` 包含 "microsoft" 或 "WSL"
- **或**：`$WSL_DISTRO_NAME` 非空
- **CLI 调用方式**：直接在 WSL 终端使用 `codex` 或 `gemini` 命令

### 2. Windows 环境
- **判定条件**：`platform.system()` 返回 "Windows"
- **CLI 调用方式**：通过 PowerShell 使用 `codex` 或 `gemini` 命令
- **命令格式**：`powershell -Command "codex"` 或 `pwsh -Command "codex"`

### 3. macOS 环境
- **判定条件**：`uname -s` 返回 "Darwin"
- **或**：`platform.system()` 返回 "Darwin"
- **CLI 调用方式**：直接在终端使用 `codex` 或 `gemini` 命令

### 4. Linux 环境
- **判定条件**：`uname -s` 返回 "Linux" 且不包含 "microsoft"
- **CLI 调用方式**：直接在终端使用 `codex` 或 `gemini` 命令

---

## CLI 工具调用标准流程（强制执行）

```
STEP 1: 环境检测
→ 执行检测命令确定操作系统类型

STEP 2: 选择调用方式
→ WSL/Linux/macOS: 直接使用 CLI 命令
→ Windows: 通过 PowerShell 调用

STEP 3: ⚠️ MANDATORY - 使用 mcp__zen__clink 启动 CLI
→ 工具: mcp__zen__clink
→ 参数: prompt="codex" 或 "gemini", cli_name="codex" 或 "gemini"
→ 结果: 创建运行中的 CLI 会话
→ 根据环境自动调整调用方式

STEP 4: 使用依赖 CLI 的工具（如 mcp__zen__consensus）
→ 这些工具将使用 STEP 3 创建的 CLI 会话
→ 不能跳过 STEP 3 直接调用这些工具
```

---

## 严格执行顺序（针对 codex/gemini + consensus 工作流）

```
✅ CORRECT:
1. mcp__zen__clink (启动 CLI) → 创建 CLI 会话
2. mcp__zen__consensus (使用 CLI) → 使用已创建的会话

❌ WRONG:
直接调用 mcp__zen__consensus with "codex" model
→ 导致 401 API 错误
→ 原因: consensus 无法直接调用 codex API，必须通过 CLI 会话
```

---

## 示例实现

### 所有环境通用 - 启动 codex CLI

```yaml
Tool: mcp__zen__clink
Parameters:
  prompt: "codex"
  cli_name: "codex"
  # 注意：无需指定 working_directory，clink 不支持此参数
```

---

## CRITICAL - Codex CLI 启动说明与参数规范

- **MCP 已内置 `--skip-git-repo-check` 参数**，无需手动传递
- **正确调用示例**: `prompt: "codex"` + `cli_name: "codex"`（仅这两个必填参数）

### clink 工具参数合同（仅支持以下字段）

**支持的参数（完整列表）**：
- `prompt` - 必填，非空字符串
- `cli_name` - 必填，CLI 名称（"codex" / "gemini" / "claude"）
- `role` - 可选，角色预设（"default" / "codereviewer" / "planner"）
- `files` - 可选，文件路径列表
- `images` - 可选，图像路径列表
- `continuation_id` - 可选，会话延续 ID

**不支持的参数（会被拒绝）**：
- `args` - 已内置参数，不可手动传递
- `working_directory` - 不支持，CLI 会在当前目录运行
- 任何其他未列出的字段

---

## 重要说明

- `mcp__zen__clink` 工具设计为**跨平台兼容**，会自动适配不同操作系统
- 在 WSL 环境中，CLI 工具（codex, gemini）应该已经安装在 WSL 的 PATH 中
- 在 Windows 环境中，CLI 工具应该可以通过 PowerShell 访问
- 在 macOS/Linux 环境中，CLI 工具应该在系统 PATH 中
- **首次使用前应确认 CLI 工具已正确安装并可访问**
- **关键**: 某些 MCP 工具（如 `mcp__zen__consensus`）在使用 codex/gemini 模型时，**必须先通过 clink 启动 CLI**，不能直接调用 API

---

## 环境检测失败处理

- 如果环境检测失败，默认假设为 Linux 环境
- 如果 CLI 启动失败，应向用户报告错误并提供安装指南
- 建议在任务开始时进行一次性环境检测，结果可缓存用于后续使用

---

## 完成条件（Quality Gate）

- ✅ 已执行环境检测（STEP 1）
- ✅ 已选择正确的调用方式（STEP 2）
- ✅ 已通过 `mcp__zen__clink` 启动 CLI 会话（STEP 3）
- ✅ 确认 CLI 会话创建成功（无 401 错误）
- ✅ 后续工具（如 consensus）可以正常使用 CLI 会话

---

**变更历史**：
- 2025-01-14：从 CLAUDE.md G10 section 抽取，增加"何时使用"和"完成条件"上下文
