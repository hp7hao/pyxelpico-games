"""Pico-8 Tunes Volume 1 - PyxelPico port.

Adapted from the PICO-8 music cart by Gruber and Krajzeg (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=29008
"""

from __future__ import annotations

import os
import sys
import math

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from pico8tunesvol1_core import Pico8TunesVol1Core  # noqa: E402


SCREEN = 240


class Pico8TunesVol1:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Pico-8 Tunes Vol. 1", fps=30)
        self.core = Pico8TunesVol1Core()
        self.beat_timer = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        for index, track in enumerate(self.core.tracks[:8]):
            note_a, note_b = track.motif[0], track.motif[1]
            pyxel.sound(index).set(
                f"{note_a}{note_b}{track.motif[2]}{note_b}",
                "tp" if index % 2 == 0 else "sp",
                "4565",
                "n",
                max(6, min(18, 180 // track.tempo)),
            )

    def update(self) -> None:
        changed = False
        if ih.btnp_right(hold=12, repeat=8) or ih.btnp_down(hold=12, repeat=8):
            self.core.next_track()
            changed = True
        elif ih.btnp_left(hold=12, repeat=8) or ih.btnp_up(hold=12, repeat=8):
            self.core.previous_track()
            changed = True
        if ih.btnp_a() or ih.btnp_start():
            self.core.toggle_pause()
        if ih.btnp_b() or ih.btnp_select():
            self.core.select_track(0)
            changed = True

        self.beat_timer += 1
        frames_per_beat = max(7, int(1800 / self.core.current_track.tempo))
        if self.beat_timer >= frames_per_beat:
            self.beat_timer = 0
            before = self.core.current_index
            self.core.tick()
            changed = changed or before != self.core.current_index
            self._play_step()
        if changed:
            self._play_step()

    def _play_step(self) -> None:
        if self.core.status != "playing":
            return
        sound = self.core.current_index % 8
        pyxel.play(0, sound)
        if self.core.elapsed_beats % 4 == 0:
            pyxel.play(1, (sound + 3) % 8)

    def draw(self) -> None:
        track = self.core.current_track
        bg, accent, glow = track.palette
        pyxel.cls(bg)
        self._draw_album_field(accent, glow)
        self._draw_visualizer()
        self._draw_setlist()
        self._draw_player_panel()

    def _draw_album_field(self, accent: int, glow: int) -> None:
        for y in range(0, SCREEN, 12):
            offset = (pyxel.frame_count + y * 3) % SCREEN
            pyxel.line(0, y, SCREEN, (y + offset // 12) % SCREEN, accent)
        for i in range(18):
            x = (i * 37 + pyxel.frame_count * (1 + i % 3)) % SCREEN
            y = (i * 29 + pyxel.frame_count * 2) % SCREEN
            pyxel.pset(x, y, glow)

    def _draw_visualizer(self) -> None:
        pyxel.circb(120, 126, 74, 7)
        pyxel.circb(120, 126, 52, 5)
        for x, y, color in self.core.visualizer_points(beat=pyxel.frame_count // 4, count=28):
            pyxel.circ(x, y, 3, color)
        needle_angle = self.core.progress() * 6.28318 - 1.5708
        nx = int(120 + 68 * math.cos(needle_angle))
        ny = int(126 + 68 * math.sin(needle_angle))
        pyxel.line(120, 126, nx, ny, 7)
        pyxel.circ(120, 126, 5, 0)

    def _draw_setlist(self) -> None:
        start = max(0, min(len(self.core.tracks) - 5, self.core.current_index - 2))
        pyxel.rect(8, 10, 100, 74, 0)
        pyxel.rectb(8, 10, 100, 74, 7)
        pyxel.text(14, 16, "vol.1 setlist", 7)
        for row, index in enumerate(range(start, min(start + 5, len(self.core.tracks)))):
            track = self.core.tracks[index]
            y = 30 + row * 10
            marker = ">" if index == self.core.current_index else " "
            color = 10 if index == self.core.current_index else 6
            pyxel.text(14, y, f"{marker}{index + 1:02d} {track.title[:16]}", color)

    def _draw_player_panel(self) -> None:
        track = self.core.current_track
        pyxel.rect(18, 178, 204, 46, 0)
        pyxel.rectb(18, 178, 204, 46, 7)
        self._center(track.title.upper(), 186, 7)
        self._center(f"{track.mood}  {track.tempo} bpm", 198, 6)
        bar_w = 160
        pyxel.rect(40, 212, bar_w, 5, 5)
        pyxel.rect(40, 212, int(bar_w * self.core.progress()), 5, 10)
        state = "paused" if self.core.status == "paused" else "playing"
        pyxel.text(26, 230, f"Left/Right track  A {state}  B reset", 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Pico8TunesVol1()
