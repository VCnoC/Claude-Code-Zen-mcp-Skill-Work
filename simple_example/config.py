"""
游戏配置文件
包含窗口大小、颜色、速度等全局配置参数
"""

# 窗口配置
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "贪吃蛇游戏"

# 网格配置
GRID_SIZE = 20  # 每个方格的大小（像素）
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE  # 30
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE  # 30

# 颜色配置（RGB）
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_DARK_GREEN = (0, 200, 0)
COLOR_GRAY = (128, 128, 128)

# 游戏配置
FPS = 60  # 帧率
SNAKE_SPEED = 10  # 蛇的移动速度（每秒移动格数）
INITIAL_SNAKE_LENGTH = 3  # 初始蛇身长度

# 方向常量（dx, dy）
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
