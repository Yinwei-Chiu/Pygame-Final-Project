import pygame


explosion_animation = []
for i in range(9):
    explosion_image = pygame.image.load(f"Image/animation/explosion/expl{i}.png")
    explosion_animation.append(explosion_image)

heal_animation = []
for i in range(4):
    heal_image = pygame.image.load(f"Image/animation/heal/heal{i}.png")
    heal_animation.append(heal_image)


class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, size, animations, delay, sound_path):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.animation = [pygame.transform.scale(frame, (size, size)) for frame in animations]
        self.image = self.animation[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame = 0
        self.animation_time = 0
        self.animation_delay = delay
        self.sound = pygame.mixer.Sound(sound_path)

    def update(self):
        if self.frame == 0:
            self.sound.play()

        now = pygame.time.get_ticks()
        if now - self.animation_time > self.animation_delay:
            self.frame += 1
            self.animation_time = now
            if self.frame >= len(self.animation):
                self.kill()
            else:
                self.image = self.animation[self.frame]


class Explosion(Animation):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, explosion_animation, 50, "Sound/explosion.mp3")

class Heal(Animation):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, heal_animation, 100, "Sound/heal.mp3")


                
