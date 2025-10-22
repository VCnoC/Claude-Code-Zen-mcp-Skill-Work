#!/bin/bash

# Claude Code Zen - Linux/Mac 一键安装脚本
# 自动安装 Zen MCP Server + 技能包 + 全局配置

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 日志函数
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_step() { echo -e "${CYAN}📦 $1${NC}"; }

# 配置路径
HOME_DIR="$HOME"
CLAUDE_CONFIG_DIR="$HOME/.claude"
SKILLS_DIR="$CLAUDE_CONFIG_DIR/skills"
ZEN_MCP_DIR="$HOME/zen-mcp-server"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Claude Desktop 配置路径
if [[ "$OSTYPE" == "darwin"* ]]; then
  CLAUDE_DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
else
  CLAUDE_DESKTOP_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
fi

# 检查 Git
check_git() {
  log_step "检查 Git 安装状态..."
  if command -v git &> /dev/null; then
    log_success "Git 已安装"
    return 0
  else
    log_error "未检测到 Git，请先安装 Git"
    log_info "下载地址: https://git-scm.com/downloads"
    return 1
  fi
}

# 检查 Node.js
check_node() {
  log_step "检查 Node.js 版本..."
  if command -v node &> /dev/null; then
    VERSION=$(node -v)
    log_success "Node.js 版本: $VERSION"
    return 0
  else
    log_error "未检测到 Node.js，请先安装 Node.js >= 14.0.0"
    log_info "下载地址: https://nodejs.org/"
    return 1
  fi
}

# 创建目录
ensure_dir() {
  if [ ! -d "$1" ]; then
    mkdir -p "$1"
    log_success "创建目录: $1"
  fi
}

# 安装 Zen MCP Server
install_zen_mcp() {
  log_step "安装 Zen MCP Server..."

  if [ -d "$ZEN_MCP_DIR" ]; then
    log_warning "Zen MCP Server 目录已存在，跳过下载"
    log_info "路径: $ZEN_MCP_DIR"
    log_info "如需重新安装，请先删除该目录"
    return 0
  fi

  log_info "正在克隆 Zen MCP Server 仓库..."
  git clone https://github.com/BeehiveInnovations/zen-mcp-server.git "$ZEN_MCP_DIR"
  log_success "Zen MCP Server 下载完成"

  # 安装依赖
  log_info "正在安装 Zen MCP Server 依赖..."
  cd "$ZEN_MCP_DIR"
  npm install
  log_success "Zen MCP Server 依赖安装完成"

  # 创建 .env 示例文件
  if [ ! -f "$ZEN_MCP_DIR/.env" ]; then
    cat > "$ZEN_MCP_DIR/.env" << 'EOF'
# Zen MCP Server 配置
# 请填写您的 API Keys

# OpenAI API Key（用于 codex-code-reviewer）
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_ALLOWED_MODELS=gpt-4,gpt-4-turbo,o1-mini,o1-preview

# Google Gemini API Key（用于 simple-gemini 和 deep-gemini）
GEMINI_API_KEY=your-gemini-api-key-here

# 禁用的工具（删除 docgen 以启用文档生成）
DISABLED_TOOLS=
EOF
    log_success "已创建 .env 配置文件（请填写您的 API Keys）"
    log_warning "配置文件路径: $ZEN_MCP_DIR/.env"
  fi

  cd "$SCRIPT_DIR"
}

# 安装技能包
install_skills() {
  log_step "安装技能包..."

  ensure_dir "$SKILLS_DIR"

  SKILLS=(
    "main-router"
    "plan-down"
    "codex-code-reviewer"
    "simple-gemini"
    "deep-gemini"
  )

  SUCCESS_COUNT=0

  for SKILL in "${SKILLS[@]}"; do
    ZIP_FILE="$SCRIPT_DIR/skills/$SKILL.zip"
    TARGET_DIR="$SKILLS_DIR/$SKILL"

    if [ ! -f "$ZIP_FILE" ]; then
      log_warning "技能包不存在: $SKILL.zip"
      continue
    fi

    if [ -d "$TARGET_DIR" ]; then
      log_warning "技能包已存在: $SKILL，跳过安装"
      ((SUCCESS_COUNT++))
      continue
    fi

    log_info "正在安装: $SKILL..."
    unzip -q "$ZIP_FILE" -d "$SKILLS_DIR"
    log_success "$SKILL 安装完成"
    ((SUCCESS_COUNT++))
  done

  log_success "技能包安装完成 ($SUCCESS_COUNT/${#SKILLS[@]})"
}

