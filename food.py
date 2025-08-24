import pygame
import random
from Config import *

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, image, food_type, hunger, speedx_range=(-4, -2), speedy_range=(-2, 2)):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speedx = random.randint(*speedx_range)
        self.speedy = random.randint(*speedy_range)
        self.change_direction_time = 0
        self.change_direction_delay = 1200
        self.food_type = food_type
        self.hunger = hunger  # 食物價值（恢復飢餓度）
        self.frame = 0
        self.animation_time = 0
        self.animation_delay = 50
        
        # 食物飛行範圍限制（玩家能跳到的高度）
        self.min_y = SCREEN_HEIGHT - 300  # 最高點（玩家跳躍能到達）
        self.max_y = SCREEN_HEIGHT - 100  # 最低點（接近地面）

    def constrain_movement(self):
        # 限制在玩家能跳到的高度範圍內
        if self.rect.top < self.min_y or self.rect.bottom > self.max_y:
            self.speedy = -self.speedy
        
        # 超出左邊界就消失
        if self.rect.right < 0:
            self.kill()

    def change_direction(self):
        now = pygame.time.get_ticks()
        if now - self.change_direction_time > self.change_direction_delay:
            self.speedy = self.speedy * random.choice([-1, 1])
            self.change_direction_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.constrain_movement()
        self.change_direction()
