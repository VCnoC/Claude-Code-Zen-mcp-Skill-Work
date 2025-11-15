"""
贪吃蛇游戏核心逻辑模块
包含 Snake、Food、Game 三个核心类
"""

import pygame
import random
from typing import List, Tuple
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    COLOR_BLACK, COLOR_WHITE, COLOR_GREEN, COLOR_RED, COLOR_DARK_GREEN,
    FPS, SNAKE_SPEED, INITIAL_SNAKE_LENGTH,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
)


class Snake:
    """蛇类：管理蛇的状态和行为"""

    def __init__(self, start_pos: Tuple[int, int], start_length: int = INITIAL_SNAKE_LENGTH) -> None:
        """初始化蛇

        Args:
            start_pos: 起始位置（grid 坐标）
            start_length: 初始长度
        """
        self.body: List[Tuple[int, int]] = [
            (start_pos[0] - i, start_pos[1]) for i in range(start_length)
        ]
        self.direction: Tuple[int, int] = DIRECTION_RIGHT
        self.grow_pending: bool = False

    def move(self) -> None:
        """根据当前方向移动蛇"""
        # 计算新头部位置
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # 在列表前端插入新头部
        self.body.insert(0, new_head)

        # 如果不需要增长，移除尾部
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self) -> None:
        """标记蛇在下次移动时增长"""
        self.grow_pending = True

    def check_collision(self, grid_size: Tuple[int, int]) -> bool:
        """检测碰撞

        Args:
            grid_size: 网格大小（宽, 高）

        Returns:
            True 表示碰撞，False 表示未碰撞
        """
        head_x, head_y = self.body[0]

        # 检测撞墙
        if head_x < 0 or head_x >= grid_size[0] or head_y < 0 or head_y >= grid_size[1]:
            return True

        # 检测撞自己（头部与身体任意节点重合）
        if self.body[0] in self.body[1:]:
            return True

        return False

    def change_direction(self, new_direction: Tuple[int, int]) -> None:
        """改变移动方向（防止反向移动）

        Args:
            new_direction: 新方向（dx, dy）
        """
        # 防止反向移动（例如正在向右时不能直接向左）
        if (self.direction[0] + new_direction[0], self.direction[1] + new_direction[1]) != (0, 0):
            self.direction = new_direction


class Food:
    """食物类：管理食物的生成和碰撞检测"""

    def __init__(self, grid_size: Tuple[int, int]) -> None:
        """初始化食物

        Args:
            grid_size: 网格大小（宽, 高）
        """
        self.grid_size = grid_size
        self.position: Tuple[int, int] = (0, 0)
        self.randomize_position([])

    def randomize_position(self, snake_body: List[Tuple[int, int]]) -> None:
        """随机生成食物位置（避开蛇身）

        Args:
            snake_body: 蛇的身体坐标列表
        """
        max_attempts = self.grid_size[0] * self.grid_size[1]
        attempts = 0

        while attempts < max_attempts:
            x = random.randint(0, self.grid_size[0] - 1)
            y = random.randint(0, self.grid_size[1] - 1)
            new_position = (x, y)

            # 确保食物不在蛇身上
            if new_position not in snake_body:
                self.position = new_position
                return

            attempts += 1

        # 降级策略：遍历所有空位
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                pos = (x, y)
                if pos not in snake_body:
                    self.position = pos
                    return

    def is_eaten(self, snake_head: Tuple[int, int]) -> bool:
        """检测食物是否被吃

        Args:
            snake_head: 蛇头坐标

        Returns:
            True 表示被吃，False 表示未被吃
        """
        return self.position == snake_head


class Game:
    """游戏主控制器：管理游戏循环和状态"""

    def __init__(self) -> None:
        """初始化游戏"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        # 初始化游戏对象
        start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = Snake(start_pos)
        self.food = Food((GRID_WIDTH, GRID_HEIGHT))

        # 游戏状态
        self.running = True
        self.game_over = False
        self.score = 0
        self.move_timer = 0
        self.move_interval = 1000 // SNAKE_SPEED  # 毫秒

    def run(self) -> None:
        """运行游戏主循环"""
        while self.running:
            dt = self.clock.tick(FPS)
            self.handle_events()

            if not self.game_over:
                self.update(dt)

            self.render()

        pygame.quit()

    def handle_events(self) -> None:
        """处理键盘输入和窗口事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # 方向键控制
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake.change_direction(DIRECTION_UP)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake.change_direction(DIRECTION_DOWN)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake.change_direction(DIRECTION_LEFT)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake.change_direction(DIRECTION_RIGHT)

                # 游戏结束后按空格重新开始
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset()

    def update(self, dt: int) -> None:
        """更新游戏状态

        Args:
            dt: 距离上一帧的时间差（毫秒）
        """
        # 使用定时器控制蛇的移动速度
        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            self.move_timer = 0

            # 移动蛇
            self.snake.move()

            # 检测碰撞
            if self.snake.check_collision((GRID_WIDTH, GRID_HEIGHT)):
                self.game_over = True
                return

            # 检测是否吃到食物
            if self.food.is_eaten(self.snake.body[0]):
                self.snake.grow()
                self.score += 1
                self.food.randomize_position(self.snake.body)

    def render(self) -> None:
        """渲染游戏画面"""
        # 清屏
        self.screen.fill(COLOR_BLACK)

        # 绘制蛇
        for i, segment in enumerate(self.snake.body):
            color = COLOR_GREEN if i == 0 else COLOR_DARK_GREEN  # 头部用亮绿色
            rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 2,  # 留2像素间隙
                GRID_SIZE - 2
            )
            pygame.draw.rect(self.screen, color, rect)

        # 绘制食物
        food_rect = pygame.Rect(
            self.food.position[0] * GRID_SIZE,
            self.food.position[1] * GRID_SIZE,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        )
        pygame.draw.rect(self.screen, COLOR_RED, food_rect)

        # 绘制分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, COLOR_WHITE)
        self.screen.blit(score_text, (10, 10))

        # 绘制游戏结束提示
        if self.game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render('GAME OVER', True, COLOR_RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render('Press SPACE to restart', True, COLOR_WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def reset(self) -> None:
        """重置游戏"""
        start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = Snake(start_pos)
        self.food = Food((GRID_WIDTH, GRID_HEIGHT))
        self.game_over = False
        self.score = 0
        self.move_timer = 0
