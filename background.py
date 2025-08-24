import pygame
from Config import *


class Background:
    def __init__(self, image_path, speed=1):
        self.speed = speed
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # 兩張背景圖，一張在左邊，一張接在右邊
        self.x1 = 0
        self.x2 = SCREEN_WIDTH

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        # 如果背景完全離開畫面左側，就把它放回最右邊
        if self.x1 <= -SCREEN_WIDTH:
            self.x1 = self.x2 + SCREEN_WIDTH
        if self.x2 <= -SCREEN_WIDTH:
            self.x2 = self.x1 + SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))