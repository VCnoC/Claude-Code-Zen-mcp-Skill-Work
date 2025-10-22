# Windows 用户发布指南

> 在 Windows 上发布到 NPM 的完整步骤

---

## 📍 第一步：打开 PowerShell

1. 按 `Win + X`
2. 选择 "Windows PowerShell" 或 "终端"

或者：
- 在项目文件夹中，按住 `Shift` + 右键
- 选择 "在此处打开 PowerShell 窗口"

---

## 📂 第二步：进入项目目录

```powershell
# 进入项目目录
cd "D:\All_Project\提示词工程\Claude Code Zen mcp Skill Work"

# 验证当前目录
pwd
```

**预期输出**：
```
Path
----
D:\All_Project\提示词工程\Claude Code Zen mcp Skill Work
```

---

## 🔐 第三步：登录 NPM（首次需要）

```powershell
npm login
```

**会提示输入**：
```
Username: your-username
Password: your-password
Email: your-email@example.com
```

如果启用了 2FA（双因素认证），还需要输入验证码。

**验证登录**：
```powershell
npm whoami
```

应该显示您的用户名。

---

## 🧪 第四步：测试打包（可选）

```powershell
# 预览会被发布的文件
npm pack --dry-run
```

**预期输出**：
```
📦  claude-code-zen-installer@1.0.0
Tarball Contents
  47.5kB AGENTS.md
  3.0kB  CHANGELOG.md
  ...
total files: 14
```

---

## 🚀 第五步：发布到 NPM

```powershell
npm publish
```

**预期输出**：
```
+ claude-code-zen-installer@1.0.0
```

---

## ⬆️ 第六步：推送到 GitHub

```powershell
# 如果有未提交的更改，先提交
git add .
git commit -m "chore: 发布 v1.0.0"

# 推送到 GitHub
git push origin main
```

---

## ✅ 第七步：验证发布

```powershell
# 查看 NPM 包信息
npm view claude-code-zen-installer

# 在浏览器中访问
# https://www.npmjs.com/package/claude-code-zen-installer
```

---

## 🔄 更新版本（后续发布）

### 修复 Bug（1.0.0 → 1.0.1）

```powershell
# 更新版本号
npm version patch -m "fix: 修复问题描述"

# 发布
npm publish

# 推送（包括 tags）
git push origin main --tags
```

### 新增功能（1.0.0 → 1.1.0）

```powershell
npm version minor -m "feat: 新功能描述"
npm publish
git push origin main --tags
```

### 破坏性变更（1.0.0 → 2.0.0）

```powershell
npm version major -m "BREAKING CHANGE: 变更描述"
npm publish
git push origin main --tags
```

---

## 📋 完整命令清单（复制粘贴）

```powershell
# 进入项目目录
cd "D:\All_Project\提示词工程\Claude Code Zen mcp Skill Work"

# 登录 NPM（首次）
npm login

# 验证登录
npm whoami

# 测试打包
npm pack --dry-run

# 发布
npm publish

# 提交并推送
git add .
git commit -m "chore: 发布 v1.0.0"
git push origin main

# 后续更新（选择一个）
npm version patch && npm publish && git push --tags    # Bug 修复
npm version minor && npm publish && git push --tags    # 新功能
npm version major && npm publish && git push --tags    # 破坏性变更
```

---

## ❓ 常见问题

### Q1: 提示 "npm login" 失败？

**检查网络**：
```powershell
npm ping
```

**尝试切换镜像源**：
```powershell
# 使用官方源
npm config set registry https://registry.npmjs.org/

# 验证
npm config get registry
```

### Q2: 提示包名已存在？

**检查包名**：
```powershell
npm search claude-code-zen-installer
```

**解决方案**：
1. 使用 scoped package: `@your-username/claude-code-zen-installer`
2. 或更换包名: `claude-code-zen-mcp-installer`

### Q3: Git 推送失败？

**检查远程仓库**：
```powershell
git remote -v
```

**配置远程仓库**（如果还没配置）：
```powershell
git remote add origin https://github.com/VCnoC/Claude-Code-Zen-mcp-Skill-Work.git
```

---

## 🎉 发布成功后

用户可以使用：

```bash
# 直接运行
npx claude-code-zen-installer

# 全局安装
npm install -g claude-code-zen-installer
claude-code-zen-installer

# 使用别名
npx ccz-install
```

---

## 📞 需要帮助？

查看完整指南：
- [NPM_PUBLISH_GUIDE.md](NPM_PUBLISH_GUIDE.md) - 详细发布指南
- [QUICK_PUBLISH.md](QUICK_PUBLISH.md) - 快速命令清单

---

**祝发布顺利！** 🚀

