# 贪吃蛇游戏

<p align="center">
  <strong>经典贪吃蛇游戏 - Python + Pygame 实现</strong>
</p>

## 项目简介

这是一个使用 Python 和 Pygame 开发的经典贪吃蛇游戏。游戏具有简洁的界面、流畅的操作和完善的测试覆盖。

### 主要特性

- ✅ 经典游戏玩法：控制蛇吃食物，避免撞墙和撞自己
- 🎮 双键位支持：支持方向键和 WASD 键位
- 🎯 计分系统：实时显示当前得分
- 🔄 重新开始：游戏结束后可按空格键重新开始
- 🧪 高测试覆盖：98% 代码覆盖率，56 个测试用例全部通过
- 📐 模块化设计：Snake、Food、Game 三个核心类，职责清晰

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- pip 包管理工具

### 安装依赖

```bash
# 安装游戏依赖
pip install pygame>=2.5.0

# 安装测试依赖（可选）
pip install pytest>=7.4.0 pytest-cov>=4.1.0
```

### 运行游戏

```bash
# 进入项目目录
cd 贪吃蛇

# 启动游戏
python main.py
```

## 游戏控制

### 方向控制

- **方向键**：↑ ↓ ← → 控制蛇的移动方向
- **WASD 键**：W (上) / S (下) / A (左) / D (右)

### 游戏操作

- **空格键**：游戏结束后重新开始
- **关闭窗口**：退出游戏

## 游戏规则

1. 🐍 蛇初始长度为 3 格，初始方向向右
2. 🍎 吃到红色食物后，蛇身长度增加 1 格，得分 +1
3. ⚠️ 撞到墙壁或自己身体，游戏结束
4. 🎮 食物随机生成在空白位置
5. 🚀 蛇的移动速度为每秒 10 格

## 项目结构

```
贪吃蛇/
├── main.py              # 游戏入口文件
├── snake_game.py        # 游戏核心逻辑（Snake, Food, Game 类）
├── config.py            # 游戏配置文件
├── requirements.txt     # 项目依赖
├── tests/               # 测试文件目录
│   ├── test_config.py      # 配置模块测试
│   ├── test_main.py        # 主程序测试
│   └── test_snake_game.py  # 核心逻辑测试
├── plan.md              # 项目实施计划
├── PROJECTWIKI.md       # 项目知识库文档
├── CHANGELOG.md         # 变更日志
└── README.md            # 本文件
```

## 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ -v --cov=. --cov-report=term-missing

# 当前测试覆盖率：98%
# - 56 个测试用例全部通过
# - config.py: 100%
# - main.py: 83%
# - snake_game.py: 93%
```

## 技术栈

- **编程语言**：Python 3.8+
- **游戏框架**：Pygame 2.5.0
- **测试框架**：pytest 7.4.0
- **测试覆盖**：pytest-cov 4.1.0

## 核心架构

### 类设计

```
Snake 类 - 蛇的行为
├── move()              # 移动蛇
├── grow()              # 增长蛇身
├── check_collision()   # 检测碰撞
└── change_direction()  # 改变方向

Food 类 - 食物管理
├── randomize_position()  # 随机生成位置
└── is_eaten()            # 检测是否被吃

Game 类 - 游戏主控制
├── run()             # 游戏主循环
├── handle_events()   # 处理输入事件
├── update()          # 更新游戏状态
├── render()          # 渲染画面
└── reset()           # 重置游戏
```

### 配置参数

- 窗口大小：600x600 像素
- 网格大小：20 像素/格
- 网格数量：30x30
- 帧率：60 FPS
- 蛇移动速度：10 格/秒
- 初始蛇长度：3 格

## 开发文档

- **详细设计文档**：查看 [PROJECTWIKI.md](./PROJECTWIKI.md)
- **实施计划**：查看 [plan.md](./plan.md)
- **变更历史**：查看 [CHANGELOG.md](./CHANGELOG.md)

## 许可证

本项目仅用于学习和交流目的。

---

**🎮 开始游戏，享受经典贪吃蛇的乐趣！**
