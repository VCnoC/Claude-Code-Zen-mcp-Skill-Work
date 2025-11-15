"""
主程序入口测试
测试 main.py 的游戏启动逻辑
"""

import pytest
from unittest.mock import Mock, patch
from main import main


class TestMain:
    """测试主函数"""

    @patch('main.Game')
    def test_main_creates_game_instance(self, mock_game_class):
        """测试 main() 创建 Game 实例"""
        # Arrange
        mock_game_instance = Mock()
        mock_game_class.return_value = mock_game_instance

        # Act
        main()

        # Assert
        mock_game_class.assert_called_once(), "应该调用 Game() 创建实例"

    @patch('main.Game')
    def test_main_runs_game(self, mock_game_class):
        """测试 main() 调用 game.run()"""
        # Arrange
        mock_game_instance = Mock()
        mock_game_class.return_value = mock_game_instance

        # Act
        main()

        # Assert
        mock_game_instance.run.assert_called_once(), "应该调用 game.run() 启动游戏"

    @patch('main.Game')
    def test_main_execution_order(self, mock_game_class):
        """测试 main() 执行顺序：先创建后运行"""
        # Arrange
        mock_game_instance = Mock()
        mock_game_class.return_value = mock_game_instance
        call_order = []

        def track_game_creation(*args, **kwargs):
            call_order.append('create')
            return mock_game_instance

        def track_game_run():
            call_order.append('run')

        mock_game_class.side_effect = track_game_creation
        mock_game_instance.run.side_effect = track_game_run

        # Act
        main()

        # Assert
        assert call_order == ['create', 'run'], "应该先创建 Game 实例，再调用 run()"
