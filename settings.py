# ── Board ──────────────────────────────────────────────────────────────────
BOARD_WIDTH:  int = 20
BOARD_HEIGHT: int = 20

# ── Window ─────────────────────────────────────────────────────────────────
CELL_SIZE: int = 30
FPS:       int = 8

WINDOW_TITLE: str = "Snake Game"

# ── Colors ─────────────────────────────────────────────────────────────────
COLOR_BACKGROUND:   tuple[int, int, int]         = (15,  15,  15)
COLOR_GRID:         tuple[int, int, int]         = (30,  30,  30)
COLOR_SNAKE_HEAD:   tuple[int, int, int]         = (80,  220, 100)
COLOR_SNAKE_BODY:   tuple[int, int, int]         = (50,  170,  70)
COLOR_FOOD:         tuple[int, int, int]         = (220,  60,  60)
COLOR_OBSTACLE:     tuple[int, int, int]         = (100, 100, 100)
COLOR_TEXT_PRIMARY: tuple[int, int, int]         = (220, 220, 220)
COLOR_TEXT_DIM:     tuple[int, int, int]         = (120, 120, 120)
COLOR_OVERLAY:      tuple[int, int, int, int]    = (0,   0,   0,  160)

# ── Scoring ────────────────────────────────────────────────────────────────
POINTS_PER_FOOD: int = 10

# ── Tipos de comida ──────────────────────────────────────────────
FOOD_TYPES: dict[str, dict] = {
    "normal": {
        "color": COLOR_FOOD,
        "points": POINTS_PER_FOOD,
        "growth": 1,
        "temporary": False,
        "lifetime_ticks": None,
    },
    "golden": {
        "color": (255, 215, 0),
        "points": POINTS_PER_FOOD * 2,
        "growth": 2,
        "temporary": False,
        "lifetime_ticks": None,
    },
    "bad": {
        "color": (160, 32, 200),
        "points": -POINTS_PER_FOOD,
        "growth": 0,
        "temporary": True,
        "lifetime_ticks": 40,
    },
}

SPECIAL_FOOD_SPAWN_CHANCE: float = 0.02