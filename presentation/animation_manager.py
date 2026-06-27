import pygame

from presentation.floating_text import FloatingText

class AnimationManager:
    DURATION_SECONDS: float = 0.8

    def __init__(self) -> None:
        self._texts: list[FloatingText] = []
        self._font: pygame.font.Font | None = None

    # ── Configuración ──────────────────────────────────────────
    def setup(self) -> None:
        self._font = pygame.font.SysFont("monospace", 22, bold=True)

    # ── Comandos ───────────────────────────────────────────────
    def spawn_score_popup(self, pixel_position: tuple[float, float], points: int) -> None:
        x, y = pixel_position
        text = f"+{points}" if points >= 0 else str(points)
        color = (90, 220, 110) if points >= 0 else (220, 70, 70)

        self._texts.append(
            FloatingText(
                text=text,
                color=color,
                x=x,
                y=y,
                time_left=self.DURATION_SECONDS,
                max_time=self.DURATION_SECONDS,
            )
        )

    def tick(self, dt: float) -> None:
        for floating_text in self._texts:
            floating_text.advance(dt)
        self._texts = [t for t in self._texts if not t.is_finished]

    # ── Dibujo ─────────────────────────────────────────────────
    def draw(self, screen: pygame.Surface) -> None:
        for floating_text in self._texts:
            surface = self._font.render(floating_text.text, True, floating_text.color)
            surface.set_alpha(floating_text.alpha)
            rect = surface.get_rect(center=(floating_text.x, floating_text.y))
            screen.blit(surface, rect)