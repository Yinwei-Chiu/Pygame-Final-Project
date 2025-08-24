import pygame
from game_model import GameModel
from game_view import GameView
from Config import *
from quit_menu import QuitMenu

class GameController:
    def __init__(self, user, model, view):
        self.user = user
        self.model = model
        self.view = view
        self.quit_menu = QuitMenu()

    def handle_events(self, events, keys):
        for event in events:
            if event.type == pygame.QUIT:
                self.user.save_data()
                return "QUIT"
            
            if event.type == pygame.KEYDOWN:
                # 處理退出選單中的按鍵
                if self.quit_menu.active:
                    if event.key == pygame.K_c:
                        self.quit_menu.hide()
                        return None
                    elif event.key == pygame.K_m:
                        self.quit_menu.hide()
                        return "MENU"
                    elif event.key == pygame.K_q:
                        self.user.save_data()
                        return "QUIT"
                    return None
                
                # 正常遊戲中的按鍵
                if event.key == pygame.K_r and not self.model.run:
                    if self.model.next_level:
                        self.create_new_game()
                    else:
                    # R鍵重新開始
                        self.model.reset()
                
                elif event.key == pygame.K_q:
                    if not self.model.run:
                        # 遊戲結束畫面時，Q鍵回到主選單
                        self.model.wait = False
                        return "MENU"
                    else:
                        # 遊戲進行中時，Q鍵顯示退出選單
                        self.quit_menu.show()
                        return None

        return None

    def start_game(self):
        self.model.reset()

    def create_new_game(self):
        self.model = GameModel(self.user)
        self.model.play_BGM()

    def update(self):
        if self.model.run and not self.quit_menu.active:
            self.model.update()

    def draw(self, surface):
        self.view.draw(self.model, surface)
        self.quit_menu.draw(surface)