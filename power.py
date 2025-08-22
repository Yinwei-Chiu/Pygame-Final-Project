import pygame
import random
from Config import *

# 在 Power 類別之前就載好
POWER_SIZE = (40, 32)
POWER_IMAGES = {
    "heal": pygame.transform.scale(
        pygame.image.load("Image/power/heal.png"),
        POWER_SIZE
    ),
    "double_shoot": pygame.transform.scale(
        pygame.image.load("Image/power/double_shoot.png"),
        POWER_SIZE
    ), 
    "triple_shoot": pygame.transform.scale(
        pygame.image.load("Image/power/triple_shoot.png"),
        POWER_SIZE
    )
}

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.type = random.choice(list(POWER_IMAGES.keys()))
        self.image = POWER_IMAGES[self.type]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = 1


    def update(self):
        self.rect.y += self.speed

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

