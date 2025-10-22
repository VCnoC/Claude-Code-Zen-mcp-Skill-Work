#!/bin/bash
# 一键发布脚本 - 发布到 NPM

set -e

echo "📦 准备发布 Claude Code Zen Installer..."
echo ""

# 检查登录状态
echo "🔐 检查 NPM 登录状态..."
if ! npm whoami > /dev/null 2>&1; then
  echo "❌ 未登录 NPM"
  echo "请先运行: npm login"
  exit 1
fi

LOGGED_USER=$(npm whoami)
echo "✅ 已登录为: $LOGGED_USER"
echo ""

# 检查 Git 状态
echo "🔍 检查 Git 状态..."
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️  检测到未提交的更改："
  git status --short
  echo ""
  read -p "是否继续？(y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 取消发布"
    exit 1
  fi
else
  echo "✅ Git 工作目录干净"
fi
echo ""

# 测试打包
echo "📋 检查打包内容..."
npm pack --dry-run
echo ""

# 选择版本类型
echo "📈 选择版本更新类型："
echo "1) patch  (bug 修复, 1.0.0 → 1.0.1)"
echo "2) minor  (新功能, 1.0.0 → 1.1.0)"
echo "3) major  (破坏性变更, 1.0.0 → 2.0.0)"
read -p "请选择 (1/2/3): " -n 1 -r VERSION_TYPE
echo ""

case $VERSION_TYPE in
  1)
    VERSION_BUMP="patch"
    ;;
  2)
    VERSION_BUMP="minor"
    ;;
  3)
    VERSION_BUMP="major"
    ;;
  *)
    echo "❌ 无效选择"
    exit 1
    ;;
esac

# 获取新版本号（预览）
CURRENT_VERSION=$(npm pkg get version | tr -d '"')
echo ""
echo "当前版本: $CURRENT_VERSION"
echo "将更新为: $VERSION_BUMP 版本"
echo ""

# 确认发布
read -p "确认发布到 NPM？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "❌ 取消发布"
  exit 1
fi

# 更新版本
echo "📈 更新版本号..."
npm version $VERSION_BUMP
NEW_VERSION=$(npm pkg get version | tr -d '"')
echo "✅ 版本已更新: $CURRENT_VERSION → $NEW_VERSION"
echo ""

# 发布到 NPM
echo "🚀 发布到 NPM..."
npm publish
echo "✅ 发布成功！"
echo ""

# 推送到 GitHub
echo "⬆️  推送到 GitHub..."
git push origin main --tags
echo "✅ 已推送到 GitHub"
echo ""

# 验证发布
echo "🔍 验证发布..."
npm view claude-code-zen-installer version
echo ""

# 显示成功信息
echo "============================================================"
echo "🎉 发布完成！"
echo "============================================================"
echo ""
echo "📦 包名: claude-code-zen-installer"
echo "📌 版本: $NEW_VERSION"
echo "👤 发布者: $LOGGED_USER"
echo ""
echo "🌐 NPM 页面:"
echo "   https://www.npmjs.com/package/claude-code-zen-installer"
echo ""
echo "📖 使用方法:"
echo "   npx claude-code-zen-installer"
echo "   npm install -g claude-code-zen-installer"
echo ""
echo "✅ 用户可以在 1-2 分钟后使用 npx 安装"
echo ""

