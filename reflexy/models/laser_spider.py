import pygame
import math
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

        self.images = [self.get_surface(filename) for filename in ("laser-spider.png",)]
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.x = 50
        self.y = 50
        self.rect = pygame.Rect(self.x, self.y, 128, 64)

        self.firing = False
        self.cooldown_fire = True
        self.cd_tracker = time.time()
        self.cd_init_fire = None
        self.bullet = None

    def rad_to_degree(self, value):
        return value * 180 / math.pi

    def aim(self, self_coordenates, player_coordenates):
        x = self_coordenates[0] - player_coordenates[0]
        y = self_coordenates[1] - player_coordenates[1]

        self.aim_angle = self.rad_to_degree(math.atan2(y, -x))
        self.direction = (-1 if x >= 0 else 1, -1 if y >= 0 else 1)

    def update(self, screen, player_coordenates):

        self.aim((self.x, self.y), player_coordenates[0:2])

        if self.firing:
            if not self.cd_init_fire:
                self.call_bullet(screen)
                self.cd_init_fire = time.time()

            elif time.time() - self.cd_init_fire < FREEZE_TIME:
                self.bullet.next_sprite(screen)

            else:
                self.firing = False
                self.cd_tracker = time.time()
                self.cd_init_fire = None
                self.bullet = None

        else:
            self.x += self.direction[0] * SPIDER_SPEED
            self.y += self.direction[1] * SPIDER_SPEED
            self.rect = pygame.Rect(self.x, self.y, 128, 64)

        if not self.firing and time.time() - self.cd_tracker > COOLDOWN_FIRE:
            self.firing = True

    def call_bullet(self, screen):
        self.bullet = Bullet(screen, self.rect, self.direction, self.aim_angle)

    def get_surface(self, filename, angle=0, scale=1):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )
