import pygame
import random
from Config import*


def create_spoon_image():
    """創建臨時湯匙圖片"""
    spoon_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
    
    # 湯匙柄
    pygame.draw.rect(spoon_surface, (139, 69, 19), (0, 24, 30, 12))  # 棕色柄，朝右，更大
    
    # 湯匙頭
    pygame.draw.ellipse(spoon_surface, (192, 192, 192), (24, 16, 16, 28))  # 銀色匙頭，朝右，更大
    pygame.draw.ellipse(spoon_surface, (255, 255, 255), (25, 17, 14, 26))   # 高光，更大
    
    return spoon_surface


class SpoonItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # 嘗試載入湯匙圖片
        try:
            self.image = pygame.image.load("Image/bullet/spoon.png")
            self.image = pygame.transform.scale(self.image, (40, 60))
        except pygame.error:
            self.image = create_spoon_image()
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speedx = 0   # 不水平移動
        self.speedy = 3   # 向下掉落，速度適中
        self.value = random.randint(2, 5)  # 隨機給予2-5個湯匙
        
        # 地面高度
        self.ground_y = SCREEN_HEIGHT - 100

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # 碰到地面就消失
        if self.rect.bottom >= self.ground_y:
            self.kill()
        
        # 超出畫面左右兩側也消失
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()