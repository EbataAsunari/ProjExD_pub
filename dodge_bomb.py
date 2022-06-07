import pygame as pg
import sys
import random


class Screen: #画面を生成
    def __init__(self, fn, wh, title):
        pg.display.set_caption(title)  
        self.width, self.height = wh
        self.disp = pg.display.set_mode((self.width, self.height))
        self.rect = self.disp.get_rect()  
        self.image = pg.image.load(fn) 


class Bird(pg.sprite.Sprite):
    key_delta = {pg.K_UP   : [0, -2],
                 pg.K_DOWN : [0, +2],
                 pg.K_LEFT : [-2, 0],
                 pg.K_RIGHT: [+2, 0],}      #1→2に変更　地神

    def __init__(self, fn, r, xy):
        super().__init__()
        self.zanki = 5
        self.image = pg.image.load(fn)
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect = self.image.get_rect()
        self.rect.center = xy

    def update(self, screen):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key] == True:
                self.rect.centerx += delta[0]
                self.rect.centery += delta[1]
                
                if check_bound(screen.rect, self.rect) != (1,1): 
                    self.rect.centerx -= delta[0]
                    self.rect.centery -= delta[1]


class Bomb(pg.sprite.Sprite):
    def __init__(self,color, r, vxy, screen):
        super().__init__()
        self.image = pg.Surface((2*r, 2*r))
        self.image.set_colorkey((0,0,0))
        pg.draw.circle(self.image, color, (r,r),r)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, screen.rect.width)
        self.rect.centery = random.randint(0, screen.rect.height)
        self.vx, self.vy =vxy

    def update(self, screen):
        self.rect.move_ip(self.vx, self.vy)
        x, y = check_bound(screen.rect, self.rect)
        self.vx *= x 
        self.vy *= y

    
def main():
    clock = pg.time.Clock()

    zanki = 5
    muteki = 0
    time = 200
    col = {0:(255,0,0),1:(255,255,0),2:(255,0,255),3:(0,255,0),4:(0,255,255)}   #色辞書追加　地神

    screen = Screen("fig/pg_bg.jpg", (1600, 900), "逃げろ！こうかとん")
    screen.disp.blit(screen.image, (0,0))                  

    tori = pg.sprite.Group()
    tori.add(Bird("fig/3.png", 2, (900, 400)))

    bombs = pg.sprite.Group()
    for i in range(5):
        bombs.add(Bomb((col[i]), 10/(i*0.1+0.3), (+1+i*1,+2+i*1), screen)) #（色, サイズ, 速度）を各々変更した爆弾を５つ生成　地神

    hoshi = pg.sprite.Group()
    hoshi.add(Bird("fig/9.png",2,(900,400))) #無敵状態の差し替え画像　地神

    while True:
        score = pg.time.get_ticks()
        screen.disp.blit(screen.image, (0,0))

        if time < 0: #無敵状態でないとき
            tori.update(screen)
            hoshi.update(screen)
            tori.draw(screen.disp) #通常状態の画像を表示
        else:       #無敵状態のとき
            tori.update(screen)
            hoshi.update(screen)
            hoshi.draw(screen.disp) #無敵状態の画像を表示　地神

        bombs.update(screen)
        bombs.draw(screen.disp)

        if len(pg.sprite.groupcollide(tori,bombs,False, False)) != 0:
            if zanki == 0 and muteki == 0:#残機も無敵時間もない場合に爆弾に接触したならゲームオーバー
                while True:
                    font = pg.font.Font(None,50) #フォント指定
                    text = font.render("GAME OVER", True,(0,0,255)) #"GAME OVER"と表示
                    screen.disp.blit(text,(750,450))
                    text2 = font.render(f"SCORE:{score}", True,(0,0,255)) #スコアを表示
                    screen.disp.blit(text2,(750,500))

                    pg.display.update() 
                    pg.time.delay(1000)#ゲームオーバーした後遅延をいれてリターン
                    return
                                                                      
                                                
            else:
                if muteki ==0:
                    zanki -= 1 
                    muteki = 1
                    time = 200
        for event in pg.event.get():
            if event.type == pg.QUIT: return
      
        font = pg.font.Font(None,50)
        text = font.render(f"STOCK:{zanki}", True,(0,0,255)) #残機
        screen.disp.blit(text,(0,0))

        font = pg.font.Font(None,50)
        text = font.render(f"SCORE:{score}", True,(0,0,255)) #スコア
        screen.disp.blit(text,(0,50))
        
        time -= 1
        if time < 0:
            muteki = 0 
        
        pg.display.update()  
        clock.tick(1000)
        

def check_bound(sc_r, obj_r): 
    x, y = +1, +1
    if obj_r.left < sc_r.left or sc_r.right  < obj_r.right : x = -1
    if obj_r.top  < sc_r.top  or sc_r.bottom < obj_r.bottom: y = -1
    return x, y

                            


if __name__ == "__main__":
    pg.init() 
    main()
    pg.quit()
    sys.exit()