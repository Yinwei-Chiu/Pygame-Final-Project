import pygame
import random
from Config import *
from LevelConfig import LEVELS
from background import Background
from spaceship import Spaceship
from enemy_factory import EnemyFactory
from animation import Explosion, Heal
from progress import Progress
import boss
from power import Power

EnemyFactory.load_images()

class GameModel:
    def __init__(self, user):
        self.user = user
        self.level = user.level
        self.config = LEVELS[user.level]

        self.background = Background(self.config["background"], 1)
        self.spaceship_group = pygame.sprite.GroupSingle(Spaceship())
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.animation_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.GroupSingle()
        self.power_group = pygame.sprite.Group()

        self.enemy_generator_time = 0
        self.enemy_generator_delay = random.randint(*self.config["enemy_delay"])

        self.run = False
        self.wait = False
        self.is_pass = False

        self.money = 0
        self.game_time = 0
        self.start_time = pygame.time.get_ticks()
        self.boss_time = self.config["boss_time"]
        self.progress = Progress(SCREEN_WIDTH - 50, 60, self.game_time, self.boss_time)
        self.power_probability = 0.8

    # ------------------ 更新遊戲 ------------------
    def update(self):
        self.background.update()
        self.spaceship_group.update()
        self.enemy_group.update()
        self.enemy_bullet_group.update()
        self.animation_group.update()
        self.boss_group.update()
        
        # 檢查Boss是否需要重新刷新
        if self.boss_group.sprite:
            if self.boss_group.sprite.should_respawn():
                # 保存當前血量
                current_hp = self.boss_group.sprite.hp
                # 移除舊Boss
                self.boss_group.sprite.kill()
                # 在畫面右側外創建新Boss，血量不變
                boss_y = SCREEN_HEIGHT - 160  # 調高位置
                new_boss = boss.Boss1(SCREEN_WIDTH + 150, boss_y, current_hp)
                self.boss_group.add(new_boss)
                # 移除除錯訊息，保持神秘感
                # print(f"Boss respawned with HP: {current_hp}/{new_boss.hp_max}")
                # print(f"Next respawn delay will be: {new_boss.respawn_delay/1000} seconds")
        
        self.power_group.update()

        self.game_time = pygame.time.get_ticks() - self.start_time
        self.progress.update(self.game_time)

        self.enemy_generator()
        self.check_for_collisions()
        self.check_for_state()
        self.boss_appear()

    def enemy_generator(self):
        now = pygame.time.get_ticks()
        if now - self.enemy_generator_time > self.enemy_generator_delay:
            food_type = random.choice(self.config["enemies"])
            # 食物在廚師能跳到的範圍內隨機生成
            food_y = random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 150)
            food = EnemyFactory.create(food_type, SCREEN_WIDTH + 50, food_y, self.enemy_bullet_group)
            self.enemy_group.add(food)
            self.enemy_generator_time = now
            self.enemy_generator_delay = random.randint(*self.config["enemy_delay"])

    def check_for_collisions(self):
        ship = self.spaceship_group.sprite
        
        # 湯匙只能射擊Boss，不能射擊美食
        for bullet in getattr(ship, "bullet_group", []):
            # 移除子彈射擊美食的功能
            # foods_hit = pygame.sprite.spritecollide(bullet, self.enemy_group, True)
            # for food in foods_hit:
            #     # 不再加分數，而是加彈藥
            #     ship.add_ammo(food.value)
            #     bullet.kill()
            #     self.animation_group.add(Explosion(food.rect.centerx, food.rect.centery, 40))

            # Boss碰撞 - 湯匙可以射擊Boss
            bosses_hit = pygame.sprite.spritecollide(bullet, self.boss_group, False)
            for boss in bosses_hit:
                boss.hp -= bullet.damage
                bullet.kill()
                self.animation_group.add(
                    Explosion(boss.rect.centerx + random.randint(-60, 60),
                              boss.rect.centery + random.randint(-60, 60), 150)
                )

        # 玩家直接碰觸美食獲得湯匙（唯一獲得湯匙的方式）
        foods_collected = pygame.sprite.spritecollide(ship, self.enemy_group, True)
        for food in foods_collected:
            ship.add_ammo(food.value)  # 根據美食類型增加湯匙
            self.animation_group.add(Explosion(food.rect.centerx, food.rect.centery, 40))

        # Boss碰撞 - 撞到汽車直接遊戲結束
        if self.boss_group.sprite:
            if pygame.sprite.spritecollide(ship, self.boss_group, False):
                ship.lives = 0  # 直接死亡
                self.animation_group.add(Explosion(ship.rect.centerx, ship.rect.centery, 100))

        # Power道具收集（如果還有的話）
        for power in self.power_group.sprites():
            if pygame.sprite.spritecollide(power, self.spaceship_group, False):
                ship.apply_power(power)
                if power.type == "heal":
                    self.animation_group.add(Heal(ship.rect.centerx, ship.rect.centery, 100))
                power.kill()

    def check_for_state(self):
        ship = self.spaceship_group.sprite
        if ship.lives <= 0:
            self.game_over()

        boss = self.boss_group.sprite
        if boss and boss.hp <= 0:
            # 打敗汽車就過關，不再需要分數
            boss.kill()
            self.game_pass()

    def boss_appear(self):
        if self.game_time >= self.boss_time and not self.boss_group.sprite:
            # 只使用 Boss1
            boss_y = SCREEN_HEIGHT - 160  # 調高一點讓玩家能射到
            new_boss = boss.Boss1(SCREEN_WIDTH + 100, boss_y)
            self.boss_group.add(new_boss)
            # 移除除錯訊息
            # print(f"Boss appearing at time: {self.game_time}, boss_time: {self.boss_time}")
            # print(f"Boss created at position: ({SCREEN_WIDTH + 100}, {boss_y})")

    # ------------------ 控制方法 ------------------
    def reset(self):
        self.run = True
        self.wait = False
        self.is_pass = False
        self.spaceship_group.sprite.reset()
        self.enemy_group.empty()
        self.enemy_bullet_group.empty()
        self.boss_group.empty()
        self.animation_group.empty()
        self.power_group.empty()
        self.money = 0
        self.start_time = pygame.time.get_ticks()

    def game_over(self):
        self.run = False
        self.wait = True
        self.user.money += self.money

    def game_pass(self):
        self.run = False
        self.wait = True
        self.is_pass = True
        self.user.money += self.money
        self.user.level_up()

    def play_BGM(self):
        pygame.mixer.init()
        pygame.mixer.music.load("Sound/bg_music.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)