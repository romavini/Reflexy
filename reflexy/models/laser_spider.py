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
    SPIDER_EYE_X,
    SPIDER_EYE_Y,
    COOLDOWN_FIRE,
    FREEZE_TIME,
)
from reflexy.models.ray import Ray


class LaserSpider(pygame.sprite.Sprite):
    def __init__(self, time):
        pygame.sprite.Sprite.__init__(self)

        self.time = time

        self.images = [self.get_surface(filename) for filename in ("laser-spider.png",)]
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.spawn_spider()
        self.eye_aim = (self.rect[0], self.rect[1])

        self.firing = False
        self.cooldown_fire = True
        self.cd_tracker = self.time
        self.cd_init_fire = None
        self.ray = None

    def aim(self, player_center_coordenates):
        x_aim = int(self.eye_aim[0] + SPIDER_EYE_X - player_center_coordenates[0])
        y_aim = int(self.eye_aim[1] + SPIDER_EYE_Y - player_center_coordenates[1])
        self.aim_angle_rad = math.atan2(y_aim, -x_aim)

    def update(self, screen, player_center_coordenates, time):
        self.time = time

        self.eye_aim = (self.rect[0], self.rect[1])

        self.aim(player_center_coordenates)

        if self.firing:
            if not self.cd_init_fire:
                self.call_ray(screen)
                self.cd_init_fire = self.time

            elif self.time - self.cd_init_fire < FREEZE_TIME:
                self.ray.next_sprite(screen)

            else:
                self.firing = False
                self.cd_tracker = self.time
                self.cd_init_fire = None
                self.ray.kill()
                self.ray = None

        else:
            self.move_spider()

        if not self.firing and self.time - self.cd_tracker > COOLDOWN_FIRE:
            self.firing = True

    def move_spider(self):
        self.rect[0] += round(math.cos(self.aim_angle_rad) * SPIDER_SPEED)
        self.rect[1] -= round(math.sin(self.aim_angle_rad) * SPIDER_SPEED)

    def call_ray(self, screen):
        self.ray = Ray(
            screen,
            self.eye_aim,
            math.degrees(self.aim_angle_rad),
            (SPIDER_EYE_X, SPIDER_EYE_Y),
        )

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
