import random
from dataclasses import dataclass


@dataclass
class Food:
    position: tuple[int, int]

    # ── Factory ────────────────────────────────────────────────────────────
    @classmethod
    def spawn(
        cls,
        board_width: int,
        board_height: int,
        occupied: set[tuple[int, int]] | None = None,
    ) -> "Food":
        food = cls(position=(0, 0))
        food.relocate(board_width, board_height, occupied)
        return food

    # ── Commands ───────────────────────────────────────────────────────────
    def relocate(
        self,
        board_width: int,
        board_height: int,
        occupied: set[tuple[int, int]] | None = None,
    ) -> None:
        occupied = occupied or set()

        available = [
            (x, y)
            for x in range(board_width)
            for y in range(board_height)
            if (x, y) not in occupied
        ]

        if not available:
            raise RuntimeError("No free cells left to place food.")

        self.position = random.choice(available)