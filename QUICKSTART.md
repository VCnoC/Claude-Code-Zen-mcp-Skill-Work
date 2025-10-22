# 快速开始指南

> 3 分钟完成 Claude Code Zen 完整安装

## 🎯 安装前准备

请确保已安装：
- ✅ [Claude Desktop](https://claude.ai/download)
- ✅ [Git](https://git-scm.com/downloads)
- ✅ [Node.js](https://nodejs.org/) >= 14.0.0

---

## 🚀 一键安装（推荐）

### Windows 用户

```powershell
# 1. 克隆项目
git clone https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work.git
cd Claude-Code-Zen-mcp-Skill-Work

# 2. 运行安装脚本
.\install.ps1

# 等待安装完成（约 2-3 分钟）
```

### macOS/Linux 用户

```bash
# 1. 克隆项目
git clone https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work.git
cd Claude-Code-Zen-mcp-Skill-Work

# 2. 运行安装脚本
chmod +x install.sh
./install.sh

# 等待安装完成（约 2-3 分钟）
```

### 使用 NPM（推荐，无需克隆）

```bash
# 直接运行（推荐）
npx claude-code-zen-installer

# 或克隆后安装
git clone https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work.git
cd Claude-Code-Zen-mcp-Skill-Work
npm install
node install.js
```

---

## ⚙️ 配置 API Keys（必需）

安装完成后，需要配置 API Keys：

### 1. 配置 Zen MCP Server

编辑 `~/zen-mcp-server/.env`（Windows: `%USERPROFILE%\zen-mcp-server\.env`）：

```bash
# OpenAI API Key（用于代码审查）
OPENAI_API_KEY=sk-your-openai-api-key-here

# Gemini API Key（用于文档生成）
GEMINI_API_KEY=your-gemini-api-key-here
```

**获取 API Keys**：
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://makersuite.google.com/app/apikey

### 2. 配置 Claude Desktop

编辑 Claude Desktop 配置文件中的 API Keys：

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

找到 `"zen"` 部分，填写您的 API Keys：

```json
{
  "mcpServers": {
    "zen": {
      "command": "node",
      "args": ["C:/Users/YourName/zen-mcp-server/build/index.js"],
      "env": {
        "OPENAI_API_KEY": "sk-your-openai-api-key-here",
        "GEMINI_API_KEY": "your-gemini-api-key-here"
      }
    }
  }
}
```

---

## 🎬 启动服务

### 1. 启动 Zen MCP Server

```bash
# Windows
cd %USERPROFILE%\zen-mcp-server
npm start

# macOS/Linux
cd ~/zen-mcp-server
npm start
```

**预期输出**：
```
Zen MCP Server running on port 3000
✅ OpenAI API Key configured
✅ Gemini API Key configured
```

### 2. 重启 Claude Desktop

完全关闭 Claude Desktop，然后重新启动。

---

## ✅ 验证安装

在 Claude Desktop 中输入：

```
请使用 main-router 帮我分析当前可用的技能
```

**预期回复**：应该看到 5 个技能包的说明：
1. ✅ main-router - 智能路由
2. ✅ plan-down - 任务规划
3. ✅ codex-code-reviewer - 代码审查
4. ✅ simple-gemini - 文档生成
5. ✅ deep-gemini - 深度分析

如果看到以上输出，**恭喜！安装成功！** 🎉

---

## 🧪 快速测试

尝试以下命令测试各个技能：

### 1. 测试代码审查
```
使用 codex 帮我检查这段代码的质量
```

### 2. 测试文档生成
```
使用 gemini 生成一个 README 文档
```

### 3. 测试任务规划
```
帮我制定一个用户登录功能的开发计划
```

### 4. 测试智能路由
```
全程自动化，帮我分析这个项目并生成文档
```

---

## ❓ 常见问题

### Q1: Zen MCP Server 启动失败？

**检查**：
- ✅ API Keys 是否正确填写
- ✅ Node.js 版本是否 >= 14.0.0
- ✅ 端口 3000 是否被占用

**解决方案**：
```bash
# 检查 Node.js 版本
node -v

# 检查端口占用
netstat -ano | findstr :3000   # Windows
lsof -i :3000                  # macOS/Linux

# 查看错误日志
cd ~/zen-mcp-server
npm start
```

### Q2: Claude 无法识别技能包？

**检查**：
- ✅ 技能包是否正确解压到 `~/.claude/skills/`
- ✅ 每个技能包是否包含 `SKILL.md` 文件
- ✅ Claude Desktop 是否已重启

**解决方案**：
```bash
# 检查技能包目录
ls ~/.claude/skills/         # macOS/Linux
dir %USERPROFILE%\.claude\skills\   # Windows

# 应该看到 5 个文件夹：
# main-router/
# plan-down/
# codex-code-reviewer/
# simple-gemini/
# deep-gemini/
```

### Q3: API Keys 不工作？

**检查**：
- ✅ API Key 格式是否正确（OpenAI 以 `sk-` 开头）
- ✅ API Key 是否有足够的额度
- ✅ `.env` 文件和 Claude Desktop 配置是否都已填写

**测试 API Key**：
```bash
# 测试 OpenAI API Key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-your-key-here"

# 测试 Gemini API Key
curl "https://generativelanguage.googleapis.com/v1/models?key=your-key-here"
```

---

## 📚 下一步

安装完成后，建议阅读：
- 📖 [README.md](README.md) - 完整使用指南
- 📖 [AGENTS.md](AGENTS.md) - P1-P4 阶段规则
- 📖 [CLAUDE.md](CLAUDE.md) - 全局工作流规则

---

## 🆘 需要帮助？

如果遇到问题：
1. 📋 查看 [常见问题](#❓-常见问题)
2. 🔍 检查安装日志输出
3. 🐛 提交 Issue: https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work/issues

---

**祝您使用愉快！** 🎉

