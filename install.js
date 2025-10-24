#!/usr/bin/env node

/**
 * Claude Code Zen - 一键安装脚本
 * 自动安装 Zen MCP Server + 技能包 + 全局配置
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');
const os = require('os');

// 颜色输出（简化版，避免依赖）
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

const log = {
  success: (msg) => console.log(`${colors.green}✅ ${msg}${colors.reset}`),
  error: (msg) => console.log(`${colors.red}❌ ${msg}${colors.reset}`),
  warning: (msg) => console.log(`${colors.yellow}⚠️  ${msg}${colors.reset}`),
  info: (msg) => console.log(`${colors.blue}ℹ️  ${msg}${colors.reset}`),
  step: (msg) => console.log(`${colors.cyan}📦 ${msg}${colors.reset}`),
};

// 检测操作系统
const platform = os.platform();
const isWindows = platform === 'win32';
const isMac = platform === 'darwin';
const isLinux = platform === 'linux';

// 配置路径
const homeDir = os.homedir();
const claudeConfigDir = path.join(homeDir, '.claude');
const skillsDir = path.join(claudeConfigDir, 'skills');
const zenMcpDir = path.join(homeDir, 'zen-mcp-server');
const zenMcpSourceDir = path.join(__dirname, 'zen-mcp-server');

// Claude Desktop 配置路径
const claudeDesktopConfigPath = isWindows
  ? path.join(process.env.APPDATA, 'Claude', 'claude_desktop_config.json')
  : isMac
  ? path.join(homeDir, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json')
  : path.join(homeDir, '.config', 'Claude', 'claude_desktop_config.json');

/**
 * 执行命令（跨平台）
 */
function runCommand(command, cwd = process.cwd(), options = {}) {
  try {
    const result = execSync(command, {
      cwd,
      stdio: options.silent ? 'pipe' : 'inherit',
      encoding: 'utf-8',
      shell: isWindows ? 'powershell.exe' : '/bin/bash',
      ...options,
    });
    return { success: true, output: result };
  } catch (error) {
    return { success: false, error: error.message, output: error.stdout };
  }
}

/**
 * 检查 Git 是否安装
 */
function checkGit() {
  log.step('检查 Git 安装状态...');
  const result = runCommand('git --version', process.cwd(), { silent: true });
  if (result.success) {
    log.success('Git 已安装');
    return true;
  } else {
    log.error('未检测到 Git，请先安装 Git');
    log.info('下载地址: https://git-scm.com/downloads');
    return false;
  }
}

/**
 * 检查 Node.js 版本
 */
function checkNodeVersion() {
  log.step('检查 Node.js 版本...');
  const version = process.version;
  const majorVersion = parseInt(version.slice(1).split('.')[0]);
  if (majorVersion >= 14) {
    log.success(`Node.js 版本: ${version}`);
    return true;
  } else {
    log.error(`Node.js 版本过低: ${version}，需要 >= 14.0.0`);
    return false;
  }
}

/**
 * 创建目录（如果不存在）
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    log.success(`创建目录: ${dirPath}`);
  }
}

/**
 * 安装 Zen MCP Server（从本地复制，无需下载）
 */
