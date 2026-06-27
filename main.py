from pathlib import Path

import settings
from persistence.high_score_repository import HighScoreRepository
from application.game_controller import GameController, GameState
from presentation.animation_manager import AnimationManager
from presentation.window import Window
from presentation.renderer import Renderer
from presentation.input_handler import InputHandler
from presentation.music_player import MusicPlayer


def main() -> None:
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
    animations = AnimationManager()
    animations.setup()

    previous_state = game.state

    # ── Game loop ──────────────────────────────────────────────────────────
    while not handler.quit_requested:
        for action in handler.collect():
            if action == "QUIT":
                break
            game.handle_input(action)
        dt = window.tick()
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

        if game.last_food_event is not None:
            grid_pos, points = game.last_food_event
            pixel_x, pixel_y = window.to_pixels(grid_pos)
            centro = (pixel_x + window.cell_size // 2, pixel_y + window.cell_size // 2)
            animations.spawn_score_popup(centro, points)

        animations.tick(dt)
        renderer.draw(game, animations)
        window.flip()

    # ── Teardown ───────────────────────────────────────────────────────────
    music.stop()
    window.teardown()


if __name__ == "__main__":
    main()