import pygame
import random
from Config import *

def create_temp_car_image(width, height, color=(0, 0, 0)):
    """創建臨時的汽車圖片"""
    car_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # 車身 (主體矩形)
    pygame.draw.rect(car_surface, color, (10, height//3, width-20, height//2))
    
    # 車頂
    pygame.draw.rect(car_surface, color, (width//4, height//6, width//2, height//3))
    
    # 車輪
    wheel_radius = height//8
    wheel_color = (64, 64, 64)  # 深灰色
    pygame.draw.circle(car_surface, wheel_color, (width//4, height-10), wheel_radius)
    pygame.draw.circle(car_surface, wheel_color, (3*width//4, height-10), wheel_radius)
    
    # 車窗 (藍色)
    window_color = (100, 150, 255)
    pygame.draw.rect(car_surface, window_color, (width//4 + 5, height//6 + 5, width//2 - 10, height//4))
    
    return car_surface

# 載入Boss汽車圖片
try:
    boss_car_image = pygame.image.load("Image/boss_car.png")
    # 調整大小 - 縮短車身長度，高度保持
    boss_car_image = pygame.transform.scale(boss_car_image, (100, 60))  # 從120縮短到100
except pygame.error:
    # 如果找不到圖片，使用臨時汽車圖片
    print("Warning: boss_car.png not found, using temporary car image")
    boss_car_image = create_temp_car_image(100, 60, (0, 0, 0))  # 從120縮短到100

class Boss1(pygame.sprite.Sprite):
    def __init__(self, x, y, existing_hp=None):
        super().__init__()
        self.x = x
        self.y = y
        self.image = boss_car_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speedx = -8  # 提高速度，快速往左衝
        self.speedy = 0   # 不要上下移動
        self.value = 10000  # 通關獎勵
        
        # 血量管理 - 如果有傳入現有血量就使用，否則用滿血
        if existing_hp is not None:
            self.hp = existing_hp
        else:
            self.hp = 60  # 從100降低到60
        self.hp_max = 60  # 最大血量也調整為60
        
        # 加入bullet_group以避免錯誤，雖然不使用
        self.bullet_group = pygame.sprite.Group()
        
        # 固定在地面上的Y座標 - 調高一點讓玩家能射到
        self.ground_y = SCREEN_HEIGHT - 160
        
        # 重新刷新計時器
        self.respawn_timer = 0
        self.respawn_delay = random.randint(4000, 7000)  # 隨機4-7秒重新刷新
        self.is_respawning = False

    def constrain_movement(self):
        # 保持在地面上，不允許上下移動
        self.rect.centery = self.ground_y
        
        # 如果汽車完全離開畫面左側，標記為需要重新刷新
        if self.rect.right < 0:
            if not self.is_respawning:
                self.is_respawning = True
                self.respawn_timer = pygame.time.get_ticks()
                # 每次離開畫面時重新設定隨機刷新時間
                self.respawn_delay = random.randint(4000, 7000)
                # 移除除錯訊息，讓玩家需即時反應
                # print(f"Boss left screen, will respawn in {self.respawn_delay/1000} seconds")
            return True  # 返回True表示需要重新刷新
        return False

    def should_respawn(self):
        """檢查是否應該重新刷新"""
        if self.is_respawning:
            now = pygame.time.get_ticks()
            if now - self.respawn_timer >= self.respawn_delay:
                return True
        return False

    def update(self):
        # 只有水平移動
        self.rect.x += self.speedx
        return self.constrain_movement()  # 返回是否需要重新刷新

    def draw_hp(self, surface):
        hp_width = self.rect.width * (self.hp / self.hp_max)
        
        # HP條背景
        pygame.draw.rect(surface, WHITE, (self.rect.x, self.rect.y - 25, self.rect.width, 15), 2)
        # HP條
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 25, hp_width, 15))
        
        # HP文字
        font = pygame.font.Font(None, 24)
        hp_text = font.render(f"Boss HP: {self.hp}/{self.hp_max}", True, WHITE)
        surface.blit(hp_text, (self.rect.x, self.rect.y - 50))