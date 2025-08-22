import pygame
from Config import *

class GameView:
    def draw(self, model, surface):
        model.background.draw(surface)
        model.spaceship_group.draw(surface)
        model.spaceship_group.sprite.bullet_group.draw(surface)
        model.enemy_group.draw(surface)
        model.enemy_bullet_group.draw(surface)
        model.animation_group.draw(surface)
        model.boss_group.draw(surface)
        model.power_group.draw(surface)

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
        spoon_text = f"{model.spaceship_group.sprite.ammo}/{model.spaceship_group.sprite.max_ammo}"
        self.draw_text(surface, spoon_text, 24, WHITE, False, 50, SCREEN_HEIGHT-40)
        
        # 顯示關卡
        self.draw_text(surface, f"Level {model.user.level}", 24, WHITE, False, SCREEN_WIDTH-65, 0)

    def draw_text(self, surface, text, size, color, bold, x, y):
        font = pygame.font.Font("Font/BoutiqueBitmap9x9_Bold_1.9.ttf", size=size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surface.blit(text_surface, text_rect)