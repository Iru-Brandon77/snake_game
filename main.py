from pathlib import Path

import settings
from persistence.high_score_repository import HighScoreRepository
from application.game_controller import GameController, GameState
from presentation.window import Window
from presentation.renderer import Renderer
from presentation.input_handler import InputHandler
from presentation.music_player import MusicPlayer


def main() -> None:
    # ── Wire services ──────────────────────────────────────────────────────
    repo = HighScoreRepository(Path("highscore.json"))
    game = GameController(repo)
    window = Window(board_width=settings.BOARD_WIDTH, board_height=settings.BOARD_HEIGHT, title=settings.WINDOW_TITLE)
    renderer = Renderer(window)
    handler = InputHandler()
    music = MusicPlayer()

    # ── Startup ────────────────────────────────────────────────────────────
    window.setup()
    renderer.setup()
    music.setup()
    music.pause()

    previous_state = game.state

    # ── Game loop ──────────────────────────────────────────────────────────
    while not handler.quit_requested:
        for action in handler.collect():
            if action == "QUIT":
                break
            game.handle_input(action)

        game.tick()

        # Sync music with game state transitions
        current_state = game.state
        if previous_state != current_state:
            if current_state == GameState.PAUSED:
                music.pause()
            elif current_state == GameState.RUNNING:
                music.resume()
            elif current_state == GameState.GAME_OVER:
                music.play_death()
            elif current_state == GameState.WAITING:
                music.pause()

        previous_state = current_state

        renderer.draw(game)
        window.flip()
        window.tick()

    # ── Teardown ───────────────────────────────────────────────────────────
    music.stop()
    window.teardown()


if __name__ == "__main__":
    main()