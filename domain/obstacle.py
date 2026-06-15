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

    # ── Queries ────────────────────────────────────────────────────────────
    def is_blocked(self, position: tuple[int, int]) -> bool:
        return position in self.cells