function installZenMcp() {
  log.step('安装 Zen MCP Server...');

  if (fs.existsSync(zenMcpDir)) {
    log.warning('Zen MCP Server 目录已存在，跳过安装');
    log.info(`路径: ${zenMcpDir}`);
    log.info('如需重新安装，请先删除该目录');
    return true;
  }

  // 检查本地是否有 zen-mcp-server
  if (!fs.existsSync(zenMcpSourceDir)) {
    log.error('未找到 zen-mcp-server 目录');
    log.info('请确保项目完整克隆');
    return false;
  }

  log.info('正在复制 Zen MCP Server...');
  try {
    // 递归复制整个目录
    copyRecursiveSync(zenMcpSourceDir, zenMcpDir);
    log.success('Zen MCP Server 复制完成');

    // 安装依赖
    log.info('正在安装 Zen MCP Server 依赖...');
    const installResult = runCommand('npm install', zenMcpDir);

    if (installResult.success) {
      log.success('Zen MCP Server 依赖安装完成');

      // 创建 .env 示例文件（如果不存在）
      const envPath = path.join(zenMcpDir, '.env');
      if (!fs.existsSync(envPath)) {
        const envExample = `# Zen MCP Server 配置
# 请填写您的 API Keys

# OpenAI API Key（用于 codex-code-reviewer）
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_ALLOWED_MODELS=gpt-4,gpt-4-turbo,o1-mini,o1-preview

# Google Gemini API Key（用于 simple-gemini 和 deep-gemini）
GEMINI_API_KEY=your-gemini-api-key-here

# 禁用的工具（删除 docgen 以启用文档生成）
DISABLED_TOOLS=
`;
        fs.writeFileSync(envPath, envExample);
        log.success('已创建 .env 配置文件（请填写您的 API Keys）');
        log.warning(`配置文件路径: ${envPath}`);
      }

      return true;
    } else {
      log.error('Zen MCP Server 依赖安装失败');
      return false;
    }
  } else {
    log.error('Zen MCP Server 下载失败');
    return false;
  }
}

/**
 * 复制技能包文件夹（直接复制，无需解压）
 */
function installSkills() {
  log.step('安装技能包...');

  ensureDir(skillsDir);

  const skillsSourceDir = path.join(__dirname, 'skills');
  const skillFolders = [
    'main-router',
    'plan-down',
    'codex-code-reviewer',
    'simple-gemini',
    'deep-gemini',
  ];

  let successCount = 0;

  for (const skillName of skillFolders) {
    const sourceDir = path.join(skillsSourceDir, skillName);
    const targetDir = path.join(skillsDir, skillName);

    // 检查源文件夹是否存在
    if (!fs.existsSync(sourceDir)) {
      log.warning(`技能包文件夹不存在: ${skillName}`);
      continue;
    }

    // 检查是否已安装
    if (fs.existsSync(targetDir)) {
      log.warning(`技能包已存在: ${skillName}，跳过安装`);
      successCount++;
      continue;
    }

    // 复制文件夹（跨平台）
    log.info(`正在安装: ${skillName}...`);
    try {
      // 使用递归复制
      copyRecursiveSync(sourceDir, targetDir);
      log.success(`${skillName} 安装完成`);
      successCount++;
    } catch (error) {
      log.error(`${skillName} 安装失败: ${error.message}`);
    }
  }

  log.success(`技能包安装完成 (${successCount}/${skillFolders.length})`);
  return successCount > 0;
}

/**
 * 递归复制文件夹
 */
function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();

  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

/**
 * 安装全局配置 CLAUDE.md
 */
function installGlobalConfig() {
  log.step('安装全局配置 CLAUDE.md...');

  ensureDir(claudeConfigDir);

  const sourcePath = path.join(__dirname, 'CLAUDE.md');
  const targetPath = path.join(claudeConfigDir, 'CLAUDE.md');

  if (!fs.existsSync(sourcePath)) {
    log.error('CLAUDE.md 源文件不存在');
    return false;
  }

  // 备份已有文件
  if (fs.existsSync(targetPath)) {
    const backupPath = path.join(claudeConfigDir, `CLAUDE.backup.${Date.now()}.md`);
    fs.copyFileSync(targetPath, backupPath);
    log.warning(`已备份现有配置: ${backupPath}`);
  }

  // 复制文件
  fs.copyFileSync(sourcePath, targetPath);
  log.success(`CLAUDE.md 已安装到 ${targetPath}`);

  return true;
}

/**
 * 配置 Claude Desktop MCP 连接（可选）
 */
