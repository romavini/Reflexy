import pygame
import random
from reflexy.helpers import get_image_path
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPIDER_SPEED,
)


class LaserSider(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [self.get_surface(filename) for filename in ("laser-spider.png",)]

        self.current_image = 0
        self.image = self.images[self.current_image]

        self.rect = self.image.get_rect()
        self.pos = self.rect.center
        
        self.eye_pos = [0, 0]
        self.eye_pos[0] = self.rect.center[0]
        self.eye_pos[1] = self.rect.center[1] - 9

        self.rect[0] = random.randint(0, SCREEN_WIDTH - self.rect[2])
        self.rect[1] = random.randint(0, SCREEN_HEIGHT - self.rect[3])

    def update(self):
        self.rect[0] += 0
        self.rect[1] += 0

    def get_surface(self, filename, angle=0, scale=1):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )
