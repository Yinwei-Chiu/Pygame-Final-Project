import pygame
from Config import *

class InitMenu:
    def __init__(self, user):
        self.run = True
        self.user = user
        
        # 嘗試載入主畫面圖片
        # 你可以把新的主畫面圖片放在這個路徑
        self.image = pygame.image.load("Image/background/Anping.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Main menu background loaded successfully!")

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
        hello = pygame.image.load("image/background/Hello.png")
        hello = pygame.transform.scale(hello, (300, 300))
        hello_rect = hello.get_rect()
        hello_rect.centery=SCREEN_HEIGHT//2
        hello_rect.left = 0
        surface.blit(hello, (hello_rect.x,hello_rect.y))

        best_time_text = self.user.get_best_time_text()
        texts = ["台南，我吃一點", "Tainan, I eat some", f"Best Time: {best_time_text}",
                "引導可愛的貓咪! 用筷子吃遍台南，制裁三寶！",
                "雙擊方向鍵能衝刺，小心別被撞到！",
                "遊戲中按Q鍵可隨時退出",
                "Press P to start the game!"]

        sizes = [48, 36, 36, 24, 24, 24, 36]
        sizes *= 3
        colors = [(255,255,255), (255,255,255), (255,255,0),
                (255,255,255), (255,255,255), (255,255,255), (255,255,0)]

        tg = RightAlignedTextGroup(texts, sizes, colors,width=SCREEN_WIDTH//2)
        tg.draw(surface, (400, 200))
        


class RightAlignedTextGroup:
    def __init__(self, texts, font_sizes, colors, width):
        self.surfaces = []
        self.width = width
        for t, size, color in zip(texts, font_sizes, colors):
            if(t =="台南，我吃一點" or t=="Tainan, I eat some"):
                font = pygame.font.Font("Font/BoutiqueBitmap9x9_Bold_1.9.ttf", size=size+10,)
            else:
                font = pygame.font.Font("Font/Cubic_11.ttf", size=size,)
            self.surfaces.append(font.render(t, True, color))

    def draw(self, surface, pos):
        x, y = pos
        for s in self.surfaces:
            # 每行靠右對齊
            right_x = x + self.width - s.get_width()
            surface.blit(s, (right_x, y))
            y += s.get_height() + 10  # 行距

