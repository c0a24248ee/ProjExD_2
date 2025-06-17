import os
import random
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = { # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたはばくだんRect
    戻り値：横方向、縦方向の画面内判定結果
    画面内ならTrue, 画面外ならFalse"""
    yoko, tate = True, True #初期値は画面の中
    if rct.left < 0 or WIDTH < rct.right: #横方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向の画面外判定
        tate = False
    return yoko, tate #横方向、縦方向の画面内判定結果を返す

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数：画面Surface
    戻り値：なし
    """
    black = pg.Surface((WIDTH, HEIGHT)) #黒いSurfaceを生成
    pg.draw.rect(black, (0, 0, 0), (0, 0, WIDTH, HEIGHT)) #黒色で塗りつぶす
    black.set_alpha(200) #透明度を設定
    screen.blit(black, (0, 0)) #画面に黒いSurfaceを描画
    fonto = pg.font.Font(None, 80) #フォントオブジェクトを生成
    text = fonto.render("Game Over", True, (255, 255, 255)) #文字を描画
    screen.blit(text, (390, 290)) #画面に描画
    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9) #こうかとん画像を読み込み
    screen.blit(kk2_img, (320, 290)) #画面にこうかとん画像を描画
    screen.blit(kk2_img, (730, 290)) #画面にこうかとん画像を描画
    pg.display.update() #画面更新
    time.sleep(5) #5秒待つ

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の画像を初期化する関数
    戻り値：爆弾画像のリスト、爆弾の半径のリスト
    """
    bb_imags = [] #爆弾画像のリスト
    bb_accs = [a for a in range(1, 11)] #爆弾の半径のリスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r)) #空のSurfaceを作る（爆弾用）
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r) # 赤い円を描く
        bb_img.set_colorkey((0, 0, 0)) # 黒色を透明色に設定
        bb_imags.append(bb_img)
        bb_accs.append(10*r)
    return bb_imags, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のSurfaceを作る（爆弾用）
    pg.draw.circle(bb_img,(255, 0, 0),(10,10),10) # 赤い円を描く
    bb_img.set_colorkey((0, 0, 0)) # 黒色を透明色に設定
    bb_rct = bb_img.get_rect() #爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH) #横座標の乱数
    bb_rct.centery = random.randint(0, HEIGHT) #縦座標の乱数
    vx,vy = +5, +5 #爆弾の移動速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): #こうかとんRectと爆弾rectの衝突判定
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        #if key_lst[pg.K_UP]:
        #   sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #移動をなかったことにする
        screen.blit(kk_img, kk_rct) 
        
        bb_imgs, bb_accs = init_bb_imgs() #爆弾の画像と半径を初期化
        avx = vx*bb_accs[min(tmr//500, 9)] #爆弾の横方向の加速度
        avy = vy*bb_accs[min(tmr//500, 9)] #爆弾の縦方向の加速度
        bb_img = bb_imgs[min(tmr//500, 9)] #爆弾の画像を更新
        bb_rct.move_ip(avx, avy) #爆弾の移動
        bb_rct.move_ip(vx,vy) #爆弾の移動


        yoko,tate = check_bound(bb_rct)
        if not yoko: #横方向にはみ出ていたら
            vx *= -1
        if not tate:
            vy *= -1 #縦方向にはみ出ていたら
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
