# Claude Code Zen - Windows PowerShell 一键安装脚本
# 自动安装 Zen MCP Server + 技能包 + 全局配置

# 设置错误时停止
$ErrorActionPreference = "Stop"

# 颜色函数
function Write-Success { param($msg) Write-Host "✅ $msg" -ForegroundColor Green }
function Write-Error { param($msg) Write-Host "❌ $msg" -ForegroundColor Red }
function Write-Warning { param($msg) Write-Host "⚠️  $msg" -ForegroundColor Yellow }
function Write-Info { param($msg) Write-Host "ℹ️  $msg" -ForegroundColor Blue }
function Write-Step { param($msg) Write-Host "📦 $msg" -ForegroundColor Cyan }

# 配置路径
$HomeDir = $env:USERPROFILE
$ClaudeConfigDir = Join-Path $HomeDir ".claude"
$SkillsDir = Join-Path $ClaudeConfigDir "skills"
$ZenMcpDir = Join-Path $HomeDir "zen-mcp-server"
$ScriptDir = $PSScriptRoot

# Claude Desktop 配置路径
$ClaudeDesktopConfig = Join-Path $env:APPDATA "Claude\claude_desktop_config.json"

# 检查 Git
function Test-Git {
    Write-Step "检查 Git 安装状态..."
    try {
        $gitVersion = git --version
        Write-Success "Git 已安装"
        return $true
    } catch {
        Write-Error "未检测到 Git，请先安装 Git"
        Write-Info "下载地址: https://git-scm.com/downloads"
        return $false
    }
}

# 检查 Node.js
function Test-Node {
    Write-Step "检查 Node.js 版本..."
    try {
        $nodeVersion = node -v
        Write-Success "Node.js 版本: $nodeVersion"
        return $true
    } catch {
        Write-Error "未检测到 Node.js，请先安装 Node.js >= 14.0.0"
        Write-Info "下载地址: https://nodejs.org/"
        return $false
    }
}

# 创建目录
function Ensure-Dir {
    param($Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Success "创建目录: $Path"
    }
}

# 安装 Zen MCP Server
function Install-ZenMcp {
    Write-Step "安装 Zen MCP Server..."

    if (Test-Path $ZenMcpDir) {
        Write-Warning "Zen MCP Server 目录已存在，跳过下载"
        Write-Info "路径: $ZenMcpDir"
        Write-Info "如需重新安装，请先删除该目录"
        return $true
    }

    Write-Info "正在克隆 Zen MCP Server 仓库..."
    try {
        Set-Location $HomeDir
        git clone https://github.com/BeehiveInnovations/zen-mcp-server.git
        Write-Success "Zen MCP Server 下载完成"

        # 安装依赖
        Write-Info "正在安装 Zen MCP Server 依赖..."
        Set-Location $ZenMcpDir
        npm install
        Write-Success "Zen MCP Server 依赖安装完成"

        # 创建 .env 示例文件
        $envPath = Join-Path $ZenMcpDir ".env"
        if (-not (Test-Path $envPath)) {
            $envContent = @"
# Zen MCP Server 配置
# 请填写您的 API Keys

# OpenAI API Key（用于 codex-code-reviewer）
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_ALLOWED_MODELS=gpt-4,gpt-4-turbo,o1-mini,o1-preview

# Google Gemini API Key（用于 simple-gemini 和 deep-gemini）
GEMINI_API_KEY=your-gemini-api-key-here

# 禁用的工具（删除 docgen 以启用文档生成）
DISABLED_TOOLS=
"@
            Set-Content -Path $envPath -Value $envContent
            Write-Success "已创建 .env 配置文件（请填写您的 API Keys）"
            Write-Warning "配置文件路径: $envPath"
        }

        Set-Location $ScriptDir
        return $true
    } catch {
        Write-Error "Zen MCP Server 安装失败: $_"
        Set-Location $ScriptDir
        return $false
    }
}

# 安装技能包
function Install-Skills {
    Write-Step "安装技能包..."

    Ensure-Dir $SkillsDir

    $skills = @(
        "main-router",
        "plan-down",
        "codex-code-reviewer",
        "simple-gemini",
        "deep-gemini"
    )

    $successCount = 0

    foreach ($skill in $skills) {
        $zipFile = Join-Path $ScriptDir "skills\$skill.zip"
        $targetDir = Join-Path $SkillsDir $skill

        if (-not (Test-Path $zipFile)) {
            Write-Warning "技能包不存在: $skill.zip"
            continue
        }

        if (Test-Path $targetDir) {
            Write-Warning "技能包已存在: $skill，跳过安装"
            $successCount++
            continue
        }

        Write-Info "正在安装: $skill..."
        try {
            Expand-Archive -Path $zipFile -DestinationPath $SkillsDir -Force
            Write-Success "$skill 安装完成"
            $successCount++
        } catch {
            Write-Error "$skill 安装失败: $_"
        }
    }

    Write-Success "技能包安装完成 ($successCount/$($skills.Count))"
}

