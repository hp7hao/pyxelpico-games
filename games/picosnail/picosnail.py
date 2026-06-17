"""Pico Snail!: Dream Castle - PyxelPico port.

Adapted from the PICO-8 cart by GiantLNT / Floofinator (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=39897
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from picosnail_core import PicoSnailCore  # noqa: E402


SCREEN = 240


class PicoSnail:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Pico Snail", fps=30)
        self.core = PicoSnailCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4g4", "t", "456", "n", 12)
        pyxel.sound(1).set("g4c5", "p", "65", "n", 8)
        pyxel.sound(2).set("c3", "n", "7", "f", 8)
        pyxel.sound(3).set("e4g4c5", "s", "567", "n", 18)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if ih.btnp_select():
            self.core.restart()
            return
        if self.core.victory:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
                self.screen = "play"
            return
        move = int(ih.btn_right()) - int(ih.btn_left())
        if ih.btnp_a():
            self.core.tick(move=move, jump=True, hold_jump=True)
            pyxel.play(3, 0)
        else:
            self.core.tick(move=move, hold_jump=ih.btn_a())
        if ih.btnp_b():
            if self.core.thwack():
                pyxel.play(3, 1)
            elif self.core.cast_wand():
                pyxel.play(3, 1)
        if ih.btnp_up():
            self.core.collect_star()
            pyxel.play(3, 0)
        if ih.btnp_down():
            self.core.press_switch()
            pyxel.play(3, 3)
        if ih.btnp_start():
            if self.core.level_index == self.core.boss_level:
                self.core.attack_boss()
            else:
                self.core.enter_warp()

    def draw(self) -> None:
        pyxel.cls(12 if self.core.level_name == "garden" else 1)
        if self.screen == "title":
            self._draw_world()
            self._draw_title()
            return
        self._draw_world()
        self._draw_entities()
        self._draw_hud()
        if self.core.victory:
            self._panel("dream castle saved", "A dream again")

    def _draw_world(self) -> None:
        sky = {"garden": 12, "courtyard": 1, "entrance": 5, "halls": 13, "rooftops": 6, "the moon": 0, "nightmare": 2, "the end": 12}.get(self.core.level_name, 1)
        pyxel.cls(sky)
        for i in range(18):
            x = i * 16 + (self.core.level_index * 7) % 12
            y = 18 + (i * 23 + self.core.level_index * 11) % 92
            pyxel.pset(x % SCREEN, y, 7 if self.core.level_name in ("the moon", "nightmare", "courtyard") else 10)
        pyxel.rect(0, self.core.ground_y + 8, SCREEN, 70, 4 if self.core.level_name in ("garden", "the end") else 5)
        pyxel.rect(0, self.core.ground_y, SCREEN, 10, 11 if self.core.level_name == "garden" else 6)
        pyxel.rect(self.core.warp_x - 6, self.core.ground_y - 38, 12, 38, 10)
        pyxel.circ(self.core.warp_x, self.core.ground_y - 42, 10, 14 if self.core.level_index < self.core.boss_level or self.core.boss_defeated else 8)
        if not self.core.door_open:
            pyxel.rect(186, self.core.ground_y - 34, 16, 34, 4)
        pyxel.rect(40, self.core.ground_y - 8, 12, 8, 9)
        pyxel.text(34, self.core.ground_y - 18, "switch", 7)

    def _draw_entities(self) -> None:
        p = self.core.player
        x, y = int(p.x), int(p.y)
        pyxel.circ(x, y - 8, 8, 14)
        pyxel.circ(x - 6, y - 14, 4, 14)
        pyxel.pset(x - 7, y - 15, 0)
        pyxel.line(x - 10, y - 8, x - 18, y - 5, 14)
        pyxel.line(x - 14, y - 7, x - 21, y - 7, 14)
        pyxel.line(x, y - 8, x + p.facing * 14, y - 11, 10)
        for enemy in self.core.enemies:
            ex = int(enemy["x"])
            kind = str(enemy["kind"])
            color = {"thorn": 8, "salt": 7, "tar": 0}.get(kind, 8)
            pyxel.tri(ex - 7, self.core.ground_y, ex, self.core.ground_y - 16, ex + 7, self.core.ground_y, color)
        for shot in self.core.shots:
            pyxel.circ(int(shot["x"]), int(shot["y"]), 3, 10)
        if self.core.level_index == self.core.boss_level and not self.core.boss_defeated:
            pyxel.circ(204, self.core.ground_y - 18, 18, 8)
            pyxel.tri(190, self.core.ground_y - 30, 196, self.core.ground_y - 48, 202, self.core.ground_y - 30, 8)
            pyxel.tri(206, self.core.ground_y - 30, 212, self.core.ground_y - 48, 218, self.core.ground_y - 30, 8)
            pyxel.text(184, self.core.ground_y - 56, f"cat {self.core.boss_hp}", 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 34, 0)
        pyxel.text(5, 5, f"{self.core.level_name}  hp {self.core.health}/{self.core.max_health}  stars {self.core.stars}", 7)
        door = "open" if self.core.door_open else "closed"
        pyxel.text(5, 16, f"door {door}  {self.core.message[:28]}", 10)
        pyxel.text(5, 228, "D-pad move  A jump  B thwack/wand  Up star  Down switch  Start warp/boss", 6)

    def _draw_title(self) -> None:
        self._panel("PICO SNAIL!", "Dream Castle")
        self._center("GiantLNT / Floofinator", 122, 6)
        self._center("A start", 220, 10 if pyxel.frame_count % 40 < 28 else 5)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(22, 72, 196, 72, 0)
        pyxel.rectb(22, 72, 196, 72, 7)
        self._center(title, 92, 7)
        self._center(subtitle, 110, 10)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    PicoSnail()
