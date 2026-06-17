"""MOTION REC - PyxelPico port.

Adapted from the PICO-8 cart by shomaisshi (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=53392
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from motionrec_core import MotionRecCore  # noqa: E402


SCREEN = 240
FLOOR = int(MotionRecCore.floor_y)


class MotionRec:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="MOTION REC", fps=30)
        self.core = MotionRecCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4g4", "p", "6", "n", 8)
        pyxel.sound(1).set("g3c4e4g4", "t", "5", "f", 10)
        pyxel.sound(2).set("c3", "n", "7", "f", 8)
        pyxel.sound(3).set("e4g4c5", "s", "6", "n", 8)

    def reset(self) -> None:
        self.core.restart_level()
        self.screen = "play"
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 0)
            return
        if self.core.cleared:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.screen = "title"
            return

        old_message = self.core.message
        if ih.btnp_a():
            if ih.btn_up():
                self.core.start_recording()
                pyxel.play(3, 1)
            elif ih.btn_down():
                self.core.start_playback(reverse=True)
                pyxel.play(3, 3)
            elif self.core.mode == "record":
                self.core.stop_recording()
                pyxel.play(3, 1)
            else:
                self.core.start_playback(reverse=False)
                pyxel.play(3, 3)

        self.core.tick(left=ih.btn_left(), right=ih.btn_right(), jump=ih.btnp_b())
        if self.core.message != old_message and "solved" in self.core.message:
            self.flash = 8
            pyxel.play(3, 0)
        if ih.btnp_select():
            self.reset()

    def draw(self) -> None:
        pyxel.cls(7 if self.flash else self._bg_color())
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_stage()
        self._draw_ghost_path()
        self._draw_clone()
        self._draw_player()
        self._draw_hud()
        if self.core.cleared:
            self._panel("motion solved", "A replay   Select title")

    def _bg_color(self) -> int:
        if self.core.mode == "record":
            return 2
        if self.core.mode == "playback":
            return 12
        return 1

    def _draw_title(self) -> None:
        self._draw_stage_grid()
        self._center("MOTION", 58, 7)
        self._center("REC", 78, 10)
        self._center("shomaisshi", 98, 6)
        self._draw_record_icon(120, 132, 24)
        self._center("A start", 208, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_stage(self) -> None:
        self._draw_stage_grid()
        pyxel.rect(0, FLOOR + 8, SCREEN, 72, 5)
        for x in range(0, SCREEN, 20):
            pyxel.rectb(x, FLOOR + 8, 20, 16, 13)
        self._draw_switch()
        self._draw_goal()

    def _draw_stage_grid(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, self._bg_color())
        for x in range(0, SCREEN, 16):
            pyxel.line(x, 0, x, SCREEN, 13)
        for y in range(0, SCREEN, 16):
            pyxel.line(0, y, SCREEN, y, 13)

    def _draw_switch(self) -> None:
        color = 10 if self.core.switch_active else 8
        x = int(self.core.switch_x)
        pyxel.rect(x - 12, FLOOR + 2, 24, 6, color)
        pyxel.rectb(x - 12, FLOOR + 2, 24, 6, 0)
        pyxel.text(x - 10, FLOOR - 10, "rec", color)

    def _draw_goal(self) -> None:
        x = int(self.core.goal_x)
        color = 8 if self.core.goal_locked else 11
        pyxel.rect(x - 8, FLOOR - 35, 16, 43, color)
        pyxel.rectb(x - 8, FLOOR - 35, 16, 43, 0)
        pyxel.text(x - 8, FLOOR - 45, "goal", color)

    def _draw_ghost_path(self) -> None:
        points = self.core.replay_ghost_points()
        for index, (x, y) in enumerate(points):
            color = 10 if index % 2 == 0 else 6
            pyxel.circ(int(x), int(y) - 10, 2, color)

    def _draw_clone(self) -> None:
        if self.core.mode != "playback" and not self.core.switch_active:
            return
        self._draw_actor(int(self.core.clone.x), int(self.core.clone.y), 12, ghost=True)

    def _draw_player(self) -> None:
        color = 10 if self.core.mode == "record" else 7
        self._draw_actor(int(self.core.player.x), int(self.core.player.y), color, ghost=False)

    def _draw_actor(self, x: int, y: int, color: int, *, ghost: bool) -> None:
        pyxel.rect(x - 5, y - 18, 10, 18, color)
        pyxel.circ(x, y - 22, 5, 7 if not ghost else 6)
        pyxel.pset(x + (2 if self.core.player.facing > 0 else -2), y - 23, 0)
        if ghost:
            pyxel.circb(x, y - 12, 14, 12)

    def _draw_record_icon(self, x: int, y: int, radius: int) -> None:
        pyxel.circb(x, y, radius, 7)
        pyxel.circ(x, y, radius - 9, 8)
        pyxel.text(x - 13, y + radius + 8, "record", 6)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 30, 0)
        pyxel.text(8, 6, f"mode {self.core.mode}", 7)
        pyxel.text(82, 6, f"frames {len(self.core.recorded_path)}", 10)
        pyxel.text(158, 6, "door open" if not self.core.goal_locked else "door locked", 11 if not self.core.goal_locked else 8)
        pyxel.rect(8, 20, 82, 5, 5)
        pyxel.rect(8, 20, int(82 * self.core.recording_ratio), 5, 10)
        pyxel.text(100, 19, "Up+A rec  A play  Down+A reverse  B jump", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 91, 192, 58, 0)
        pyxel.rectb(24, 91, 192, 58, 7)
        self._center(title, 110, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    MotionRec()
