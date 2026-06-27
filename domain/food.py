import random
from dataclasses import dataclass


@dataclass
class Food:
    position: tuple[int, int]
    food_type: str = "normal"
    ticks_left: int | None = None

    # ── Fábrica ─────────────────────────
    @classmethod
    def spawn(
        cls,
        board_width: int,
        board_height: int,
        occupied: set[tuple[int, int]] | None = None,
        food_type: str = "normal",
        lifetime_ticks: int | None = None,
    ) -> "Food":
        food = cls(position=(0, 0), food_type=food_type, ticks_left=lifetime_ticks)
        food.relocate(board_width, board_height, occupied)
        return food

    # ── Acciones ───────────────────────────────────────────────
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

    def advance_tick(self) -> None:
        if self.ticks_left is not None:
            self.ticks_left -= 1

    # ── Preguntas sobre el estado ────────────────────────────────
    def is_expired(self) -> bool:        return self.ticks_left is not None and self.ticks_left <= 0