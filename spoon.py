import pygame
import random
from Config import*


class SpoonItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # 嘗試載入湯匙圖片
        
        self.image = pygame.image.load("Image/bullet/chopsticks.png")
        self.image = pygame.transform.scale(self.image, (40, 60))
        
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