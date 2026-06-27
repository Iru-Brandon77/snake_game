import random
import settings
from domain.food import Food
from domain.snake import Snake
from domain.obstacle import Obstacle


class FoodController:
    def __init__(self, food: Food, board_width: int, board_height: int) -> None:
        self._board_width = board_width
        self._board_height = board_height
        self._score: int = 0
        self._foods: list[Food] = [food]

    # ── Consultas ──────────────────────────────────────────────
    @property
    def foods(self) -> list[Food]:
        return self._foods

    @property
    def food(self) -> Food:
        return self._foods[0]

    @property
    def score(self) -> int:
        return self._score

    # ── Acciones ───────────────────────────────────────────────
    def tick(self, snake: Snake, obstacle: Obstacle) -> None:
        for food in self._foods:
            food.advance_tick()

        self._foods = [food for food in self._foods if not food.is_expired()]

        self._try_spawn_special_food(snake, obstacle)

    def on_food_eaten(self, food: Food, snake: Snake, obstacle: Obstacle) -> None:
        properties = settings.FOOD_TYPES[food.food_type]
        self._score = max(0, self._score + properties["points"])

        if properties["growth"] > 0:
            snake.schedule_growth(properties["growth"])

        if food.food_type == "normal":
            occupied = set(snake.body) | obstacle.cells
            food.relocate(self._board_width, self._board_height, occupied)
        else:
            self._foods.remove(food)

    def reset(self, snake: Snake, obstacle: Obstacle) -> None:
        self._score = 0
        normal_food = self._foods[0]
        normal_food.food_type = "normal"
        normal_food.ticks_left = None

        occupied = set(snake.body) | obstacle.cells
        normal_food.relocate(self._board_width, self._board_height, occupied)

        self._foods = [normal_food]

    def _try_spawn_special_food(self, snake: Snake, obstacle: Obstacle) -> None:
        has_special_food = any(food.food_type != "normal" for food in self._foods)
        if has_special_food:
            return

        if random.random() > settings.SPECIAL_FOOD_SPAWN_CHANCE:
            return

        special_types = [name for name in settings.FOOD_TYPES if name != "normal"]
        chosen_type = random.choice(special_types)
        properties = settings.FOOD_TYPES[chosen_type]

        occupied = set(snake.body) | obstacle.cells | {food.position for food in self._foods}

        new_food = Food.spawn(
            self._board_width,
            self._board_height,
            occupied=occupied,
            food_type=chosen_type,
            lifetime_ticks=properties["lifetime_ticks"],
        )
        self._foods.append(new_food)