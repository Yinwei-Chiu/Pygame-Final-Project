import pygame
import random
from Config import *

# 在 Power 類別之前就載好
POWER_SIZE = (72, 72)
POWER_IMAGES = {
    "cube_sugar": pygame.transform.scale(
        pygame.image.load("image/power/cube_sugar.png"),
        POWER_SIZE
    ),
    "ice_bar": pygame.transform.scale(
        pygame.image.load("image/power/Ice_bar.png"),
        POWER_SIZE
    ), 
    "turtle_cake": pygame.transform.scale(
        pygame.image.load("image/power/turtle_cake.png"),
        POWER_SIZE
    ),
    "chopsticks": pygame.transform.scale(
        pygame.image.load("image/bullet/chopsticks.png"),
        POWER_SIZE 
    )
}

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y,chopsticks = False):
        super().__init__()
        self.x = x
        self.y = y
        if chopsticks:
            self.type = "chopsticks"
            self.speed = 3
            self.hunger = 0 # 筷子不新增飢餓度
        else:
            self.type = random.choice(list(POWER_IMAGES.keys()-{"chopsticks"}))
            self.hunger = 5 # 每個強化道具吃了恢復5點飢餓度
            self.speed = 1
        self.image = POWER_IMAGES[self.type]
        self.rect = self.image.get_rect(center=(self.x, self.y))


    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()


