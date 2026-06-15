from domain.food import Food
from domain.snake import Snake
from domain.obstacle import Obstacle


class FoodController:
    """
    Handles food relocation and score tracking.

    Knows:
      - When and how to relocate food after it is eaten.
      - How to track and expose the current score.

    Does NOT know:
      - Whether the snake actually ate the food (that is GameRules).
      - How to draw food.
      - The high score (that belongs to persistence).
    """

    def __init__(
        self,
        food: Food,
        board_width: int,
        board_height: int,
        points_per_food: int = 10,
    ) -> None:
        self._food = food
        self._board_width = board_width
        self._board_height = board_height
        self._points_per_food = points_per_food
        self._score: int = 0

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def food(self) -> Food:
        return self._food

    @property
    def score(self) -> int:
        return self._score

    # ── Commands ───────────────────────────────────────────────────────────
    def on_food_eaten(self, snake: Snake, obstacle: Obstacle) -> None:
        """
        Called when the snake eats the food.
        Adds points and relocates the food to a free cell.
        """
        self._score += self._points_per_food
        occupied = set(snake.body) | obstacle.cells
        self._food.relocate(self._board_width, self._board_height, occupied)

    def reset(self, snake: Snake, obstacle: Obstacle) -> None:
        """Resets the score and relocates food. Used on game restart."""
        self._score = 0
        occupied = set(snake.body) | obstacle.cells
        self._food.relocate(self._board_width, self._board_height, occupied)