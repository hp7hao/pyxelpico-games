"""Field Jump — side-scrolling platformer.

Adapted for PyxelPico from PICO-8 cart "Field Jump" by fieldjump
(CC BY-NC-SA 4.0).
Source thread: https://www.lexaloffle.com/bbs/?tid=154315
Original cart: https://www.lexaloffle.com/bbs/cposts/fi/fieldjump-0.p8.png

This is a first playable PyxelPico port pass based on the BBS description and
cart label/API audit. Exact Lua parity is blocked until the local cart tooling
can decode PICO-8 0.2.7+ `pxa` compressed code.
"""

from __future__ import annotations

import os
import random
import sys
from dataclasses import dataclass

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402


SCREEN_W = 240
SCREEN_H = 240
FPS = 30
GROUND_Y = 188
PLAYER_X = 54
GRAVITY = 0.55
JUMP_V = -9.2
RUN_SPEED = 2.6
MAX_LEVEL = 5

COLORS = {
    "sky": 12,
    "far": 6,
    "field": 3,
    "dirt": 4,
    "text": 7,
    "shadow": 5,
    "player": 10,
    "player_dark": 9,
    "coin": 10,
    "coin_hi": 7,
    "obstacle": 8,
    "flag": 11,
}


@dataclass
class Obstacle:
    x: float
    w: int
    h: int
    kind: str = "crate"
    y: int = GROUND_Y


@dataclass
class Coin:
    x: float
    y: float
    taken: bool = False


