import numpy as np
import pygame

# ── Audio settings ─────────────────────────────────────────────────────────
_SAMPLE_RATE   = 44100
_VOLUME_BG     = 0.15
_VOLUME_DEATH  = 0.4

# ── Note frequencies (Hz) ──────────────────────────────────────────────────
_NOTES = {
    "C4":  261.63, "D4":  293.66, "E4":  329.63,
    "F4":  349.23, "G4":  392.00, "A4":  440.00,
    "B4":  493.88, "C5":  523.25, "D5":  587.33,
    "E5":  659.25, "F5":  698.46, "G5":  783.99,
    "REST": 0.0,
}

# ── Background melody: simple, calm, original loop ─────────────────────────
# Gentle descending/ascending pattern — no famous songs involved :)
_BG_BPM  = 120
_BG_BEAT = 60.0 / _BG_BPM

_BG_MELODY: list[tuple[str, float]] = [
    ("C5", 1.0), ("G4", 0.5), ("E4", 0.5), ("A4", 1.0),
    ("REST", 0.5), ("G4", 0.5), ("F4", 1.0),
    ("E4", 0.5), ("D4", 0.5), ("C4", 1.0), ("REST", 1.0),
    ("E4", 0.5), ("F4", 0.5), ("G4", 1.0),
    ("A4", 0.5), ("REST", 0.5), ("C5", 1.0),
    ("D5", 0.5), ("C5", 0.5), ("B4", 0.5), ("A4", 0.5),
    ("G4", 1.0), ("REST", 1.0),
]

# ── Death sound: short descending tones — "wah wah wah" feel ──────────────
_DEATH_SEQUENCE: list[tuple[float, float]] = [
    (440.0, 0.18),   # A4
    (370.0, 0.18),   # F#4
    (311.0, 0.18),   # Eb4
    (220.0, 0.40),   # A3 — long final drop
]


class MusicPlayer:
    def __init__(self) -> None:
        self._initialized  = False
        self._bg_sound:    pygame.mixer.Sound | None = None
        self._death_sound: pygame.mixer.Sound | None = None
        self._bg_channel:  pygame.mixer.Channel | None = None

    # ── Setup ──────────────────────────────────────────────────────────────
    def setup(self) -> None:
        """Generates all audio and starts background music. Call once at startup."""
        pygame.mixer.pre_init(_SAMPLE_RATE, -16, 2, 512)
        pygame.mixer.init()

        self._bg_sound    = self._make_sound(self._build_sequence(_BG_MELODY, _BG_BEAT), _VOLUME_BG)
        self._death_sound = self._make_sound(self._build_death(), _VOLUME_DEATH)

        self._bg_channel = self._bg_sound.play(loops=-1)
        self._initialized = True

    # ── Commands ───────────────────────────────────────────────────────────
    def pause(self) -> None:
        """Pauses background music (on game pause)."""
        if self._bg_channel:
            self._bg_channel.pause()

    def resume(self) -> None:
        """Resumes background music (on game resume)."""
        if self._bg_channel:
            self._bg_channel.unpause()

    def play_death(self) -> None:
        """Pauses background music and plays the death sound effect."""
        if not self._initialized:
            return
        self.pause()
        self._death_sound.play()

    def stop(self) -> None:
        """Stops all audio (on teardown)."""
        if self._initialized:
            pygame.mixer.stop()

    # ── Private ────────────────────────────────────────────────────────────
    def _make_sound(self, mono: np.ndarray, volume: float) -> pygame.mixer.Sound:
        """Converts a mono int16 array to a stereo pygame Sound."""
        stereo = np.column_stack((mono, mono))
        sound  = pygame.sndarray.make_sound(stereo)
        sound.set_volume(volume)
        return sound

    def _build_sequence(
        self,
        melody: list[tuple[str, float]],
        beat_secs: float,
    ) -> np.ndarray:
        """Builds a melody from (note_name, beats) pairs."""
        chunks = [
            self._make_tone(_NOTES[note], beats * beat_secs)
            for note, beats in melody
        ]
        return np.concatenate(chunks).astype(np.int16)

    def _build_death(self) -> np.ndarray:
        """Builds the death sound from (frequency, seconds) pairs."""
        chunks = [
            self._make_tone(freq, secs)
            for freq, secs in _DEATH_SEQUENCE
        ]
        return np.concatenate(chunks).astype(np.int16)

    def _make_tone(self, freq: float, duration: float) -> np.ndarray:
        n  = int(_SAMPLE_RATE * duration)
        t  = np.linspace(0, duration, n, endpoint=False)

        if freq == 0.0:
            wave = np.zeros(n)
        else:
            wave = np.sign(np.sin(2 * np.pi * freq * t))

        # Fade-out last 5% to avoid clicks
        fade_len = max(1, int(n * 0.05))
        wave[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)

        return (wave * 32767).astype(np.int16)