"""Pure 8-ball pool rules for Mot's 8-Ball Pool PyxelPico port."""

from __future__ import annotations

import math
import random


class Mot8BallPoolCore:
    table_w = 210
    table_h = 112
    cue_start_x = 70.0
    cue_start_y = 120.0

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.mode = "aim"
        self.aim = 0.0
        self.power = 10.0
        self.cue_ball = {"x": self.cue_start_x, "y": self.cue_start_y, "vx": 0.0, "vy": 0.0}
        self.balls = self._rack_balls()
        self.players = [
            {"name": "player 1", "color": None, "sunk": 0, "free_ball": False},
            {"name": "player 2", "color": None, "sunk": 0, "free_ball": False},
        ]
        self.current_player = 0
        self.first_hit: str | None = None
        self.game_over = False
        self.winner: int | None = None
        self.message = "aim"

    def adjust_aim(self, direction: int) -> None:
        self.aim += direction * 0.09
        self.message = "aim"

    def adjust_power(self, amount: int) -> None:
        self.power = max(1.0, min(25.0, self.power + amount))
        self.message = f"power {int(self.power)}"

    def shoot(self) -> bool:
        if self.mode != "aim" or self.game_over:
            return False
        self.cue_ball["vx"] = math.cos(self.aim) * self.power * 0.22
        self.cue_ball["vy"] = math.sin(self.aim) * self.power * 0.22
        self.mode = "sim"
        self.first_hit = None
        self.message = "shot"
        return True

    def tick(self) -> None:
        if self.mode != "sim":
            return
        b = self.cue_ball
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        b["vx"] *= 0.96
        b["vy"] *= 0.96
        self._bounce_cue_ball()
        self._check_ball_hits()
        if abs(b["vx"]) + abs(b["vy"]) < 0.06:
            self.mode = "aim"
            self._finish_turn()

    def resolve_pocket(self, color: str) -> None:
        player = self.players[self.current_player]
        other = self.players[1 - self.current_player]
        if color == "white":
            self.commit_foul("white sunk")
            return
        if color == "black":
            if player["color"] is not None and int(player["sunk"]) >= 7:
                self.winner = self.current_player
            else:
                self.winner = 1 - self.current_player
            self.game_over = True
            self.message = "black sunk"
            return
        if player["color"] is None:
            player["color"] = color
            other["color"] = "stripe" if color == "solid" else "solid"
        if player["color"] == color:
            player["sunk"] = int(player["sunk"]) + 1
            self.message = f"{color} sunk"
        else:
            self.commit_foul("wrong color")

    def commit_foul(self, reason: str) -> None:
        self.current_player = 1 - self.current_player
        self.players[self.current_player]["free_ball"] = True
        self.mode = "aim"
        self.message = f"foul: {reason}"

    def _rack_balls(self) -> list[dict[str, object]]:
        balls = []
        colors = ["solid"] * 7 + ["stripe"] * 7 + ["black"]
        for i, color in enumerate(colors):
            balls.append({"x": 142 + (i % 5) * 8, "y": 96 + (i // 5) * 9, "color": color, "pocketed": False})
        return balls

    def _bounce_cue_ball(self) -> None:
        b = self.cue_ball
        if b["x"] < 18 or b["x"] > 222:
            b["vx"] *= -0.7
            b["x"] = max(18, min(222, b["x"]))
        if b["y"] < 68 or b["y"] > 178:
            b["vy"] *= -0.7
            b["y"] = max(68, min(178, b["y"]))

    def _check_ball_hits(self) -> None:
        for ball in self.balls:
            if ball["pocketed"]:
                continue
            if abs(float(ball["x"]) - self.cue_ball["x"]) < 8 and abs(float(ball["y"]) - self.cue_ball["y"]) < 8:
                color = str(ball["color"])
                self.first_hit = self.first_hit or color
                if self.rng.random() < 0.35 + self.power / 80:
                    ball["pocketed"] = True
                    self.resolve_pocket(color)
                self.cue_ball["vx"] *= -0.35
                self.cue_ball["vy"] *= -0.35
                return

    def _finish_turn(self) -> None:
        if self.game_over or self.message.startswith("foul"):
            return
        player = self.players[self.current_player]
        if self.first_hit is None:
            self.commit_foul("miss")
            return
        target = player["color"]
        if target is not None and self.first_hit not in (target, "black"):
            self.commit_foul("wrong first hit")
            return
        if player["free_ball"]:
            player["free_ball"] = False
            self.message = "free ball used"
            return
        self.current_player = 1 - self.current_player
        self.message = "next player"

    def restart(self) -> None:
        self.__init__(self.seed)
