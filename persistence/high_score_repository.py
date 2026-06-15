import json
from pathlib import Path


class HighScoreRepository:
    """
    Persists the high score in a JSON file.

    Knows:
      - How to load the high score from disk.
      - How to save a new high score to disk.

    Does NOT know:
      - The snake, food, or any game entity.
      - When to save (that decision belongs to the application layer).
      - How the score is calculated.
    """

    def __init__(self, file_path: Path = Path("highscore.json")) -> None:
        self._file_path = file_path

    # ── Queries ────────────────────────────────────────────────────────────
    def load(self) -> int:
        """
        Reads the high score from disk.
        Returns 0 if the file does not exist or is corrupted.
        """
        try:
            data = json.loads(self._file_path.read_text())
            return int(data["high_score"])
        except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError):
            return 0

    # ── Commands ───────────────────────────────────────────────────────────
    def save(self, score: int) -> None:
        """
        Writes the score to disk only if it beats the current high score.
        """
        if score > self.load():
            self._file_path.write_text(
                json.dumps({"high_score": score}, indent=2)
            )