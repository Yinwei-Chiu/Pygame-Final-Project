import pygame
import random
from Config import *


# 載入Boss汽車圖片
Boss_dict= {
    1:{ "pic_path" :"image/boss_chair.png", "hp":50,"speed":-5,"size":(72, 72)},
    2:{ "pic_path" :"image/boss_scooter.png", "hp":60,"speed":-6,"size":(72, 72)},
    3:{ "pic_path" :"image/boss_car.png", "hp":100,"speed":-10,"size":(100,60)}
}


class Boss(pygame.sprite.Sprite):
    def __init__(self, level, x, y, existing_hp=None):
        super().__init__()
        self.level = level
        self.x = x
        self.y = y

        boss_image = pygame.image.load(Boss_dict[level]["pic_path"])
        boss_car_image = pygame.transform.scale(boss_image, Boss_dict[level]["size"])
        self.image = boss_car_image
        self.hp_max = Boss_dict[level]["hp"]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speedx = Boss_dict[level]["speed"]  # 快速往左衝
        self.value = 10000  # 通關獎勵
        
        # 血量管理
        if existing_hp is not None:
            self.hp = existing_hp
        else:
            self.hp = self.hp_max
        
        # 固定在地面上的Y座標 - 與玩家摩托車同高度
        self.ground_y = SCREEN_HEIGHT - 150  # 改為與玩家相同的高度
        
        # 重新刷新計時器
        self.respawn_timer = 0
        self.respawn_delay = random.randint(4000, 7000)  # 隨機4-7秒重新刷新
        self.is_respawning = False
        
        # 無敵時間系統
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_duration = 3000  # 3秒無敵時間
        
        # 閃爍效果（無敵時）
        self.blink_time = 0
        self.blink_delay = 150  # 閃爍間隔
        self.visible = True

    def take_stomp_damage(self, damage):
        """受到踩車傷害"""
        if not self.invincible:
            self.hp -= damage
            self.start_invincible()
            return True
        return False

    def take_bullet_damage(self, damage):
        """受到湯匙傷害"""
        self.hp -= damage
        return True

    def start_invincible(self):
        """開始無敵時間"""
        self.invincible = True
        self.invincible_start_time = pygame.time.get_ticks()

    def update_invincible(self):
        """更新無敵狀態"""
        if self.invincible:
            now = pygame.time.get_ticks()
            # 檢查無敵時間是否結束
            if now - self.invincible_start_time >= self.invincible_duration:
                self.invincible = False
                self.visible = True  # 確保結束時可見
            else:
                # 無敵時閃爍效果
                if now - self.blink_time > self.blink_delay:
                    self.visible = not self.visible
                    self.blink_time = now

    def constrain_movement(self):
        # 保持在地面上，不允許上下移動
        self.rect.centery = self.ground_y
        
        # 如果汽車完全離開畫面左側，標記為需要重新刷新
        if self.rect.right < 0:
            if not self.is_respawning:
                self.is_respawning = True
                self.respawn_timer = pygame.time.get_ticks()
                # 每次離開畫面時重新設定隨機刷新時間
                self.respawn_delay = random.randint(4000, 7000)
            return True  # 返回True表示需要重新刷新
        return False

    def should_respawn(self):
        """檢查是否應該重新刷新"""
        if self.is_respawning:
            now = pygame.time.get_ticks()
            if now - self.respawn_timer >= self.respawn_delay:
                return True
        return False

    def update(self):
        # 只有水平移動
        self.rect.x += self.speedx
        need_respawn = self.constrain_movement()
        self.update_invincible()  # 更新無敵狀態
        return need_respawn  # 返回是否需要重新刷新

    def draw_hp(self, surface):
        hp_width = self.rect.width * (self.hp / self.hp_max)
        
        # 只有在可見時才繪製（配合閃爍效果）
        if self.visible:
            # HP條背景
            pygame.draw.rect(surface, WHITE, (self.rect.x, self.rect.y - 25, self.rect.width, 15), 2)
            # HP條
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 25, hp_width, 15))
            
            # HP文字
            font = pygame.font.Font(None, 24)
            hp_text = font.render(f"Boss HP: {self.hp}/{self.hp_max}", True, WHITE)
            surface.blit(hp_text, (self.rect.x, self.rect.y - 50))
            
            # 無敵狀態提示
            if self.invincible:
                invincible_text = font.render("INVINCIBLE", True, YELLOW)
                surface.blit(invincible_text, (self.rect.x, self.rect.y - 75))