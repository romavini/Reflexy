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
        self.eye = (self.rect[0] + 35, self.rect[1] + 11)

        self.firing = False
        self.cooldown_fire = True
        self.cd_tracker = time.time()
        self.cd_init_fire = None
        self.ray = None

    def aim(self, self_eye_coordenates, player_center_coordenates):
        x_aim = int(self_eye_coordenates[0] - player_center_coordenates[0])
        y_aim = int(self_eye_coordenates[1] - player_center_coordenates[1])

        self.aim_angle_rad = math.atan2(y_aim, -x_aim)

    def update(self, screen, player_center_coordenates):
        self.eye = (self.rect[0] + 35, self.rect[1] + 11)
        self.aim(self.eye, player_center_coordenates)

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
                self.ray.kill()
                self.ray = None

        else:
            self.move_spider()

        if not self.firing and time.time() - self.cd_tracker > COOLDOWN_FIRE:
            self.firing = True

    def move_spider(self):
        self.rect[0] += SPIDER_SPEED * math.cos(self.aim_angle_rad)
        self.rect[1] -= SPIDER_SPEED * math.sin(self.aim_angle_rad)
        pass

    def call_ray(self, screen):
        self.ray = Ray(screen, self.eye, math.degrees(self.aim_angle_rad))

    def kill_ray(self):
        pass

    def spawn_spider(self):
        """spawn the spider sprite in a random position"""
        axis = random.randint(0, 1)
        side = random.randint(0, 1) if axis else random.randint(0, 1)

        if axis:
            if side:
                y = random.randint(0, SCREEN_HEIGHT)
                x = -SPIDER_WIDTH

            else:
                y = random.randint(0, SCREEN_HEIGHT)
                x = SCREEN_WIDTH

        else:
            if side:
                x = random.randint(0, SCREEN_WIDTH)
                y = -SPIDER_HEIGHT

            else:
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT

        self.rect = pygame.Rect(x, y, 128, 64)

    def get_surface(self, filename, angle=0, scale=1):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )
