import pygame
from enemy import Enemy

class EnemyFactory:
    enemy_images = {}

    @staticmethod
    def load_images():
        # 台南美食：棺材板和芒果冰
        # 確保使用正確的路徑
        try:
            EnemyFactory.enemy_images = {
                "coffin_bread": [pygame.transform.scale(
                    pygame.image.load("Image/tainan_food/coffin_bread.png"), (45, 35)) for _ in range(5)],
                "mango_ice": [pygame.transform.scale(
                    pygame.image.load("Image/tainan_food/mango_ice.png"), (35, 40)) for _ in range(5)],
            }
        except pygame.error as e:
            print(f"Error loading food images: {e}")
            # 如果找不到台南美食圖片，使用預設圖片
            try:
                # 嘗試使用其他可用的圖片作為替代
                default_image = pygame.image.load("Image/man.png")
                EnemyFactory.enemy_images = {
                    "coffin_bread": [pygame.transform.scale(default_image, (45, 35)) for _ in range(5)],
                    "mango_ice": [pygame.transform.scale(default_image, (35, 40)) for _ in range(5)],
                }
            except pygame.error:
                # 如果連預設圖片都找不到，創建簡單的彩色方塊
                coffin_surface = pygame.Surface((45, 35))
                coffin_surface.fill((139, 69, 19))  # 棕色代表棺材板
                
                mango_surface = pygame.Surface((35, 40))
                mango_surface.fill((255, 165, 0))  # 橘色代表芒果冰
                
                EnemyFactory.enemy_images = {
                    "coffin_bread": [coffin_surface for _ in range(5)],
                    "mango_ice": [mango_surface for _ in range(5)],
                }

    @staticmethod
    def create(food_type, x, y, bullet_group):
        if food_type == "coffin_bread":
            return Enemy(x, y, animation=EnemyFactory.enemy_images[food_type], 
                         bullet_group=bullet_group, bullet_type=food_type, value=1, speedx_range=(-2, -1))  # 只給1個湯匙
        elif food_type == "mango_ice":
            return Enemy(x, y, animation=EnemyFactory.enemy_images[food_type], 
                         bullet_group=bullet_group, bullet_type=food_type, value=2, speedx_range=(-4, -2))  # 給2個湯匙