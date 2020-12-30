import pygame
from reflexy.helpers import get_image_path
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [self.get_surface(filename) for filename in ("player",)]

        self.current_image = 0
        self.image = self.images[self.current_image]

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

        # self.score = 0
        # self.life = 3

        self.direction = "down"

    def update(self):
        pass

    def down(self):
        self.rect[1] += PLAYER_SPEED
        self.direction = "down"

    def up(self):
        self.rect[1] -= PLAYER_SPEED
        self.direction = "up"

    def left(self):
        self.rect[0] -= PLAYER_SPEED
        self.direction = "left"

    def right(self):
        self.rect[0] += PLAYER_SPEED
        self.direction = "right"

    def get_surface(self, filename, direction="down", angle=0, scale=1):
        return pygame.transform.rotozoom(
            pygame.image.load(
                get_image_path(f"{filename}-{direction}.png")
            ).convert_alpha(),
            angle,
            scale,
        )
