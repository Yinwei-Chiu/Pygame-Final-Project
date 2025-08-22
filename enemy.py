import pygame
import random
from Config import *
from bullet_factory import BulletFactory


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, animation, bullet_group, bullet_type="enemy1", value=100, speedx_range=(-4, -2), speedy_range=(-2, 2)):
        super().__init__()
        self.x = x
        self.y = y
        self.animation = animation
        self.image = self.animation[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speedx = random.randint(*speedx_range)
        self.speedy = random.randint(*speedy_range)
        self.change_direction_time = 0
        self.change_direction_delay = 1200
        self.bullet_group = bullet_group
        self.bullet_time = 0
        self.min_delay = 1000   # 最短間隔（毫秒）
        self.max_delay = 2000  # 最長間隔（毫秒）
        self.bullet_delay = random.randint(self.min_delay, self.max_delay)
        self.bullet_type = bullet_type
        self.value = value
        self.frame = 0
        self.animation_time = 0
        self.animation_delay = 50
        
        # 食物飛行範圍限制（廚師能跳到的高度）
        self.min_y = SCREEN_HEIGHT - 300  # 最高點（廚師跳躍能到達）
        self.max_y = SCREEN_HEIGHT - 100  # 最低點（接近地面）

    def constrain_movement(self):
        # 限制在廚師能跳到的高度範圍內
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

    def shoot_bullet(self):
        # 食物不射擊
        pass

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.constrain_movement()
        self.change_direction()
        # 移除射擊功能
        # self.shoot_bullet()
        # self.bullet_group.update()

        # 動畫效果
        now = pygame.time.get_ticks()
        if now - self.animation_time > self.animation_delay:
            self.frame += 1
            self.animation_time = pygame.time.get_ticks()
            if self.frame == len(self.animation):
                self.frame = 0
            else:
                self.image = self.animation[self.frame]