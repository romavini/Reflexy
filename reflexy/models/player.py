import pygame
from helpers import get_image_path
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = self.get_surface("player-down.png")
        self.x = SCREEN_WIDTH / 2 - 100
        self.y = SCREEN_HEIGHT / 2 - 50

        self.rect = pygame.Rect(self.x, self.y, 128, 64)
        
        self.mouse = pygame.mouse.get_pos()
        self.hp = 3

        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

    def update(self):
        if self.moveDown and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.top += PLAYER_SPEED
        if self.moveUp and self.rect.top > 0:
            self.rect.top -= PLAYER_SPEED
        if self.moveLeft and self.rect.left > 0:
            self.rect.left -= PLAYER_SPEED
        if self.moveRight and self.rect.right < SCREEN_WIDTH:
            self.rect.right += PLAYER_SPEED


    def get_surface(self, filename, angle=0, scale=1):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )
