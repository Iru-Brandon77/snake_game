from dataclasses import dataclass, field
from enum import Enum, auto


class Direction(Enum):
    UP    = auto()
    DOWN  = auto()
    LEFT  = auto()
    RIGHT = auto()


# Directions that cannot be combined (would cause instant self-collision)
_OPPOSITES: dict[Direction, Direction] = {
    Direction.UP:    Direction.DOWN,
    Direction.DOWN:  Direction.UP,
    Direction.LEFT:  Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


@dataclass
class Snake:
    """
    Represents the snake's body and movement logic.

    body[0]  → head
    body[-1] → tail

    The snake does NOT know the board dimensions.
    Collision detection belongs to a separate GameRules class.
    """

    body: list[tuple[int, int]] = field(default_factory=list)
    direction: Direction = Direction.RIGHT
    _pending_growth: int = field(default=0, repr=False)

    # ── Factory ────────────────────────────────────────────────────────────
    @classmethod
    def spawn(cls, head: tuple[int, int]) -> "Snake":
        """
        Creates a snake with 3 segments starting at `head`,
        extending to the left (natural for a right-moving snake).
        """
        x, y = head
        body = [(x, y), (x - 1, y), (x - 2, y)]
        return cls(body=body, direction=Direction.RIGHT)

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def head(self) -> tuple[int, int]:
        return self.body[0]

    @property
    def segments(self) -> list[tuple[int, int]]:
        """All body cells except the head (useful for collision checks)."""
        return self.body[1:]

    # ── Commands ───────────────────────────────────────────────────────────
    def change_direction(self, new_direction: Direction) -> None:
        """
        Updates the direction only if it is not the direct opposite
        of the current one (prevents reversing into itself).
        """
        if new_direction != _OPPOSITES[self.direction]:
            self.direction = new_direction

    def schedule_growth(self, segments: int = 1) -> None:
        """Queues extra segments to be added on the next move calls."""
        self._pending_growth += segments

    def move(self) -> None:
        """
        Advances the snake one cell in the current direction.
        If growth is pending, the tail is NOT removed (snake grows).
        """
        new_head = self._next_head_position()
        self.body.insert(0, new_head)

        if self._pending_growth > 0:
            self._pending_growth -= 1   # grow: keep the tail
        else:
            self.body.pop()             # normal move: remove the tail

    # ── Private helpers ────────────────────────────────────────────────────
    def _next_head_position(self) -> tuple[int, int]:
        x, y = self.head
        match self.direction:
            case Direction.UP:    return (x,     y - 1)
            case Direction.DOWN:  return (x,     y + 1)
            case Direction.LEFT:  return (x - 1, y)
            case Direction.RIGHT: return (x + 1, y)