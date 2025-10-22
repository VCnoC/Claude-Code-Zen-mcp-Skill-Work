# Claude Code Zen mcp Skill Work

> 面向 AI 编程智能体的技能包集合

## 📋 项目简介

本项目基于 [Zen MCP Server](https://github.com/BeehiveInnovations/zen-mcp-server) 构建，采用多阶段工作流（P1-P4）的 AI 智能体技能系统。通过智能路由自动选择最合适的工具处理编程任务，借助 Zen MCP 可在 Claude 中调用 Codex 和 Gemini CLI 处理相关任务。

> **⚠️ 重要配置提示**  
> 1. **API Keys 配置**：安装前请在环境变量中设置 `OPENAI_API_KEY` 和 `GEMINI_API_KEY`
> 2. **Zen MCP 配置**：在 `zen-mcp/.env` 中：
>    - 设置 `OPENAI_ALLOWED_MODELS=` 指定使用的模型
>    - 在 `DISABLED_TOOLS` 中删除 `docgen` 以启用文档生成
> 3. **全局规则**：将 `CLAUDE.md` 复制到 `~/.claude/CLAUDE.md`（仅需一次）

**核心特性**：
- 🧠 智能路由 - 自动选择最佳技能
- 📊 多阶段工作流 - P1(分析) → P2(方案) → P3(执行) → P4(修复)
- 🔍 5 维代码审查 - 质量、安全、性能、架构、文档
- 📝 文档自动生成 - README、测试代码、项目文档

---

## 📁 项目结构

```
Claude-Code-Zen-mcp-Skill-Work/
├── skills/                          # 技能包目录
│   ├── main-router.zip             # 智能路由和技能匹配
│   ├── plan-down.zip               # 任务分解和计划生成
│   ├── codex-code-reviewer.zip     # 代码质量审查（5维度）
│   ├── simple-gemini.zip           # 标准文档生成
│   └── deep-gemini.zip             # 深度技术分析
├── AGENTS.md                        # 项目级阶段规则（P1-P4）
├── CLAUDE.md                        # 全局规则模板（需配置到 Claude）
└── README.md                       # 项目说明（本文件）
```

**目录说明**：
- `skills/` - 包含 5 个压缩的技能包，需解压后安装到 `~/.claude/skills/`
- `CLAUDE.md` - **全局规则**，需复制到 `~/.claude/CLAUDE.md`，适用于所有项目
- `AGENTS.md` - **项目级规则**，放在项目根目录，定义 P1-P4 阶段工作流

---

## 🎯 技能清单

本项目包含 5 个核心技能包（位于 `skills/` 目录）：

### 1. main-router
智能路由和技能匹配，负责意图分析和任务调度。

### 2. plan-down
智能任务分解和执行计划生成，输出结构化的 `plan.md`。

### 3. codex-code-reviewer
代码质量审查，提供 5 维度检查（质量、安全、性能、架构、文档）。

### 4. simple-gemini
标准文档生成，用于 README、PROJECTWIKI、CHANGELOG 和测试代码。

### 5. deep-gemini
深度技术分析，提供架构分析、性能优化建议等。

---

## 🏗️ 工作流程

```mermaid
flowchart LR
    A[用户请求] --> B[main-router]
    B --> C[P1 分析]
    C --> D[P2 方案]
    D --> E[P3 执行]
    E --> F{成功?}
    F -->|是| G[完成]
    F -->|否| H[P4 修复]
    H --> G
```

**四个阶段**：
- **P1 分析问题** - 理解需求，定位根因
- **P2 制定方案** - 设计解决方案，调用 plan-down 生成计划
- **P3 执行方案** - 实施代码，调用 codex 检查，调用 gemini 生成文档
- **P4 错误处理** - 修复问题，验证修复

---

## 🚀 快速开始

### 环境要求

**必需组件**：
- [Claude Desktop](https://claude.ai/download) - AI 编程助手
- [Zen MCP Server](https://github.com/BeehiveInnovations/zen-mcp-server) - MCP 服务器

**可选 CLI 工具**（增强功能）：
- **Gemini CLI** - 用于文档生成和深度分析
- **Codex CLI** - 用于代码审查和质量检查

### 安装步骤

#### 1. 安装 Zen MCP Server

```bash
git clone https://github.com/BeehiveInnovations/zen-mcp-server.git
cd zen-mcp-server
./run-server.sh
```

#### 2. 下载本项目技能包

```bash
git clone https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work.git
cd Claude-Code-Zen-mcp-Skill-Work
```

**手动安装**

1. 解压 `skills/` 目录下的所有 `.zip` 文件
2. 将解压后的 `.skill` 文件夹复制到 Claude 配置目录：
   - **Windows**: `%USERPROFILE%\.claude\skills\`
   - **macOS/Linux**: `~/.claude/skills/`

#### 4. 验证安装

启动 Claude Desktop，在对话中输入：
```
请使用 main-router 帮我分析当前可用的技能
```

如果看到 5 个技能包（main-router、plan-down、codex-code-reviewer、simple-gemini、deep-gemini），说明安装成功。

### 使用方式

**交互模式**：
```
用户：帮我分析这个功能
→ AI 自动进入 P1 分析
→ 输出分析报告
→ 等待用户确认后进入 P2/P3
```

**全自动模式**：
```
用户：全程自动化，开发注册功能
→ AI 自动完成 P1→P2→P3 全流程
→ 自动调用技能（plan-down、codex、gemini）
→ 生成 auto_log.md 决策日志
```

---

## ⚙️ 详细配置说明

### Zen MCP Server 配置

#### 1. 配置 API Keys

编辑 `zen-mcp-server/.env` 文件：

```bash
# OpenAI API Key（必需，用于 codex-code-reviewer）
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_ALLOWED_MODELS=gpt-4,gpt-4-turbo,o1-mini,o1-preview

# Google Gemini API Key（可选，用于 simple-gemini 和 deep-gemini）
GEMINI_API_KEY=your-gemini-api-key-here

# 其他配置
DISABLED_TOOLS=  # 删除 docgen 以启用文档生成
```

> 📌 **获取 API Key**：
> - OpenAI: https://platform.openai.com/api-keys
> - Google Gemini: https://makersuite.google.com/app/apikey

#### 2. 配置 Claude Desktop

编辑 Claude Desktop 的 MCP 配置文件：

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

添加 Zen MCP Server：

```json
{
  "mcpServers": {
    "zen": {
      "command": "node",
      "args": ["/path/to/zen-mcp-server/build/index.js"],
      "env": {
        "OPENAI_API_KEY": "sk-your-key-here",
        "GEMINI_API_KEY": "your-gemini-key-here"
      }
    }
  }
}
```

### 可选 CLI 工具安装

> ⚠️ **前置要求**：安装前请确保已在环境变量中配置相关 API Keys（`OPENAI_API_KEY`、`GEMINI_API_KEY`）

#### Gemini CLI

用于文档生成和深度技术分析。

```bash
npm install -g @google/gemini-cli
```

**参考文档**：[google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)

#### Codex CLI

用于代码质量审查和 5 维度检查。

```bash
npm install -g @openai/codex
```

**参考文档**：[openai/codex](https://github.com/openai/codex)

**验证安装**：

```bash
# 检查 Gemini CLI
gemini --version

# 检查 Codex CLI
codex --version
```
### 配置文件优先级

系统按以下优先级读取配置：

1. **环境变量**（最高优先级）
2. **`.env` 文件**（zen-mcp-server 目录）
3. **MCP 配置**（claude_desktop_config.json）
4. **CLI 工具配置**（~/.openai/config, gemini config）

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| [AGENTS.md](AGENTS.md) | 全局规则和 P1-P4 阶段定义 |
| [PROJECTWIKI.md](PROJECTWIKI.md) | 项目知识库和详细文档 |
| [CHANGELOG.md](CHANGELOG.md) | 变更日志 |

---

## 💡 主要规则

1. **强制技能使用**
   - 生成 plan.md → 必须用 plan-down
   - 代码完成后 → 必须用 codex-code-reviewer
   - 生成文档 → 必须用 simple-gemini

2. **文档一等公民**
   - 代码变更时必须同步更新 PROJECTWIKI.md 和 CHANGELOG.md
   - 建立代码与文档的双向链接

3. **低风险执行**
   - P3 执行前需满足：代码≤200行、文件≤5个、无破坏性变更

---

## 📄 许可证

MIT License

---

## 🙏 致谢

感谢以下项目和贡献者：

- **[HelloAgents](https://github.com/hellowind777/helloagents)** - 提供了 AGENTS.md 规范和多阶段工作流设计
- **[Zen MCP Server](https://github.com/BeehiveInnovations/zen-mcp-server)** - 提供了 MCP 服务器实现和技能包架构参考

