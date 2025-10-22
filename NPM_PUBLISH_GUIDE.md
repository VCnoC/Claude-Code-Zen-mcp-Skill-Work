# NPM 发布指南

> 将 Claude Code Zen Installer 发布到 NPM，让用户可以直接使用 `npx claude-code-zen-installer`

---

## 📋 前置准备

### 1. 注册 NPM 账号

如果还没有 NPM 账号：

1. 访问 https://www.npmjs.com/signup
2. 填写信息：
   - Username（用户名）
   - Email（邮箱）
   - Password（密码）
3. 验证邮箱

### 2. 检查包名是否可用

```bash
# 搜索包名是否已被占用
npm search claude-code-zen-installer
```

如果已被占用，需要修改 `package.json` 中的 `name` 字段：

```json
{
  "name": "@your-username/claude-code-zen-installer",
  // 或
  "name": "claude-code-zen-mcp-installer"
}
```

---

## 🚀 发布步骤

### 步骤 1: 更新 package.json

确保 `package.json` 包含必要信息：

```json
{
  "name": "claude-code-zen-installer",
  "version": "1.0.0",
  "description": "One-click installer for Claude Code Zen MCP Skills - Automatically installs Zen MCP Server, skill packages, and global configurations",
  "main": "install.js",
  "bin": {
    "claude-code-zen-installer": "./install.js",
    "ccz-install": "./install.js"
  },
  "scripts": {
    "install": "node install.js",
    "test": "node install.js --dry-run"
  },
  "keywords": [
    "claude",
    "mcp",
    "ai",
    "skills",
    "code-review",
    "documentation",
    "planning",
    "zen-mcp",
    "installer",
    "automation"
  ],
  "author": "VCnoC",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work.git"
  },
  "homepage": "https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work#readme",
  "bugs": {
    "url": "https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work/issues"
  },
  "engines": {
    "node": ">=14.0.0"
  },
  "files": [
    "install.js",
    "install.sh",
    "install.ps1",
    "skills/",
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    "QUICKSTART.md",
    "CHANGELOG.md"
  ]
}
```

**关键字段说明**：
- `name`: 包名（必须唯一）
- `version`: 版本号（遵循 SemVer 规范）
- `bin`: 可执行命令（让用户可以使用 `npx` 运行）
- `files`: 包含在发布包中的文件（白名单）
- `keywords`: 关键词（方便搜索）
- `repository`: 仓库地址
- `homepage`: 主页地址
- `bugs`: 问题追踪地址

### 步骤 2: 确保 install.js 有正确的 shebang

打开 `install.js`，确保第一行是：

```javascript
#!/usr/bin/env node
```

这样用户可以直接运行脚本，无需 `node` 前缀。

### 步骤 3: 测试本地安装（重要！）

在发布前务必测试：

```bash
# 方法 1: 使用 npm link
npm link

# 然后在另一个目录测试
cd /tmp
claude-code-zen-installer
# 或
npx claude-code-zen-installer

# 测试完成后取消链接
npm unlink -g claude-code-zen-installer
```

```bash
# 方法 2: 使用 npm pack 模拟发布
npm pack

# 这会生成 claude-code-zen-installer-1.0.0.tgz
# 在另一个目录测试
cd /tmp
npm install /path/to/claude-code-zen-installer-1.0.0.tgz

# 测试后删除
rm claude-code-zen-installer-1.0.0.tgz
```

### 步骤 4: 登录 NPM

```bash
# 登录 NPM
npm login

# 输入：
# Username: your-username
# Password: your-password
# Email: your-email@example.com
# 可能需要输入一次性验证码（OTP）如果启用了 2FA

# 验证登录状态
npm whoami
```

### 步骤 5: 发布到 NPM

```bash
# 发布包
npm publish

# 如果包名是 scoped（如 @your-username/package），需要：
npm publish --access public
```

**预期输出**：
```
npm notice
npm notice 📦  claude-code-zen-installer@1.0.0
npm notice === Tarball Contents ===
npm notice 15.2kB install.js
npm notice 8.1kB  install.sh
npm notice 9.3kB  install.ps1
npm notice 2.3kB  package.json
npm notice 12.4kB README.md
npm notice ...
npm notice === Tarball Details ===
npm notice name:          claude-code-zen-installer
npm notice version:       1.0.0
npm notice filename:      claude-code-zen-installer-1.0.0.tgz
npm notice package size:  XXX kB
npm notice unpacked size: XXX kB
npm notice shasum:        ...
npm notice integrity:     ...
npm notice total files:   XX
npm notice
+ claude-code-zen-installer@1.0.0
```

### 步骤 6: 验证发布

```bash
# 搜索您的包
npm search claude-code-zen-installer

# 查看包信息
npm view claude-code-zen-installer

# 在浏览器中查看
# https://www.npmjs.com/package/claude-code-zen-installer
```

### 步骤 7: 测试已发布的包

```bash
# 等待 1-2 分钟让 NPM CDN 同步
# 然后在一个新目录测试

cd /tmp/test-install
npx claude-code-zen-installer

# 或安装后使用
npm install -g claude-code-zen-installer
claude-code-zen-installer
```

---

## 🔄 发布更新版本

### 更新版本号

使用 `npm version` 命令自动更新版本号：

```bash
# 补丁版本（1.0.0 → 1.0.1）：修复 bug
npm version patch

# 次要版本（1.0.0 → 1.1.0）：新增功能，向后兼容
npm version minor

# 主要版本（1.0.0 → 2.0.0）：破坏性变更
npm version major
```

这个命令会：
1. 更新 `package.json` 中的版本号
2. 创建一个 git commit
3. 创建一个 git tag

### 发布更新

```bash
# 更新版本号
npm version patch -m "fix: 修复安装脚本在 Windows 下的路径问题"

# 推送到 GitHub（包括 tag）
git push origin main --tags

# 发布到 NPM
npm publish
```

---

## 📝 最佳实践

### 1. 使用 .npmignore

确保 `.npmignore` 文件排除不必要的文件：

```
# 开发文件
.git/
.gitignore
.vscode/
.idea/

# 测试文件
test/
*.test.js

# 临时文件
temp_extract/
*.log
*.tmp

# 文档草稿
docs/draft/

# 系统文件
.DS_Store
Thumbs.db
```

或使用 `package.json` 中的 `files` 字段（推荐）：

```json
{
  "files": [
    "install.js",
    "install.sh",
    "install.ps1",
    "skills/",
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    "QUICKSTART.md",
    "CHANGELOG.md"
  ]
}
```

### 2. 语义化版本号（SemVer）

遵循 `MAJOR.MINOR.PATCH` 规范：

- **MAJOR（主版本）**: 不兼容的 API 变更
- **MINOR（次版本）**: 向下兼容的功能新增
- **PATCH（补丁版本）**: 向下兼容的 bug 修复

示例：
```
1.0.0 → 1.0.1  (修复 bug)
1.0.1 → 1.1.0  (新增功能)
1.1.0 → 2.0.0  (破坏性变更)
```

### 3. 维护 CHANGELOG.md

每次发布前更新 `CHANGELOG.md`：

```markdown
## [1.0.1] - 2025-01-23

### Fixed
- 修复 Windows PowerShell 脚本路径解析问题
- 修复技能包解压权限错误

## [1.0.0] - 2025-01-22

### Added
- 初始发布
- 一键安装功能
```

### 4. 添加 NPM Badge

在 `README.md` 顶部添加徽章：

```markdown
[![npm version](https://badge.fury.io/js/claude-code-zen-installer.svg)](https://www.npmjs.com/package/claude-code-zen-installer)
[![npm downloads](https://img.shields.io/npm/dm/claude-code-zen-installer.svg)](https://www.npmjs.com/package/claude-code-zen-installer)
[![license](https://img.shields.io/npm/l/claude-code-zen-installer.svg)](https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work/blob/main/LICENSE)
```

