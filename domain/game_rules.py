from domain.snake import Snake
from domain.obstacle import Obstacle

class GameRules:
    @staticmethod
    def is_out_of_bounds(
        position: tuple[int, int],
        board_width: int,
        board_height: int,
    ) -> bool:
        x, y = position
        return not (0 <= x < board_width and 0 <= y < board_height)

    @staticmethod
    def is_self_collision(snake: Snake) -> bool:
        return snake.head in snake.segments

    @staticmethod
    def is_obstacle_collision(
        position: tuple[int, int],
        obstacle: Obstacle,
    ) -> bool:
        return obstacle.is_blocked(position)

    @staticmethod
    def ate_food(
        position: tuple[int, int],
        food_position: tuple[int, int],
    ) -> bool:
        return position == food_position

    @classmethod
    def is_dead(
        cls,
        snake: Snake,
        obstacle: Obstacle,
        board_width: int,
        board_height: int,
    ) -> bool:
        return (
            cls.is_out_of_bounds(snake.head, board_width, board_height)
            or cls.is_self_collision(snake)
            or cls.is_obstacle_collision(snake.head, obstacle)
        )