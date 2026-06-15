from domain.snake import Snake, Direction


# Maps raw input strings to Direction values
_INPUT_MAP: dict[str, Direction] = {
    "UP":    Direction.UP,
    "DOWN":  Direction.DOWN,
    "LEFT":  Direction.LEFT,
    "RIGHT": Direction.RIGHT,
}


class SnakeController:
    """
    Handles player input and drives the snake's movement each tick.

    Knows:
      - How to translate input commands into direction changes.
      - When to tell the snake to move.

    Does NOT know:
      - Food, obstacles, scoring, or collisions.
      - How input is captured (keyboard, AI, network — doesn't matter).
      - How to draw the snake.
    """

    def __init__(self, snake: Snake) -> None:
        self._snake = snake

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def snake(self) -> Snake:
        return self._snake

    # ── Commands ───────────────────────────────────────────────────────────
    def handle_input(self, action: str) -> None:
        """
        Receives an abstract input command and updates the snake's direction.
        Unknown commands are silently ignored.

        Valid actions: "UP", "DOWN", "LEFT", "RIGHT"
        """
        direction = _INPUT_MAP.get(action.upper())
        if direction:
            self._snake.change_direction(direction)

    def tick(self) -> None:
        """Advances the snake one step. Called once per game tick."""
        self._snake.move()