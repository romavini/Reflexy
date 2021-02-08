import pygame
import math
import random
from reflexy.helpers import get_image_path
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPIDER_SPEED,
    SPIDER_WIDTH,
    SPIDER_HEIGHT,
    COOLDOWN_FIRE,
    FREEZE_TIME,
)
from reflexy.models.ray import Ray
import time


class LaserSpider(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [self.get_surface(filename) for filename in ("laser-spider.png",)]
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.spawn_spider()

        self.firing = False
        self.cooldown_fire = True
        self.cd_tracker = time.time()
        self.cd_init_fire = None
        self.ray = None

    def rad_to_degree(self, value):
        return value * 180 / math.pi

    def aim(self, self_coordenates, player_coordenates):
        x_aim = int(self_coordenates[0] - player_coordenates[0])
        y_aim = int(self_coordenates[1] - player_coordenates[1])

        self.aim_angle_rad = math.atan2(y_aim, -x_aim)
        self.aim_angle_degree = self.rad_to_degree(self.aim_angle_rad)
        self.direction = (-1 if x_aim >= 0 else 1, -1 if y_aim >= 0 else 1)

    def update(self, screen, player_coordenates):

        self.aim((self.x, self.y), player_coordenates[0:2])

        if self.firing:
            if not self.cd_init_fire:
                self.call_ray(screen)
                self.cd_init_fire = time.time()

            elif time.time() - self.cd_init_fire < FREEZE_TIME:
                self.ray.next_sprite(screen)

            else:
                self.firing = False
                self.cd_tracker = time.time()
                self.cd_init_fire = None
                self.ray = None

        else:
            self.move_spider()

        if not self.firing and time.time() - self.cd_tracker > COOLDOWN_FIRE:
            self.firing = True

    def move_spider(self):
        self.x += self.direction[0] * SPIDER_SPEED
        self.y += self.direction[1] * SPIDER_SPEED

        self.x += SPIDER_SPEED * math.cos(self.aim_angle_degree) * -1
        self.y += SPIDER_SPEED * math.sin(self.aim_angle_degree)

        self.rect = pygame.Rect(self.x, self.y, SPIDER_WIDTH, SPIDER_HEIGHT)

    def call_ray(self, screen):
        self.ray = Ray(screen, self.rect, self.direction, self.aim_angle_degree)

    def spawn_spider(self):
        """spawn the spider sprite in a random position"""
        axis = random.randint(0, 1)
        side = random.randint(0, 1) if axis else random.randint(0, 1)

        if axis:
            if side:
                self.y = random.randint(0, SCREEN_HEIGHT)
                self.x = -SPIDER_WIDTH

            else:
                self.y = random.randint(0, SCREEN_HEIGHT)
                self.x = SCREEN_WIDTH + SPIDER_WIDTH

        else:
            if side:
                self.x = random.randint(0, SCREEN_WIDTH)
                self.y = -SPIDER_HEIGHT

            else:
                self.x = random.randint(0, SCREEN_WIDTH)
                self.y = SCREEN_HEIGHT + SPIDER_HEIGHT

        self.rect = pygame.Rect(self.x, self.y, 128, 64)

    def get_surface(self, filename, angle=0, scale=1):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )
