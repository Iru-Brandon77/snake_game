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
    """
    Listens to pygame events and translates them to abstract actions.

    Knows:
      - Which keys map to which actions.
      - How to detect a quit event (window close button).

    Does NOT know:
      - What the game does with those actions.
      - Any game state or entity.
      - How to draw anything.
    """

    def __init__(self) -> None:
        self._quit_requested: bool = False

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def quit_requested(self) -> bool:
        return self._quit_requested

    # ── Commands ───────────────────────────────────────────────────────────
    def collect(self) -> list[str]:
        """
        Processes all pending pygame events and returns a list of
        abstract action strings detected this frame.
        Returns an empty list if no relevant keys were pressed.
        """
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