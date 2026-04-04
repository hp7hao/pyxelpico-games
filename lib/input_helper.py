"""Dual-input helper for Pico8Go games.

Provides functions that respond to both keyboard and gamepad input,
matching the Pico8Go 8-button controller layout.

Controller layout:
    D-pad (4-way)  |  A (east) = confirm/action
                   |  B (south) = back/cancel
    Select         |  Start = pause/menu
"""
import pyxel

# --- Continuous (held) --- #


def btn_up():
    return pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)


def btn_down():
    return pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(
        pyxel.GAMEPAD1_BUTTON_DPAD_DOWN
    )


def btn_left():
    return pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT
    )


def btn_right():
    return pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
    )


def btn_a():
    return pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)


def btn_b():
    return pyxel.btn(pyxel.KEY_X) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)


# --- Edge (pressed this frame) --- #


def btnp_up(hold=0, repeat=0):
    return pyxel.btnp(pyxel.KEY_UP, hold, repeat) or pyxel.btnp(
        pyxel.GAMEPAD1_BUTTON_DPAD_UP, hold, repeat
    )


def btnp_down(hold=0, repeat=0):
    return pyxel.btnp(pyxel.KEY_DOWN, hold, repeat) or pyxel.btnp(
        pyxel.GAMEPAD1_BUTTON_DPAD_DOWN, hold, repeat
    )


def btnp_left(hold=0, repeat=0):
    return pyxel.btnp(pyxel.KEY_LEFT, hold, repeat) or pyxel.btnp(
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, hold, repeat
    )


def btnp_right(hold=0, repeat=0):
    return pyxel.btnp(pyxel.KEY_RIGHT, hold, repeat) or pyxel.btnp(
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, hold, repeat
    )


def btnp_a():
    return pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)


def btnp_b():
    return pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)


def btnp_start():
    return pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(
        pyxel.GAMEPAD1_BUTTON_START
    )


def btnp_select():
    return pyxel.btnp(pyxel.KEY_TAB) or pyxel.btnp(
        pyxel.GAMEPAD1_BUTTON_BACK
    )
