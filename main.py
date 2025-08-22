import pygame, sys
from Config import *
from user import User
from init_menu import InitMenu
from game_model import GameModel
from game_view import GameView
from game_controller import GameController

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game!!")
clock = pygame.time.Clock()

user = User()
init_menu = InitMenu(user)

# 初始化第一關
model = GameModel(user)
view = GameView()
controller = GameController(user, model, view)
model.play_BGM()

running = True
while running:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    # 選單或遊戲
    if init_menu.run:
        for event in events:
            if event.type == pygame.QUIT:
                user.save_data()
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            init_menu.run = False
            controller.create_new_game()
            controller.start_game()
            
        
        init_menu.draw(screen)

    else:
        result = controller.handle_events(events, keys)
        if result == "QUIT":
            running = False
        if result == "MENU":
            init_menu.run = True

        controller.update()
        controller.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
