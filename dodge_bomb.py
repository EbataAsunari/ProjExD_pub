import pygame as pg
import sys
import random
import time # 船渡川拓真


class Screen: #画面を生成
    def __init__(self, fn, wh, title):
        pg.display.set_caption(title)  
        self.width, self.height = wh
        self.disp = pg.display.set_mode((self.width, self.height))
        self.rect = self.disp.get_rect()  
        self.image = pg.image.load(fn) 


class Bird(pg.sprite.Sprite):
    key_delta = {pg.K_UP   : [0, -1],
                 pg.K_DOWN : [0, +1],
                 pg.K_LEFT : [-1, 0],
                 pg.K_RIGHT: [+1, 0],}

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
            ##福光　こうかとんが遅すぎるので高速化
            if key_states[key] == True:
                self.rect.centerx += 5 *delta[0]
                self.rect.centery += 5 *delta[1]
                if check_bound(screen.rect, self.rect) != (1, 1):
                    self.rect.centerx -= 5 *delta[0]
                    self.rect.centery -= 5 *delta[1]


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
    time = 80

    screen = Screen("fig/pg_bg.jpg", (1600, 900), "逃げろ！こうかとん")
    screen.disp.blit(screen.image, (0,0))                  

    tori = pg.sprite.Group()
    tori.add(Bird("fig/3.png", 2, (900, 400)))
    
    hoshi = pg.sprite.Group()
    hoshi.add(Bird("fig/9.png",2,(900,400))) #無敵状態の差し替え画像　地神

    bombs = pg.sprite.Group()
    bombs.add(Bomb((255,0,0), 10, (+2, +2), screen))

    while True:
        score = pg.time.get_ticks()
        screen.disp.blit(screen.image, (0,0))

        if time < 0: #無敵状態でないとき　地神
            tori.update(screen)
            hoshi.update(screen)
            tori.draw(screen.disp) #通常状態の画像を表示　地神
        else:       #無敵状態のとき　地神
            tori.update(screen)
            hoshi.update(screen)
            hoshi.draw(screen.disp) #無敵状態の画像を表示　地神

        
        

        # 船渡川拓真：追加機能の関数
        increase_bombs(bombs, screen)

        bombs.update(screen)
        bombs.draw(screen.disp)

        if len(pg.sprite.groupcollide(tori,bombs,False, False)):
            if zanki == 0 and muteki == 0:#残機も無敵時間もない場合に爆弾に接触したならゲームオーバー
                while True:
                    font = pg.font.Font(None,50) #フォント指定
                    text = font.render("GAME OVER", True,(0,0,255)) #"GAME OVER"と表示
                    screen.disp.blit(text,(750,450))
                    text2 = font.render(f"SCORE:{score/100}", True,(0,0,255)) #スコアを表示
                    screen.disp.blit(text2,(750,500))

                    pg.display.update() 
                    pg.time.delay(3000)#ゲームオーバーした後遅延をいれてリターン
                    return
                                                                      
                                                
            else:
                if muteki ==0:
                    zanki -= 1 
                    muteki = 1
                    time = 80
        for event in pg.event.get():
            if event.type == pg.QUIT: return
      
        font = pg.font.Font(None,50)
        text = font.render(f"STOCK:{zanki}", True,(0,0,255)) #残機
        screen.disp.blit(text,(0,0))

        font = pg.font.Font(None,50)
        text = font.render(f"SCORE:{score//100}", True,(0,0,255)) #スコア
        screen.disp.blit(text,(0,50))
        
        time -= 1
        if time < 0:
            muteki = 0 
        
        pg.display.update()  
        ##福光　fpsの制限が高すぎて重いので1000から120に変更
        clock.tick(120)
        

def check_bound(sc_r, obj_r): 
    x, y = +1, +1
    if obj_r.left < sc_r.left or sc_r.right  < obj_r.right : x = -1
    if obj_r.top  < sc_r.top  or sc_r.bottom < obj_r.bottom: y = -1
    return x, y

# 船渡川拓真：追加機能：5秒ごとに爆弾を1つ追加する
def increase_bombs(bombs, screen):
    global time_count
    time_now = time.time()
    if ((time_now-time_count) > 5):
        #福光　ランダムに色と大きさが決定されるように
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
        bombs.add( Bomb(r, random.randint(10, 50), (+2, +2), screen) )
        time_count = time_now

if __name__ == "__main__":
    time_count = time.time()    # 船渡川拓真：追加機能で使うための変数
    pg.init() 
    main()
    pg.quit()
    sys.exit()
