"""Kektris - A Tetris variant where pieces come from all four sides.

Adapted for Pico8Go (240x240, 8-button gamepad).
Original by Konstantin Klepikov (MIT License).
"""
import os
import sys
import pyxel
import random
from typing import Optional
from blocks import Grid, Figure, Window
from constraints import Direction, FigureOrientation
from constraints import GameConst as const
from constraints import (
    GRID_ORIGIN_X,
    GRID_ORIGIN_Y,
    GRID_SIZE,
    CELL_PX,
    CELL_STRIDE,
    GRID_CELLS,
    SIDEBAR_X,
)

# Add lib to path for input_helper
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))

SCREEN_W = 240
SCREEN_H = 240

# Grid pixel geometry
GRID_INNER_X = GRID_ORIGIN_X + 1  # 5
GRID_INNER_Y = GRID_ORIGIN_Y + 1  # 5
GRID_CENTER_PX = GRID_INNER_X + (GRID_CELLS // 2) * CELL_STRIDE  # center pixel


class Game:
    def __init__(self) -> None:
        pyxel.init(SCREEN_W, SCREEN_H, title="Kektris", fps=30)
        pyxel.images[0].load(
            0, 0, os.path.join(os.path.dirname(__file__), "assets", "Q-tris-s.png")
        )
        pyxel.sounds[0].set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr"
            "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "p",
            "4",
            "vffn fnff vffs vfnn",
            25,
        )
        pyxel.sounds[1].set(
            "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2"
            "f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
            "s",
            "4",
            "nnff vfff vvvv vfff svff vfff vvvv svnn",
            25,
        )
        pyxel.sounds[2].set(
            "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1"
            "a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
            "t",
            "5",
            "n",
            25,
        )
        pyxel.sounds[3].set(
            "f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1"
            "f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1",
            "t",
            "5",
            "n",
            25,
        )
        pyxel.sounds[4].set(
            "f0ra4r f0ra4r f0ra4r f0f0a4r",
            "n",
            "5511 5511 5511 5411",
            "f",
            25,
        )
        pyxel.sounds[5].set("g1a1", "s", "75", "f", 8)
        pyxel.sounds[6].set("f1g1f1g1", "p", "7755", "s", 8)
        pyxel.sounds[7].set("c2d3c2d3 c2d3c2d3", "p", "7775 7775", "s", 12)
        pyxel.sounds[8].set("c1d2e3f2 g1a0b0", "p", "7777 655", "f", 20)
        self.music: bool = True
        self.play_music()
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        """Reset game state"""
        self.paused: bool = True
        self.score: int = 0
        self.speed: int = 0
        self.line_lenght: int = const.START_CLEAR_LENGTH
        self.score_color_timeout = const.COLOR_TIMOUT
        self.speed_color_timeout = const.COLOR_TIMOUT
        self.line_color_timeout = const.COLOR_TIMOUT

        self.grid: Grid = Grid()
        self.grid_higlight: bool = False
        self.figure = self.arrive_figure()
        self.figure_next = self.arrive_figure()

        self.frame_count_from_last_move: int = const.START_FRAME_COUNT
        self.is_game_over: bool = False

    def play_music(self):
        pyxel.play(0, [0, 1], loop=True)
        pyxel.play(1, [2, 3], loop=True)
        pyxel.play(2, 4, loop=True)

    def draw(self) -> None:
        """Draw current screen"""
        pyxel.cls(0)
        self.draw_controls()
        self.draw_aside()
        self.mark_grid()
        self.draw_cells()

    def update(self) -> None:
        """Update current game state"""
        # Restart: R key or A button on game-over
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
            return
        if self.is_game_over and (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START)
        ):
            self.reset()
            return

        # Pause: P key or Start button
        if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            self.paused = not self.paused

        # Music toggle: M key or Select button
        if pyxel.btnp(pyxel.KEY_M) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_BACK):
            if self.music:
                self.music = False
                pyxel.stop()
            else:
                self.music = True
                self.play_music()

        # Grid toggle: G key or B button (when paused or playing)
        if pyxel.btnp(pyxel.KEY_G) or (
            self.paused
            and not self.is_game_over
            and pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
        ):
            self.grid_higlight = not self.grid_higlight

        # Quit (dev only)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.is_game_over:
            return

        if self.paused:
            return

        move_direction = None
        rotate_direction = None

        # D-pad / arrow movement
        if pyxel.btnp(pyxel.KEY_LEFT, 8, 1) or pyxel.btnp(
            pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, 8, 1
        ):
            move_direction = Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_RIGHT, 8, 1) or pyxel.btnp(
            pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, 8, 1
        ):
            move_direction = Direction.RIGHT
        elif pyxel.btnp(pyxel.KEY_DOWN, 8, 1) or pyxel.btnp(
            pyxel.GAMEPAD1_BUTTON_DPAD_DOWN, 8, 1
        ):
            move_direction = Direction.DOWN
        elif pyxel.btnp(pyxel.KEY_UP, 8, 1) or pyxel.btnp(
            pyxel.GAMEPAD1_BUTTON_DPAD_UP, 8, 1
        ):
            move_direction = Direction.UP

        # Rotate: Z/X keys or A/B buttons
        elif pyxel.btnp(pyxel.KEY_Z, 12, 20) or pyxel.btnp(
            pyxel.GAMEPAD1_BUTTON_B, 12, 20
        ):
            rotate_direction = Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_X, 12, 20) or pyxel.btnp(
            pyxel.GAMEPAD1_BUTTON_A, 12, 20
        ):
            rotate_direction = Direction.RIGHT

        self.move_figure(move_direction, self.figure.move_figure)
        self.move_figure(rotate_direction, self.figure.rotate_figure)

        if (
            self.frame_count_from_last_move
            == const.GAME_SPEED_LIMIT - self.speed
        ):
            window = self.figure.move_figure(self.figure.window.move_direction)
            self.final_moves_and_game_checks(window)
            return

        self.frame_count_from_last_move += 1

    @classmethod
    def get_chunked(
        cls,
        line: list[int],
        chunked: list[list[int]],
    ) -> tuple[list, list[list[int]]]:
        """Separate line to chunked lines"""
        chunk = []
        while line:
            a = line.pop()
            if chunk:
                if chunk[-1] - a == 1:
                    chunk.append(a)
                else:
                    line.append(a)
                    line, chunked = cls.get_chunked(line, chunked)
            else:
                chunk.append(a)
        chunked.append(chunk)
        return line, chunked

    @staticmethod
    def sign(n: int) -> int:
        """Return sign of int"""
        if n > 0:
            return 1
        elif n == 0:
            return 0
        else:
            return -1

    @staticmethod
    def generate_figure_start_position() -> (
        tuple[tuple[int, int], FigureOrientation]
    ):
        """Generate random start position"""
        return (
            random.choice(const.ARRIVE),
            random.choice(FigureOrientation.get_includes()),
        )

    @staticmethod
    def display_next_figure(window: Window) -> None:
        """Draw next figure"""
        blocked_color = window.orientation.get_figure_color()
        for maps, cells in zip(
            window.orientation.value, const.NEXT_FIGURE_GRID_POS
        ):
            [
                pyxel.rect(pos[0], pos[1], 5, 5, blocked_color)
                for cell, pos in zip(maps, cells)
                if cell
            ]

    @staticmethod
    def draw_up_marker(x: int, y: int, color: int = 12) -> None:
        """Draw up marker"""
        pyxel.pset(x, y, color)
        pyxel.pset(x - 1, y + 1, color)
        pyxel.pset(x + 1, y + 1, color)
        pyxel.pset(x - 2, y + 2, color)
        pyxel.pset(x + 2, y + 2, color)

    @staticmethod
    def draw_down_marker(x: int, y: int, color: int = 12) -> None:
        """Draw down marker"""
        pyxel.pset(x - 2, y - 2, color)
        pyxel.pset(x + 2, y - 2, color)
        pyxel.pset(x - 1, y - 1, color)
        pyxel.pset(x + 1, y - 1, color)
        pyxel.pset(x, y, color)

    def draw_controls(self) -> None:
        """Draw controls helper at bottom of sidebar"""
        sx = SIDEBAR_X
        y_base = 180

        # Gamepad button hints
        pyxel.text(sx, y_base, "[A] rot L", 1)
        pyxel.text(sx, y_base + 8, "[B] rot R", 1)
        pyxel.text(sx, y_base + 16, "[STA] pause", 12)
        pyxel.text(sx, y_base + 24, "[SEL] music", 12)

        # Logo (scaled down, show only if it fits)
        pyxel.blt(sx, y_base + 36, 0, 0, 0, 55, 16)

    def draw_aside(self) -> None:
        """Draw aside parameters"""
        sx = SIDEBAR_X

        pyxel.text(sx, 8, "SCORE", 10)
        pyxel.text(sx, 16, str(self.score), self.set_color("score_color_timeout"))

        pyxel.text(sx, 30, "SPEED", 10)
        pyxel.text(sx, 38, str(self.speed), self.set_color("speed_color_timeout"))

        pyxel.text(sx, 52, "LINE", 10)
        pyxel.text(sx, 60, str(self.line_lenght), self.set_color("line_color_timeout"))

        # display next figure preview
        for p in const.NEXT_FIGURE_GRID[0]:
            pyxel.line(p, 115, p, 139, 13)
        for p in const.NEXT_FIGURE_GRID[1]:
            pyxel.line(sx, p, sx + 24, p, 13)

        if not self.is_game_over:
            pyxel.text(sx, 78, "NEXT", 10)
            if not self.figure.window.is_full_on_grid():
                window = self.figure.window
            else:
                window = self.figure_next.window

            match window.move_direction:
                case Direction.RIGHT:
                    pyxel.text(sx, 88, ">>>", pyxel.frame_count % 8)
                case Direction.LEFT:
                    pyxel.text(sx, 88, "<<<", pyxel.frame_count % 8)
                case Direction.UP:
                    self.draw_up_marker(sx + 2, 88, pyxel.frame_count % 8)
                    self.draw_up_marker(sx + 8, 88, pyxel.frame_count % 8)
                    self.draw_up_marker(sx + 14, 88, pyxel.frame_count % 8)
                case Direction.DOWN:
                    self.draw_down_marker(sx + 2, 90, pyxel.frame_count % 8)
                    self.draw_down_marker(sx + 8, 90, pyxel.frame_count % 8)
                    self.draw_down_marker(sx + 14, 90, pyxel.frame_count % 8)

            self.display_next_figure(window)

        # pause or game over
        if self.is_game_over:
            pyxel.text(sx, 150, "GAME", pyxel.frame_count % 8)
            pyxel.text(sx, 158, "OVER", pyxel.frame_count % 8)
            pyxel.text(sx, 170, "[A]retry", 10)
        elif self.paused:
            pyxel.text(sx, 150, "[STA]", pyxel.frame_count % 8)
            pyxel.text(sx, 158, "to play", pyxel.frame_count % 8)

    def mark_grid(self) -> None:
        """Draw grid mark"""
        # grid border
        pyxel.rectb(GRID_ORIGIN_X, GRID_ORIGIN_Y, GRID_SIZE, GRID_SIZE, 1)

        # grid lines
        if self.grid_higlight:
            for i in range(GRID_CELLS + 1):
                p = GRID_INNER_X + i * CELL_STRIDE
                pyxel.line(p, GRID_INNER_Y, p, GRID_INNER_Y + GRID_CELLS * CELL_STRIDE - 1, 13)
                pyxel.line(GRID_INNER_X, p, GRID_INNER_X + GRID_CELLS * CELL_STRIDE - 1, p, 13)

        # axis
        if not self.is_game_over and not self.paused:
            match self.figure.window.move_direction:
                case Direction.RIGHT | Direction.LEFT:
                    pyxel.line(
                        GRID_CENTER_PX,
                        GRID_INNER_Y,
                        GRID_CENTER_PX,
                        GRID_INNER_Y + GRID_CELLS * CELL_STRIDE - 1,
                        pyxel.frame_count % 8,
                    )
                case Direction.DOWN | Direction.UP:
                    pyxel.line(
                        GRID_INNER_X,
                        GRID_CENTER_PX,
                        GRID_INNER_X + GRID_CELLS * CELL_STRIDE - 1,
                        GRID_CENTER_PX,
                        pyxel.frame_count % 8,
                    )

        # central point
        pyxel.pset(GRID_CENTER_PX, GRID_CENTER_PX, 8)

    def arrive_figure(self) -> Figure:
        """Arrive figure at random"""
        top_left, orientation = self.generate_figure_start_position()
        window = Window(top_left, orientation, self.grid)
        return Figure(window)

    def push_next_figure(self) -> None:
        """Push figure_next to replace current and arrive next"""
        self.figure = self.figure_next
        self.figure_next = self.arrive_figure()

    def draw_cells(self) -> None:
        """Draw blocked and frozen cells from Grid object"""
        blocked_color = self.figure.window.orientation.get_figure_color()
        for n, row in enumerate(self.grid.grid):
            for m, cell in enumerate(row):
                x = cell.pos[0] * CELL_STRIDE + GRID_INNER_X
                y = cell.pos[1] * CELL_STRIDE + GRID_INNER_Y
                if cell.is_blocked:
                    pyxel.rect(x, y, CELL_PX, CELL_PX, blocked_color)
                if cell.is_frozen:
                    pyxel.rect(x, y, CELL_PX, CELL_PX, 7)

    def check_line(
        self,
        dimension: int,
        frozen_pos: list[tuple[int, int]],
    ) -> Optional[list[tuple[int, int]]]:
        """Check is line ready to clear and return positions to clear"""
        s_d = 0 if dimension else 1
        comparison = [c[dimension] for c in frozen_pos]
        min_ = min(comparison)
        max_ = max(comparison) + 1
        for n in range(min_, max_):
            line = [pos for pos in frozen_pos if pos[dimension] == n]
            if len(line) >= self.line_lenght:
                l_comparison = sorted([pos[s_d] for pos in line])
                _, chunked = self.get_chunked(l_comparison, [])
                to_clear = [
                    n
                    for chunk in chunked
                    for n in chunk
                    if len(chunk) >= self.line_lenght
                ]
                if to_clear:
                    return [pos for pos in line if pos[s_d] in to_clear]

    def get_shift(self, shift_x: int, shift_y: int) -> tuple[int, int]:
        """Get shift for frozen to move it when clear line"""
        match self.figure.window.move_direction:
            case Direction.RIGHT:
                shift_x -= 1
            case Direction.LEFT:
                shift_x += 1
            case Direction.UP:
                shift_y += 1
            case Direction.DOWN:
                shift_y -= 1
        return shift_x, shift_y

    def get_shifted_frozen(
        self,
        line: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        """Get shifted frozen positions to move cells when clear line"""
        shift_x, shift_y = 0, 0
        shifted = []
        while True:
            shift_x, shift_y = self.get_shift(shift_x, shift_y)
            s_x, s_y = self.sign(shift_x), self.sign(shift_y)
            sh = []
            for pos in line:
                p = (pos[0] + shift_x, pos[1] + shift_y)

                if (
                    p in self.figure.window.quarter
                    and p not in line
                    and self.grid.grid[p[0]][p[1]].is_frozen
                    and (
                        self.grid.grid[p[0] - s_x][p[1] - s_y].is_frozen
                        or self.grid.grid[p[0] - s_x][p[1] - s_y].pos in line
                    )
                ):
                    sh.append(p)
            if sh:
                shifted.extend(sh)
            else:
                break
        return shifted

    def move_shifted_frozen(self, shifted: list[tuple[int, int]]) -> None:
        """Move frozen rows after clear"""
        shift_x, shift_y = self.get_shift(0, 0)
        [self.grid.grid[pos[0]][pos[1]].clear() for pos in shifted]
        [
            self.grid.grid[pos[0] - shift_x][pos[1] - shift_y].freeze()
            for pos in shifted
            if pos in self.figure.window.quarter
        ]

    def move_figure(self, direction: Optional[Direction], operation) -> None:
        """Move or rotate figure"""
        if direction and self.figure.window.is_on_grid():
            window: Window = operation(direction)
            if self.figure.is_valid_figure(window) and window.is_on_grid():
                self.figure.block_figure(window)
                pyxel.play(3, 5)

    def clear_lines(self) -> None:
        """Clear line"""
        frozen_pos = [cell.pos for cell in self.grid.get_frozen]
        if len(frozen_pos) >= self.line_lenght:
            for dim in [0, 1]:
                line = self.check_line(dim, frozen_pos)
                if line:
                    for pos in line:
                        self.grid.grid[pos[0]][pos[1]].clear()
                        self.change_score()
                        self.change_speed()
                        self.change_line_lenght()
                        pyxel.play(3, 7)
                    shifted = self.get_shifted_frozen(line)
                    if shifted:
                        self.move_shifted_frozen(shifted)
                    self.clear_lines()

    def final_moves_and_game_checks(self, window: Window) -> None:
        """Move figures and check game conditions"""
        if self.figure.is_valid_figure(window):
            self.figure.block_figure(window)
            pyxel.play(3, 5)
        elif not self.figure.window.is_full_on_grid():
            self.is_game_over = True
            pyxel.play(3, 8)
        else:
            if self.grid.get_blocked:
                pyxel.play(3, 6)
                self.grid.freeze_blocked()
            self.clear_lines()
            self.push_next_figure()
        self.frame_count_from_last_move = const.START_FRAME_COUNT

    def change_score(self) -> None:
        """Change score and set flash timeout"""
        self.score += const.PRIZE_BY_CLEAR
        self.score_color_timeout = const.COLOR_TIMOUT

    def change_speed(self) -> None:
        """Change speed and set flash timeout"""
        if (
            self.score // const.SPEED_MODIFICATOR > self.speed
            and self.speed < const.MAX_GAME_SPEED
        ):
            self.speed += 1
            self.speed_color_timeout = const.COLOR_TIMOUT

    def change_line_lenght(self) -> None:
        """Change line length every X points to maximum y"""
        if (
            self.score // const.LENGHT_MODIFICATOR
            > self.line_lenght - const.START_CLEAR_LENGTH
            and self.line_lenght < const.MAX_CLEAR_LENGHT
        ):
            self.line_lenght += 1
            self.line_color_timeout = const.COLOR_TIMOUT

    def set_color(self, color_attr: str) -> int:
        """Set flash color"""
        val = getattr(self, color_attr)
        if val:
            setattr(self, color_attr, val - 1)
            return pyxel.frame_count % 8
        return 12

    def hide_reveal(self, marker: bool) -> int:
        """Hide or reveal flashed marker"""
        if marker:
            return pyxel.frame_count % 8
        return 12


if __name__ == "__main__":
    Game()
