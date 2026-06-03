"""PICO-BALL — sports game starring Jelpi.

Adapted for PyxelPico from PICO-8 cart "PICO-BALL: a Sports Game
Starring Jelpi" by Munchkin (CC BY-NC-SA 4.0).
Source thread: https://www.lexaloffle.com/bbs/?tid=150620
Original cart: https://www.lexaloffle.com/bbs/cposts/pi/pico_ball-5.p8.png

This is a first playable PyxelPico adaptation of the solo/wallball premise:
keep the ball alive; two bounces on one side gives the other side a point.
Exact Lua/API parity is blocked because the cart code is PICO-8 `pxa`
compressed and the local tooling cannot decode it yet.
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402


SCREEN_W = 240
SCREEN_H = 240
FPS = 60
COURT_X = 22
COURT_Y = 20
COURT_W = 196
COURT_H = 178
NET_X = COURT_X + COURT_W // 2
FLOOR_Y = COURT_Y + COURT_H
PLAYER_W = 12
PLAYER_H = 18
PLAYER_SPEED = 2.0
JUMP_V = -6.2
GRAVITY = 0.22
BALL_GRAVITY = 0.105
BALL_R = 4
WIN_SCORE = 7


class PicoBall:
    def __init__(self) -> None:
        pyxel.init(SCREEN_W, SCREEN_H, title="PICO-BALL", fps=FPS)
        self._init_audio()
        self.best_rally = 0
        self.reset(match=False)
        pyxel.run(self.update, self.draw)

    def _init_audio(self) -> None:
        pyxel.sounds[0].set("c4e4", "t", "76", "n", 6)          # racket
        pyxel.sounds[1].set("c3", "n", "5", "f", 5)             # bounce
        pyxel.sounds[2].set("g4c5e5", "s", "567", "f", 12)      # point
        pyxel.sounds[3].set("c4e4g4c5", "t", "4567", "n", 16)   # win

    def reset(self, match: bool = True) -> None:
        self.mode = "serve" if match else "title"
        self.left_score = 0
        self.right_score = 0
        self.rally = 0
        self.serve_side = -1
        self.message_timer = 0
        self._reset_point()

    def _reset_point(self) -> None:
        self.player_x = COURT_X + 35.0
        self.player_y = FLOOR_Y - PLAYER_H
        self.player_vy = 0.0
        self.player_grounded = True
        self.cpu_x = COURT_X + COURT_W - 47.0
        self.cpu_y = FLOOR_Y - PLAYER_H
        self.cpu_vy = 0.0
        self.cpu_grounded = True
        self.ball_x = self.player_x + PLAYER_W + 8 if self.serve_side < 0 else self.cpu_x - 8
        self.ball_y = FLOOR_Y - 54.0
        self.ball_vx = 0.0
        self.ball_vy = 0.0
        self.last_side = 0
        self.side_bounces = {-1: 0, 1: 0}
        self.rally = 0
        self.mode = "serve"

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.reset(match=True)
            return
        if self.mode == "gameover":
            if ih.btnp_a() or ih.btnp_start():
                self.reset(match=True)
            return
        if self.mode == "serve":
            self._update_players(active_ball=False)
            if ih.btnp_a() or ih.btnp_start():
                self._serve()
            return
        self._update_play()

    def _serve(self) -> None:
        self.mode = "play"
        direction = 1 if self.serve_side < 0 else -1
        self.ball_vx = 2.0 * direction
        self.ball_vy = -3.0
        if self.serve_side < 0:
            self.ball_x = self.player_x + PLAYER_W + 9
            self.ball_y = self.player_y + 2
        else:
            self.ball_x = self.cpu_x - 9
            self.ball_y = self.cpu_y + 2
        self.side_bounces = {-1: 0, 1: 0}
        self.last_side = 0

    def _update_play(self) -> None:
        self._update_players(active_ball=True)
        self._update_ball()

    def _update_players(self, active_ball: bool) -> None:
        dx = (1 if ih.btn_right() else 0) - (1 if ih.btn_left() else 0)
        self.player_x += dx * PLAYER_SPEED
        if (ih.btnp_a() or ih.btnp_up()) and self.player_grounded:
            self.player_vy = JUMP_V
            self.player_grounded = False
        self.player_x = self._clamp_player(self.player_x, -1)
        self.player_y, self.player_vy, self.player_grounded = self._step_body(
            self.player_y, self.player_vy
        )

        target = self.ball_x - PLAYER_W / 2 if active_ball and self.ball_x > NET_X - 20 else NET_X + 45
        cpu_speed = 1.45 + min(0.55, (self.left_score + self.rally / 12) * 0.05)
        if self.cpu_x + PLAYER_W / 2 < target - 4:
            self.cpu_x += cpu_speed
        elif self.cpu_x + PLAYER_W / 2 > target + 4:
            self.cpu_x -= cpu_speed
        if active_ball and self.cpu_grounded and self.ball_x > NET_X and self.ball_y < self.cpu_y + 20:
            if abs(self.ball_x - (self.cpu_x + PLAYER_W / 2)) < 26 and self.ball_vy > -1:
                self.cpu_vy = JUMP_V * 0.92
                self.cpu_grounded = False
        self.cpu_x = self._clamp_player(self.cpu_x, 1)
        self.cpu_y, self.cpu_vy, self.cpu_grounded = self._step_body(self.cpu_y, self.cpu_vy)

    def _clamp_player(self, x: float, side: int) -> float:
        if side < 0:
            return max(COURT_X + 4, min(NET_X - PLAYER_W - 5, x))
        return max(NET_X + 5, min(COURT_X + COURT_W - PLAYER_W - 4, x))

    def _step_body(self, y: float, vy: float) -> tuple[float, float, bool]:
        vy += GRAVITY
        y += vy
        if y >= FLOOR_Y - PLAYER_H:
            return FLOOR_Y - PLAYER_H, 0.0, True
        return y, vy, False

    def _update_ball(self) -> None:
        self.ball_vy += BALL_GRAVITY
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy
        self.ball_vx *= 0.999

        if self.ball_x - BALL_R <= COURT_X:
            self.ball_x = COURT_X + BALL_R
            self.ball_vx = abs(self.ball_vx) * 0.92
            pyxel.play(2, 1)
        elif self.ball_x + BALL_R >= COURT_X + COURT_W:
            self.ball_x = COURT_X + COURT_W - BALL_R
            self.ball_vx = -abs(self.ball_vx) * 0.92
            pyxel.play(2, 1)
        if self.ball_y - BALL_R <= COURT_Y:
            self.ball_y = COURT_Y + BALL_R
            self.ball_vy = abs(self.ball_vy) * 0.86
            pyxel.play(2, 1)

        # Short squash-style divider: the ball can cross above it but bounces off its post.
        if NET_X - 3 < self.ball_x < NET_X + 3 and self.ball_y + BALL_R > FLOOR_Y - 42:
            self.ball_x = NET_X - 4 if self.ball_vx > 0 else NET_X + 4
            self.ball_vx *= -0.86
            pyxel.play(2, 1)

        self._hit_player(self.player_x, self.player_y, -1)
        self._hit_player(self.cpu_x, self.cpu_y, 1)

        if self.ball_y + BALL_R >= FLOOR_Y:
            side = -1 if self.ball_x < NET_X else 1
            self.ball_y = FLOOR_Y - BALL_R
            self.ball_vy = -abs(self.ball_vy) * 0.74
            self.ball_vx *= 0.96
            if self.last_side != side:
                self.side_bounces[-1] = 0
                self.side_bounces[1] = 0
                self.last_side = side
            self.side_bounces[side] += 1
            pyxel.play(2, 1)
            if self.side_bounces[side] >= 2:
                self._score_point(-side)

        if abs(self.ball_vx) < 0.75:
            self.ball_vx += 0.018 if self.ball_x < NET_X else -0.018

    def _hit_player(self, x: float, y: float, side: int) -> None:
        closest_x = max(x, min(self.ball_x, x + PLAYER_W))
        closest_y = max(y, min(self.ball_y, y + PLAYER_H))
        if (self.ball_x - closest_x) ** 2 + (self.ball_y - closest_y) ** 2 > (BALL_R + 1) ** 2:
            return
        cx = x + PLAYER_W / 2
        cy = y + PLAYER_H / 2
        ang = max(-1.0, min(1.0, (self.ball_x - cx) / 12.0))
        lift = -3.6 - max(0, cy - self.ball_y) * 0.035
        self.ball_vx = ang * 2.8 + (0.8 if side < 0 else -0.8)
        self.ball_vy = min(lift, -1.6)
        self.ball_y = y - BALL_R - 1 if self.ball_y < cy else self.ball_y
        self.side_bounces[-1] = 0
        self.side_bounces[1] = 0
        self.last_side = 0
        self.rally += 1
        self.best_rally = max(self.best_rally, self.rally)
        pyxel.play(0, 0)

    def _score_point(self, winner: int) -> None:
        if winner < 0:
            self.left_score += 1
        else:
            self.right_score += 1
        self.serve_side = -winner
        pyxel.play(3, 2)
        if self.left_score >= WIN_SCORE or self.right_score >= WIN_SCORE:
            pyxel.play(3, 3)
            self.mode = "gameover"
            return
        self._reset_point()

    def draw(self) -> None:
        pyxel.cls(1)
        self._draw_court()
        self._draw_character(self.cpu_x, self.cpu_y, 1, cpu=True)
        self._draw_character(self.player_x, self.player_y, -1, cpu=False)
        self._draw_ball()
        self._draw_hud()
        if self.mode == "title":
            self._draw_title()
        elif self.mode == "serve":
            self._draw_serve()
        elif self.mode == "gameover":
            self._draw_gameover()

    def _draw_court(self) -> None:
        pyxel.rect(COURT_X - 4, COURT_Y - 4, COURT_W + 8, COURT_H + 14, 5)
        pyxel.rect(COURT_X, COURT_Y, COURT_W, COURT_H, 12)
        pyxel.rect(COURT_X, FLOOR_Y - 38, COURT_W, 38, 3)
        pyxel.rectb(COURT_X, COURT_Y, COURT_W, COURT_H, 7)
        for y in range(COURT_Y + 8, FLOOR_Y - 48, 16):
            pyxel.line(NET_X, y, NET_X, y + 7, 6)
        pyxel.rect(NET_X - 2, FLOOR_Y - 42, 4, 42, 6)
        pyxel.line(COURT_X, FLOOR_Y, COURT_X + COURT_W, FLOOR_Y, 7)
        for i in range(8):
            x = COURT_X + 8 + i * 24
            pyxel.line(x, FLOOR_Y + 1, x + 10, FLOOR_Y + 6, 11)

    def _draw_character(self, x: float, y: float, side: int, cpu: bool) -> None:
        ix, iy = int(x), int(y)
        body = 8 if cpu else 11
        shade = 2 if cpu else 3
        face = 7
        pyxel.elli(ix + 1, iy + 5, ix + PLAYER_W - 1, iy + PLAYER_H - 1, body)
        pyxel.circ(ix + PLAYER_W // 2, iy + 4, 5, body)
        pyxel.pset(ix + (8 if side < 0 else 4), iy + 3, face)
        pyxel.line(ix + 2, iy + 15, ix - 2, iy + 19, shade)
        pyxel.line(ix + 10, iy + 15, ix + 14, iy + 19, shade)
        arm_x = ix + (PLAYER_W + 2 if side < 0 else -2)
        pyxel.line(ix + PLAYER_W // 2, iy + 9, arm_x, iy + 6, shade)
        pyxel.circ(arm_x, iy + 6, 2, 10 if not cpu else 9)

    def _draw_ball(self) -> None:
        pyxel.circ(int(self.ball_x), int(self.ball_y), BALL_R, 10)
        pyxel.pset(int(self.ball_x - 1), int(self.ball_y - 1), 7)
        pyxel.circb(int(self.ball_x), int(self.ball_y), BALL_R, 9)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN_W, 16, 1)
        pyxel.text(30, 5, f"JELPI {self.left_score}", 7)
        pyxel.text(151, 5, f"CPU {self.right_score}", 7)
        pyxel.text(92, 5, f"RALLY {self.rally}", 10)
        if self.mode == "play":
            side = "left" if self.ball_x < NET_X else "right"
            bounces = self.side_bounces[-1 if self.ball_x < NET_X else 1]
            pyxel.text(82, 204, f"{side} bounces: {bounces}/2", 7)

    def _draw_panel(self, x: int, y: int, w: int, h: int) -> None:
        pyxel.rect(x, y, w, h, 0)
        pyxel.rectb(x, y, w, h, 7)
        pyxel.rectb(x + 2, y + 2, w - 4, h - 4, 5)

    def _draw_title(self) -> None:
        self._draw_panel(30, 60, 180, 96)
        pyxel.text(75, 74, "PICO-BALL", 10)
        pyxel.text(48, 90, "a sports game starring jelpi", 7)
        pyxel.text(44, 110, "two bounces on one side", 6)
        pyxel.text(58, 119, "gives away a point", 6)
        pyxel.text(56, 139, "A/START: begin wall match", 11)
        pyxel.text(47, 149, "D-pad move, A/UP jump", 13)

    def _draw_serve(self) -> None:
        self._draw_panel(54, 82, 132, 50)
        who = "JELPI" if self.serve_side < 0 else "CPU"
        pyxel.text(80, 96, f"{who} serves", 10)
        pyxel.text(68, 113, "press A/START", 7)

    def _draw_gameover(self) -> None:
        self._draw_panel(46, 70, 148, 76)
        if self.left_score > self.right_score:
            pyxel.text(72, 84, "JELPI WINS!", 10)
        else:
            pyxel.text(75, 84, "CPU WINS", 8)
        pyxel.text(68, 101, f"final {self.left_score}-{self.right_score}", 7)
        pyxel.text(58, 116, f"best rally {self.best_rally}", 11)
        pyxel.text(64, 132, "A/START: rematch", 6)


if __name__ == "__main__":
    PicoBall()
