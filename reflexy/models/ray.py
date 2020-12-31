import pygame
from pygame.math import Vector2
from reflexy.helpers import get_image_path
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)


class Ray(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.is_animating = False

        self.images = [
            self.get_surface(filename)
            for filename in ("ray-0.png", "ray-1.png", "ray-2.png", "ray-3.png")
        ]
        
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.rect = self.image.get_rect(center = (11, 18))  

    def shot(self):
        self.is_animating = True

    def rotatePivoted(self, angle):
        self.image = pygame.transform.rotate(
            self.images[int(self.current_image)], angle
        )
        print(self.image, angle)

    def update(self, enemy_center, aim):
        self.rect[0] = enemy_center[0]
        self.rect[1] = enemy_center[1] - 9
        
        self.rotatePivoted(aim)

        if self.is_animating == True:
            self.current_image += 0.25

            if self.current_image >= len(self.images):
                self.current_image = 0
                self.is_animating = False

            self.image = self.images[int(self.current_image)]

    def get_surface(self, filename, angle=0, scale=1):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )
