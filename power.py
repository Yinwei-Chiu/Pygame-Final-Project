import pygame
import random
from Config import *

# 在 Power 類別之前就載好
POWER_SIZE = (40, 32)
POWER_IMAGES = {
    "cube_sugar": pygame.transform.scale(
        pygame.image.load("image/power/cube_sugar.png"),
        POWER_SIZE
    ),
    "ice_bar": pygame.transform.scale(
        pygame.image.load("image/power/Ice_bar.png"),
        POWER_SIZE
    ), 
    "turte_cake": pygame.transform.scale(
        pygame.image.load("image/power/turtle_cake.png"),
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