# 安装全局配置
install_global_config() {
  log_step "安装全局配置 CLAUDE.md..."

  ensure_dir "$CLAUDE_CONFIG_DIR"

  SOURCE_PATH="$SCRIPT_DIR/CLAUDE.md"
  TARGET_PATH="$CLAUDE_CONFIG_DIR/CLAUDE.md"

  if [ ! -f "$SOURCE_PATH" ]; then
    log_error "CLAUDE.md 源文件不存在"
    return 1
  fi

  # 备份已有文件
  if [ -f "$TARGET_PATH" ]; then
    BACKUP_PATH="$CLAUDE_CONFIG_DIR/CLAUDE.backup.$(date +%s).md"
    cp "$TARGET_PATH" "$BACKUP_PATH"
    log_warning "已备份现有配置: $BACKUP_PATH"
  fi

  # 复制文件
  cp "$SOURCE_PATH" "$TARGET_PATH"
  log_success "CLAUDE.md 已安装到 $TARGET_PATH"
}

# 配置 Claude Desktop
configure_claude_desktop() {
  log_step "配置 Claude Desktop MCP 连接..."

  CONFIG_DIR="$(dirname "$CLAUDE_DESKTOP_CONFIG")"
  ensure_dir "$CONFIG_DIR"

  # 创建或更新配置
  if [ -f "$CLAUDE_DESKTOP_CONFIG" ]; then
    log_info "已读取现有 Claude Desktop 配置"
    # 检查是否已配置 zen
    if grep -q '"zen"' "$CLAUDE_DESKTOP_CONFIG"; then
      log_warning "Zen MCP Server 已在 Claude Desktop 中配置，跳过"
      return 0
    fi
  fi

  # 生成配置（简化版，手动编辑更安全）
  log_warning "请手动配置 Claude Desktop:"
  log_info "配置文件路径: $CLAUDE_DESKTOP_CONFIG"
  log_info "添加以下配置:"
  echo ""
  cat << EOF
{
  "mcpServers": {
    "zen": {
      "command": "node",
      "args": ["$ZEN_MCP_DIR/build/index.js"],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key-here",
        "GEMINI_API_KEY": "your-gemini-api-key-here"
      }
    }
  }
}
EOF
  echo ""
}

# 显示安装后说明
show_post_install_instructions() {
  echo ""
  echo "============================================================"
  log_success "🎉 安装完成！"
  echo "============================================================"
  echo ""
  log_info "📝 后续步骤:"
  echo ""
  echo "1. 配置 API Keys:"
  echo "   ${CYAN}$ZEN_MCP_DIR/.env${NC}"
  echo "   填写 OPENAI_API_KEY 和 GEMINI_API_KEY"
  echo ""
  echo "2. 更新 Claude Desktop 配置中的 API Keys:"
  echo "   ${CYAN}$CLAUDE_DESKTOP_CONFIG${NC}"
  echo ""
  echo "3. 启动 Zen MCP Server:"
  echo "   ${CYAN}cd $ZEN_MCP_DIR && ./run-server.sh${NC}"
  echo ""
  echo "4. 重启 Claude Desktop"
  echo ""
  echo "5. 验证安装:"
  echo "   在 Claude 中输入: \"请使用 main-router 帮我分析当前可用的技能\""
  echo ""
  log_info "📚 文档和示例:"
  echo "   README: ${CYAN}$SCRIPT_DIR/README.md${NC}"
  echo "   全局规则: ${CYAN}$CLAUDE_CONFIG_DIR/CLAUDE.md${NC}"
  echo ""
  echo "============================================================"
  echo ""
}

# 主安装流程
main() {
  echo ""
  echo "============================================================"
  echo "${CYAN}  Claude Code Zen - 一键安装脚本${NC}"
  echo "============================================================"
  echo ""

  # 前置检查
  check_git || exit 1
  check_node || exit 1

  echo ""

  # 步骤 1: 安装 Zen MCP Server
  install_zen_mcp || { log_error "Zen MCP Server 安装失败"; exit 1; }

  echo ""

  # 步骤 2: 安装技能包
  install_skills

  echo ""

  # 步骤 3: 安装全局配置
  install_global_config || log_warning "全局配置安装失败，但可继续使用"

  echo ""

  # 步骤 4: 配置 Claude Desktop（可选）
  configure_claude_desktop

  echo ""

  # 显示后续步骤
  show_post_install_instructions
}

# 运行安装
main "$@"

