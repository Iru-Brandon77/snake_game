import pygame

# Maps pygame key constants to abstract action strings
_KEY_MAP: dict[int, str] = {
    pygame.K_UP:     "UP",
    pygame.K_w:      "UP",
    pygame.K_DOWN:   "DOWN",
    pygame.K_s:      "DOWN",
    pygame.K_LEFT:   "LEFT",
    pygame.K_a:      "LEFT",
    pygame.K_RIGHT:  "RIGHT",
    pygame.K_d:      "RIGHT",
    pygame.K_p:      "PAUSE",
    pygame.K_r:      "RESTART",
    pygame.K_ESCAPE: "QUIT",
}


class InputHandler:
    def __init__(self) -> None:
        self._quit_requested: bool = False

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def quit_requested(self) -> bool:
        return self._quit_requested

    # ── Commands ───────────────────────────────────────────────────────────
    def collect(self) -> list[str]:
        actions: list[str] = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_requested = True
                actions.append("QUIT")

            elif event.type == pygame.KEYDOWN:
                action = _KEY_MAP.get(event.key)
                if action:
                    actions.append(action)

        return actions