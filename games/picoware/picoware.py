"""PICOWARE — PyxelPico port.

Adapted from the PICO-8 collaboration cart by the PICOWARE team
(CC BY-NC-SA 4.0). Original BBS thread:
https://www.lexaloffle.com/bbs/?tid=34751
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from picoware_core import MicroKind, PicowareCore, RoundState  # noqa: E402


SCREEN = 240


class Picoware:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="PICOWARE", fps=30)
        self.core = PicowareCore()
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4g4", "t", "6", "n", 6)
        pyxel.sound(1).set("g4c5", "p", "7", "n", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 12)

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.core.state is RoundState.TITLE:
            if ih.btnp_a() or ih.btnp_start():
                self.core.start()
                pyxel.play(3, 0)
            return
        if self.core.state is RoundState.GAME_OVER:
            if ih.btnp_a() or ih.btnp_start():
                self.core.start()
                pyxel.play(3, 0)
            return

        if self.core.state is RoundState.PLAYING:
            for name, pressed in self._pressed_buttons().items():
                if pressed:
                    prev_state = self.core.state
                    self.core.input_press(name)
                    if prev_state is RoundState.PLAYING and self.core.state is RoundState.RESULT:
                        pyxel.play(3, 1 if self.core.success else 2)
                        self.flash = 8
                    break
        prev_state = self.core.state
        self.core.tick()
        if prev_state is RoundState.PLAYING and self.core.state is RoundState.RESULT:
            pyxel.play(3, 1 if self.core.success else 2)
            self.flash = 8

    def draw(self) -> None:
        pyxel.cls(7 if self.flash and self.core.success else 1 if not self.flash else 8)
        if self.core.state is RoundState.TITLE:
            self._draw_title()
            return
        if self.core.state is RoundState.GAME_OVER:
            self._draw_game_over()
            return
        self._draw_header()
        self._draw_microgame()
        if self.core.state is RoundState.RESULT:
            self._draw_result()

    def _pressed_buttons(self) -> dict[str, bool]:
        return {
            "up": ih.btnp_up(),
            "down": ih.btnp_down(),
            "left": ih.btnp_left(),
            "right": ih.btnp_right(),
            "a": ih.btnp_a(),
            "b": ih.btnp_b() or ih.btnp_select(),
        }

    def _draw_title(self) -> None:
        self._draw_party_backdrop()
        self._center("PICOWARE", 54, 10)
        self._center("microgame rush", 70, 7)
        self._draw_button_grid(120, 126)
        self._center("d-pad + A/B", 184, 7)
        self._center("press A", 210, 11)

    def _draw_game_over(self) -> None:
        self._draw_party_backdrop()
        self._center("game over", 84, 8)
        self._center(f"score {self.core.score}", 108, 10)
        self._center("press A", 150, 11)

    def _draw_header(self) -> None:
        pyxel.rect(0, 0, SCREEN, 30, 0)
        pyxel.text(8, 7, f"round {self.core.round_index}", 7)
        pyxel.text(82, 7, f"score {self.core.score}", 7)
        pyxel.text(160, 7, "life " + "*" * self.core.lives, 8 if self.core.lives <= 1 else 7)
        w = max(0, int(224 * self.core.time_left / max(1, self.core.current.duration if self.core.current else 1)))
        pyxel.rect(8, 22, 224, 4, 5)
        pyxel.rect(8, 22, w, 4, 10 if w > 60 else 8)

    def _draw_microgame(self) -> None:
        micro = self.core.current
        if micro is None:
            return
        self._center(micro.prompt, 48, 10)
        if micro.kind is MicroKind.TAP_TARGET:
            self._draw_target_button(micro.target, 120, 130, 11)
        elif micro.kind is MicroKind.DODGE:
            self._center("do not press it", 70, 6)
            self._draw_target_button(micro.target, 120, 130, 8)
        elif micro.kind is MicroKind.MASH:
            self._draw_target_button(micro.target, 120, 120, 12)
            pyxel.rect(66, 168, 108, 8, 5)
            pyxel.rect(66, 168, int(108 * micro.progress / micro.goal), 8, 11)

    def _draw_result(self) -> None:
        text = "clear" if self.core.success else "miss"
        color = 11 if self.core.success else 8
        pyxel.rect(54, 94, 132, 50, 0)
        pyxel.rectb(54, 94, 132, 50, color)
        self._center(text, 113, color)

    def _draw_party_backdrop(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(0, SCREEN, 24):
            pyxel.line(0, y, SCREEN, y, 13)
        for x in range(0, SCREEN, 24):
            pyxel.line(x, 0, x, SCREEN, 13)
        for i in range(18):
            x = (i * 37 + pyxel.frame_count) % SCREEN
            y = 30 + (i * 53) % 170
            pyxel.rect(x, y, 5, 5, 8 + i % 6)

    def _draw_button_grid(self, x: int, y: int) -> None:
        for label, dx, dy in (("UP", 0, -28), ("DN", 0, 28), ("LT", -34, 0), ("RT", 34, 0), ("A", 72, -12), ("B", 72, 24)):
            self._draw_labeled_button(label, x + dx, y + dy, 6)

    def _draw_target_button(self, button: str, x: int, y: int, color: int) -> None:
        labels = {"up": "UP", "down": "DN", "left": "LT", "right": "RT", "a": "A", "b": "B"}
        self._draw_labeled_button(labels.get(button, button.upper()), x, y, color)

    def _draw_labeled_button(self, label: str, x: int, y: int, color: int) -> None:
        pyxel.rect(x - 18, y - 12, 36, 24, color)
        pyxel.rectb(x - 18, y - 12, 36, 24, 0)
        pyxel.text(x - len(label) * 2, y - 3, label, 0)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Picoware()
