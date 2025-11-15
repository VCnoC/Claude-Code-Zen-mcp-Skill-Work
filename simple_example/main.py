#!/usr/bin/env python3
"""
贪吃蛇游戏入口文件
运行此文件启动游戏
"""

from snake_game import Game


def main() -> None:
    """游戏主函数"""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
