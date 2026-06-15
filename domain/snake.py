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
    body: list[tuple[int, int]] = field(default_factory=list)
    direction: Direction = Direction.RIGHT
    _pending_growth: int = field(default=0, repr=False)

    # ── Factory ────────────────────────────────────────────────────────────
    @classmethod
    def spawn(cls, head: tuple[int, int]) -> "Snake":
        x, y = head
        body = [(x, y), (x - 1, y), (x - 2, y)]
        return cls(body=body, direction=Direction.RIGHT)

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def head(self) -> tuple[int, int]:
        return self.body[0]

    @property
    def segments(self) -> list[tuple[int, int]]:
        return self.body[1:]

    # ── Commands ───────────────────────────────────────────────────────────
    def change_direction(self, new_direction: Direction) -> None:
        if new_direction != _OPPOSITES[self.direction]:
            self.direction = new_direction

    def schedule_growth(self, segments: int = 1) -> None:
        self._pending_growth += segments

    def move(self) -> None:
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