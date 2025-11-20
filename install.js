#!/usr/bin/env node

/**
 * Claude Code Zen - 一键安装脚本
 * 自动安装 Zen MCP Server + 技能包 + 全局配置
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

// 检测 dry-run 模式
const isDryRun = process.argv.includes('--dry-run');

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

/**
 * 执行命令（跨平台）
 */
function runCommand(command, cwd = process.cwd(), options = {}) {
  // 环境检查命令即使在 dry-run 下也要实际执行
  const forceRun = options.forceRun || false;

  if (isDryRun && !forceRun) {
    log.info(`[Dry Run] 将执行命令: ${command}`);
    return { success: true, output: '[dry-run] 命令未实际执行' };
  }
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
  const result = runCommand('git --version', process.cwd(), { silent: true, forceRun: true });
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
    if (isDryRun) {
      log.info(`[Dry Run] 将创建目录: ${dirPath}`);
    } else {
      fs.mkdirSync(dirPath, { recursive: true });
      log.success(`创建目录: ${dirPath}`);
    }
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

    // 安装依赖（Zen MCP Server 是 Python 项目）
    log.info('正在安装 Zen MCP Server Python 依赖...');
    const installResult = runCommand('pip3 install -r requirements.txt', zenMcpDir);

    if (installResult.success) {
      log.success('Zen MCP Server 依赖安装完成');
      log.info('提示: 也可以运行 ./run-server.sh 自动配置环境');

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
        if (isDryRun) {
          log.info(`[Dry Run] 将创建 .env 配置文件: ${envPath}`);
        } else {
          fs.writeFileSync(envPath, envExample, { mode: 0o600 });
          log.success('已创建 .env 配置文件（请填写您的 API Keys）');
          log.warning(`配置文件路径: ${envPath}`);
        }
      }

      return true;
    } else {
      log.error('Zen MCP Server 依赖安装失败');
      return false;
    }
  } catch (error) {
    log.error(`Zen MCP Server 安装失败（复制或配置写入出错）: ${error.message}`);
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
  let hasExisting = false;

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
      log.warning(`⚠️  技能包已存在: ${skillName}，将覆盖安装`);
      hasExisting = true;
      // 不跳过，继续覆盖安装
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

  if (hasExisting) {
    log.info('💡 提示: 如果您有自定义的技能包，建议在安装前手动备份');
  }

  log.success(`技能包安装完成 (${successCount}/${skillFolders.length})`);
  return successCount > 0;
}

/**
 * 安装共享资源（skills/shared + references）
 */
function installShared() {
  log.step('安装共享资源...');

  let successCount = 0;

  // 复制 skills/shared
  const sharedSource = path.join(__dirname, 'skills', 'shared');
  const sharedTarget = path.join(skillsDir, 'shared');

  if (fs.existsSync(sharedSource)) {
    if (fs.existsSync(sharedTarget)) {
      log.warning('skills/shared 已存在，跳过安装');
      successCount++;
    } else {
      log.info('正在安装 skills/shared...');
      try {
        copyRecursiveSync(sharedSource, sharedTarget);
        log.success('skills/shared 安装完成');
        successCount++;
      } catch (error) {
        log.error(`skills/shared 安装失败: ${error.message}`);
      }
    }
  } else {
    log.warning('未找到 skills/shared 目录');
  }

  // 复制 references（全局标准文档）
  const refSource = path.join(__dirname, 'references');
  const refTarget = path.join(claudeConfigDir, 'references');

  if (fs.existsSync(refSource)) {
    if (fs.existsSync(refTarget)) {
      log.warning('references 已存在，跳过安装');
      successCount++;
    } else {
      log.info('正在安装 references...');
      try {
        copyRecursiveSync(refSource, refTarget);
        log.success('references 安装完成');
        successCount++;
      } catch (error) {
        log.error(`references 安装失败: ${error.message}`);
      }
    }
  } else {
    log.warning('未找到 references 目录');
  }

  if (successCount === 2) {
    log.success(`共享资源就绪 (${successCount}/2)${isDryRun ? ' [Dry Run]' : ''}`);
  } else if (successCount > 0) {
    log.warning(`共享资源部分就绪 (${successCount}/2)`);
  } else {
    log.error('共享资源均未就绪');
  }
  return successCount > 0;
}

/**
 * 递归复制文件夹
 */
function copyRecursiveSync(src, dest) {
  if (isDryRun) {
    log.info(`[Dry Run] 将复制: ${src} -> ${dest}`);
    return;
  }

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

  // 备份已有文件（自动备份，带时间戳）
  if (fs.existsSync(targetPath)) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const backupPath = path.join(claudeConfigDir, `CLAUDE.backup.${timestamp}.md`);
    if (isDryRun) {
      log.info(`[Dry Run] 将备份现有 CLAUDE.md → ${backupPath}`);
    } else {
      fs.copyFileSync(targetPath, backupPath);
      log.success(`✅ 已备份现有 CLAUDE.md → ${backupPath}`);
    }
  }

  // 复制文件
  if (isDryRun) {
    log.info(`[Dry Run] 将复制 CLAUDE.md 到 ${targetPath}`);
  } else {
    fs.copyFileSync(sourcePath, targetPath);
    log.success(`CLAUDE.md 已安装到 ${targetPath}`);
  }

  return true;
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
  console.log('2. 启动 Zen MCP Server:');
  if (isWindows) {
    console.log(`   ${colors.cyan}cd ${zenMcpDir}${colors.reset}`);
    console.log(`   ${colors.cyan}.\\run-server.ps1${colors.reset}`);
  } else {
    console.log(`   ${colors.cyan}cd ${zenMcpDir}${colors.reset}`);
    console.log(`   ${colors.cyan}./run-server.sh${colors.reset}`);
  }
  console.log('');
  console.log('3. 验证安装:');
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

  // 步骤 3: 安装共享资源
  if (!installShared()) {
    log.warning('共享资源安装失败，但可继续使用');
  }

  console.log('');

  // 步骤 4: 安装全局配置
  if (!installGlobalConfig()) {
    log.warning('全局配置安装失败，但可继续使用');
  }

  console.log('');

  // 显示后续步骤
  showPostInstallInstructions();
}

// 运行安装
main().catch((error) => {
  log.error(`安装过程中出错: ${error.message}`);
  process.exit(1);
});

