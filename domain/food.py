import random
from dataclasses import dataclass


@dataclass
class Food:
    """
    Represents a single food item on the board.

    Knows:
      - Its current position.
      - How to move itself to a new random position.

    Does NOT know:
      - The snake, obstacles, or any other game entity.
      - How to draw itself.
      - What happens when the snake eats it.
    """

    position: tuple[int, int]

    # ── Factory ────────────────────────────────────────────────────────────
    @classmethod
    def spawn(
        cls,
        board_width: int,
        board_height: int,
        occupied: set[tuple[int, int]] | None = None,
    ) -> "Food":
        """Creates a Food item at a random unoccupied cell."""
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
        """
        Moves the food to a new random cell that is not in `occupied`.
        `occupied` should contain the snake body + obstacle positions.
        """
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