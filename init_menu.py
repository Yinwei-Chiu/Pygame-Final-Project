import pygame
from Config import *

def create_temp_menu_background():
    """創建臨時的主畫面背景"""
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # 漸層背景 - 台南天空色調
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        # 從天空藍漸變到夕陽橘
        r = int(135 + (255 - 135) * ratio)
        g = int(206 + (165 - 206) * ratio)
        b = int(235 + (0 - 235) * ratio)
        color = (min(255, r), min(255, g), min(255, b))
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
    
    # 添加一些裝飾元素
    # 地面
    pygame.draw.rect(surface, (101, 67, 33), (0, SCREEN_HEIGHT-100, SCREEN_WIDTH, 100))
    
    # 簡單的建築剪影
    building_color = (50, 50, 50)
    pygame.draw.rect(surface, building_color, (100, SCREEN_HEIGHT-200, 80, 100))
    pygame.draw.rect(surface, building_color, (250, SCREEN_HEIGHT-180, 60, 80))
    pygame.draw.rect(surface, building_color, (400, SCREEN_HEIGHT-220, 90, 120))
    
    return surface

class InitMenu:
    def __init__(self, user):
        self.run = True
        self.user = user
        
        # 嘗試載入主畫面圖片
        try:
            # 你可以把新的主畫面圖片放在這個路徑
            self.image = pygame.image.load("Image/background/Anping.png")
            self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            print("Main menu background loaded successfully!")
        except pygame.error:
            # 如果都找不到，使用程式生成的背景
            self.image = create_temp_menu_background()
            print("Using temporary generated background")

    def draw(self, surface):
        # 畫出背景圖片
        surface.blit(self.image, (0, 0))
        
        # 半透明覆蓋層讓文字更清楚
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)  # 透明度
        overlay.fill((0, 0, 0))  # 黑色覆蓋
        surface.blit(overlay, (0, 0))
        
        # 遊戲標題和資訊（移除金錢顯示）
        # self.draw_text(surface, f"Money:{self.user.money}", 24, WHITE, False, 120, 20)
        
        # 主標題 - 台南美食大冒險
        self.draw_text(surface, "台南美食大冒險", 36, WHITE, False, SCREEN_WIDTH//2, 250)
        self.draw_text(surface, "Tainan Food Adventure", 28, WHITE, False, SCREEN_WIDTH//2, 290)
        
        # 最佳紀錄顯示
        best_time_text = self.user.get_best_time_text()
        self.draw_text(surface, f"Best Time: {best_time_text}", 24, YELLOW, False, SCREEN_WIDTH//2, 320)
        
        # 遊戲說明
        self.draw_text(surface, "騎摩托車收集台南美食，用湯匙射擊黑道汽車!", 20, WHITE, False, SCREEN_WIDTH//2, 360)
        self.draw_text(surface, "雙擊方向鍵衝刺，小心別被撞到!", 18, WHITE, False, SCREEN_WIDTH//2, 385)
        self.draw_text(surface, "遊戲中按Q鍵可隨時退出", 16, WHITE, False, SCREEN_WIDTH//2, 410)
        
        # 開始遊戲提示
        self.draw_text(surface, "Press P to start the game!", 24, YELLOW, False, SCREEN_WIDTH//2, 450)
        
        # 移除關卡資訊顯示
        # self.draw_text(surface, f"- Level {self.user.level} -", 20, WHITE, False, SCREEN_WIDTH//2, 500)
        
        # 移除關卡預覽圖片顯示
        # try:
        #     level_image = pygame.image.load(f"Image/level{self.user.level}.jpg")
        #     level_image = pygame.transform.scale(level_image, (200, 120))
        #     surface.blit(level_image, (SCREEN_WIDTH//2 - 100, 530))
        # except pygame.error:
        #     # 如果沒有關卡圖片，顯示簡單的關卡資訊框
        #     pygame.draw.rect(surface, (50, 50, 50), (SCREEN_WIDTH//2 - 100, 530, 200, 120))
        #     pygame.draw.rect(surface, WHITE, (SCREEN_WIDTH//2 - 100, 530, 200, 120), 2)
        #     self.draw_text(surface, f"Level {self.user.level}", 24, WHITE, False, SCREEN_WIDTH//2, 580)

    def draw_text(self, surface, text, size, color, bold, x, y):
        font = pygame.font.Font("Font/BoutiqueBitmap9x9_Bold_1.9.ttf", size=size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surface.blit(text_surface, text_rect)