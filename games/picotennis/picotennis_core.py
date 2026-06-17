"""Pure tennis rally and scoring rules for the Pico Tennis PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Ball:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    owner: int = 0
    in_play: bool = False


class PicoTennisCore:
    width = 120
    height = 180
    center_x = 60
    player_y = 150
    ai_y = 30
    court_left = 12
    court_right = 108

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.player_x = self.center_x
        self.ai_x = self.center_x
        self.server = 0
        self.faults = 0
        self.points = [0, 0]
        self.games = [0, 0]
        self.sets = [0, 0]
        self.power = [0, 0]
        self.match_over = False
        self.winner: int | None = None
        self.message = "ready"
        self.ball = Ball(self.center_x, self.player_y)

    def serve(self) -> bool:
        if self.match_over:
            return False
        x = self.player_x if self.server == 0 else self.ai_x
        y = self.player_y if self.server == 0 else self.ai_y
        direction = -1 if self.server == 0 else 1
        angle = (x - self.center_x) / 16
        if abs(angle) > 2.2:
            self.faults += 1
            if self.faults >= 2:
                self.award_point(1 - self.server, message="double fault")
            else:
                self.message = "fault"
            return True
        self.ball = Ball(x=x, y=y, vx=angle, vy=3.0 * direction, owner=self.server, in_play=True)
        self.message = "serve"
        return True

    def tick(self, *, player_move: int = 0) -> None:
        if self.match_over:
            return
        self.player_x = self._clamp(self.player_x + player_move * 3.0)
        self._ai_track()
        if not self.ball.in_play:
            return
        self.ball.x += self.ball.vx
        self.ball.y += self.ball.vy
        self.ball.vx *= 0.995
        if self.ball.x < self.court_left or self.ball.x > self.court_right:
            self.award_point(1 - self.ball.owner, message="out")
        elif self.ball.y < 5:
            self.award_point(0, message="player point")
        elif self.ball.y > self.height - 5:
            self.award_point(1, message="ai point")
        elif self.ball.vy > 0 and abs(self.ball.y - self.player_y) < 4 and abs(self.ball.x - self.player_x) < 14:
            self.hit(0, power=False)
        elif self.ball.vy < 0 and abs(self.ball.y - self.ai_y) < 4 and abs(self.ball.x - self.ai_x) < 16:
            self.hit(1, power=self.power[1] >= 3 and self.rng.random() < 0.35)

    def hit(self, player: int, power: bool = False) -> bool:
        if self.match_over:
            return False
        paddle_x = self.player_x if player == 0 else self.ai_x
        paddle_y = self.player_y if player == 0 else self.ai_y
        if abs(self.ball.x - paddle_x) > 24 or abs(self.ball.y - paddle_y) > 12:
            self.message = "miss"
            return False
        offset = self.ball.x - paddle_x
        speed = 4.0 + min(2.4, self.power[player] * 0.35)
        if power and self.power[player] > 0:
            speed += 1.8
            self.power[player] = 0
            self.message = "power shot"
        else:
            self.power[player] = min(6, self.power[player] + 1)
            self.message = "return"
        direction = -1 if player == 0 else 1
        self.ball.owner = player
        self.ball.vx = -(offset / 10.0)
        self.ball.vy = speed * direction
        self.ball.in_play = True
        return True

    def award_point(self, player: int, message: str | None = None) -> None:
        self.points[player] += 1
        self.faults = 0
        self.ball.in_play = False
        self.power = [0, 0]
        self.message = message or f"player {player + 1} point"
        if self.points[player] >= 4 and self.points[player] - self.points[1 - player] >= 2:
            self.games[player] += 1
            self.points = [0, 0]
            self.server = 1 - self.server
            self.message = f"player {player + 1} game"
            if self.games[player] >= 3 and self.games[player] - self.games[1 - player] >= 1:
                self.sets[player] += 1
                self.games = [0, 0]
                self.message = f"player {player + 1} set"
                if self.sets[player] >= 2:
                    self.match_over = True
                    self.winner = player
                    self.message = f"player {player + 1} match"
        self.reset_ball()

    def reset_ball(self) -> None:
        self.ball = Ball(
            x=self.player_x if self.server == 0 else self.ai_x,
            y=self.player_y if self.server == 0 else self.ai_y,
            owner=self.server,
            in_play=False,
        )

    def _ai_track(self) -> None:
        target = self.ball.x if self.ball.vy < 0 else self.center_x
        if abs(target - self.ai_x) > 2:
            self.ai_x = self._clamp(self.ai_x + (2.2 if target > self.ai_x else -2.2))

    def _clamp(self, x: float) -> float:
        return max(self.court_left + 5, min(self.court_right - 5, x))

    def restart(self) -> None:
        self.__init__(self.seed)
