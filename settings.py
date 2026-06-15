# ── Board ──────────────────────────────────────────────────────────────────
BOARD_WIDTH:  int = 20   # columns
BOARD_HEIGHT: int = 20   # rows

# ── Window ─────────────────────────────────────────────────────────────────
CELL_SIZE: int = 30      # pixels per grid cell
FPS:       int = 10      # game speed
# (ticks per second)
WINDOW_TITLE: str = "Snake Game"

# ── Colors (R, G, B) ───────────────────────────────────────────────────────
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