import pygame
import random
from Config import *

def create_spoon_image():
    """創建臨時湯匙圖片"""
    spoon_surface = pygame.Surface((20, 30), pygame.SRCALPHA)
    
    # 湯匙柄
    pygame.draw.rect(spoon_surface, (139, 69, 19), (0, 12, 15, 6))  # 棕色柄，朝右
    
    # 湯匙頭
    pygame.draw.ellipse(spoon_surface, (192, 192, 192), (12, 8, 8, 14))  # 銀色匙頭，朝右
    pygame.draw.ellipse(spoon_surface, (255, 255, 255), (13, 9, 6, 12))   # 高光
    
    return spoon_surface

class SpoonItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # 嘗試載入湯匙圖片
        try:
            self.image = pygame.image.load("Image/spoon.png")
            self.image = pygame.transform.scale(self.image, (20, 30))
            print("Spoon image loaded successfully!")
        except pygame.error:
            # 如果找不到圖片，使用程式生成的臨時圖片
            self.image = create_spoon_image()
            print("Using temporary spoon image")
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speedx = -3  # 向左移動
        self.speedy = random.choice([-1, 0, 1])  # 輕微上下飄動
        self.value = random.randint(2, 5)  # 隨機給予2-5個湯匙
        
        # 閃爍效果
        self.blink_time = 0
        self.blink_delay = 300
        self.visible = True

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # 閃爍效果
        now = pygame.time.get_ticks()
        if now - self.blink_time > self.blink_delay:
            self.visible = not self.visible
            self.blink_time = now
        
        # 超出畫面左側就消失
        if self.rect.right < 0:
            self.kill()

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)