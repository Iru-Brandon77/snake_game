from pathlib import Path

import settings
from persistence.high_score_repository import HighScoreRepository
from application.game_controller import GameController
from presentation.window import Window
from presentation.renderer import Renderer
from presentation.input_handler import InputHandler


def main() -> None:
    # ── Wire services ──────────────────────────────────────────────────────
    repo     = HighScoreRepository(Path("highscore.json"))
    game     = GameController(repo)
    window   = Window(board_width=settings.BOARD_WIDTH, board_height=settings.BOARD_HEIGHT, title=settings.WINDOW_TITLE)
    renderer = Renderer(window)
    handler  = InputHandler()

    # ── Startup ────────────────────────────────────────────────────────────
    window.setup()
    renderer.setup()

    # ── Game loop ──────────────────────────────────────────────────────────
    while not handler.quit_requested:
        for action in handler.collect():
            if action == "QUIT":
                break
            game.handle_input(action)

        game.tick()
        renderer.draw(game)
        window.flip()
        window.tick()

    # ── Teardown ───────────────────────────────────────────────────────────
    window.teardown()


if __name__ == "__main__":
    main()