import pygame
from helpers import get_image_path
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPIDER_SPEED,
    COOLDOWN_FIRE,
    FREEZE_TIME,
)
from models.bullet import Bullet
import time


class LaserSpider(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [
            self.get_surface(filename)
            for filename in ("laser-spider.png",)
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.x = 50
        self.y = 50
        self.rect = pygame.Rect(self.x, self.y, 128, 64)

        self.firing = False
        self.cooldown_fire = True
        self.cd_tracker = time.time()
        self.cd_init_fire = time.time()

    def update(self, screen):
        if self.firing == False:
            self.x += SPIDER_SPEED
            self.y += SPIDER_SPEED
            self.rect = pygame.Rect(self.x, self.y, 128, 64)

        if self.cooldown_fire == True:
            self.cd_tracker = time.time()

        else:
            self.cd_init_fire = self.cd_tracker
            self.call_bullet(screen)

        if self.cd_tracker - self.cd_init_fire > FREEZE_TIME:
            # Freeze
            self.firing = False

        if self.cd_tracker - self.cd_init_fire > COOLDOWN_FIRE:
            # Fire!
            self.firing = True
            self.cd_init_fire = time.time()
            self.cooldown_fire = True

        # return screen

    def call_bullet(self, screen):
        bullet = Bullet(screen, self.x, self.y)
        

    def fire(self, cooldown_fire):
        if cooldown_fire == False:
            self.bullet = Bullet()

    def get_surface(self, filename, angle=0, scale=1):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )
    

