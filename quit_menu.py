import pygame
from game_model import GameModel
from game_view import GameView
from Config import *

class QuitMenu:
    def __init__(self):
        self.active = False
        
    def draw(self, surface):
        if not self.active:
            return
            
        # 半透明背景覆蓋
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # 選單背景框
        menu_width = 400
        menu_height = 200
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        
        pygame.draw.rect(surface, (50, 50, 50), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(surface, WHITE, (menu_x, menu_y, menu_width, menu_height), 3)
        
        # 標題
        self.draw_text(surface, "Game Paused", 32, WHITE, menu_x + menu_width//2, menu_y + 40)
        
        # 選項
        self.draw_text(surface, "C - Continue Game", 24, WHITE, menu_x + menu_width//2, menu_y + 90)
        self.draw_text(surface, "M - Return to Main Menu", 24, WHITE, menu_x + menu_width//2, menu_y + 120)
        self.draw_text(surface, "Q - Quit Game", 24, WHITE, menu_x + menu_width//2, menu_y + 150)
    
    def draw_text(self, surface, text, size, color, x, y):
        try:
            font = pygame.font.Font("Font/BoutiqueBitmap9x9_Bold_1.9.ttf", size)
        except:
            font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surface.blit(text_surface, text_rect)
    
    def show(self):
        self.active = True
    
    def hide(self):
        self.active = False