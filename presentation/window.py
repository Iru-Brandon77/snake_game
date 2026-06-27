import pygame
import settings


class Window:
    CELL_SIZE: int = settings.CELL_SIZE
    FPS: int       = settings.FPS

    def __init__(
        self,
        board_width: int,
        board_height: int,
        title: str = "Snake Game",
    ) -> None:
        self._board_width  = board_width
        self._board_height = board_height
        self._title        = title
        self._screen: pygame.Surface | None = None
        self._clock: pygame.time.Clock | None = None

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def screen(self) -> pygame.Surface:
        if self._screen is None:
            raise RuntimeError("Window not initialized. Call setup() first.")
        return self._screen

    @property
    def cell_size(self) -> int:
        return self.CELL_SIZE

    @property
    def width(self) -> int:
        return self._board_width * self.CELL_SIZE

    @property
    def height(self) -> int:
        return self._board_height * self.CELL_SIZE

    def to_pixels(self, grid_pos: tuple[int, int]) -> tuple[int, int]:
        col, row = grid_pos
        return col * self.CELL_SIZE, row * self.CELL_SIZE

    # ── Commands ───────────────────────────────────────────────────────────
    def setup(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self._title)
        self._clock = pygame.time.Clock()

    def tick(self) -> float:
        if self._clock is None:
            raise RuntimeError("Window not initialized. Call setup() first.")
        milliseconds = self._clock.tick(self.FPS)
        return milliseconds / 1000.0

    def flip(self) -> None:
        pygame.display.flip()

    def teardown(self) -> None:
        pygame.quit()