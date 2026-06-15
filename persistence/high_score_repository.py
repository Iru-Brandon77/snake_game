import json
from pathlib import Path


class HighScoreRepository:
    def __init__(self, file_path: Path = Path("highscore.json")) -> None:
        self._file_path = file_path

    # ── Queries ────────────────────────────────────────────────────────────
    def load(self) -> int:
        try:
            data = json.loads(self._file_path.read_text())
            return int(data["high_score"])
        except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError):
            return 0

    # ── Commands ───────────────────────────────────────────────────────────
    def save(self, score: int) -> None:
        if score > self.load():
            self._file_path.write_text(
                json.dumps({"high_score": score}, indent=2)
            )