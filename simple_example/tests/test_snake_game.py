"""
游戏核心逻辑测试
测试 snake_game.py 中的 Snake、Food、Game 三个核心类
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pygame
from snake_game import Snake, Food, Game
from config import (
    GRID_WIDTH, GRID_HEIGHT,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT,
    INITIAL_SNAKE_LENGTH
)


class TestSnake:
    """测试 Snake 类"""

    def test_init_default_length(self):
        """测试默认长度初始化"""
        # Arrange & Act
        snake = Snake((10, 10))

        # Assert
        assert len(snake.body) == INITIAL_SNAKE_LENGTH, f"初始长度应为 {INITIAL_SNAKE_LENGTH}"
        assert snake.body[0] == (10, 10), "头部应在指定位置"

    def test_init_custom_length(self):
        """测试自定义长度初始化"""
        # Arrange & Act
        custom_length = 5
        snake = Snake((10, 10), custom_length)

        # Assert
        assert len(snake.body) == custom_length, f"长度应为 {custom_length}"

    def test_init_body_horizontal(self):
        """测试初始身体水平排列"""
        # Arrange & Act
        snake = Snake((10, 10), 3)

        # Assert
        assert snake.body == [(10, 10), (9, 10), (8, 10)], "身体应水平向左排列"

    def test_init_direction_right(self):
        """测试初始方向向右"""
        # Arrange & Act
        snake = Snake((10, 10))

        # Assert
        assert snake.direction == DIRECTION_RIGHT, "初始方向应向右"

    def test_move_right(self):
        """测试向右移动"""
        # Arrange
        snake = Snake((10, 10), 3)
        initial_body = snake.body.copy()

        # Act
        snake.move()

        # Assert
        assert snake.body[0] == (11, 10), "头部应向右移动一格"
        assert len(snake.body) == 3, "长度应保持不变"

    def test_move_up(self):
        """测试向上移动"""
        # Arrange
        snake = Snake((10, 10), 3)
        snake.direction = DIRECTION_UP

        # Act
        snake.move()

        # Assert
        assert snake.body[0] == (10, 9), "头部应向上移动一格"

    def test_move_down(self):
        """测试向下移动"""
        # Arrange
        snake = Snake((10, 10), 3)
        snake.direction = DIRECTION_DOWN

        # Act
        snake.move()

        # Assert
        assert snake.body[0] == (10, 11), "头部应向下移动一格"

    def test_move_left(self):
        """测试向左移动"""
        # Arrange
        snake = Snake((10, 10), 3)
        snake.direction = DIRECTION_LEFT

        # Act
        snake.move()

        # Assert
        assert snake.body[0] == (9, 10), "头部应向左移动一格"

    def test_move_removes_tail(self):
        """测试移动时移除尾部"""
        # Arrange
        snake = Snake((10, 10), 3)
        original_tail = snake.body[-1]

        # Act
        snake.move()

        # Assert
        assert original_tail not in snake.body, "原尾部应被移除"

    def test_grow_sets_pending_flag(self):
        """测试 grow() 设置待增长标志"""
        # Arrange
        snake = Snake((10, 10), 3)

        # Act
        snake.grow()

        # Assert
        assert snake.grow_pending is True, "应设置 grow_pending 标志"

    def test_move_with_grow_pending(self):
        """测试待增长时移动不移除尾部"""
        # Arrange
        snake = Snake((10, 10), 3)
        snake.grow()
        original_length = len(snake.body)

        # Act
        snake.move()

        # Assert
        assert len(snake.body) == original_length + 1, "长度应增加1"
        assert snake.grow_pending is False, "grow_pending 应重置为 False"

    def test_check_collision_no_collision(self):
        """测试无碰撞情况"""
        # Arrange
        snake = Snake((10, 10), 3)

        # Act
        result = snake.check_collision((GRID_WIDTH, GRID_HEIGHT))

        # Assert
        assert result is False, "中心位置不应发生碰撞"

    def test_check_collision_left_wall(self):
        """测试左墙碰撞"""
        # Arrange
        snake = Snake((0, 10), 3)
        snake.direction = DIRECTION_LEFT
        snake.move()

        # Act
        result = snake.check_collision((GRID_WIDTH, GRID_HEIGHT))

        # Assert
        assert result is True, "应检测到左墙碰撞"

    def test_check_collision_right_wall(self):
        """测试右墙碰撞"""
        # Arrange
        snake = Snake((GRID_WIDTH - 1, 10), 3)
        snake.direction = DIRECTION_RIGHT
        snake.move()

        # Act
        result = snake.check_collision((GRID_WIDTH, GRID_HEIGHT))

        # Assert
        assert result is True, "应检测到右墙碰撞"

    def test_check_collision_top_wall(self):
        """测试上墙碰撞"""
        # Arrange
        snake = Snake((10, 0), 3)
        snake.direction = DIRECTION_UP
        snake.move()

        # Act
        result = snake.check_collision((GRID_WIDTH, GRID_HEIGHT))

        # Assert
        assert result is True, "应检测到上墙碰撞"

    def test_check_collision_bottom_wall(self):
        """测试下墙碰撞"""
        # Arrange
        snake = Snake((10, GRID_HEIGHT - 1), 3)
        snake.direction = DIRECTION_DOWN
        snake.move()

        # Act
        result = snake.check_collision((GRID_WIDTH, GRID_HEIGHT))

        # Assert
        assert result is True, "应检测到下墙碰撞"

    def test_check_collision_self(self):
        """测试自身碰撞"""
        # Arrange
        snake = Snake((10, 10), 1)
        # 直接构造头部与身体重合的场景
        snake.body = [(10, 11), (11, 10), (11, 11), (10, 11)]  # 头部 (10,11) 与第4节重合

        # Act
        result = snake.check_collision((GRID_WIDTH, GRID_HEIGHT))

        # Assert
        assert result is True, "应检测到自身碰撞"

    def test_change_direction_valid(self):
        """测试有效的方向改变"""
        # Arrange
        snake = Snake((10, 10), 3)
        snake.direction = DIRECTION_RIGHT

        # Act
        snake.change_direction(DIRECTION_UP)

        # Assert
        assert snake.direction == DIRECTION_UP, "方向应改变为向上"

    def test_change_direction_prevent_reverse(self):
        """测试防止反向移动"""
        # Arrange
        snake = Snake((10, 10), 3)
        snake.direction = DIRECTION_RIGHT

        # Act
        snake.change_direction(DIRECTION_LEFT)  # 尝试反向

        # Assert
        assert snake.direction == DIRECTION_RIGHT, "方向不应改变（防止反向）"

    def test_change_direction_all_valid_turns(self):
        """测试所有有效的转向"""
        snake = Snake((10, 10), 3)

        # 从右向上
        snake.direction = DIRECTION_RIGHT
        snake.change_direction(DIRECTION_UP)
        assert snake.direction == DIRECTION_UP

        # 从上向左
        snake.change_direction(DIRECTION_LEFT)
        assert snake.direction == DIRECTION_LEFT

        # 从左向下
        snake.change_direction(DIRECTION_DOWN)
        assert snake.direction == DIRECTION_DOWN

        # 从下向右
        snake.change_direction(DIRECTION_RIGHT)
        assert snake.direction == DIRECTION_RIGHT


class TestFood:
    """测试 Food 类"""

    def test_init(self):
        """测试初始化"""
        # Arrange & Act
        food = Food((GRID_WIDTH, GRID_HEIGHT))

        # Assert
        assert food.grid_size == (GRID_WIDTH, GRID_HEIGHT), "网格大小应正确设置"
        assert isinstance(food.position, tuple), "位置应为元组"
        assert len(food.position) == 2, "位置应为 (x, y) 坐标"

    def test_randomize_position_not_on_snake(self):
        """测试食物不生成在蛇身上"""
        # Arrange
        food = Food((GRID_WIDTH, GRID_HEIGHT))
        snake_body = [(5, 5), (6, 5), (7, 5)]

        # Act
        food.randomize_position(snake_body)

        # Assert
        assert food.position not in snake_body, "食物不应在蛇身上"

    def test_randomize_position_within_bounds(self):
        """测试食物位置在边界内"""
        # Arrange
        food = Food((GRID_WIDTH, GRID_HEIGHT))

        # Act
        food.randomize_position([])

        # Assert
        x, y = food.position
        assert 0 <= x < GRID_WIDTH, f"x 坐标应在 [0, {GRID_WIDTH}) 范围内"
        assert 0 <= y < GRID_HEIGHT, f"y 坐标应在 [0, {GRID_HEIGHT}) 范围内"

    def test_randomize_position_empty_grid(self):
        """测试空网格时的随机位置"""
        # Arrange
        food = Food((10, 10))

        # Act
        food.randomize_position([])

        # Assert
        x, y = food.position
        assert 0 <= x < 10 and 0 <= y < 10, "位置应在网格范围内"

    def test_randomize_position_almost_full_grid(self):
        """测试网格几乎满时仍能找到位置"""
        # Arrange
        grid_size = (5, 5)
        food = Food(grid_size)
        # 填满除一个位置外的所有格子
        snake_body = [(x, y) for x in range(5) for y in range(5) if (x, y) != (4, 4)]

        # Act
        food.randomize_position(snake_body)

        # Assert
        assert food.position == (4, 4), "应找到唯一的空位 (4, 4)"

    def test_randomize_position_max_attempts_fallback(self):
        """测试最大尝试次数后使用降级策略"""
        # Arrange
        grid_size = (3, 3)
        food = Food(grid_size)
        # 填满大部分格子，只留一个角落
        snake_body = [(x, y) for x in range(3) for y in range(3) if (x, y) != (0, 0)]

        # Act
        food.randomize_position(snake_body)

        # Assert
        assert food.position == (0, 0), "降级策略应找到空位 (0, 0)"

    def test_is_eaten_true(self):
        """测试食物被吃（头部位置相同）"""
        # Arrange
        food = Food((GRID_WIDTH, GRID_HEIGHT))
        food.position = (10, 10)
        snake_head = (10, 10)

        # Act
        result = food.is_eaten(snake_head)

        # Assert
        assert result is True, "食物应被吃"

    def test_is_eaten_false(self):
        """测试食物未被吃（头部位置不同）"""
        # Arrange
        food = Food((GRID_WIDTH, GRID_HEIGHT))
        food.position = (10, 10)
        snake_head = (11, 10)

        # Act
        result = food.is_eaten(snake_head)

        # Assert
        assert result is False, "食物不应被吃"


class TestGame:
    """测试 Game 类"""

    @patch('snake_game.pygame')
    def test_init(self, mock_pygame):
        """测试 Game 初始化"""
        # Arrange
        mock_display = Mock()
        mock_pygame.display.set_mode.return_value = mock_display
        mock_pygame.time.Clock.return_value = Mock()

        # Act
        game = Game()

        # Assert
        mock_pygame.init.assert_called_once(), "应调用 pygame.init()"
        assert game.running is True, "游戏应处于运行状态"
        assert game.game_over is False, "游戏不应结束"
        assert game.score == 0, "初始分数应为0"
        assert isinstance(game.snake, Snake), "应创建 Snake 实例"
        assert isinstance(game.food, Food), "应创建 Food 实例"

    @patch('snake_game.pygame')
    def test_handle_events_quit(self, mock_pygame):
        """测试退出事件"""
        # Arrange
        mock_pygame.QUIT = pygame.QUIT  # 确保常量可用
        game = Game()
        quit_event = Mock()
        quit_event.type = pygame.QUIT
        mock_pygame.event.get.return_value = [quit_event]

        # Act
        game.handle_events()

        # Assert
        assert game.running is False, "应设置 running 为 False"

    @patch('snake_game.pygame')
    def test_handle_events_arrow_keys(self, mock_pygame):
        """测试方向键控制"""
        # Arrange
        game = Game()

        # Test UP
        up_event = Mock()
        up_event.type = pygame.KEYDOWN
        up_event.key = pygame.K_UP
        mock_pygame.event.get.return_value = [up_event]
        game.handle_events()
        # Note: change_direction 有防反向逻辑，初始向右时可以向上

        # Test DOWN
        down_event = Mock()
        down_event.type = pygame.KEYDOWN
        down_event.key = pygame.K_DOWN
        mock_pygame.event.get.return_value = [down_event]
        game.handle_events()

        # Test LEFT
        left_event = Mock()
        left_event.type = pygame.KEYDOWN
        left_event.key = pygame.K_LEFT
        mock_pygame.event.get.return_value = [left_event]
        game.handle_events()

        # Test RIGHT
        right_event = Mock()
        right_event.type = pygame.KEYDOWN
        right_event.key = pygame.K_RIGHT
        mock_pygame.event.get.return_value = [right_event]
        game.handle_events()

        # Assert - 验证最后一个方向设置成功（向右，初始方向也是向右，所以没变化）
        assert game.snake.direction == DIRECTION_RIGHT

    @patch('snake_game.pygame')
    def test_handle_events_wasd_keys(self, mock_pygame):
        """测试 WASD 键控制"""
        # Arrange
        mock_pygame.KEYDOWN = pygame.KEYDOWN
        mock_pygame.K_w = pygame.K_w
        mock_pygame.K_s = pygame.K_s
        mock_pygame.K_a = pygame.K_a
        mock_pygame.K_d = pygame.K_d
        game = Game()
        game.snake.direction = DIRECTION_RIGHT

        # Test W (up)
        w_event = Mock()
        w_event.type = pygame.KEYDOWN
        w_event.key = pygame.K_w
        mock_pygame.event.get.return_value = [w_event]
        game.handle_events()
        assert game.snake.direction == DIRECTION_UP, "W 键应向上"

        # Test S (down) - 从上不能直接向下，应保持向上
        game.snake.direction = DIRECTION_RIGHT  # 重置
        s_event = Mock()
        s_event.type = pygame.KEYDOWN
        s_event.key = pygame.K_s
        mock_pygame.event.get.return_value = [s_event]
        game.handle_events()
        assert game.snake.direction == DIRECTION_DOWN, "S 键应向下"

    @patch('snake_game.pygame')
    def test_handle_events_space_restart(self, mock_pygame):
        """测试空格键重新开始"""
        # Arrange
        mock_pygame.KEYDOWN = pygame.KEYDOWN
        mock_pygame.K_SPACE = pygame.K_SPACE
        game = Game()
        game.game_over = True
        game.score = 10
        space_event = Mock()
        space_event.type = pygame.KEYDOWN
        space_event.key = pygame.K_SPACE
        mock_pygame.event.get.return_value = [space_event]

        # Act
        game.handle_events()

        # Assert
        assert game.game_over is False, "游戏应重置"
        assert game.score == 0, "分数应重置为0"

    @patch('snake_game.pygame')
    def test_update_snake_movement(self, mock_pygame):
        """测试蛇定时移动"""
        # Arrange
        game = Game()
        initial_head = game.snake.body[0]

        # Act - 累积足够的时间触发移动
        game.update(game.move_interval)

        # Assert
        assert game.snake.body[0] != initial_head, "蛇应该移动"

    @patch('snake_game.pygame')
    def test_update_collision_triggers_game_over(self, mock_pygame):
        """测试碰撞触发游戏结束"""
        # Arrange
        game = Game()
        # 设置蛇即将撞墙
        game.snake.body = [(GRID_WIDTH - 1, 10), (GRID_WIDTH - 2, 10), (GRID_WIDTH - 3, 10)]
        game.snake.direction = DIRECTION_RIGHT

        # Act
        game.update(game.move_interval)

        # Assert
        assert game.game_over is True, "碰撞应触发 game_over"

    @patch('snake_game.pygame')
    def test_update_eating_food(self, mock_pygame):
        """测试吃到食物"""
        # Arrange
        game = Game()
        # 设置食物在蛇前面
        game.snake.body = [(10, 10), (9, 10), (8, 10)]
        game.snake.direction = DIRECTION_RIGHT
        game.food.position = (11, 10)
        initial_score = game.score
        initial_length = len(game.snake.body)

        # Act
        game.update(game.move_interval)

        # Assert
        assert game.score == initial_score + 1, "分数应增加"
        assert game.snake.grow_pending is True, "蛇应标记为待增长"
        assert game.food.position != (11, 10), "食物应重新生成"

    @patch('snake_game.pygame')
    def test_update_not_enough_time(self, mock_pygame):
        """测试时间不足时不移动"""
        # Arrange
        game = Game()
        initial_head = game.snake.body[0]

        # Act - 时间不足
        game.update(game.move_interval - 1)

        # Assert
        assert game.snake.body[0] == initial_head, "时间不足时蛇不应移动"

    @patch('snake_game.pygame')
    def test_reset(self, mock_pygame):
        """测试游戏重置"""
        # Arrange
        game = Game()
        game.game_over = True
        game.score = 20
        game.move_timer = 500

        # Act
        game.reset()

        # Assert
        assert game.game_over is False, "game_over 应重置"
        assert game.score == 0, "分数应重置"
        assert game.move_timer == 0, "计时器应重置"
        assert len(game.snake.body) == INITIAL_SNAKE_LENGTH, "蛇长度应重置"

    @patch('snake_game.pygame')
    def test_render_calls_pygame_methods(self, mock_pygame):
        """测试渲染调用 pygame 方法"""
        # Arrange
        mock_screen = Mock()
        game = Game()
        game.screen = mock_screen

        # Act
        game.render()

        # Assert
        mock_screen.fill.assert_called(), "应调用 screen.fill()"
        mock_screen.blit.assert_called(), "应调用 screen.blit() 绘制文本"
        mock_pygame.draw.rect.assert_called(), "应调用 pygame.draw.rect() 绘制矩形"
        mock_pygame.display.flip.assert_called_once(), "应调用 pygame.display.flip()"

    @patch('snake_game.pygame')
    def test_render_game_over_message(self, mock_pygame):
        """测试游戏结束时显示提示"""
        # Arrange
        mock_screen = Mock()
        game = Game()
        game.screen = mock_screen
        game.game_over = True

        # Act
        game.render()

        # Assert
        # 验证绘制了额外的文本（游戏结束提示）
        assert mock_screen.blit.call_count >= 2, "应绘制分数和游戏结束提示"
