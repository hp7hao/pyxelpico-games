"""Office Hell — one-button puzzle platformer.

Adapted for PyxelPico from PICO-8 cart "Office Hell" by OlieB123
(CC BY-NC-SA 4.0).
Source thread: https://www.lexaloffle.com/bbs/?tid=154283
Original cart: https://www.lexaloffle.com/bbs/cposts/of/office_hell_1_0-0.p8.png

This first PyxelPico port pass preserves the documented premise and controls:
choose Jimbo's direction, then time jumps while he auto-runs through office
hazards. Exact Lua/API parity is blocked because the cart code uses newer
PICO-8 `pxa` compression that the vendored picotool cannot decode yet.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402


SCREEN_W = 240
SCREEN_H = 240
FPS = 30
FLOOR_Y = 206
GRAVITY = 0.58
JUMP_V = -8.8
RUN_SPEED = 2.0
PLAYER_W = 12
PLAYER_H = 18


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    w: int
    h: int


@dataclass(frozen=True)
class Level:
    name: str
    start: tuple[int, int]
    platforms: tuple[Rect, ...]
    hazards: tuple[Rect, ...]
    exit: Rect
    ghosts: tuple[Rect, ...] = ()
    hint: str = ""


LEVELS: tuple[Level, ...] = (
    Level(
        "late again",
        (20, 188),
        (Rect(0, FLOOR_Y, 240, 34),),
        (Rect(94, 196, 12, 10), Rect(150, 196, 12, 10)),
        Rect(214, 176, 14, 30),
        hint="pick right, then jump",
    ),
    Level(
        "printer jam",
        (214, 188),
        (Rect(0, FLOOR_Y, 240, 34), Rect(92, 158, 58, 8)),
        (Rect(40, 196, 18, 10), Rect(174, 196, 18, 10)),
        Rect(16, 176, 14, 30),
        (Rect(110, 146, 12, 12),),
        "left wall bounce is safe",
    ),
    Level(
        "meeting maze",
        (18, 188),
        (Rect(0, FLOOR_Y, 240, 34), Rect(54, 174, 48, 8), Rect(144, 146, 58, 8)),
        (Rect(112, 196, 22, 10), Rect(68, 164, 20, 10)),
        Rect(206, 116, 14, 30),
        (Rect(162, 134, 12, 12),),
        "stairs are made of desks",
    ),
    Level(
        "coffee debt",
        (210, 188),
        (Rect(0, FLOOR_Y, 240, 34), Rect(136, 174, 42, 8), Rect(54, 142, 54, 8)),
        (Rect(88, 196, 16, 10), Rect(188, 196, 18, 10), Rect(70, 132, 16, 10)),
        Rect(18, 112, 14, 30),
        (Rect(150, 162, 12, 12),),
        "commit to the route",
    ),
    Level(
        "open plan",
        (18, 188),
        (
            Rect(0, FLOOR_Y, 240, 34),
            Rect(42, 174, 40, 8),
            Rect(112, 154, 38, 8),
            Rect(178, 132, 42, 8),
        ),
        (Rect(90, 196, 15, 10), Rect(156, 196, 15, 10), Rect(122, 144, 14, 10)),
        Rect(210, 102, 14, 30),
        (Rect(190, 120, 12, 12),),
        "no changing your mind",
    ),
    Level(
        "annual review",
        (210, 188),
        (
            Rect(0, FLOOR_Y, 240, 34),
            Rect(158, 174, 42, 8),
            Rect(86, 150, 48, 8),
            Rect(20, 126, 42, 8),
        ),
        (Rect(126, 196, 20, 10), Rect(48, 140, 20, 10), Rect(190, 196, 15, 10)),
        Rect(16, 96, 14, 30),
        (Rect(100, 138, 12, 12),),
        "jump late, land clean",
    ),
)


class OfficeHell:
    def __init__(self) -> None:
        pyxel.init(SCREEN_W, SCREEN_H, title="Office Hell", fps=FPS)
        self._init_audio()
        self.best_level = 1
        self.reset(title=True)
        pyxel.run(self.update, self.draw)

    def _init_audio(self) -> None:
        pyxel.sounds[0].set("c3e3g3", "t", "765", "f", 10)       # jump
        pyxel.sounds[1].set("f2c2", "n", "76", "f", 12)          # hazard
        pyxel.sounds[2].set("c3e3g3c4", "s", "4567", "n", 16)    # clear
        pyxel.sounds[3].set("c2", "n", "4", "f", 8)              # bump

    def reset(self, title: bool = False) -> None:
        self.mode = "title" if title else "play"
        self.level_i = 0
        self.deaths = 0
        self._load_level()

    def _load_level(self) -> None:
        level = LEVELS[self.level_i]
        self.player_x = float(level.start[0])
        self.player_y = float(level.start[1])
        self.player_vy = 0.0
        self.dir = 0
        self.face = 1 if self.player_x < SCREEN_W // 2 else -1
        self.on_ground = False
        self.win_timer = 0
        self.dead_timer = 0
        self.coyote = 0

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.reset(title=False)
            return
        if self.mode == "clear":
            if ih.btnp_a() or ih.btnp_start():
                self.reset(title=False)
            return
        if self.mode == "dead":
            self.dead_timer -= 1
            if self.dead_timer <= 0 or ih.btnp_a() or ih.btnp_start():
                self.mode = "play"
                self._load_level()
            return
        if self.mode == "level_clear":
            self.win_timer -= 1
            if self.win_timer <= 0:
                self.level_i += 1
                if self.level_i >= len(LEVELS):
                    self.mode = "clear"
                    self.best_level = len(LEVELS)
                else:
                    self.best_level = max(self.best_level, self.level_i + 1)
                    self.mode = "play"
                    self._load_level()
            return

        self._update_play()

    def _update_play(self) -> None:
        if self.dir == 0:
            if ih.btnp_left():
                self.dir = -1
                self.face = -1
            elif ih.btnp_right():
                self.dir = 1
                self.face = 1
        if (ih.btnp_a() or ih.btnp_up()) and (self.on_ground or self.coyote > 0):
            self.player_vy = JUMP_V
            self.on_ground = False
            self.coyote = 0
            pyxel.play(0, 0)

        old_x = self.player_x
        self.player_x += self.dir * RUN_SPEED
        if self._collides(self.player_rect()):
            self.player_x = old_x
            if self.dir:
                pyxel.play(3, 3)
            self.dir = 0

        self.player_vy += GRAVITY
        self.player_vy = min(self.player_vy, 7.5)
        old_y = self.player_y
        self.player_y += self.player_vy
        self.on_ground = False
        if self._collides(self.player_rect()):
            if self.player_vy > 0:
                while not self._collides(self.player_rect_at(self.player_x, self.player_y - 1)):
                    self.player_y -= 1
                self.player_y = old_y
                while not self._collides(self.player_rect_at(self.player_x, self.player_y + 1)):
                    self.player_y += 1
                self.on_ground = True
                self.coyote = 4
            else:
                self.player_y = old_y
            self.player_vy = 0.0
        elif self.coyote > 0:
            self.coyote -= 1

        if self.player_x < -20 or self.player_x > SCREEN_W + 20 or self.player_y > SCREEN_H + 10:
            self._kill()
            return

        rect = self.player_rect()
        if any(self._overlap(rect, h) for h in self.level.hazards + self.level.ghosts):
            self._kill()
            return
        if self._overlap(rect, self.level.exit):
            self.mode = "level_clear"
            self.win_timer = 28
            pyxel.play(0, 2)

    @property
    def level(self) -> Level:
        return LEVELS[self.level_i]

    def _kill(self) -> None:
        self.deaths += 1
        self.mode = "dead"
        self.dead_timer = 30
        pyxel.play(0, 1)

    def player_rect(self) -> Rect:
        return self.player_rect_at(self.player_x, self.player_y)

    def player_rect_at(self, x: float, y: float) -> Rect:
        return Rect(int(x), int(y), PLAYER_W, PLAYER_H)

    def _collides(self, rect: Rect) -> bool:
        return any(self._overlap(rect, p) for p in self.level.platforms)

    @staticmethod
    def _overlap(a: Rect, b: Rect) -> bool:
        return a.x < b.x + b.w and a.x + a.w > b.x and a.y < b.y + b.h and a.y + a.h > b.y

    def draw(self) -> None:
        pyxel.cls(1)
        self._draw_office()
        self._draw_exit(self.level.exit)
        for p in self.level.platforms:
            self._draw_platform(p)
        for h in self.level.hazards:
            self._draw_hazard(h)
        for g in self.level.ghosts:
            self._draw_ghost(g)
        self._draw_player()
        self._draw_hud()
        if self.mode == "title":
            self._draw_title()
        elif self.mode == "dead":
            self._draw_center_box("FIRED!", "press A to retry")
        elif self.mode == "level_clear":
            self._draw_center_box("ESCAPED ROOM", "next memo loading...")
        elif self.mode == "clear":
            self._draw_center_box("OUT OF OFFICE", "A/START replay")

    def _draw_office(self) -> None:
        pyxel.rect(0, 0, SCREEN_W, SCREEN_H, 1)
        pyxel.rect(0, 188, SCREEN_W, 52, 13)
        for x in range(0, SCREEN_W, 32):
            pyxel.rect(x + 4, 24, 18, 18, 6)
            pyxel.rect(x + 7, 27, 12, 12, 12)
        for x in range(-20, SCREEN_W, 52):
            pyxel.line(x, 188, x + 30, 240, 5)
        pyxel.rect(0, 0, SCREEN_W, 18, 0)

    def _draw_platform(self, r: Rect) -> None:
        pyxel.rect(r.x, r.y, r.w, r.h, 4)
        pyxel.rect(r.x, r.y, r.w, max(2, r.h // 3), 9)
        for x in range(r.x + 3, r.x + r.w, 10):
            pyxel.line(x, r.y, x + 4, r.y + r.h - 1, 13)

    def _draw_hazard(self, r: Rect) -> None:
        pyxel.rect(r.x, r.y + 3, r.w, r.h - 3, 8)
        for x in range(r.x, r.x + r.w, 6):
            pyxel.tri(x, r.y + 3, x + 3, r.y, x + 6, r.y + 3, 8)

    def _draw_ghost(self, r: Rect) -> None:
        y = r.y + (1 if pyxel.frame_count % 24 < 12 else -1)
        pyxel.circ(r.x + r.w // 2, y + 5, 6, 7)
        pyxel.rect(r.x + 1, y + 5, r.w - 2, 8, 7)
        pyxel.pset(r.x + 4, y + 4, 0)
        pyxel.pset(r.x + 8, y + 4, 0)
        pyxel.line(r.x + 2, y + 12, r.x + 4, y + 10, 7)
        pyxel.line(r.x + 7, y + 12, r.x + 9, y + 10, 7)

    def _draw_exit(self, r: Rect) -> None:
        pyxel.rect(r.x, r.y, r.w, r.h, 3)
        pyxel.rectb(r.x, r.y, r.w, r.h, 11)
        pyxel.circ(r.x + 10, r.y + 16, 1, 10)
        pyxel.text(r.x - 2, r.y - 8, "EXIT", 11)

    def _draw_player(self) -> None:
        r = self.player_rect()
        if self.mode == "dead" and pyxel.frame_count % 6 < 3:
            return
        pyxel.rect(r.x + 3, r.y + 6, 7, 10, 10)
        pyxel.rect(r.x + 4, r.y + 1, 7, 7, 15)
        pyxel.rect(r.x + 2, r.y + 8, 10, 2, 6)
        pyxel.pset(r.x + (9 if self.face > 0 else 5), r.y + 3, 0)
        pyxel.line(r.x + 4, r.y + 16, r.x + 2, r.y + 18, 4)
        pyxel.line(r.x + 9, r.y + 16, r.x + 11, r.y + 18, 4)
        if self.dir == 0 and self.mode == "play":
            pyxel.text(r.x - 7, r.y - 11, "?", 7)

    def _draw_hud(self) -> None:
        pyxel.text(5, 6, f"OFFICE HELL {self.level_i + 1}/{len(LEVELS)}", 7)
        pyxel.text(137, 6, f"deaths {self.deaths}", 8)
        if self.mode == "play":
            if self.dir == 0:
                pyxel.text(46, 224, "LEFT/RIGHT choose  A jump", 7)
            elif self.level.hint:
                pyxel.text(6, 224, self.level.hint[:38], 6)

    def _draw_title(self) -> None:
        pyxel.rect(22, 56, 196, 116, 0)
        pyxel.rectb(22, 56, 196, 116, 7)
        pyxel.text(83, 70, "OFFICE HELL", 8)
        pyxel.text(42, 92, "jimbo only follows orders once", 7)
        pyxel.text(42, 108, "choose LEFT/RIGHT, then jump", 6)
        pyxel.text(52, 130, "A/UP jump  START begin", 11)
        pyxel.text(64, 150, "press A or START", 10)

    def _draw_center_box(self, title: str, subtitle: str) -> None:
        pyxel.rect(34, 78, 172, 64, 0)
        pyxel.rectb(34, 78, 172, 64, 7)
        pyxel.text(120 - len(title) * 2, 94, title, 10)
        pyxel.text(120 - len(subtitle) * 2, 116, subtitle, 7)


if __name__ == "__main__":
    OfficeHell()
