import pygame
from Config import *

class GameView:
    def draw(self, model, surface):
        model.background.draw(surface)
        model.player_group.draw(surface)
        model.player_group.sprite.bullet_group.draw(surface)
        model.food_group.draw(surface)
        model.animation_group.draw(surface)
        
        # Boss需要特殊繪製以配合閃爍效果
        if model.boss_group.sprite:
            boss = model.boss_group.sprite
            if boss.visible:
                surface.blit(boss.image, boss.rect)
        
        model.spoon_group.draw(surface)

        # Boss HP
        if model.boss_group.sprite:
            model.boss_group.sprite.draw_hp(surface)

        # Game Over/Win Text
        if not model.run:
            if model.is_pass:
                self.draw_text(surface, "You Win!!", 48, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-80)
                self.draw_text(surface, "Press R to start the next level", 28, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            else:
                self.draw_text(surface, "Game Over!!", 48, RED, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-80)
                self.draw_text(surface, "Press R to restart the game", 28, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            self.draw_text(surface, "Press Q to return the initial menu", 26, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50)

        # 顯示湯匙數量
        self.draw_text(surface, "Spoons", 24, WHITE, False, 50, SCREEN_HEIGHT-65)
        spoon_text = f"{model.player_group.sprite.ammo}/{model.player_group.sprite.max_ammo}"
        self.draw_text(surface, spoon_text, 24, WHITE, False, 50, SCREEN_HEIGHT-40)
        
        # 顯示遊戲時間
        current_time = model.game_time / 1000  # 轉換為秒
        self.draw_text(surface, f"Time: {current_time:.1f}s", 24, WHITE, False, SCREEN_WIDTH-80, 20)
        
        # 顯示飢餓度
        hunger = model.player_group.sprite.hunger
        max_hunger = model.player_group.sprite.max_hunger
        hunger_color = WHITE
        if hunger < 30:
            hunger_color = RED  # 快餓死時顯示紅色
        elif hunger < 60:
            hunger_color = YELLOW  # 有點餓時顯示黃色
        
        self.draw_text(surface, "Hunger", 24, hunger_color, False, 200, SCREEN_HEIGHT-65)
        hunger_text = f"{hunger}/{max_hunger}"
        self.draw_text(surface, hunger_text, 24, hunger_color, False, 200, SCREEN_HEIGHT-40)
        
        # 飢餓度條
        bar_width = 100
        bar_height = 10
        bar_x = 150
        bar_y = SCREEN_HEIGHT - 20
        
        # 背景條
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # 飢餓度條
        hunger_width = int(bar_width * (hunger / max_hunger))
        pygame.draw.rect(surface, hunger_color, (bar_x, bar_y, hunger_width, bar_height))
        # 邊框
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)

    def draw_text(self, surface, text, size, color, bold, x, y):
        try:
            font = pygame.font.Font("Font/BoutiqueBitmap9x9_Bold_1.9.ttf", size=size)
        except:
            font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surface.blit(text_surface, text_rect)