class FieldJump:
    def __init__(self) -> None:
        pyxel.init(SCREEN_W, SCREEN_H, title="Field Jump", fps=FPS)
        self._init_audio()
        self.best_score = 0
        self.reset(attract=True)
        pyxel.run(self.update, self.draw)

    def _init_audio(self) -> None:
        pyxel.sounds[0].set("c3e3g3", "t", "777", "n", 10)       # jump
        pyxel.sounds[1].set("c4e4g4c5", "s", "7654", "f", 12)    # coin
        pyxel.sounds[2].set("f2c2", "n", "76", "f", 10)          # hit
        pyxel.sounds[3].set("c3d3e3g3", "t", "4456", "f", 16)    # level up

    def reset(self, attract: bool = False) -> None:
        self.mode = "title" if attract else "play"
        self.player_y = GROUND_Y - 18
        self.player_vy = 0.0
        self.on_ground = True
        self.ducking = False
        self.scroll = 0.0
        self.score = 0
        self.bonus_score = 0
        self.coins = 0
        self.level = 1
        self.distance = 0
        self.stage_distance = 0.0
        self.clear_timer = 0
        self.lives = 3
        self.invuln = 0
        self.spawn_timer = 32
        self.coin_timer = 18
        self.obstacles: list[Obstacle] = []
        self.coin_items: list[Coin] = []
        self.rng = random.Random(154315)

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.reset(attract=False)
            return
        if self.mode == "levelclear":
            self.clear_timer -= 1
            if self.clear_timer <= 0 or ih.btnp_a() or ih.btnp_start():
                self._advance_level()
            return
        if self.mode in ("gameover", "win"):
            if ih.btnp_a() or ih.btnp_start():
                self.reset(attract=False)
            return

        self._update_play()

    def _stage_goal(self) -> int:
        return 720 + (self.level - 1) * 180

    def _advance_level(self) -> None:
        if self.level >= MAX_LEVEL:
            self.best_score = max(self.best_score, self.score)
            self.mode = "win"
            return
        self.level += 1
        self.stage_distance = 0.0
        self.player_y = GROUND_Y - 18
        self.player_vy = 0.0
        self.on_ground = True
        self.ducking = False
        self.invuln = 30
        self.spawn_timer = 34
        self.coin_timer = 22
        self.mode = "play"

    def _update_play(self) -> None:
        speed = RUN_SPEED + min(2.5, (self.level - 1) * 0.34 + self.stage_distance / 1700)
        self.scroll += speed
        self.distance += int(speed)
        self.stage_distance += speed
        self.score = self.distance // 8 + self.coins * 25 + self.bonus_score
        self.invuln = max(0, self.invuln - 1)

        if self.stage_distance >= self._stage_goal():
            self.bonus_score += self.level * 100
            self.score = self.distance // 8 + self.coins * 25 + self.bonus_score
            self.clear_timer = 90
            self.mode = "levelclear"
            self.obstacles.clear()
            self.coin_items.clear()
            pyxel.play(3, 3)
            return

        self.ducking = ih.btn_down() and self.on_ground
        if (ih.btnp_a() or ih.btnp_up()) and self.on_ground:
            self.player_vy = JUMP_V
            self.on_ground = False
            pyxel.play(0, 0)

        self.player_vy += GRAVITY
        self.player_y += self.player_vy
        floor_y = GROUND_Y - (11 if self.ducking else 18)
        if self.player_y >= floor_y:
            self.player_y = floor_y
            self.player_vy = 0.0
            self.on_ground = True

        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self._spawn_obstacle()
            self.spawn_timer = max(22, int(55 - self.level * 2.2 + self.rng.randint(-7, 12)))

        self.coin_timer -= 1
        if self.coin_timer <= 0:
            self._spawn_coins()
            self.coin_timer = self.rng.randint(46, 82)

        for obstacle in self.obstacles:
            obstacle.x -= speed
        for coin in self.coin_items:
            coin.x -= speed
        self.obstacles = [o for o in self.obstacles if o.x + o.w > -8]
        self.coin_items = [c for c in self.coin_items if c.x > -8 and not c.taken]

        self._check_collisions()

    def _spawn_obstacle(self) -> None:
        kinds = ["stump", "rock", "crate", "hay"]
        if self.level >= 2:
            kinds.append("bird")
        kind = self.rng.choice(kinds)
        if kind == "stump":
            self.obstacles.append(Obstacle(SCREEN_W + 6, 10, 18, kind))
        elif kind == "rock":
            self.obstacles.append(Obstacle(SCREEN_W + 6, 15, 11, kind))
        elif kind == "hay":
            self.obstacles.append(Obstacle(SCREEN_W + 6, 18, 14, kind))
        elif kind == "bird":
            self.obstacles.append(Obstacle(SCREEN_W + 6, 18, 10, kind, GROUND_Y - 34))
        else:
            self.obstacles.append(Obstacle(SCREEN_W + 6, 14, 14, kind))

    def _spawn_coins(self) -> None:
        base_y = self.rng.choice([118, 136, 154])
        start_x = SCREEN_W + self.rng.randint(4, 24)
        for i in range(self.rng.randint(3, 5)):
            self.coin_items.append(Coin(start_x + i * 13, base_y - abs(2 - i) * 5))

    def _player_rect(self) -> tuple[float, float, float, float]:
        if self.ducking:
            return (PLAYER_X + 2, self.player_y + 3, 14, 9)
        return (PLAYER_X + 3, self.player_y + 1, 12, 17)

    def _check_collisions(self) -> None:
        px, py, pw, ph = self._player_rect()
        for coin in self.coin_items:
            if coin.taken:
                continue
            if abs((px + pw / 2) - coin.x) < 12 and abs((py + ph / 2) - coin.y) < 13:
                coin.taken = True
                self.coins += 1
                pyxel.play(1, 1)
        if self.invuln:
            return
        for obstacle in self.obstacles:
            ox, oy, ow, oh = obstacle.x, obstacle.y - obstacle.h, obstacle.w, obstacle.h
            if px < ox + ow and px + pw > ox and py < oy + oh and py + ph > oy:
                self.lives -= 1
                self.invuln = 50
                pyxel.play(2, 2)
                if self.lives <= 0:
                    self.best_score = max(self.best_score, self.score)
                    self.mode = "gameover"
                break

    def draw(self) -> None:
        pyxel.cls(COLORS["sky"])
        self._draw_field()
        for coin in self.coin_items:
            self._draw_coin(coin)
        for obstacle in self.obstacles:
            self._draw_obstacle(obstacle)
        self._draw_player()
        self._draw_hud()
        if self.mode == "title":
            self._draw_title()
        elif self.mode == "levelclear":
            self._draw_levelclear()
        elif self.mode == "gameover":
            self._draw_gameover()
        elif self.mode == "win":
            self._draw_win()

    def _draw_field(self) -> None:
        pyxel.rect(0, 154, SCREEN_W, 34, COLORS["field"])
        pyxel.rect(0, GROUND_Y, SCREEN_W, SCREEN_H - GROUND_Y, COLORS["dirt"])
        pyxel.line(0, GROUND_Y, SCREEN_W, GROUND_Y, 11)
        for i in range(9):
            x = int((i * 38 - self.scroll * 0.35) % 280) - 28
            pyxel.tri(x, 154, x + 34, 154, x + 16, 135, COLORS["far"])
        for i in range(18):
            x = int((i * 18 - self.scroll) % 270) - 20
            pyxel.line(x, 188, x + 8, 181, 11)
            pyxel.line(x + 4, 189, x + 14, 183, 11)
        for i in range(14):
            x = int((i * 22 - self.scroll * 0.5) % 270) - 20
            pyxel.pset(x, 148 + (i % 3) * 4, 10)

    def _draw_player(self) -> None:
        if self.invuln and pyxel.frame_count % 6 < 3:
            return
        x = PLAYER_X
        y = int(self.player_y)
        c = COLORS["player"]
        d = COLORS["player_dark"]
        if self.ducking:
            pyxel.rect(x + 2, y + 4, 14, 8, c)
            pyxel.rect(x + 11, y + 2, 6, 6, c)
            pyxel.pset(x + 15, y + 4, 0)
            pyxel.rect(x + 1, y + 12, 16, 2, d)
        else:
            bob = 1 if self.on_ground and pyxel.frame_count % 12 < 6 else 0
            pyxel.rect(x + 5, y + 3 + bob, 10, 12, c)
            pyxel.rect(x + 8, y, 8, 7, c)
            pyxel.pset(x + 14, y + 2, 0)
            pyxel.line(x + 5, y + 15 + bob, x + 1, y + 18, d)
            pyxel.line(x + 13, y + 15 + bob, x + 17, y + 18, d)

    def _draw_obstacle(self, obstacle: Obstacle) -> None:
        x = int(obstacle.x)
        y = obstacle.y - obstacle.h
        if obstacle.kind == "rock":
            pyxel.circ(x + obstacle.w // 2, y + obstacle.h // 2, obstacle.w // 2, 5)
            pyxel.circ(x + obstacle.w // 2, y + obstacle.h // 2 - 2, obstacle.w // 2 - 3, 13)
        elif obstacle.kind == "stump":
            pyxel.rect(x + 2, y, obstacle.w - 4, obstacle.h, COLORS["obstacle"])
            pyxel.rect(x, y + 1, obstacle.w, 5, 4)
            pyxel.line(x + 5, y + 3, x + 5, y + obstacle.h - 2, 4)
        elif obstacle.kind == "hay":
            pyxel.rect(x, y + 2, obstacle.w, obstacle.h - 2, 9)
            pyxel.line(x, y + 5, x + obstacle.w, y + 3, 10)
            pyxel.line(x + 2, y + obstacle.h - 4, x + obstacle.w - 2, y + 6, 10)
        elif obstacle.kind == "bird":
            wing = 2 if pyxel.frame_count % 14 < 7 else -2
            pyxel.rect(x + 5, y + 3, 8, 5, 8)
            pyxel.pset(x + 12, y + 4, 0)
            pyxel.line(x + 5, y + 5, x, y + 5 + wing, 8)
            pyxel.line(x + 12, y + 5, x + 17, y + 5 + wing, 8)
        else:
            pyxel.rect(x, y, obstacle.w, obstacle.h, COLORS["obstacle"])
            pyxel.rectb(x, y, obstacle.w, obstacle.h, 4)
            pyxel.line(x, y, x + obstacle.w - 1, y + obstacle.h - 1, 4)

    def _draw_coin(self, coin: Coin) -> None:
        x = int(coin.x)
        y = int(coin.y)
        r = 4 + (1 if pyxel.frame_count % 20 < 10 else 0)
        pyxel.circ(x, y, r, COLORS["coin"])
        pyxel.circ(x - 1, y - 1, max(1, r - 3), COLORS["coin_hi"])

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN_W, 18, 0)
        pyxel.text(5, 5, f"score {self.score:05d}", COLORS["text"])
        pyxel.text(88, 5, f"coins {self.coins}", COLORS["coin"])
        pyxel.text(150, 5, f"lv {self.level}/{MAX_LEVEL}", COLORS["flag"])
        pyxel.text(196, 5, "*" * self.lives, 8)
        if self.mode == "play":
            progress = min(1.0, self.stage_distance / self._stage_goal())
            pyxel.rect(4, 18, 60, 3, 5)
            pyxel.rect(4, 18, int(60 * progress), 3, 11)

    def _draw_title(self) -> None:
        pyxel.rect(24, 58, 192, 92, 0)
        pyxel.rectb(24, 58, 192, 92, 7)
        pyxel.text(80, 72, "FIELD JUMP", 10)
        pyxel.text(45, 91, "collect coins, avoid obstacles", 7)
        pyxel.text(55, 112, "A/UP jump  DOWN duck", 6)
        pyxel.text(58, 130, "press A or START", 11)

    def _draw_levelclear(self) -> None:
        pyxel.rect(34, 66, 172, 82, 0)
        pyxel.rectb(34, 66, 172, 82, 11)
        pyxel.text(83, 80, f"LEVEL {self.level} CLEAR", 11)
        pyxel.text(71, 101, f"bonus {self.level * 100}", 10)
        next_text = "next field ahead" if self.level < MAX_LEVEL else "final sprint complete"
        pyxel.text(70, 119, next_text, 7)

    def _draw_gameover(self) -> None:
        pyxel.rect(32, 64, 176, 86, 0)
        pyxel.rectb(32, 64, 176, 86, 8)
        pyxel.text(91, 78, "GAME OVER", 8)
        pyxel.text(73, 98, f"score {self.score}", 7)
        pyxel.text(73, 110, f"best  {self.best_score}", 10)
        pyxel.text(58, 132, "press A or START", 11)

    def _draw_win(self) -> None:
        pyxel.rect(30, 58, 180, 98, 0)
        pyxel.rectb(30, 58, 180, 98, 11)
        pyxel.text(83, 74, "FIELDS CLEARED!", 11)
        pyxel.text(70, 96, f"score {self.score}", 7)
        pyxel.text(70, 108, f"best  {self.best_score}", 10)
        pyxel.text(58, 134, "press A or START", 11)


if __name__ == "__main__":
    FieldJump()