function configureClaudeDesktop() {
  log.step('配置 Claude Desktop MCP 连接...');

  const configDir = path.dirname(claudeDesktopConfigPath);
  ensureDir(configDir);

  let config = {};

  // 读取现有配置
  if (fs.existsSync(claudeDesktopConfigPath)) {
    try {
      const content = fs.readFileSync(claudeDesktopConfigPath, 'utf-8');
      config = JSON.parse(content);
      log.info('已读取现有 Claude Desktop 配置');
    } catch (error) {
      log.warning('现有配置文件格式错误，将创建新配置');
    }
  }

  // 检查是否已配置 zen-mcp
  if (config.mcpServers && config.mcpServers.zen) {
    log.warning('Zen MCP Server 已在 Claude Desktop 中配置，跳过');
    return true;
  }

  // 添加 zen-mcp 配置
  if (!config.mcpServers) {
    config.mcpServers = {};
  }

  const zenMcpIndexPath = path.join(zenMcpDir, 'build', 'index.js');

  config.mcpServers.zen = {
    command: 'node',
    args: [zenMcpIndexPath],
    env: {
      OPENAI_API_KEY: 'your-openai-api-key-here',
      GEMINI_API_KEY: 'your-gemini-api-key-here',
    },
  };

  // 写入配置
  try {
    fs.writeFileSync(claudeDesktopConfigPath, JSON.stringify(config, null, 2));
    log.success('Claude Desktop 配置已更新');
    log.warning('⚠️  请在配置文件中填写您的 API Keys:');
    log.info(`配置文件路径: ${claudeDesktopConfigPath}`);
    return true;
  } catch (error) {
    log.error(`配置文件写入失败: ${error.message}`);
    return false;
  }
}

/**
 * 显示安装后说明
 */
function showPostInstallInstructions() {
  console.log('\n' + '='.repeat(60));
  log.success('🎉 安装完成！');
  console.log('='.repeat(60) + '\n');

  log.info('📝 后续步骤:');
  console.log('');
  console.log('1. 配置 API Keys:');
  console.log(`   ${colors.cyan}${path.join(zenMcpDir, '.env')}${colors.reset}`);
  console.log('   填写 OPENAI_API_KEY 和 GEMINI_API_KEY');
  console.log('');
  console.log('2. 更新 Claude Desktop 配置中的 API Keys:');
  console.log(`   ${colors.cyan}${claudeDesktopConfigPath}${colors.reset}`);
  console.log('');
  console.log('3. 启动 Zen MCP Server:');
  if (isWindows) {
    console.log(`   ${colors.cyan}cd ${zenMcpDir} && npm start${colors.reset}`);
  } else {
    console.log(`   ${colors.cyan}cd ${zenMcpDir} && ./run-server.sh${colors.reset}`);
  }
  console.log('');
  console.log('4. 重启 Claude Desktop');
  console.log('');
  console.log('5. 验证安装:');
  console.log('   在 Claude 中输入: "请使用 main-router 帮我分析当前可用的技能"');
  console.log('');
  log.info('📚 文档和示例:');
  console.log(`   README: ${colors.cyan}${path.join(__dirname, 'README.md')}${colors.reset}`);
  console.log(`   全局规则: ${colors.cyan}${path.join(claudeConfigDir, 'CLAUDE.md')}${colors.reset}`);
  console.log('');
  console.log('='.repeat(60) + '\n');
}

/**
 * 主安装流程
 */
async function main() {
  console.log('\n' + '='.repeat(60));
  console.log(`${colors.cyan}  Claude Code Zen - 一键安装脚本${colors.reset}`);
  console.log('='.repeat(60) + '\n');

  // 前置检查
  if (!checkNodeVersion()) {
    process.exit(1);
  }

  if (!checkGit()) {
    process.exit(1);
  }

  console.log('');

  // 步骤 1: 安装 Zen MCP Server
  if (!installZenMcp()) {
    log.error('Zen MCP Server 安装失败，退出安装');
    process.exit(1);
  }

  console.log('');

  // 步骤 2: 安装技能包
  if (!installSkills()) {
    log.error('技能包安装失败，退出安装');
    process.exit(1);
  }

  console.log('');

  // 步骤 3: 安装全局配置
  if (!installGlobalConfig()) {
    log.warning('全局配置安装失败，但可继续使用');
  }

  console.log('');

  // 步骤 4: 配置 Claude Desktop（可选）
  configureClaudeDesktop();

  console.log('');

  // 显示后续步骤
  showPostInstallInstructions();
}

// 运行安装
main().catch((error) => {
  log.error(`安装过程中出错: ${error.message}`);
  process.exit(1);
});

