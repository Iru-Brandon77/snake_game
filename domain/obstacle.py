import random
from dataclasses import dataclass, field

@dataclass
class Obstacle:
    cells: set[tuple[int, int]] = field(default_factory=set)

    # ── Factory ────────────────────────────────────────────────────────────
    @classmethod
    def empty(cls) -> "Obstacle":
        return cls(cells=set())

    @classmethod
    def from_level(cls, level: int = 1) -> "Obstacle":
        layouts: dict[int, list[tuple[int, int]]] = {
            1: [
                (5, 5), (5, 6), (5, 7),
                (14, 12), (14, 13), (14, 14),
                (9, 2), (10, 2), (11, 2),
                (9, 17), (10, 17), (11, 17),
            ],
            2: [
                (3, 3), (3, 4), (3, 5), (3, 6),
                (16, 13), (16, 14), (16, 15), (16, 16),
                (7, 9), (8, 9), (9, 9), (10, 9), (11, 9),
            ],
        }

        cells = layouts.get(level, [])
        return cls(cells=set(cells))

    @classmethod
    def random(cls, board_width: int, board_height: int, count: int = 12) -> "Obstacle":
        cells = set()
        center_x = board_width // 2
        center_y = board_height // 2

        safe_zone = {
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
            (center_x - 3, center_y),
            (center_x + 1, center_y)
        }

        attempts = 0
        while len(cells) < count and attempts < 100:
            attempts += 1
            x = random.randint(0, board_width - 1)
            y = random.randint(0, board_height - 1)

            if (x, y) not in safe_zone:
                cells.add((x, y))

        return cls(cells=cells)

    # ── Queries ────────────────────────────────────────────────────────────
    def is_blocked(self, position: tuple[int, int]) -> bool:
        return position in self.cells