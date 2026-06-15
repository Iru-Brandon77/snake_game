from domain.snake import Snake, Direction

_INPUT_MAP: dict[str, Direction] = {
    "UP":    Direction.UP,
    "DOWN":  Direction.DOWN,
    "LEFT":  Direction.LEFT,
    "RIGHT": Direction.RIGHT,
}


class SnakeController:
    def __init__(self, snake: Snake) -> None:
        self._snake = snake

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def snake(self) -> Snake:
        return self._snake

    # ── Commands ───────────────────────────────────────────────────────────
    def handle_input(self, action: str) -> None:
        direction = _INPUT_MAP.get(action.upper())
        if direction:
            self._snake.change_direction(direction)

    def tick(self) -> None:
        self._snake.move()