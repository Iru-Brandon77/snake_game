import settings
from domain.obstacle import Obstacle

class ObstacleController:
    def __init__(self, board_width: int, board_height: int) -> None:
        self._board_width = board_width
        self._board_height = board_height
        self._obstacle: Obstacle = Obstacle.empty()

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def obstacle(self) -> Obstacle:
        return self._obstacle

    # ── Commands ───────────────────────────────────────────────────────────
    def generate_random_map(self, count: int = 12) -> None:
        self._obstacle = Obstacle.random(self._board_width, self._board_height, count)