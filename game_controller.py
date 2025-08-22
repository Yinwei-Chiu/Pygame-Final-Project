import pygame
from game_model import GameModel
from game_view import GameView

class GameController:
    def __init__(self, user, model, view):
        self.user = user
        self.model = model
        self.view = view

    def handle_events(self, events, keys):
        for event in events:
            if event.type == pygame.QUIT:
                self.user.save_data()
                return "QUIT"

        if keys[pygame.K_r] and not self.model.run:
            if self.model.is_pass:
                # 玩家按 R 開始下一關
                self.create_new_game()

            else:
                # 玩家按 R 重玩這一關
                self.model.reset()


        if keys[pygame.K_q] and not self.model.run:
            self.model.wait = False
            return "MENU"
    

    def start_game(self):
        self.model.reset()


    def create_new_game(self):
        # 建立新的 Model，對應 user 的目前 level
        self.model = GameModel(self.user)
        self.model.play_BGM()


    def update(self):
        if self.model.run:
            self.model.update()

    def draw(self, surface):
        self.view.draw(self.model, surface)
