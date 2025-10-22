# 🚀 快速发布到 NPM

> 一键命令清单，用于快速发布新版本

---

## ⚡ 超快速发布（5 步）

```bash
# 1. 登录 NPM（首次需要）
npm login

# 2. 测试打包内容
npm pack --dry-run

# 3. 更新版本并发布
npm version patch && npm publish && git push --tags

# 4. 验证
npm view claude-code-zen-installer

# 5. 测试
npx claude-code-zen-installer@latest
```

---

## 📋 标准发布流程

### 首次发布

```bash
# 1. 检查包名是否可用
npm search claude-code-zen-installer

# 2. 登录 NPM
npm login
# 输入用户名、密码、邮箱

# 3. 验证登录
npm whoami

# 4. 测试本地打包
npm pack
# 检查生成的 .tgz 文件

# 5. 发布
npm publish

# 6. 验证发布
npm view claude-code-zen-installer

# 7. 测试安装
cd /tmp
npx claude-code-zen-installer
```

### 发布更新版本

```bash
# 修复 bug（1.0.0 → 1.0.1）
npm version patch -m "fix: 修复问题描述"
npm publish
git push origin main --tags

# 新增功能（1.0.0 → 1.1.0）
npm version minor -m "feat: 新功能描述"
npm publish
git push origin main --tags

# 破坏性变更（1.0.0 → 2.0.0）
npm version major -m "BREAKING CHANGE: 变更描述"
npm publish
git push origin main --tags
```

---

## 🔍 发布前检查

```bash
# 检查哪些文件会被发布
npm pack --dry-run

# 检查 package.json 配置
npm pkg get name version files

# 检查登录状态
npm whoami

# 测试本地链接
npm link
claude-code-zen-installer --help
npm unlink -g claude-code-zen-installer
```

---

## ⚠️ 常用命令

### 查看包信息

```bash
# 查看包详情
npm view claude-code-zen-installer

# 查看所有版本
npm view claude-code-zen-installer versions

# 查看最新版本
npm view claude-code-zen-installer version

# 查看下载统计
npm view claude-code-zen-installer downloads
```

### 管理版本

```bash
# 查看当前版本
npm version

# 弃用某个版本
npm deprecate claude-code-zen-installer@1.0.0 "请升级到最新版本"

# 撤销发布（24小时内）
npm unpublish claude-code-zen-installer@1.0.0
```

### 安全和权限

```bash
# 启用 2FA
npm profile enable-2fa auth-only

# 查看个人信息
npm profile get

# 查看访问令牌
npm token list
```

---

## 📝 发布前确认

- [ ] 代码已提交到 Git
- [ ] CHANGELOG.md 已更新
- [ ] package.json 版本号正确
- [ ] README.md 已更新
- [ ] 本地测试通过
- [ ] 已登录 NPM

---

## 🎯 完整发布命令（推荐）

```bash
#!/bin/bash
# publish.sh - 一键发布脚本

set -e

echo "📦 准备发布..."

# 检查登录状态
if ! npm whoami > /dev/null 2>&1; then
  echo "❌ 未登录 NPM，请先运行: npm login"
  exit 1
fi

# 检查 Git 状态
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️  有未提交的更改，请先提交"
  exit 1
fi

# 测试打包
echo "🔍 检查打包内容..."
npm pack --dry-run

# 确认发布
read -p "确认发布？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "❌ 取消发布"
  exit 1
fi

# 更新版本（补丁）
echo "📈 更新版本号..."
npm version patch

# 发布
echo "🚀 发布到 NPM..."
npm publish

# 推送到 GitHub
echo "⬆️  推送到 GitHub..."
git push origin main --tags

# 验证
echo "✅ 验证发布..."
npm view claude-code-zen-installer

echo "🎉 发布成功！"
echo "访问: https://www.npmjs.com/package/claude-code-zen-installer"
```

保存为 `publish.sh` 并添加可执行权限：

```bash
chmod +x publish.sh
./publish.sh
```

---

## 🐛 常见问题

### 包名已被占用

```bash
# 使用 scoped package
npm init --scope=@your-username

# 修改 package.json
{
  "name": "@your-username/claude-code-zen-installer"
}

# 发布时指定公开访问
npm publish --access public
```

### 发布失败

```bash
# 检查登录状态
npm whoami

# 重新登录
npm logout
npm login

# 检查网络
npm ping
```

### 撤销错误的发布

```bash
# 24 小时内可以撤销
npm unpublish claude-code-zen-installer@1.0.1

# 或标记为弃用
npm deprecate claude-code-zen-installer@1.0.1 "此版本有问题，请使用 1.0.2"
```

---

## 📊 发布后验证

```bash
# 等待 1-2 分钟，然后测试
cd /tmp/test-npm-install

# 测试 npx
npx claude-code-zen-installer@latest

# 测试全局安装
npm install -g claude-code-zen-installer@latest
claude-code-zen-installer

# 测试别名
npx ccz-install@latest

# 清理
npm uninstall -g claude-code-zen-installer
```

---

## 🎉 发布成功！

用户现在可以：

```bash
# 直接运行
npx claude-code-zen-installer

# 或全局安装
npm install -g claude-code-zen-installer
claude-code-zen-installer

# 或使用别名
npx ccz-install
```

NPM 包页面：
https://www.npmjs.com/package/claude-code-zen-installer

---

## 📚 相关文档

- [NPM_PUBLISH_GUIDE.md](NPM_PUBLISH_GUIDE.md) - 完整发布指南
- [CHANGELOG.md](CHANGELOG.md) - 版本变更记录
- [README.md](README.md) - 项目文档

---

**祝发布顺利！** 🚀

