from enum import Enum, auto

import settings
from application.obstacle_controller import ObstacleController
from domain.game_rules import GameRules
from domain.obstacle import Obstacle
from domain.snake import Snake
from domain.food import Food
from application.snake_controller import SnakeController
from application.food_controller import FoodController
from persistence.high_score_repository import HighScoreRepository


class GameState(Enum):
    WAITING = auto()
    RUNNING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class GameController:
    BOARD_WIDTH = settings.BOARD_WIDTH
    BOARD_HEIGHT = settings.BOARD_HEIGHT

    def __init__(self, high_score_repo: HighScoreRepository) -> None:
        self._repo = high_score_repo
        self._high_score = high_score_repo.load()
        self._state = GameState.WAITING
        self._obstacle_ctrl = ObstacleController(self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self._obstacle_ctrl.generate_random_map(count=12)
        self._snake_ctrl, self._food_ctrl = self._build_controllers()

    # ── Queries ────────────────────────────────────────────────────────────
    @property
    def state(self) -> GameState:
        return self._state

    @property
    def score(self) -> int:
        return self._food_ctrl.score

    @property
    def high_score(self) -> int:
        return self._high_score

    @property
    def snake(self) -> Snake:
        return self._snake_ctrl.snake

    @property
    def food(self) -> Food:
        return self._food_ctrl.food

    @property
    def obstacle(self) -> Obstacle:
        return self._obstacle_ctrl.obstacle

    # ── Commands ───────────────────────────────────────────────────────────
    def handle_input(self, action: str) -> None:
        if self._state == GameState.WAITING:
            self._state = GameState.RUNNING
            return

        if action == "PAUSE" and self._state == GameState.RUNNING:
            self._state = GameState.PAUSED
            return

        if action == "PAUSE" and self._state == GameState.PAUSED:
            self._state = GameState.RUNNING
            return

        if action == "RESTART" and self._state == GameState.GAME_OVER:
            self._restart()
            return

        if self._state == GameState.RUNNING:
            self._snake_ctrl.handle_input(action)

    def _on_restart(self) -> None:
        self._state = GameState.WAITING

    def tick(self) -> None:
        if self._state != GameState.RUNNING:
            return

        self._snake_ctrl.tick()

        if GameRules.is_dead(self.snake, self.obstacle, self.BOARD_WIDTH, self.BOARD_HEIGHT):
            self._on_game_over()
            return

        if GameRules.ate_food(self.snake.head, self.food.position):
            self.snake.schedule_growth()
            self._food_ctrl.on_food_eaten(self.snake, self.obstacle)

    # ── Private ────────────────────────────────────────────────────────────
    def _on_game_over(self) -> None:
        self._state = GameState.GAME_OVER
        self._repo.save(self.score)
        self._high_score = self._repo.load()

    def _restart(self) -> None:
        self._state = GameState.RUNNING
        self._obstacle_ctrl.generate_random_map(count=12)

        self._snake_ctrl, self._food_ctrl = self._build_controllers()

    def _build_controllers(self) -> tuple[SnakeController, FoodController]:
        snake = Snake.spawn(head=(self.BOARD_WIDTH // 2, self.BOARD_HEIGHT // 2))
        food = Food.spawn(
            self.BOARD_WIDTH,
            self.BOARD_HEIGHT,
            occupied=set(snake.body) | self.obstacle.cells,
        )
        snake_ctrl = SnakeController(snake)
        food_ctrl = FoodController(food, self.BOARD_WIDTH, self.BOARD_HEIGHT, settings.POINTS_PER_FOOD)
        return snake_ctrl, food_ctrl