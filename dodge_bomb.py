from tkinter import CENTER
from typing import MutableMapping
import pygame as pg
import sys
import random
import time

class Screen:
    def __init__(self, fn, wh ,title):
        pg.init()
        pg.display.set_caption(title)
        self.width, self.height = wh #(1600, 900)
        self.center_wh = (self.width/2, self.height/2)
        self.disp = pg.display.set_mode((self.width, self.height)) #Surface
        self.rect = self.disp.get_rect() #rect
        self.image = pg.image.load(fn) #Surface

    def set_text(self, text, font_type = None, font_size = 100, color = 0):

        font = pg.font.Font(font_type, font_size)

        return font.render(text, True, color)
        
class Bird(pg.sprite.Sprite):
    key_delta = {
            pg.K_UP   : [0, -1],
            pg.K_DOWN : [0, +1],
            pg.K_LEFT : [-1, 0],
            pg.K_RIGHT: [+1, 0],
            }
    def __init__(self, fn, r, xy):

        super().__init__()
        self.image = pg.image.load(fn) #surface
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect = self.image.get_rect() # rect
        self.rect.center = xy
    
    def update(self, screen):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key] == True:
                self.rect.centerx += 10 *delta[0]
                self.rect.centery += 10 *delta[1]
                if check_bound(screen.rect, self.rect) != (1, 1):
                    self.rect.centerx -= 10 *delta[0]
                    self.rect.centery -= 10 *delta[1]

class Bomb(pg.sprite.Sprite):
    def __init__(self, color, r, vxy, screen):

        super().__init__()
        self.image = pg.Surface((2 * r, 2 * r))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.image, color, (r, r), r)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, screen.rect.width)
        self.rect.centery = random.randint(0, screen.rect.height)
        self.vx, self.vy = vxy
    
    def update(self, screen):
        self.rect.move_ip(self.vx, self.vy)
        x, y = check_bound(screen.rect, self.rect)
        self.vx *= x
        self.vy *= y


def main():
    tori_health = 10
    muteki = 0
    score = 0

    clock = pg.time.Clock()
    
    # 練習1
    screen = Screen("fig/pg_bg.jpg", (1600, 900), "逃げろ！こうかとん")

    # 練習3
    tori = pg.sprite.Group()
    tori.add(Bird("fig/3.png", 2, (900, 400)))

    # 練習5
    bombs = pg.sprite.Group()
    for i in range(0, 6):
        r = random.randint(0, 3)
        if r == 0:
            r = (255, 0, 0)
        elif r == 1:
            r = (0, 255, 0)
        elif r == 2:
            r = (0, 0, 255)
        elif r == 3:
            r = (255, 255, 0)
        bombs.add( Bomb(r, random.randint(10, 50), (2 * (i + 1), 2 * (i + 1)), screen) )

    health = screen.set_text("Health: " + str(tori_health))

    while True:
        if muteki > 0:
            muteki -= 1
        score += 1

        # 練習2
        screen.disp.blit(screen.image, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT: return       # ✕ボタンでmain関数から戻る

        # 練習4
        tori.update(screen)
        tori.draw(screen.disp)

        # 練習6
        bombs.update(screen)
        bombs.draw(screen.disp)
            
        screen.disp.blit(health, health.get_rect(center=(200, 50)))

        gscore = screen.set_text("Score: " + str(score))
        screen.disp.blit(gscore, gscore.get_rect(center=(200, 100)))

        # 練習8
        if len(pg.sprite.groupcollide(tori, bombs, False, False)) != 0:
            if muteki <= 0:
                tori_health -= 1
            muteki = 10
            health = screen.set_text("Health: " + str(tori_health))
            if tori_health < 0:
                while True:
                    gameover = screen.set_text("Game Over")
                    screen.disp.blit(gameover, gameover.get_rect(center=(screen.width/2, screen.height/2)))
                    screen.disp.blit(gscore, gscore.get_rect(center=(screen.width/2, screen.height/2 + 50)))
                    pg.display.update()
                    for event in pg.event.get(): #終了処理
                        if event.type == pg.QUIT:
                            return
            

        pg.display.update()  # 画面の更新
        clock.tick(120) 
    
# 練習7
def check_bound(sc_r, obj_r): # 画面用Rect, ｛こうかとん，爆弾｝Rect
    # 画面内：+1 / 画面外：-1
    x, y = +1, +1
    if obj_r.left < sc_r.left or sc_r.right  < obj_r.right : x = -1
    if obj_r.top  < sc_r.top  or sc_r.bottom < obj_r.bottom: y = -1
    return x, y

if __name__ == "__main__":
    pg.init() 
    main()
    pg.quit()
    sys.exit()