from domain.snake import Snake
from domain.obstacle import Obstacle


class GameRules:
    """
    Evaluates all collision conditions for the game.

    Knows:
      - How to detect every type of collision.

    Does NOT know:
      - How to move the snake.
      - How to update the score.
      - How to draw anything.
    """

    @staticmethod
    def is_out_of_bounds(
        position: tuple[int, int],
        board_width: int,
        board_height: int,
    ) -> bool:
        """Returns True if the position is outside the board limits."""
        x, y = position
        return not (0 <= x < board_width and 0 <= y < board_height)

    @staticmethod
    def is_self_collision(snake: Snake) -> bool:
        """Returns True if the snake's head overlaps any of its body segments."""
        return snake.head in snake.segments

    @staticmethod
    def is_obstacle_collision(
        position: tuple[int, int],
        obstacle: Obstacle,
    ) -> bool:
        """Returns True if the position hits a blocked cell."""
        return obstacle.is_blocked(position)

    @staticmethod
    def ate_food(
        position: tuple[int, int],
        food_position: tuple[int, int],
    ) -> bool:
        """Returns True if the position matches the food's position."""
        return position == food_position

    @classmethod
    def is_dead(
        cls,
        snake: Snake,
        obstacle: Obstacle,
        board_width: int,
        board_height: int,
    ) -> bool:
        """
        Convenience method: returns True if any lethal collision is detected.
        Combines wall, self, and obstacle checks in one call.
        """
        return (
            cls.is_out_of_bounds(snake.head, board_width, board_height)
            or cls.is_self_collision(snake)
            or cls.is_obstacle_collision(snake.head, obstacle)
        )