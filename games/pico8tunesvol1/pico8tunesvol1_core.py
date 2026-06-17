"""Pure album-player state for the Pico-8 Tunes Volume 1 PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class Track:
    title: str
    mood: str
    tempo: int
    palette: tuple[int, int, int]
    length_beats: int
    motif: tuple[str, ...]


class Pico8TunesVol1Core:
    """Controller-friendly 12-track music-cart/player state."""

    tracks = (
        Track("Pastoral", "bright meadow", 96, (11, 3, 10), 64, ("c3", "e3", "g3", "c4")),
        Track("Dungeon", "echo chamber", 84, (5, 13, 1), 72, ("c2", "d#2", "g2", "a#2")),
        Track("Sand", "desert swing", 108, (9, 10, 4), 80, ("d3", "f3", "a3", "c4")),
        Track("Orbit", "small stars", 112, (12, 6, 7), 64, ("g2", "b2", "d3", "g3")),
        Track("Clockwork", "tiny machine", 124, (8, 15, 2), 64, ("e3", "g3", "b3", "e4")),
        Track("Rain", "glass drops", 88, (1, 5, 6), 72, ("a2", "c3", "e3", "a3")),
        Track("Cavern", "low crystals", 76, (2, 13, 6), 72, ("f2", "g#2", "c3", "f3")),
        Track("Run", "arcade chase", 132, (8, 2, 10), 64, ("c3", "g3", "c4", "d#4")),
        Track("Harbor", "late lights", 92, (3, 12, 7), 80, ("g2", "a#2", "d3", "f3")),
        Track("Snow", "soft pulse", 86, (6, 7, 5), 72, ("d3", "a3", "b3", "f#3")),
        Track("Factory", "metal loop", 118, (0, 14, 8), 64, ("c2", "c3", "f#2", "g2")),
        Track("Finale", "two channel bloom", 104, (10, 12, 7), 96, ("c3", "e3", "a3", "c4")),
    )

    def __init__(self) -> None:
        self.current_index = 0
        self.elapsed_beats = 0
        self.status = "playing"
        self.message = "12 tunes"

    @property
    def current_track(self) -> Track:
        return self.tracks[self.current_index]

    def next_track(self) -> None:
        self.select_track(self.current_index + 1)

    def previous_track(self) -> None:
        self.select_track(self.current_index - 1)

    def select_track(self, index: int) -> None:
        self.current_index = index % len(self.tracks)
        self.elapsed_beats = 0
        self.status = "playing"
        self.message = self.current_track.title.lower()

    def toggle_pause(self) -> None:
        self.status = "paused" if self.status == "playing" else "playing"
        self.message = self.status

    def tick(self, beats: int = 1) -> None:
        if self.status != "playing":
            return
        self.elapsed_beats += max(0, beats)
        while self.elapsed_beats >= self.current_track.length_beats:
            self.elapsed_beats -= self.current_track.length_beats
            self.current_index = (self.current_index + 1) % len(self.tracks)
            self.message = self.current_track.title.lower()

    def progress(self) -> float:
        return self.elapsed_beats / self.current_track.length_beats

    def visualizer_points(self, *, beat: int | None = None, count: int = 24) -> list[tuple[int, int, int]]:
        track = self.current_track
        beat_value = self.elapsed_beats if beat is None else beat
        rng = random.Random(self.current_index * 4099 + beat_value * 17)
        points: list[tuple[int, int, int]] = []
        radius_base = 34 + (self.current_index % 5) * 6
        for i in range(count):
            angle = (i / count) * math.tau + beat_value * 0.08
            pulse = math.sin(beat_value * 0.19 + i * 0.7) * 18
            radius = radius_base + pulse + rng.randint(-5, 5)
            x = int(120 + math.cos(angle) * radius)
            y = int(126 + math.sin(angle) * radius)
            color = track.palette[i % len(track.palette)]
            points.append((max(0, min(239, x)), max(0, min(239, y)), color))
        return points

    def sequencer_notes(self) -> tuple[str, str]:
        motif = self.current_track.motif
        step = (self.elapsed_beats // 2) % len(motif)
        bass_step = (self.elapsed_beats // 4) % len(motif)
        return motif[step], motif[bass_step]
