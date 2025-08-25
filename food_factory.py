import pygame
from food_config import food_dict
from food import Food

class FoodFactory:
    food_images = {}

    @staticmethod
    def load_image():
        """載入所有食物圖片到快取（只做一次）"""
        if FoodFactory.food_images:  # 已載入就略過
            return
        for food_name, food_info in food_dict.items():
            try:
                image = pygame.image.load(food_info["path"]).convert_alpha()
                image = pygame.transform.scale(image, (72, 72))
                FoodFactory.food_images[food_name] = image
            except pygame.error as e:
                print(f"Error loading image for {food_name}: {e}")

    @staticmethod
    def create(food_type, x, y):
        """建立 Food 物件，確保圖已載入並回傳"""
        # 確保已先載圖（或你也可以在 main 啟動時手動呼叫一次 load_image）
        if not FoodFactory.food_images:
            FoodFactory.load_image()

        if food_type not in FoodFactory.food_images:
            # 這裡給更友善的錯誤訊息（避免直接 KeyError）
            raise ValueError(f"Unknown food_type: {food_type}. "
                             f"Known types: {list(FoodFactory.food_images.keys())}")

        image = FoodFactory.food_images[food_type]
        hunger = food_dict[food_type]["hunger"]
        return Food(x, y, image=image, food_type=food_type, hunger=hunger, speedx_range=(-2, -1))
