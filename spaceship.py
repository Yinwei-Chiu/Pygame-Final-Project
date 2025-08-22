import pygame
from Config import *
from attack_strategy import NormalAttack, DoubleAttack, TripleAttack

# 載入角色圖片
spaceship_images = {
    "normal": pygame.transform.scale(
        pygame.image.load("Image/man.png"), (90, 60)), 
    "double": pygame.transform.scale(
        pygame.image.load("Image/man_2.png"), (90, 60)), 
    "triple": pygame.transform.scale(
        pygame.image.load("Image/man_2.png"), (90, 60))
}

ATTACK_STRATEGY_MAP = {
    "normal": lambda: (NormalAttack(), spaceship_images["normal"]),
    "double_shoot": lambda: (DoubleAttack(), spaceship_images["double"]),
    "triple_shoot": lambda: (TripleAttack(), spaceship_images["triple"])
}

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_images["normal"]
        self.ground_y = SCREEN_HEIGHT - 150  # 調整地面高度到道路位置
        self.rect = self.image.get_rect(center=(150, self.ground_y))
        self.lives = 1  # 只有一次生命
        self.max_lives = 1
        self.speed = 10
        
        # 彈藥系統（取代原本的無限子彈）
        self.ammo = 0          # 開始時沒有湯匙
        self.max_ammo = 20     # 最大湯匙數
        
        # 重力系統變數
        self.gravity = 0.8
        self.jump_strength = -18  # 從-15調整到-18，稍微跳高一些
        self.velocity_y = 0
        self.is_jumping = False
        
        # 射擊動畫變數
        self.is_shooting = False
        self.shoot_animation_time = 0
        self.shoot_animation_duration = 300  # 射擊動畫持續300毫秒
        
        # 衝刺系統變數
        self.is_dashing = False
        self.dash_speed = 20  # 衝刺速度
        self.dash_distance = 150  # 大概1.5個車長的距離
        self.dash_remaining = 0
        self.dash_direction = 0  # 1為右，-1為左
        
        # 雙擊檢測變數
        self.last_left_press = 0
        self.last_right_press = 0
        self.double_click_window = 300  # 300毫秒內的雙擊才算
        self.left_click_count = 0
        self.right_click_count = 0
        # 按鍵狀態追蹤（用來檢測按鍵的按下和釋放）
        self.left_key_pressed = False
        self.right_key_pressed = False
        
        self.attack_strategy = NormalAttack()
        self.bullet_group = pygame.sprite.Group()
        self.bullet_ready = True
        self.bullet_time = 0
        self.bullet_delay = 400
        self.shoot_sound = pygame.mixer.Sound("Sound/shoot0.mp3")

    def get_user_input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # 檢測雙擊左右鍵
        self.check_double_click(keys, current_time)

        # 如果正在衝刺，執行衝刺移動
        if self.is_dashing:
            self.perform_dash()
        else:
            # 正常左右移動
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed

        # 向上跳躍
        if keys[pygame.K_UP] and not self.is_jumping:
            self.jump_up()

        # 向下跳躍
        if keys[pygame.K_DOWN]:
            self.jump_down()

        # 射擊
        if keys[pygame.K_SPACE] and self.bullet_ready and self.ammo > 0:
            self.bullet_ready = False
            self.shoot()
            self.ammo -= 1  # 消耗彈藥
            self.start_shoot_animation()  # 開始射擊動畫
            self.bullet_time = pygame.time.get_ticks()

    def check_double_click(self, keys, current_time):
        """檢測雙擊左右鍵 - 只在按鍵從未按下變為按下時觸發"""
        # 檢測左鍵 - 只有在按鍵剛被按下時才計數
        if keys[pygame.K_LEFT] and not self.left_key_pressed:
            # 按鍵剛被按下
            if current_time - self.last_left_press < self.double_click_window:
                self.left_click_count += 1
                if self.left_click_count == 2:
                    self.start_dash(-1)  # 向左衝刺
                    self.left_click_count = 0
            else:
                self.left_click_count = 1
            self.last_left_press = current_time
        
        # 檢測右鍵 - 只有在按鍵剛被按下時才計數
        if keys[pygame.K_RIGHT] and not self.right_key_pressed:
            # 按鍵剛被按下
            if current_time - self.last_right_press < self.double_click_window:
                self.right_click_count += 1
                if self.right_click_count == 2:
                    self.start_dash(1)  # 向右衝刺
                    self.right_click_count = 0
            else:
                self.right_click_count = 1
            self.last_right_press = current_time

        # 更新按鍵狀態
        self.left_key_pressed = keys[pygame.K_LEFT]
        self.right_key_pressed = keys[pygame.K_RIGHT]

        # 重置計數器（如果太久沒按）
        if current_time - self.last_left_press > self.double_click_window:
            self.left_click_count = 0
        if current_time - self.last_right_press > self.double_click_window:
            self.right_click_count = 0

    def start_dash(self, direction):
        """開始衝刺"""
        if not self.is_dashing:  # 避免衝刺中再次觸發
            self.is_dashing = True
            self.dash_direction = direction
            self.dash_remaining = self.dash_distance

    def perform_dash(self):
        """執行衝刺移動"""
        if self.dash_remaining > 0:
            # 計算這一幀要移動的距離
            move_distance = min(self.dash_speed, self.dash_remaining)
            self.rect.x += move_distance * self.dash_direction
            self.dash_remaining -= move_distance
        else:
            # 衝刺完成
            self.is_dashing = False

    def jump_up(self):
        self.velocity_y = self.jump_strength
        self.is_jumping = True

    def jump_down(self):
        if self.is_jumping:
            self.velocity_y += 3
        elif not self.is_jumping:
            self.velocity_y = 5

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        if self.rect.centery >= self.ground_y:
            self.rect.centery = self.ground_y
            self.velocity_y = 0
            self.is_jumping = False

    def shoot(self):
        self.attack_strategy.shoot(self)

    def start_shoot_animation(self):
        """開始射擊動畫"""
        self.is_shooting = True
        self.shoot_animation_time = pygame.time.get_ticks()
        self.change_image(spaceship_images["double"])  # 立即切換到射擊姿勢

    def update_shoot_animation(self):
        """更新射擊動畫"""
        if self.is_shooting:
            now = pygame.time.get_ticks()
            if now - self.shoot_animation_time >= self.shoot_animation_duration:
                # 動畫時間結束，回到普通狀態
                self.is_shooting = False
                self.change_image(spaceship_images["normal"])

    def constrain_movement(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0

    def recharge_bullet(self):
        if not self.bullet_ready:
            now = pygame.time.get_ticks()
            if now - self.bullet_time >= self.bullet_delay:
                self.bullet_ready = True

    def add_ammo(self, amount):
        """增加彈藥"""
        self.ammo = min(self.ammo + amount, self.max_ammo)

    def apply_power(self, power):
        if power.type == "heal":
            self.lives = min(self.lives + 1, self.max_lives)
            return
        
        if power.type in ATTACK_STRATEGY_MAP:
            strategy, img = ATTACK_STRATEGY_MAP[power.type]()
            self.attack_strategy = strategy
            self.attack_strategy.activate()
            self.change_image(img)

    def check_status(self):
        if self.attack_strategy.is_expired():
            self.attack_strategy = NormalAttack()
            self.change_image(spaceship_images["normal"])

    def update(self):
        self.get_user_input()
        self.apply_gravity()
        self.update_shoot_animation()  # 更新射擊動畫
        self.constrain_movement()
        self.bullet_group.update()
        self.recharge_bullet()
        self.check_status()

    def reset(self):
        self.rect = self.image.get_rect(center=(150, self.ground_y))
        self.velocity_y = 0
        self.is_jumping = False
        self.is_shooting = False
        self.is_dashing = False  # 重置衝刺狀態
        self.dash_remaining = 0
        self.left_click_count = 0  # 重置雙擊計數
        self.right_click_count = 0
        self.left_key_pressed = False  # 重置按鍵狀態
        self.right_key_pressed = False
        self.ammo = 0  # 開始時沒有湯匙
        self.lives = self.max_lives
        self.bullet_group.empty()
        self.attack_strategy = NormalAttack()
        self.change_image(spaceship_images["normal"])

    def change_image(self, new_image):
        self.image = new_image