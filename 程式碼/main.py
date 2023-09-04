from typing import Any
import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 視窗大小
WIDTH, HEIGHT = 1200, 650

# 顏色
Background = (247, 220, 190)
# 精靈
all_sprites = pygame.sprite.Group()
# 定義
noise = [-15, -5, 5, 15]
pos_table = [60, 61, 62, 63, 64, 65, 66, 56, 55, 54, 53, 52, 51, 50, 40, 41, 42, 43, 44, 45, 46, 36,
             35, 34, 33, 32, 31, 30, 20, 21, 22, 23, 24, 25, 26, 16, 15, 14, 13, 12, 11, 10, 0, 1, 2, 3, 4, 5, 6]
snake = {1: 16, 11: 4, 18: 33, 20: 35, 22: 7, 31: 0, 30: 42, 47: 0, 44: 27}
star = [2, 4, 8, 13, 15, 17, 21, 25, 29, 32, 35, 41, 45, 47]

PX = 600/14
# 建立視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("蛇梯棋")
clock = pygame.time.Clock()
pick = 0

# 格子編號轉座標


def toXY(pos):
    row = pos_table[pos] // 10
    col = pos_table[pos] % 10
    x = 300 + PX + PX * 2 * col  # 设置玩家的初始X坐标为屏幕中心X坐标
    y = 25 + PX + PX * 2 * row  # 设置玩家的底部Y坐标为屏幕中心Y坐标
    return x, y


class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load("image/map2.png")
        self.image = pygame.transform.scale(original_image, (600, 600))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2  # 设置玩家的初始X坐标
        self.rect.centery = HEIGHT // 2  # 设置玩家的初始Y坐标


class Piece(pygame.sprite.Sprite):
    pos = 0
    team = 0

    def __init__(self, team):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load(f"image/{team + 1}.png")
        self.image = pygame.transform.scale(original_image, (80, 80))
        self.rect = self.image.get_rect()
        self.team = team

    # 移動動畫
    def animation(self, newPos, page):
        targetX, targetY = toXY(newPos)
        targetX += noise[self.team]
        targetY -= 10
        for i in range(page):
            self.rect.centerx += round((targetX-self.rect.centerx) / (page-i))
            self.rect.bottom += round((targetY-self.rect.bottom) / (page-i))
            # 重新渲染
            screen.fill(Background)
            screen.blit(map.image, map.rect.topleft)
            all_sprites.draw(screen)
            pygame.display.flip()
        self.rect.centerx, self.rect.bottom = targetX, targetY

    def move(self, steps):
        newPos = self.pos + steps
        if newPos == 49 or newPos == -1:
            newPos = 0
        self.animation(newPos, 50)
        self.pos = newPos
        self.update()

    def goto(self, newPos):
        self.animation(newPos, 120)
        self.pos = newPos
        self.update()

    def update(self):
        x, y = toXY(self.pos)
        self.rect.centerx = x + noise[self.team]  # 设置玩家的初始X坐标为屏幕中心X坐标
        self.rect.bottom = y - int(pick == self.team)*10  # 设置玩家的底部Y坐标为屏幕中心Y坐标


# 创建玩家对象
map = Map()
pieces = [Piece(0), Piece(1), Piece(2), Piece(3)]


class GameCard:
    def __init__(self, team):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load(f"image/g{team+1}.png")
        self.image = pygame.transform.scale(original_image, (366, 650))
        self.rect = self.image.get_rect()
        self.team = team
        self.rect.center = WIDTH//2, HEIGHT//2


cards = [GameCard(0), GameCard(1), GameCard(2), GameCard(3)]


def chooseCard():  # 選擇遊戲卡
    page = random.randint(100, 160)
    for i in range(page):
        clock.tick(30)
        # 重新渲染
        screen.fill(Background)
        screen.blit(map.image, map.rect.topleft)
        all_sprites.draw(screen)
        screen.blit(cards[i % 4].image, cards[i % 4].rect.topleft)
        pygame.display.flip()
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flag = False


# 创建精灵组
all_sprites.add(pieces)


# 遊戲迴圈
running = True
key_pressed = False
while running:
    clock.tick(60)  # FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # 检测按键按下事件
            if event.key == pygame.K_q:
                pick = 0
            elif event.key == pygame.K_w:
                pick = 1
            elif event.key == pygame.K_e:
                pick = 2
            elif event.key == pygame.K_r:
                pick = 3
            elif event.key == pygame.K_SPACE:
                pieces[pick].move(1)
                break
            elif event.key == pygame.K_BACKSPACE:
                pieces[pick].move(-1)
                break
            elif event.key == pygame.K_RETURN:
                if pieces[pick].pos in snake:
                    pieces[pick].goto(snake[pieces[pick].pos])
                    break
                elif pieces[pick].pos in star:
                    chooseCard()
    pygame.event.clear()
    # 更新遊戲邏輯
    all_sprites.update()
    # 渲染畫面
    screen.fill(Background)
    screen.blit(map.image, map.rect.topleft)
    all_sprites.draw(screen)  # 将所有精灵绘制到屏幕上

    pygame.display.flip()

# 退出遊戲
pygame.quit()
sys.exit()
