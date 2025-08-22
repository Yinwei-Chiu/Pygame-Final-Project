import pygame

FPS = 60

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

BG_GREY = (30, 30, 25)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKSLATEBLUE = (72, 61, 139)
DODERBLUE = (30, 144, 255)
IVORY = (255, 255, 240)
SANDYBROWN = (244, 164, 96)

# 修改為使用存在的 man.png 檔案
LIVES_ICON = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load("Image/man.png"), (50, 35)), -90)