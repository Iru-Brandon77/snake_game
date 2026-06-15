import pygame
import settings

from application.game_controller import GameController, GameState
from presentation.window import Window


class Renderer:
    def __init__(self, window: Window) -> None:
        self._window = window
        self._font_large: pygame.font.Font | None = None
        self._font_small: pygame.font.Font | None = None

    # ── Setup ──────────────────────────────────────────────────────────────
    def setup(self) -> None:
        """Loads fonts. Call once after pygame.init()."""
        self._font_large = pygame.font.SysFont("monospace", 36, bold=True)
        self._font_small = pygame.font.SysFont("monospace", 18)

    # ── Main draw call ─────────────────────────────────────────────────────
    def draw(self, game: GameController) -> None:
        screen = self._window.screen
        screen.fill(settings.COLOR_BACKGROUND)

        self._draw_grid(screen)
        self._draw_obstacles(screen, game)
        self._draw_food(screen, game)
        self._draw_snake(screen, game)
        self._draw_hud(screen, game)

        if game.state == GameState.PAUSED:
            self._draw_overlay(screen, "PAUSED", "Press P to continue")

        if game.state == GameState.GAME_OVER:
            self._draw_overlay(screen, "GAME OVER", "Press R to restart")

    # ── Private draw helpers ───────────────────────────────────────────────
    def _draw_grid(self, screen: pygame.Surface) -> None:
        cell = self._window.cell_size
        for x in range(0, self._window.width, cell):
            pygame.draw.line(screen, settings.COLOR_GRID, (x, 0), (x, self._window.height))
        for y in range(0, self._window.height, cell):
            pygame.draw.line(screen, settings.COLOR_GRID, (0, y), (self._window.width, y))

    def _draw_snake(self, screen: pygame.Surface, game: GameController) -> None:
        cell = self._window.cell_size
        for index, segment in enumerate(game.snake.body):
            x, y = self._window.to_pixels(segment)
            color = settings.COLOR_SNAKE_HEAD if index == 0 else settings.COLOR_SNAKE_BODY
            pygame.draw.rect(screen, color, (x + 1, y + 1, cell - 2, cell - 2), border_radius=4)

    def _draw_food(self, screen: pygame.Surface, game: GameController) -> None:
        cell = self._window.cell_size
        x, y = self._window.to_pixels(game.food.position)
        cx = x + cell // 2
        cy = y + cell // 2
        pygame.draw.circle(screen, settings.COLOR_FOOD, (cx, cy), cell // 2 - 3)

    def _draw_obstacles(self, screen: pygame.Surface, game: GameController) -> None:
        cell = self._window.cell_size
        for pos in game.obstacle.cells:
            x, y = self._window.to_pixels(pos)
            pygame.draw.rect(screen, settings.COLOR_OBSTACLE, (x + 1, y + 1, cell - 2, cell - 2), border_radius=2)

    def _draw_hud(self, screen: pygame.Surface, game: GameController) -> None:
        score_text = self._font_small.render(f"SCORE  {game.score}", True, settings.COLOR_TEXT_PRIMARY)
        best_text  = self._font_small.render(f"BEST   {game.high_score}", True, settings.COLOR_TEXT_DIM)
        screen.blit(score_text, (8, 8))
        screen.blit(best_text,  (8, 28))

    def _draw_overlay(
        self,
        screen: pygame.Surface,
        title: str,
        subtitle: str,
    ) -> None:
        overlay = pygame.Surface((self._window.width, self._window.height), pygame.SRCALPHA)
        overlay.fill(settings.COLOR_OVERLAY)
        screen.blit(overlay, (0, 0))

        title_surf    = self._font_large.render(title,    True, settings.COLOR_TEXT_PRIMARY)
        subtitle_surf = self._font_small.render(subtitle, True, settings.COLOR_TEXT_DIM)

        cx = self._window.width  // 2
        cy = self._window.height // 2

        screen.blit(title_surf,    title_surf.get_rect(center=(cx, cy - 24)))
        screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(cx, cy + 20)))