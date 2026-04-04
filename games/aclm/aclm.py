#
# ミサイル対決ゲーム「ACLM」
# ウィングマン氏作の「ACLM」を参考にしました．
# cf. 電波新聞社:「マイコン BASIC Magazine」, 1983年10月号, p.77.
#
# Sep 18, 2023 ver.1 (Pyxelによる実装)
#
"""ACLM — Missile duel game.

Adapted for Pico8Go (240x240, 8-button gamepad).
Original by Jay Kumogata (Apache-2.0 License),
inspired by Wingman's ACLM from BASIC Magazine (Oct 1983).
"""
import math
import pyxel

# Native 240x240 rendering (no scale-blit) for crisp pixels
SCREEN_W = 240
SCREEN_H = 240
# Scale factor from original 128x128 coordinates
S = SCREEN_W / 128  # 1.875


def init():
    global st, x, y, r, a, b, pa, pb

    # 0:開始 1:遊戯中 2:自機勝利 3:敵機勝利 4:引分 5:終了
    st = 0

    # 自機 (scaled from 128x128)
    x = 1 * S
    y = (128 - 2) * S
    r = 0.7

    # 敵機 (scaled from 128x128)
    a = (128 - 2) * S
    b = (128 - 2) * S
    pa = -1 * S
    pb = -1 * S


# 初期化
init()
pyxel.init(SCREEN_W, SCREEN_H, title="ACLM", fps=20, display_scale=3)


def update():
    """NONE"""
    global st, r, pa, pb

    # 遊戯中
    if st == 1:
        # 自機の移動: LEFT/RIGHT + D-pad + A/B buttons
        if (
            pyxel.btn(pyxel.KEY_LEFT)
            or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
            or pyxel.btn(pyxel.KEY_Z)
            or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)
        ):
            r += 0.08
        if (
            pyxel.btn(pyxel.KEY_RIGHT)
            or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
            or pyxel.btn(pyxel.KEY_X)
            or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)
        ):
            r -= 0.08

        # 自機が場外
        if x < 1 * S or x > (128 - 1) * S or y < 1 * S or y > (128 - 1) * S:
            st = 3
            return

        # 敵機の移動
        if x > a:
            pa += 0.1 * S
        if x < a:
            pa -= 0.1 * S
        if y > b:
            pb += 0.1 * S
        if y < b:
            pb -= 0.1 * S

        if pa < -1.0 * S:
            pa += 0.1 * S
        if pa > 1.0 * S:
            pa -= 0.1 * S
        if pb < -1.0 * S:
            pb += 0.1 * S
        if pb > 1.0 * S:
            pb -= 0.1 * S

        # 敵機が場外
        if a < 1 * S or a > (128 - 1) * S or b < 1 * S or b > (128 - 1) * S:
            st = 2
            return

        # 自機と敵機が衝突
        if abs(x - a) < 2 * S and abs(y - b) < 2 * S:
            st = 4
            return


def draw():
    global st, x, y, a, b, pa, pb

    # 開始処理
    if st == 0:

        # 地面
        pyxel.cls(1)
        pyxel.line(0, SCREEN_H - 1, SCREEN_W - 1, SCREEN_H - 1, 7)

        # 状態遷移
        st = 1

    # 遊戯中
    elif st == 1:
        # 自機表示
        px = math.cos(r) * S
        py = math.sin(r) * S
        pyxel.circ(x, y, 1, 14)
        x += px
        y -= py
        pyxel.circ(x, y, 1, 8)

        # 敵機表示
        pyxel.circ(a, b, 1, 11)
        a += pa
        b += pb
        pyxel.circ(a, b, 1, 3)

    # 自機の勝利
    elif st == 2:
        pyxel.text(int(16 * S), int(16 * S), "Very nice play!!", 7)

        # 爆発アニメ
        for n in range(int(16 * S)):
            pyxel.circ(a, b, n, 3)

        # 状態遷移
        st = 5

    # 敵機の勝利
    elif st == 3:
        pyxel.text(int(16 * S), int(16 * S), "Crash! Good luck.", 7)

        # 爆発アニメ
        for n in range(int(16 * S)):
            pyxel.circ(x, y, n, 8)

        # 状態遷移
        st = 5

    # 引分け
    elif st == 4:
        pyxel.text(int(16 * S), int(16 * S), "It's a draw. ", 7)

        # 爆発アニメ
        for n in range(int(16 * S)):
            pyxel.circ(x, y, n, 9)

        # 状態遷移
        st = 5

    # 終了
    elif st == 5:
        pyxel.text(int(16 * S), int(24 * S), "Press [A] to replay.", 7)

        # Restart: SPACE + Z (A button) + Gamepad A + Start
        if (
            pyxel.btn(pyxel.KEY_SPACE)
            or pyxel.btn(pyxel.KEY_Z)
            or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)
            or pyxel.btn(pyxel.KEY_RETURN)
            or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START)
        ):
            init()


# メイン
pyxel.run(update, draw)

# End of aclm.py