# 安装全局配置
function Install-GlobalConfig {
    Write-Step "安装全局配置 CLAUDE.md..."

    Ensure-Dir $ClaudeConfigDir

    $sourcePath = Join-Path $ScriptDir "CLAUDE.md"
    $targetPath = Join-Path $ClaudeConfigDir "CLAUDE.md"

    if (-not (Test-Path $sourcePath)) {
        Write-Error "CLAUDE.md 源文件不存在"
        return $false
    }

    # 备份已有文件
    if (Test-Path $targetPath) {
        $timestamp = [int][double]::Parse((Get-Date -UFormat %s))
        $backupPath = Join-Path $ClaudeConfigDir "CLAUDE.backup.$timestamp.md"
        Copy-Item $targetPath $backupPath
        Write-Warning "已备份现有配置: $backupPath"
    }

    # 复制文件
    Copy-Item $sourcePath $targetPath -Force
    Write-Success "CLAUDE.md 已安装到 $targetPath"
    return $true
}

# 配置 Claude Desktop
function Configure-ClaudeDesktop {
    Write-Step "配置 Claude Desktop MCP 连接..."

    $configDir = Split-Path $ClaudeDesktopConfig
    Ensure-Dir $configDir

    # 读取或创建配置
    $config = @{}
    if (Test-Path $ClaudeDesktopConfig) {
        try {
            $content = Get-Content $ClaudeDesktopConfig -Raw
            $config = $content | ConvertFrom-Json -AsHashtable
            Write-Info "已读取现有 Claude Desktop 配置"
        } catch {
            Write-Warning "现有配置文件格式错误，将创建新配置"
        }
    }

    # 检查是否已配置 zen
    if ($config.mcpServers -and $config.mcpServers.zen) {
        Write-Warning "Zen MCP Server 已在 Claude Desktop 中配置，跳过"
        return
    }

    # 添加 zen-mcp 配置
    if (-not $config.mcpServers) {
        $config.mcpServers = @{}
    }

    $zenMcpIndexPath = Join-Path $ZenMcpDir "build\index.js"

    $config.mcpServers.zen = @{
        command = "node"
        args = @($zenMcpIndexPath)
        env = @{
            OPENAI_API_KEY = "your-openai-api-key-here"
            GEMINI_API_KEY = "your-gemini-api-key-here"
        }
    }

    # 写入配置
    try {
        $config | ConvertTo-Json -Depth 10 | Set-Content $ClaudeDesktopConfig
        Write-Success "Claude Desktop 配置已更新"
        Write-Warning "⚠️  请在配置文件中填写您的 API Keys:"
        Write-Info "配置文件路径: $ClaudeDesktopConfig"
    } catch {
        Write-Error "配置文件写入失败: $_"
    }
}

# 显示安装后说明
function Show-PostInstallInstructions {
    Write-Host ""
    Write-Host "============================================================"
    Write-Success "🎉 安装完成！"
    Write-Host "============================================================"
    Write-Host ""
    Write-Info "📝 后续步骤:"
    Write-Host ""
    Write-Host "1. 配置 API Keys:"
    Write-Host "   $ZenMcpDir\.env" -ForegroundColor Cyan
    Write-Host "   填写 OPENAI_API_KEY 和 GEMINI_API_KEY"
    Write-Host ""
    Write-Host "2. 更新 Claude Desktop 配置中的 API Keys:"
    Write-Host "   $ClaudeDesktopConfig" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "3. 启动 Zen MCP Server:"
    Write-Host "   cd $ZenMcpDir; npm start" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "4. 重启 Claude Desktop"
    Write-Host ""
    Write-Host "5. 验证安装:"
    Write-Host "   在 Claude 中输入: `"请使用 main-router 帮我分析当前可用的技能`""
    Write-Host ""
    Write-Info "📚 文档和示例:"
    Write-Host "   README: $ScriptDir\README.md" -ForegroundColor Cyan
    Write-Host "   全局规则: $ClaudeConfigDir\CLAUDE.md" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "============================================================"
    Write-Host ""
}

# 主安装流程
function Main {
    Write-Host ""
    Write-Host "============================================================"
    Write-Host "  Claude Code Zen - 一键安装脚本" -ForegroundColor Cyan
    Write-Host "============================================================"
    Write-Host ""

    # 前置检查
    if (-not (Test-Git)) { exit 1 }
    if (-not (Test-Node)) { exit 1 }

    Write-Host ""

    # 步骤 1: 安装 Zen MCP Server
    if (-not (Install-ZenMcp)) {
        Write-Error "Zen MCP Server 安装失败，退出安装"
        exit 1
    }

    Write-Host ""

    # 步骤 2: 安装技能包
    Install-Skills

    Write-Host ""

    # 步骤 3: 安装全局配置
    if (-not (Install-GlobalConfig)) {
        Write-Warning "全局配置安装失败，但可继续使用"
    }

    Write-Host ""

    # 步骤 4: 配置 Claude Desktop（可选）
    Configure-ClaudeDesktop

    Write-Host ""

    # 显示后续步骤
    Show-PostInstallInstructions
}

# 运行安装
try {
    Main
} catch {
    Write-Error "安装过程中出错: $_"
    exit 1
}

