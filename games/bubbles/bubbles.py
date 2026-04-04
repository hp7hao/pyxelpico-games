"""Bubbles - A Pang/Buster Bros clone.

Adapted for Pico8Go (240x240, 8-button gamepad).
Original by helpcomputer (MIT License).
"""
import os
import pyxel as px

from constants import FPS, SCREEN_W, SCREEN_H, APP_WIDTH, APP_HEIGHT, SCALE, MAX_STAGE_NUMBER
from stage import Stage
from main_menu import MainMenu
import vars

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Integer 2x scale: 128*2=256, centered and cropped to 240x240 (8px off each edge)
DEST = (SCREEN_W - APP_WIDTH) // 2  # 56

STATE_MAIN_MENU = 0
STATE_PLAY = 1

class App:
   def __init__(self):
      px.init(SCREEN_W, SCREEN_H, "Bubbles", fps=FPS, display_scale=3)
      px.load(os.path.join(SCRIPT_DIR, "assets", "main.pyxres"))

      self.state = STATE_MAIN_MENU
      self.main_menu = MainMenu(self)
      self.stage = None

      px.run(self.update, self.draw)

   def go_to_main_menu(self):
      self.state = STATE_MAIN_MENU

   def go_to_next_stage(self):
      vars.stage_number = min(MAX_STAGE_NUMBER, vars.stage_number + 1)
      self.stage = Stage(self, vars.stage_number)

   def go_to_play(self):
      vars.reset()
      self.state = STATE_PLAY
      self.stage = Stage(self, vars.stage_number)

   def go_to_exit(self):
      px.quit()

   def update(self):
      vars.update_input()

      if self.state == STATE_MAIN_MENU:
         self.main_menu.update()
      elif self.state == STATE_PLAY:
         self.stage.update()

   def draw(self):
      px.cls(0)
      # Draw game at native 128x128 coords (top-left corner of 240x240 screen)
      px.bltm(0, 0, 0, 0, 0, APP_WIDTH, APP_HEIGHT)

      if self.state == STATE_MAIN_MENU:
         self.main_menu.draw()
      elif self.state == STATE_PLAY:
         self.stage.draw()

      # Copy the 128x128 game region to image bank 2
      px.images[2].blt(0, 0, px.screen, 0, 0, APP_WIDTH, APP_HEIGHT)
      # Clear and blit back scaled to fill 240x240
      px.cls(0)
      px.blt(DEST, DEST, 2, 0, 0, APP_WIDTH, APP_HEIGHT, scale=SCALE)

if __name__ == "__main__":
   App()
