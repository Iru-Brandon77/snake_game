from dataclasses import dataclass


@dataclass
class FloatingText:
    text: str
    color: tuple[int, int, int]
    x: float
    y: float
    time_left: float
    max_time: float

    # ── Acciones ───────────────────────────────────────────────
    def advance(self, dt: float) -> None:
        self.y -= 40 * dt
        self.time_left -= dt

    # ── Consultas ──────────────────────────────────────────────
    @property
    def is_finished(self) -> bool:
        return self.time_left <= 0

    @property
    def alpha(self) -> int:
        ratio = max(0.0, self.time_left / self.max_time)
        return int(255 * ratio)