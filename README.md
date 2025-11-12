# Claude Code Zen MCP Skill Work

> 🚀 一键安装的 AI 编程智能体技能包 - 自动下载 Zen MCP + 5 个核心技能

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen.svg)](https://nodejs.org/)

---

## ✨ 核心特性

- 📦 **开箱即用** - 包含 Zen MCP Server，一次克隆全部搞定
- 🧠 **智能路由** - 自动选择最佳技能处理任务
- 📊 **多阶段工作流** - P1(分析) → P2(方案) → P3(执行) → P4(修复)
- 🔍 **5 维代码审查** - 质量、安全、性能、架构、文档全方位检查
- 📝 **文档自动生成** - README、测试代码、项目知识库
- 🌍 **跨平台支持** - Windows / macOS / Linux 全平台 （可能）

---

> ⚠️ **重要提示**  
> 配置 OpenAI API Key 后，请务必在 `OPENAI_ALLOWED_MODELS` 中指定允许的模型列表（如 `gpt-5,gpt-4-turbo,o1`）。  
> 如果留空或未配置，系统可能会默认使用 GPT-5-Pro 等高成本模型，导致意外费用。

## 🚀 快速开始

### 环境要求

**可选**：
- ✅ [Claude Desktop](https://claude.ai/download)
- ✅ [Node.js](https://nodejs.org/) >= 14.0.0
- ✅ [Python](https://www.python.org/) >= 3.8（Zen MCP Server 需要）
- ✅ [Git](https://git-scm.com/downloads)（如果从 GitHub 克隆）

### 安装方式

#### 方式 1: 手动安装（推荐，最稳定）

##### Linux / macOS 用户

```bash
# 1. 下载本项目（已包含 Zen MCP Server）
git clone https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work.git
cd Claude-Code-Zen-mcp-Skill-Work

# 2. 复制并安装 Zen MCP Server（Python 项目）
cp -r zen-mcp-server ~/zen-mcp-server
cd ~/zen-mcp-server
pip3 install -r requirements.txt

# 3. 复制技能包到 Claude 配置目录
cd -  # 返回项目目录

# ⚠️ 重要：先创建目标目录
mkdir -p ~/.claude/skills

# 检查是否已有技能包，建议手动合并避免覆盖
if [ -d ~/.claude/skills/main-router ]; then
    echo "⚠️  检测到已有技能包，请手动检查是否需要备份"
fi

# 复制所有技能包到 Claude 配置目录
cp -r skills/* ~/.claude/skills/

# 4. 备份并复制全局配置
if [ -f ~/.claude/CLAUDE.md ]; then
    cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.backup.$(date +%Y%m%d%H%M%S).md
    echo "✅ 已备份现有 CLAUDE.md"
fi
cp CLAUDE.md ~/.claude/CLAUDE.md
```

##### Windows 用户

```powershell
# 1. 下载本项目（已包含 Zen MCP Server）
git clone https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work.git
cd Claude-Code-Zen-mcp-Skill-Work

# 2. 保存项目路径（方便后续返回）
$ProjectDir = Get-Location

# 3. 复制并安装 Zen MCP Server（Python 项目）
Copy-Item -Path "zen-mcp-server" -Destination "$env:USERPROFILE\zen-mcp-server" -Recurse
cd $env:USERPROFILE\zen-mcp-server
pip install -r requirements.txt

# 4. 返回项目目录，复制技能包
cd $ProjectDir

# ⚠️ 重要：先创建目标目录（避免 PowerShell 复制行为异常）
New-Item -ItemType Directory -Path "$env:USERPROFILE\.claude\skills" -Force | Out-Null

# 检查 skills 目录，如果已有技能包建议手动合并
if (Test-Path "$env:USERPROFILE\.claude\skills\main-router") {
    Write-Host "⚠️  检测到已有技能包，请手动检查是否需要备份" -ForegroundColor Yellow
}

# 复制所有技能包到 Claude 配置目录
Copy-Item -Path "skills\*" -Destination "$env:USERPROFILE\.claude\skills\" -Recurse -Force

# 5. 备份并复制全局配置
if (Test-Path "$env:USERPROFILE\.claude\CLAUDE.md") {
    Copy-Item "$env:USERPROFILE\.claude\CLAUDE.md" "$env:USERPROFILE\.claude\CLAUDE.backup.$(Get-Date -Format 'yyyyMMddHHmmss').md"
    Write-Host "✅ 已备份现有 CLAUDE.md" -ForegroundColor Green
}
Copy-Item CLAUDE.md $env:USERPROFILE\.claude\CLAUDE.md -Force
```

#### 方式 2: 自动安装脚本（实验性）

> ⚠️ **注意**：自动安装脚本仅在 NPM 包中，GitHub 版本请使用手动安装

**通过 NPM 安装**：
```bash
npx claude-code-zen-installer
```

**或从 NPM 克隆后运行**：
```bash
npm install -g claude-code-zen-installer
claude-code-zen-installer
```

**📁 最终目录结构**：

```
用户主目录（~/ 或 %USERPROFILE%）
├── zen-mcp-server/              ← Zen MCP Server（与 .claude 同级）
└── .claude/
    ├── skills/                  ← 技能包目录
    │   ├── main-router/
    │   ├── plan-down/
    │   ├── codex-code-reviewer/
    │   ├── simple-gemini/
    │   └── deep-gemini/
    └── CLAUDE.md                ← 全局规则
```

---

## ⚙️ 配置

### 1. 配置 Zen MCP Server

编辑 `~/zen-mcp-server/.env`：

```bash
# OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# 指定允许的模型（留空表示使用默认模型，避免意外使用 gpt-5-pro）
OPENAI_ALLOWED_MODELS=gpt-4,gpt-4-turbo,o1-mini,o1-preview

# Google Gemini API Key（用于文档生成）
GEMINI_API_KEY=your-gemini-api-key-here

# 启用所有工具（删除 docgen 以启用文档生成）
DISABLED_TOOLS=
```

> 📌 **获取 API Key**：
> - OpenAI: https://platform.openai.com/api-keys
> - Google Gemini: https://makersuite.google.com/app/apikey

### 2. 配置 Claude Desktop

编辑 Claude Desktop 的 MCP 配置文件：

**配置文件路径**：
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**配置内容**（参考）：

```json
{
  "mcpServers": {
    "zen": {
      "command": "python3",
      "args": ["/path/to/zen-mcp-server/server.py"],
      "env": {
        "OPENAI_API_KEY": "sk-your-key-here",
        "GEMINI_API_KEY": "your-gemini-key-here"
      }
    }
  }
}
```

> 💡 **注意**：
> - Linux/Mac 使用 `python3`
> - Windows 使用 `python` 或 `python3`（取决于安装方式）
> - 路径示例：
>   - Linux/Mac: `"/home/username/zen-mcp-server/server.py"`
>   - Windows: `"C:/Users/Username/zen-mcp-server/server.py"`

> 💡 **详细配置说明**：请参考 [Zen MCP Server 文档](https://github.com/BeehiveInnovations/zen-mcp-server)

### 3. 启动 Zen MCP Server

```bash
cd ~/zen-mcp-server

# 推荐：使用启动脚本（自动配置环境）
# Linux/Mac 用户
chmod +x run-server.sh
./run-server.sh

# Windows 用户
.\run-server.ps1

# 或直接运行
python3 server.py        # Linux/Mac
python server.py         # Windows
```

### 4. 重启 Claude Desktop

完全关闭 Claude Desktop，然后重新启动。

---

## ✅ 验证安装

启动 Claude Desktop，输入：

```
请使用 main-router 帮我分析当前可用的技能
```

**预期结果**：应该看到 5 个技能包的详细说明。

---

## 📖 使用方式

### 交互模式（默认）

```
用户：帮我分析这个功能
→ AI 自动进入 P1 分析
→ 输出分析报告
→ 等待用户确认后进入 P2/P3
```

### 全自动模式

```
用户：全程自动化，开发用户注册功能
→ AI 自动完成 P1→P2→P3 全流程
→ 自动调用技能（plan-down、codex、gemini）
→ 生成 auto_log.md 决策日志
```

---

## 🎯 技能包介绍

| 技能 | 功能 | 何时使用 |
|------|------|---------|
| **main-router** | 智能路由和任务调度 | 所有任务的入口 |
| **plan-down** | 任务分解和计划生成 | 制定开发计划时 |
| **codex-code-reviewer** | 5 维度代码审查 | 代码完成后检查质量 |
| **simple-gemini** | 标准文档生成 | 生成 README、测试代码 |
| **deep-gemini** | 深度技术分析 | 架构分析、性能优化 |

---

## 🛠️ Zen MCP Server 工具使用指南

Zen MCP Server 提供了多个强大的工具，以下是两个核心工具的使用方法：

### 1. ThinkDeep - 深度思考与扩展推理

**功能**：提供扩展推理能力，挑战假设，发现边界情况，为复杂问题提供替代方案。

**核心特性**：
- 🧠 使用 Gemini 的专业思考模型进行增强推理
- 🔍 提供第二意见，挑战 Claude 的分析
- 💡 识别边缘情况和替代视角
- ✅ 验证架构决策和设计模式
- 📄 支持文件引用和图像分析
- 🌐 自动识别需要网络搜索补充的领域

**使用方法**： 
 - 在 Claude 中直接输入类似“使用 clink 工具调用 deepthink 去思考”的指令（告诉 AI 即可）
---

### 2. Clink - CLI 到 CLI 桥接工具

**功能**：连接外部 AI CLI（Gemini CLI、Codex CLI、Claude Code），在现有工作流中复用其能力。

**使用方法**： 
 - 在 Claude 中直接输入类似“使用 clink 工具调用 codex 检查代码”的指令（告诉 AI 即可）

**核心特性**：
- 🔗 连接多个 CLI：在 Codex 中调用 Gemini，在 Gemini 中调用 Codex
- 📦 完整对话连续性：响应参与同一对话线程
- 🎭 基于角色的提示：预配置角色（planner、codereviewer、default）
- 🌐 完整 CLI 能力：Gemini 可使用自己的网络搜索、文件工具
- 💾 Token 效率：文件引用而非完整内容，节省 token
- 🔄 跨工具协作：结合 `planner` → `clink` → `codereview` 形成强大工作流

**可用角色**：

| 角色 | 用途 | 示例 |
|------|------|------|
| `default` | 一般问题、摘要、快速回答 | `"Use clink to ask gemini about React 19 features"` |
| `planner` | 战略规划，多阶段方法 | `"clink with gemini planner to map out microservices migration"` |
| `codereviewer` | 代码分析，关注严重级别 | `"Use clink codereviewer role to review auth.py for security"` |


**配置要求**：

确保相关 CLI 已安装和配置：
- [Claude Code](https://www.anthropic.com/claude-code)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)：`npm install -g @google/gemini-cli`
- [Codex CLI](https://docs.sourcegraph.com/codex)

**⚠️ 安全提示**：

Clink 启动的 CLI 代理具有宽松的权限标志（Gemini 使用 `--yolo`，Codex 使用 `--dangerously-bypass-approvals-and-sandbox`），以便它们可以通过 MCP 自主编辑文件和运行工具。如果这超出了你的需求范围，可以：
- 移除这些标志（CLI 仍可打开/读取文件并报告发现）
- 在角色提示中添加停止词/护栏
- 完全禁用 clink
- 仅在完全信任的工作区中保留预设配置

**工具对比**：

| 工具 | 用途 |
|------|------|
| `clink` | 利用外部 CLI 能力（Gemini 网络搜索、1M 上下文）、跨 CLI 协作 |
| `chat` | Zen 内直接模型到模型对话 |
| `planner` | Zen 原生规划工作流，带步骤验证 |
| `codereview` | Zen 结构化代码审查，带严重级别 |
| `thinkdeep` | 扩展特定分析、挑战假设、架构决策 |

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
- **P2 制定方案** - 设计解决方案，生成 plan.md
- **P3 执行方案** - 实施代码，自动检查质量，生成文档
- **P4 错误处理** - 修复问题，验证修复

---

## 💡 核心规则

### 1. 强制技能使用

- ✅ 生成 plan.md → **必须使用 plan-down**
- ✅ 代码完成后 → **必须使用 codex-code-reviewer**
- ✅ 生成文档 → **必须使用 simple-gemini**

### 2. 文档一等公民

- 代码变更时必须同步更新 `PROJECTWIKI.md` 和 `CHANGELOG.md`
- 建立代码与文档的双向链接

### 3. 低风险执行

- P3 执行前需满足：代码 ≤ 200 行、文件 ≤ 5 个、无破坏性变更

---

## 📁 项目结构

```
Claude-Code-Zen-mcp-Skill-Work/
├── zen-mcp-server/                  # Zen MCP Server（已包含，无需单独下载）
│   ├── server.py                   # MCP 服务器主程序
│   ├── tools/                      # MCP 工具集
│   ├── requirements.txt            # Python 依赖
│   └── ...                         # 其他文件
├── skills/                          # 技能包目录（已解压，可直接复制）
│   ├── main-router/                # 智能路由和技能匹配
│   ├── plan-down/                  # 任务分解和计划生成
│   ├── codex-code-reviewer/        # 代码质量审查
│   ├── simple-gemini/              # 标准文档生成
│   └── deep-gemini/                # 深度技术分析
├── AGENTS.md                        # 全局规则和 P1-P4 阶段定义
├── CLAUDE.md                        # 全局工作流规则
├── LICENSE                          # Apache 2.0 License
└── README.md                        # 项目说明（本文件）

注：install.js/sh/ps1、package.json、QUICKSTART.md、CHANGELOG.md 仅在 NPM 包中
```

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [AGENTS.md](AGENTS.md) | 全局规则和 P1-P4 阶段定义 |
| [CLAUDE.md](CLAUDE.md) | 全局工作流规则（需复制到 `~/.claude/`） |
| [LICENSE](LICENSE) | Apache 2.0 开源许可证 |

**NPM 包专属文档**（仅在 `npx claude-code-zen-installer` 下载的包中）：
- QUICKSTART.md - 3 分钟快速开始指南
- CHANGELOG.md - 版本变更记录

---

## 🔧 高级配置

### 可选：CLI 工具安装

> 
> 以下工具仅在需要本地命令行调试时安装：

**Gemini CLI**：
```bash
npm install -g @google/gemini-cli
```

**Codex CLI**：
```bash
npm install -g @openai/codex
```

---

## ❓ 常见问题

### Q1: 安装后 Claude 无法识别技能？

**检查**：
1. 技能包是否正确复制到 `~/.claude/skills/` 目录
2. 每个技能包文件夹内是否有 `SKILL.md` 文件
3. Claude Desktop 是否已重启

### Q2: Zen MCP Server 连接失败？

**检查**：
1. Zen MCP Server 是否正在运行（`./run-server.sh`）
2. API Keys 是否正确配置
3. Claude Desktop 配置文件中的路径是否正确

### Q3: 技能调用时报错？

**检查**：
1. `.env` 文件中的 `OPENAI_ALLOWED_MODELS` 是否正确配置（留空或指定模型）
2. `DISABLED_TOOLS` 是否为空（启用所有工具）
3. API Keys 是否有足够额度

---

## 🙏 致谢

本项目基于以下优秀项目：

- **[HelloAgents](https://github.com/hellowind777/helloagents)** - 提供了 AGENTS.md 规范和多阶段工作流设计
- **[Zen MCP Server](https://github.com/BeehiveInnovations/zen-mcp-server)** - 提供了 MCP 服务器实现和技能包架构

---

## 📄 许可证

[Apache 2.0 License](LICENSE) - 详见 LICENSE 文件

---

## 🔗 相关链接

- 📦 GitHub 仓库: https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work
- 🐛 问题反馈: https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work/issues
- 📖 Zen MCP Server: https://github.com/BeehiveInnovations/zen-mcp-server
- 📖 HelloAgents: https://github.com/hellowind777/helloagents
