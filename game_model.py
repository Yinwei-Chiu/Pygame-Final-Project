import pygame
import random
from Config import *
from LevelConfig import LEVELS
from background import Background
from player import Player
from food_factory import FoodFactory
from animation import Explosion
from progress import Progress
from spoon import SpoonItem
import boss



class GameModel:
    def __init__(self, user):
        self.user = user
        self.level = user.level
        self.config = LEVELS[user.level]

        self.background = Background(self.config["background"], 1)
        self.player_group = pygame.sprite.GroupSingle(Player())
        self.food_group = pygame.sprite.Group()
        self.animation_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.GroupSingle()
        self.spoon_group = pygame.sprite.Group()  # 湯匙道具群組

        self.food_generator_time = 0
        self.food_generator_delay = random.randint(*self.config["enemy_delay"])

        self.run = False
        self.wait = False
        self.is_pass = False

        self.money = 0
        self.game_time = 0
        self.start_time = pygame.time.get_ticks()
        self.boss_time = self.config["boss_time"]
        self.progress = Progress(SCREEN_WIDTH - 50, 60, self.game_time, self.boss_time)

    def update(self):
        self.background.update()
        self.player_group.update()
        self.food_group.update()
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
                boss_y = SCREEN_HEIGHT - 150  # 與玩家摩托車同高度
                new_boss = boss.Boss(SCREEN_WIDTH + 150, boss_y, current_hp)
                self.boss_group.add(new_boss)
        
        self.spoon_group.update()

        self.game_time = pygame.time.get_ticks() - self.start_time if self.start_time > 0 else 0
        self.progress.update(self.game_time)

        self.food_generator()
        self.check_for_collisions()
        self.check_for_state()
        self.boss_appear()

    def food_generator(self):
        now = pygame.time.get_ticks()
        if now - self.food_generator_time > self.food_generator_delay:
            # 75% 機率生成美食，25% 機率生成湯匙道具
            if random.random() < 0.75:
                # 生成美食 - 從右側進入
                food_type = random.choice(self.config["enemies"])
                food_y = random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 150)
                food = FoodFactory.create(food_type, SCREEN_WIDTH + 50, food_y)
                self.food_group.add(food)
            else:
                # 生成湯匙道具 - 從畫面上緣隨機位置掉落
                spoon_x = random.randint(50, SCREEN_WIDTH - 50)
                spoon_y = -50
                spoon = SpoonItem(spoon_x, spoon_y)
                self.spoon_group.add(spoon)
                
            self.food_generator_time = now
            self.food_generator_delay = random.randint(*self.config["enemy_delay"])

    def check_for_collisions(self):
        player = self.player_group.sprite
        
        # 湯匙射擊Boss
        for bullet in player.bullet_group:
            # Boss碰撞 - 湯匙可以射擊Boss
            bosses_hit = pygame.sprite.spritecollide(bullet, self.boss_group, False)
            for boss in bosses_hit:
                boss.take_bullet_damage(bullet.damage)
                bullet.kill()
                self.animation_group.add(
                    Explosion(boss.rect.centerx + random.randint(-60, 60),
                              boss.rect.centery + random.randint(-60, 60), 150)
                )
            for bullet in player.bullet_group:
                # 筷子吃東西
                food_hit = pygame.sprite.spritecollide(bullet, self.food_group, False)
                for food in food_hit:
                    player.eat_food(food.hunger)
                    food.kill()
                    bullet.kill()
                    self.animation_group.add(
                        Explosion(food.rect.centerx + random.randint(-60, 60),
                                food.rect.centery + random.randint(-60, 60), 150)
                    )
        # 玩家直接碰觸美食 - 吃食物恢復飢餓度
        foods_collected = pygame.sprite.spritecollide(player, self.food_group, True)
        for food in foods_collected:
            player.eat_food(food.hunger)
            self.animation_group.add(Explosion(food.rect.centerx, food.rect.centery, 40))

        # Boss碰撞檢測 - 在地面=死亡，跳躍=踩車
        if self.boss_group.sprite:
            boss = self.boss_group.sprite
            boss_collision = pygame.sprite.spritecollide(player, self.boss_group, False)
            
            if boss_collision:
                if player.is_jumping:
                    # 跳躍中碰撞 = 踩車
                    if player.is_stomping:
                        damage = player.stomp_damage  # 15點全傷害
                        effect_size = 200
                    else:
                        damage = player.stomp_damage // 2  # 7點半傷害
                        effect_size = 150
                    
                    # 嘗試造成踩車傷害
                    if boss.take_stomp_damage(damage):
                        player.is_stomping = False
                        # 踩車特效
                        self.animation_group.add(
                            Explosion(boss.rect.centerx, boss.rect.top - 20, effect_size)
                        )
                        
                        # 立即彈跳，避免落地判定
                        player.velocity_y = -18
                        player.is_jumping = True
                        
                        # 開始踩車冷卻時間
                        player.start_stomp_cooldown()
                        
                        # 將玩家稍微推離Boss，避免重複碰撞
                        if player.rect.centerx < boss.rect.centerx:
                            player.rect.x = boss.rect.left - player.rect.width - 5
                        else:
                            player.rect.x = boss.rect.right + 5
                        
                else:
                    # 在地面碰撞 = 死亡
                    player.lives = 0
                    self.animation_group.add(Explosion(player.rect.centerx, player.rect.centery, 100))

        # 玩家收集湯匙道具
        spoons_collected = pygame.sprite.spritecollide(player, self.spoon_group, True)
        for spoon in spoons_collected:
            player.add_ammo(spoon.value)
            self.animation_group.add(Explosion(spoon.rect.centerx, spoon.rect.centery, 30))

    def check_for_state(self):
        player = self.player_group.sprite
        if player.lives <= 0:
            self.game_over()

        boss = self.boss_group.sprite
        if boss and boss.hp <= 0:
            boss.kill()
            self.game_pass()

    def boss_appear(self):
        if self.game_time >= self.boss_time and not self.boss_group.sprite:
            boss_y = SCREEN_HEIGHT - 150  # 與玩家摩托車同高度
            new_boss = boss.Boss(SCREEN_WIDTH + 100, boss_y)
            self.boss_group.add(new_boss)

    def reset(self):
        self.run = True
        self.wait = False
        self.is_pass = False
        self.player_group.sprite.reset()
        self.food_group.empty()
        self.boss_group.empty()
        self.animation_group.empty()
        self.spoon_group.empty()
        self.money = 0
        self.start_time = pygame.time.get_ticks()

    def game_over(self):
        self.run = False
        self.wait = True
        self.finish_time = self.game_time
        self.user.money += self.money

    def game_pass(self):
        self.run = False
        self.wait = True
        self.is_pass = True
        self.finish_time = self.game_time
        # 更新最佳紀錄
        if self.user.best_time == 0 or self.game_time < self.user.best_time:
            self.user.best_time = self.game_time
        self.user.money += self.money

    def play_BGM(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("Sound/bg_music.mp3")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
        except:
            pass  # 如果音樂檔案不存在，就靜默處理