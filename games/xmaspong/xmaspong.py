"""XMAS Pong — holiday-themed pong.

Adapted for PyxelPico from PICO-8 cart "XMAS Pong" by ReturnOH
(CC BY-NC-SA 4.0).
Source thread: https://www.lexaloffle.com/bbs/?tid=153606
"""

from __future__ import annotations

import os
import random
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402


SCREEN_W = 240
SCREEN_H = 240
FPS = 60

PADDLE_W = 6
PADDLE_H = 34
BALL_SIZE = 5
PADDLE_SPEED = 3
AI_SPEED = 2.2
WIN_SCORE = 10

LEFT_X = 16
RIGHT_X = SCREEN_W - 16 - PADDLE_W


class XmasPong:
    def __init__(self) -> None:
        pyxel.init(SCREEN_W, SCREEN_H, title="XMAS Pong", fps=FPS)
        self.best = 0
        self.mode = "title"
        self.snow: list[list[float]] = []
        self._seed_snow()
        self.reset_round(new_match=True)
        pyxel.run(self.update, self.draw)

    def _seed_snow(self) -> None:
        self.snow = [
            [
                random.uniform(0, SCREEN_W - 1),
                random.uniform(0, SCREEN_H - 1),
                random.uniform(0.4, 1.2),
            ]
            for _ in range(40)
        ]

    def reset_round(self, new_match: bool = False) -> None:
        if new_match:
            self.player_score = 0
            self.ai_score = 0
        self.player_y = SCREEN_H // 2 - PADDLE_H // 2
        self.ai_y = SCREEN_H // 2 - PADDLE_H // 2
        self.ball_x = SCREEN_W / 2 - BALL_SIZE / 2
        self.ball_y = SCREEN_H / 2 - BALL_SIZE / 2
        self.ball_vx = random.choice([-2.8, 2.8])
        self.ball_vy = random.uniform(-1.8, 1.8)
        self.flash_timer = 0

    def start_game(self) -> None:
        self.mode = "play"
        self.reset_round(new_match=True)

    def clamp_paddles(self) -> None:
        self.player_y = max(8, min(SCREEN_H - 8 - PADDLE_H, self.player_y))
        self.ai_y = max(8, min(SCREEN_H - 8 - PADDLE_H, self.ai_y))

    def update_snow(self) -> None:
        for p in self.snow:
            p[1] += p[2]
            if p[1] >= SCREEN_H:
                p[0] = random.uniform(0, SCREEN_W - 1)
                p[1] = -1

    def update_title(self) -> None:
        if ih.btnp_a() or ih.btnp_start() or ih.btnp_b():
            self.start_game()

    def update_play(self) -> None:
        move = 0
        if ih.btn_up():
            move -= PADDLE_SPEED
        if ih.btn_down():
            move += PADDLE_SPEED
        self.player_y += move

        target = self.ball_y + BALL_SIZE / 2 - PADDLE_H / 2
        if target > self.ai_y + 2:
            self.ai_y += AI_SPEED
        elif target < self.ai_y - 2:
            self.ai_y -= AI_SPEED

        self.clamp_paddles()

        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        if self.ball_y <= 8:
            self.ball_y = 8
            self.ball_vy = abs(self.ball_vy)
        elif self.ball_y + BALL_SIZE >= SCREEN_H - 8:
            self.ball_y = SCREEN_H - 8 - BALL_SIZE
            self.ball_vy = -abs(self.ball_vy)

        if (
            self.ball_x <= LEFT_X + PADDLE_W
            and self.ball_x + BALL_SIZE >= LEFT_X
            and self.ball_y + BALL_SIZE >= self.player_y
            and self.ball_y <= self.player_y + PADDLE_H
        ):
            self.ball_x = LEFT_X + PADDLE_W
            rel = (self.ball_y + BALL_SIZE / 2) - (self.player_y + PADDLE_H / 2)
            self.ball_vx = abs(self.ball_vx) + 0.08
            self.ball_vy = rel * 0.12
            self.flash_timer = 5

        if (
            self.ball_x + BALL_SIZE >= RIGHT_X
            and self.ball_x <= RIGHT_X + PADDLE_W
            and self.ball_y + BALL_SIZE >= self.ai_y
            and self.ball_y <= self.ai_y + PADDLE_H
        ):
            self.ball_x = RIGHT_X - BALL_SIZE
            rel = (self.ball_y + BALL_SIZE / 2) - (self.ai_y + PADDLE_H / 2)
            self.ball_vx = -abs(self.ball_vx) - 0.08
            self.ball_vy = rel * 0.12
            self.flash_timer = 5

        if self.ball_x + BALL_SIZE < 0:
            self.ai_score += 1
            if self.ai_score >= WIN_SCORE:
                self.best = max(self.best, self.player_score)
                self.mode = "gameover"
            else:
                self.reset_round(new_match=False)

        if self.ball_x > SCREEN_W:
            self.player_score += 1
            if self.player_score >= WIN_SCORE:
                self.best = max(self.best, self.player_score)
                self.mode = "gameover"
            else:
                self.reset_round(new_match=False)

    def update_gameover(self) -> None:
        if ih.btnp_a() or ih.btnp_start() or ih.btnp_b():
            self.start_game()

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.start_game()

        self.update_snow()
        if self.flash_timer > 0:
            self.flash_timer -= 1

        if self.mode == "title":
            self.update_title()
        elif self.mode == "play":
            self.update_play()
        else:
            self.update_gameover()

    def draw_pitch(self) -> None:
        pyxel.cls(1 if self.flash_timer > 0 else 0)
        pyxel.rect(0, 0, SCREEN_W, 8, 2)
        pyxel.rect(0, SCREEN_H - 8, SCREEN_W, 8, 2)

        for x in range(0, SCREEN_W, 8):
            color = 8 if (x // 8) % 2 == 0 else 3
            pyxel.pset(x, 4, color)
            pyxel.pset(x + 4, SCREEN_H - 4, color)

        for y in range(12, SCREEN_H - 12, 10):
            pyxel.rect(SCREEN_W // 2 - 1, y, 2, 5, 7)

        for sx, sy, _ in self.snow:
            pyxel.pset(int(sx), int(sy), 7)

    def draw_ui(self) -> None:
        pyxel.text(16, 12, f"YOU {self.player_score}", 7)
        pyxel.text(SCREEN_W - 62, 12, f"CPU {self.ai_score}", 7)

    def draw(self) -> None:
        self.draw_pitch()

        if self.mode in ("play", "gameover"):
            pyxel.rect(LEFT_X, int(self.player_y), PADDLE_W, PADDLE_H, 8)
            pyxel.rect(RIGHT_X, int(self.ai_y), PADDLE_W, PADDLE_H, 3)
            pyxel.rect(int(self.ball_x), int(self.ball_y), BALL_SIZE, BALL_SIZE, 7)
            self.draw_ui()

        if self.mode == "title":
            pyxel.text(82, 86, "XMAS PONG", 7)
            pyxel.text(58, 108, "D-PAD UP/DOWN: MOVE", 6)
            pyxel.text(62, 120, "A OR START: SERVE", 6)
            pyxel.text(72, 146, "FIRST TO 10 WINS", 10)
            pyxel.text(62, 172, "PRESS A / START", 7 + (pyxel.frame_count // 20) % 2)
            pyxel.text(86, 186, "BEST " + str(self.best), 11)
        elif self.mode == "gameover":
            pyxel.rect(56, 92, 128, 52, 1)
            pyxel.rectb(56, 92, 128, 52, 7)
            if self.player_score > self.ai_score:
                pyxel.text(94, 106, "YOU WIN!", 11)
            else:
                pyxel.text(90, 106, "CPU WINS", 8)
            pyxel.text(70, 120, "A/START TO REMATCH", 7)

        pyxel.text(64, 228, "Q quit  R quick-restart", 5)


if __name__ == "__main__":
    XmasPong()
