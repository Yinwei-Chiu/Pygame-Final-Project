import pygame
from Config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, damage=10):
        super().__init__()
        self.x = x
        self.y = y
        # self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speedx = speedx
        self.speedy = speedy
        self.damage = damage
        self.frame = 0
        self.animation_time = 0
        self.animation_delay = 50
        self.is_animation = False
        self.animation = []
        self.image = None
        self.rect = None


    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.x > SCREEN_WIDTH + 15 or self.rect.x < -15:
            self.kill()

        if self.is_animation and self.animation:
            now = pygame.time.get_ticks()
            if now - self.animation_time > self.animation_delay:
                self.frame = (self.frame + 1) % len(self.animation)
                self.image = self.animation[self.frame]
                self.animation_time = now