"""
配置模块测试
测试 config.py 中的常量定义
"""

import pytest
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    COLOR_BLACK, COLOR_WHITE, COLOR_GREEN, COLOR_RED, COLOR_DARK_GREEN, COLOR_GRAY,
    FPS, SNAKE_SPEED, INITIAL_SNAKE_LENGTH,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
)


class TestWindowConfig:
    """测试窗口配置常量"""

    def test_window_dimensions(self):
        """测试窗口尺寸为正整数"""
        assert isinstance(WINDOW_WIDTH, int), "窗口宽度应为整数"
        assert isinstance(WINDOW_HEIGHT, int), "窗口高度应为整数"
        assert WINDOW_WIDTH > 0, "窗口宽度应大于0"
        assert WINDOW_HEIGHT > 0, "窗口高度应大于0"

    def test_window_title(self):
        """测试窗口标题为非空字符串"""
        assert isinstance(WINDOW_TITLE, str), "窗口标题应为字符串"
        assert len(WINDOW_TITLE) > 0, "窗口标题不应为空"


class TestGridConfig:
    """测试网格配置常量"""

    def test_grid_size(self):
        """测试网格大小为正整数"""
        assert isinstance(GRID_SIZE, int), "网格大小应为整数"
        assert GRID_SIZE > 0, "网格大小应大于0"

    def test_grid_dimensions_calculation(self):
        """测试网格宽高计算正确"""
        assert GRID_WIDTH == WINDOW_WIDTH // GRID_SIZE, "网格宽度计算错误"
        assert GRID_HEIGHT == WINDOW_HEIGHT // GRID_SIZE, "网格高度计算错误"

    def test_grid_dimensions_positive(self):
        """测试网格宽高为正整数"""
        assert GRID_WIDTH > 0, "网格宽度应大于0"
        assert GRID_HEIGHT > 0, "网格高度应大于0"


class TestColorConfig:
    """测试颜色配置常量"""

    def test_color_format(self):
        """测试所有颜色都是RGB三元组"""
        colors = [COLOR_BLACK, COLOR_WHITE, COLOR_GREEN, COLOR_RED, COLOR_DARK_GREEN, COLOR_GRAY]
        for color in colors:
            assert isinstance(color, tuple), f"颜色 {color} 应为元组"
            assert len(color) == 3, f"颜色 {color} 应包含3个值(RGB)"
            for value in color:
                assert isinstance(value, int), f"颜色值应为整数，得到 {value}"
                assert 0 <= value <= 255, f"颜色值应在0-255范围内，得到 {value}"

    def test_specific_colors(self):
        """测试特定颜色值正确"""
        assert COLOR_BLACK == (0, 0, 0), "黑色应为(0,0,0)"
        assert COLOR_WHITE == (255, 255, 255), "白色应为(255,255,255)"
        assert COLOR_RED == (255, 0, 0), "红色应为(255,0,0)"


class TestGameConfig:
    """测试游戏配置常量"""

    def test_fps(self):
        """测试帧率为正整数"""
        assert isinstance(FPS, int), "FPS应为整数"
        assert FPS > 0, "FPS应大于0"
        assert FPS <= 120, "FPS不应超过120（合理范围）"

    def test_snake_speed(self):
        """测试蛇速度为正整数"""
        assert isinstance(SNAKE_SPEED, int), "蛇速度应为整数"
        assert SNAKE_SPEED > 0, "蛇速度应大于0"

    def test_initial_snake_length(self):
        """测试初始蛇长度合理"""
        assert isinstance(INITIAL_SNAKE_LENGTH, int), "初始蛇长度应为整数"
        assert INITIAL_SNAKE_LENGTH >= 1, "初始蛇长度至少为1"
        assert INITIAL_SNAKE_LENGTH <= GRID_WIDTH, "初始蛇长度不应超过网格宽度"


class TestDirectionConstants:
    """测试方向常量"""

    def test_direction_format(self):
        """测试所有方向都是(dx, dy)元组"""
        directions = [DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT]
        for direction in directions:
            assert isinstance(direction, tuple), f"方向 {direction} 应为元组"
            assert len(direction) == 2, f"方向 {direction} 应包含2个值(dx, dy)"
            for value in direction:
                assert isinstance(value, int), f"方向值应为整数，得到 {value}"
                assert -1 <= value <= 1, f"方向值应在-1到1范围内，得到 {value}"

    def test_direction_values(self):
        """测试方向值正确"""
        assert DIRECTION_UP == (0, -1), "向上方向应为(0, -1)"
        assert DIRECTION_DOWN == (0, 1), "向下方向应为(0, 1)"
        assert DIRECTION_LEFT == (-1, 0), "向左方向应为(-1, 0)"
        assert DIRECTION_RIGHT == (1, 0), "向右方向应为(1, 0)"

    def test_opposite_directions(self):
        """测试相反方向的和为(0, 0)"""
        assert (DIRECTION_UP[0] + DIRECTION_DOWN[0], DIRECTION_UP[1] + DIRECTION_DOWN[1]) == (0, 0)
        assert (DIRECTION_LEFT[0] + DIRECTION_RIGHT[0], DIRECTION_LEFT[1] + DIRECTION_RIGHT[1]) == (0, 0)