### 5. 启用双因素认证（2FA）

为了安全，建议启用 NPM 的 2FA：

```bash
# 启用 2FA（仅发布时需要）
npm profile enable-2fa auth-only

# 启用 2FA（登录和发布都需要）
npm profile enable-2fa auth-and-writes
```

---

## ⚠️ 常见问题

### Q1: 包名已被占用怎么办？

**方案 1**: 使用 scoped package

```json
{
  "name": "@your-username/claude-code-zen-installer"
}
```

发布时需要：
```bash
npm publish --access public
```

**方案 2**: 修改包名

```json
{
  "name": "claude-code-zen-mcp-installer"
}
```

### Q2: 发布失败，提示权限错误？

检查：
1. 是否已登录：`npm whoami`
2. 包名是否已被他人占用
3. 是否有发布权限（如果是 scoped package）

### Q3: 如何撤销已发布的版本？

```bash
# 撤销特定版本（24 小时内）
npm unpublish claude-code-zen-installer@1.0.0

# 撤销整个包（24 小时内，慎用！）
npm unpublish claude-code-zen-installer --force
```

**⚠️ 警告**：
- 只能撤销 24 小时内发布的版本
- 撤销后的版本号不能再次使用
- 不建议撤销已被他人使用的版本

更好的做法是发布一个修复版本：
```bash
npm version patch
npm publish
```

### Q4: 如何弃用某个版本？

```bash
# 标记版本为已弃用
npm deprecate claude-code-zen-installer@1.0.0 "这个版本有严重 bug，请升级到 1.0.1"

# 弃用所有版本
npm deprecate claude-code-zen-installer "此包已不再维护，请使用 new-package"
```

### Q5: 发布的包缺少文件？

检查 `.npmignore` 或 `package.json` 中的 `files` 字段。

测试打包内容：
```bash
npm pack --dry-run
```

---

## 🎯 完整发布流程（推荐）

```bash
# 1. 确保代码已提交
git status
git add .
git commit -m "feat: 添加新功能"

# 2. 测试本地安装
npm link
# 测试...
npm unlink -g claude-code-zen-installer

# 3. 更新 CHANGELOG.md
# 编辑 CHANGELOG.md，添加本次变更

# 4. 更新版本号
npm version patch -m "chore: 发布 v%s"

# 5. 推送到 GitHub
git push origin main --tags

# 6. 发布到 NPM
npm publish

# 7. 验证发布
npm view claude-code-zen-installer

# 8. 测试安装
cd /tmp
npx claude-code-zen-installer@latest
```

---

## 📊 发布后的维护

### 监控下载量

访问 NPM 统计页面：
- https://www.npmjs.com/package/claude-code-zen-installer

### 响应用户反馈

- 关注 GitHub Issues
- 关注 NPM 评论
- 及时修复 bug 并发布更新

### 定期更新依赖

```bash
# 检查过时的依赖
npm outdated

# 更新依赖
npm update

# 或使用 npm-check-updates
npx npm-check-updates -u
npm install
```

---

## ✅ 发布前检查清单

- [ ] `package.json` 信息完整（name, version, description, keywords）
- [ ] `install.js` 第一行有 `#!/usr/bin/env node`
- [ ] `.npmignore` 或 `files` 字段配置正确
- [ ] README.md 包含安装和使用说明
- [ ] CHANGELOG.md 已更新
- [ ] 本地测试通过（`npm link` 或 `npm pack`）
- [ ] 已登录 NPM（`npm whoami`）
- [ ] Git 代码已提交
- [ ] 版本号已更新

---

## 🎉 发布成功后

用户现在可以这样安装：

```bash
# 直接运行（推荐）
npx claude-code-zen-installer

# 或全局安装
npm install -g claude-code-zen-installer
claude-code-zen-installer

# 或使用别名
npx ccz-install
```

---

**祝发布顺利！** 🚀

如有问题，请查看：
- NPM 官方文档: https://docs.npmjs.com/
- NPM CLI 文档: https://docs.npmjs.com/cli/

