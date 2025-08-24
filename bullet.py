import pygame
from Config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx = 20, speedy =0, damage=10):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("image/bullet/chopsticks.png")
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speedx = speedx
        self.speedy = speedy
        self.damage = damage
        self.frame = 0
        self.animation_time = 0
        self.animation_delay = 50
        self.is_animation = False
        self.animation = []


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