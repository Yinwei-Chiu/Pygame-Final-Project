import pygame
from Config import *


class Progress():
    def __init__(self, x, y, time, boss_time):
        self.x = x
        self.y = y
        self.time = time
        self.boss_time = boss_time


    def update(self, time):
        self.time = time
        if self.time >= self.boss_time:
            self.time = self.boss_time


    def draw(self, surface):
        bar_height = 150
        time = bar_height*(self.time/self.boss_time)
        pygame.draw.rect(surface, YELLOW, (self.x, self.y, 15, bar_height), 0)
        pygame.draw.rect(surface, WHITE, (self.x, self.y, 15, bar_height-time), 0)
        pygame.draw.rect(surface, WHITE, (self.x, self.y, 15, bar_height), 2)

