"""FlatBird — Flappy Bird clone with pipe obstacles.

Adapted for Pico8Go (240x240, 8-button gamepad).
Original by Hiekichi.
"""
import os
import pyxel

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class App():
    def __init__(self):
        pyxel.init(240,240,title="フラットバード",fps=24,display_scale=3)
        pyxel.load(os.path.join(SCRIPT_DIR, "assets", "flatbirdgame.pyxres"))
        self.init_game()
        self.is_gaming = False
        pyxel.run(self.update,self.draw)

    def init_game(self):
        self.bird_pos = [3000,3000] #鳥の位置を画面の外にしておく
        self.bird_v = 0  # 鳥の移動量
        self.dokans = [] # 土管の位置リスト
        self.score = 0   # スコア

        self.best_score = 0   # ハイスコア
        self.bird_down = 0.6 # 鳥の落下量　※フレームごとに落下
        self.bird_up = 5     # 鳥の上昇量　※スペースキー押下で

    def update(self):
        if self.is_gaming:    ### ゲーム実行中
            ### ゲームオーバーの判定
            c1 = pyxel.pget(self.bird_pos[0]+ 3,self.bird_pos[1]+ 4)
            c2 = pyxel.pget(self.bird_pos[0]+13,self.bird_pos[1]+ 3)
            c3 = pyxel.pget(self.bird_pos[0]+ 1,self.bird_pos[1]+13)
            c4 = pyxel.pget(self.bird_pos[0]+12,self.bird_pos[1]+10)
            #print("{},{}".format(self.bird_pos[0],self.bird_pos[1]))
            #print("{} {} {} {}".format(c1,c2,c3,c4))
            if c1 != 11 or c2 != 11 or c3 != 11 or c4 != 11:
                self.is_gaming = False
                pyxel.play(1,1)

            ### 加点の処理
            c = pyxel.pget(83,0)
            #print("{}".format(c))
            if c == 1:
                self.score += 1
                pyxel.play(3,2)

            ### 鳥の落下
            self.bird_v += self.bird_down
            ### 鳥のジャンプ？（スペースキー押し下しで）
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.bird_v -= self.bird_up
                pyxel.play(0,0)
            x = self.bird_pos[0]
            y = self.bird_pos[1]
            ### 鳥の位置変更
            self.bird_pos = [x,y + self.bird_v]

            ### 土管の生成
            if pyxel.frame_count%44 == 0:
                self.dokans.append([280,pyxel.rndi(-140,0)])
                #self.dokans.append([280,0])
            ### 土管の消滅
            if len(self.dokans) > 0:
                if self.dokans[0][0] < -30:
                    self.dokans.pop(0)
            ### 土管の移動
            for i in range(len(self.dokans)):
                self.dokans[i][0] -= 2 #土管の移動速度

        else:   ### ゲーム中ではない
            ### ゲームスタート！
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.is_gaming = True
                self.start_game()
            
            if self.bird_pos[1] < pyxel.height-48:
                self.bird_pos[1] += 3

    def start_game(self):
        if self.score > self.best_score:
            self.best_score = self.score 
        self.bird_pos = [100,100] #鳥の位置
        self.bird_v = 0  # 鳥の移動速度
        self.dokans = [] # 土管の位置リスト
        self.score = 0   # スコア

    def draw(self):
        ##### ゲーム状態に関係なく共通の描画処理
        ### 画面をクリア
        pyxel.cls(11)
        ### 土管の描画
        for x,y in self.dokans:
            pyxel.blt(x,y,     0,  0,16,  16,-160, 7)
            pyxel.blt(x,y+200, 0,  0,16,  16, 160, 7)

        ### 地面の描画
        pyxel.rect(0,pyxel.height-32,pyxel.width,32,4)
        pyxel.text(10,pyxel.height-16,"A-BUTTON:Jump",7)

        ### 点数の描画
        pyxel.text(170,10,"Hi-Score:{}".format(self.best_score),7)
        pyxel.text(182,18,"Score:{}".format(self.score),7)


        ##### ゲーム中特有の描画処理
        if self.is_gaming:
            ### 鳥の描画
            d = pyxel.frame_count%4 * 16
            pyxel.blt(self.bird_pos[0],self.bird_pos[1],0,0+d,0,16,16,7)
        ##### ゲームオーバー中特有の描画処理
        else:
            ### 鳥の描画
            pyxel.blt(self.bird_pos[0],self.bird_pos[1],0,16,16,16,16,7)
            ### メッセージの描画
            pyxel.blt(64,240-pyxel.frame_count%300,1,0,0,128,48,7)
            pyxel.text(96,100,"GAME OVER!",pyxel.frame_count%16)
            pyxel.text(64,110,"Push B-BUTTON to Start",7)

App()

