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
$ZenMcpSourceDir = Join-Path $ScriptDir "zen-mcp-server"

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

# 安装 Zen MCP Server（从本地复制）
function Install-ZenMcp {
    Write-Step "安装 Zen MCP Server..."

    if (Test-Path $ZenMcpDir) {
        Write-Warning "Zen MCP Server 目录已存在，跳过安装"
        Write-Info "路径: $ZenMcpDir"
        Write-Info "如需重新安装，请先删除该目录"
        return $true
    }

    # 检查本地是否有 zen-mcp-server
    if (-not (Test-Path $ZenMcpSourceDir)) {
        Write-Error "未找到 zen-mcp-server 目录"
        Write-Info "请确保项目完整克隆"
        return $false
    }

    Write-Info "正在复制 Zen MCP Server..."
    try {
        Copy-Item -Path $ZenMcpSourceDir -Destination $ZenMcpDir -Recurse -Force
        Write-Success "Zen MCP Server 复制完成"

        # 安装依赖（Zen MCP Server 是 Python 项目）
        Write-Info "正在安装 Zen MCP Server Python 依赖..."
        Set-Location $ZenMcpDir
        pip install -r requirements.txt
        Write-Success "Zen MCP Server 依赖安装完成"
        Write-Info "提示: 也可以运行 .\run-server.ps1 自动配置环境"

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

# 安装技能包（直接复制文件夹，无需解压）
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
        $sourceDir = Join-Path $ScriptDir "skills\$skill"
        $targetDir = Join-Path $SkillsDir $skill

        if (-not (Test-Path $sourceDir)) {
            Write-Warning "技能包文件夹不存在: $skill"
            continue
        }

        if (Test-Path $targetDir) {
            Write-Warning "技能包已存在: $skill，跳过安装"
            $successCount++
            continue
        }

        Write-Info "正在安装: $skill..."
        try {
            Copy-Item -Path $sourceDir -Destination $targetDir -Recurse -Force
            Write-Success "$skill 安装完成"
            $successCount++
        } catch {
            Write-Error "$skill 安装失败: $_"
        }
    }

    Write-Success "技能包安装完成 ($successCount/$($skills.Count))"
}

# 安装共享资源（skills/shared + references）
function Install-Shared {
    Write-Step "安装共享资源..."

    $successCount = 0

    # 复制 skills/shared
    $sharedSource = Join-Path $ScriptDir "skills\shared"
    $sharedTarget = Join-Path $SkillsDir "shared"

    if (Test-Path $sharedSource) {
        if (Test-Path $sharedTarget) {
            Write-Warning "skills/shared 已存在，跳过安装"
        } else {
            Write-Info "正在安装 skills/shared..."
            try {
                Copy-Item -Path $sharedSource -Destination $sharedTarget -Recurse -Force
                Write-Success "skills/shared 安装完成"
            } catch {
                Write-Error "skills/shared 安装失败: $_"
            }
        }
        $successCount++
    } else {
        Write-Warning "未找到 skills/shared 目录"
    }

    # 复制 references（全局标准文档）
    $refSource = Join-Path $ScriptDir "references"
    $refTarget = Join-Path $ClaudeConfigDir "references"

    if (Test-Path $refSource) {
        if (Test-Path $refTarget) {
            Write-Warning "references 已存在，跳过安装"
        } else {
            Write-Info "正在安装 references..."
            try {
                Copy-Item -Path $refSource -Destination $refTarget -Recurse -Force
                Write-Success "references 安装完成"
            } catch {
                Write-Error "references 安装失败: $_"
            }
        }
        $successCount++
    } else {
        Write-Warning "未找到 references 目录"
    }

    Write-Success "共享资源安装完成 ($successCount/2)"
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

    # 自动备份已有文件（带时间戳）
    if (Test-Path $targetPath) {
        $timestamp = Get-Date -Format 'yyyyMMddHHmmss'
        $backupPath = Join-Path $ClaudeConfigDir "CLAUDE.backup.$timestamp.md"
        Copy-Item $targetPath $backupPath
        Write-Success "✅ 已备份现有 CLAUDE.md → $backupPath"
    }

    # 复制文件
    Copy-Item $sourcePath $targetPath -Force
    Write-Success "CLAUDE.md 已安装到 $targetPath"
    return $true
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
    Write-Host "2. 启动 Zen MCP Server:"
    Write-Host "   cd $ZenMcpDir" -ForegroundColor Cyan
    Write-Host "   .\run-server.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "3. 验证安装:"
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

    # 步骤 3: 安装共享资源
    Install-Shared

    Write-Host ""

    # 步骤 4: 安装全局配置
    if (-not (Install-GlobalConfig)) {
        Write-Warning "全局配置安装失败，但可继续使用"
    }

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

