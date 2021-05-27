import pygame
import math
from typing import Optional, Sequence
from reflexy.helpers import (
    get_surface,
    get_image_path,
)
from reflexy.constants import (
    RAY_WIDTH,
    RAY_HEIGHT,
    RAY_ORIGIN_X,
    RAY_ANIMATION_TIME,
)


class Ray(pygame.sprite.Sprite):
    def __init__(
        self,
        screen: pygame.Surface,
        correct_spider_eye: Sequence[int],
        aim_angle: float,
        eye_position: Sequence[int],
    ):
        pygame.sprite.Sprite.__init__(self)

        self.current_angle = aim_angle
        self.correct_spider_eye = correct_spider_eye
        self.eye_position = eye_position

        self.images = [
            get_surface(filename, angle=self.current_angle)
            for filename in (
                [
                    "ray-0.png",
                    "ray-1.png",
                    "ray-2.png",
                    "ray-3.png",
                    "ray-4.png",
                    "ray-5.png",
                    "ray-6.png",
                    "ray-7.png",
                    "ray-6.png",
                    "ray-7.png",
                    "ray-6.png",
                    "ray-7.png",
                    "ray-6.png",
                    "ray-7.png",
                ]
            )
        ]
        self.gradent_animate = len(self.images) / (RAY_ANIMATION_TIME * 20)
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.correct_ray_to_eye()
        self.origin_position: Sequence[int] = (self.rect[0], self.rect[1])

    def correct_ray_to_eye(self):
        """Adjust the laser into the spider."""
        size_ray_ratated = pygame.Surface.get_size(self.image)
        B = abs(math.sin(math.radians(-self.current_angle))) * RAY_HEIGHT
        h = math.sqrt((RAY_HEIGHT) ** 2 - (B) ** 2) / 2

        if self.current_angle >= 90:
            x = int(
                self.correct_spider_eye[0]
                - size_ray_ratated[0]
                + B / 2
                - math.cos(math.radians(self.current_angle)) * RAY_ORIGIN_X
                + self.eye_position[0]
            )
            y = int(
                self.correct_spider_eye[1]
                - size_ray_ratated[1]
                + h
                + math.sin(math.radians(self.current_angle)) * RAY_ORIGIN_X
                + self.eye_position[1]
            )
        elif self.current_angle > 0:
            x = int(
                self.correct_spider_eye[0]
                - B / 2
                - math.cos(math.radians(self.current_angle)) * RAY_ORIGIN_X
                + self.eye_position[0]
            )
            y = int(
                self.correct_spider_eye[1]
                - size_ray_ratated[1]
                + h
                + math.sin(math.radians(self.current_angle)) * RAY_ORIGIN_X
                + self.eye_position[1]
            )
        elif self.current_angle <= -90:
            x = int(
                self.correct_spider_eye[0]
                - size_ray_ratated[0]
                + B / 2
                - math.cos(math.radians(self.current_angle)) * RAY_ORIGIN_X
                + self.eye_position[0]
            )
            y = int(
                self.correct_spider_eye[1]
                - h
                - math.sin(math.radians(-self.current_angle)) * RAY_ORIGIN_X
                + self.eye_position[1]
            )
        else:
            x = int(
                self.correct_spider_eye[0]
                - B / 2
                - math.cos(math.radians(self.current_angle)) * RAY_ORIGIN_X
                + self.eye_position[0]
            )
            y = int(
                self.correct_spider_eye[1]
                - h
                - math.sin(math.radians(-self.current_angle)) * RAY_ORIGIN_X
                + self.eye_position[1]
            )

        self.rect = pygame.Rect(x, y, RAY_WIDTH, RAY_HEIGHT)

    def next_sprite(
        self, screen: pygame.Surface, x_correction: float, y_correction: float
    ):
        """Animate laser.

        Keyword arguments:
        screen -- surface to print
        x_correction -- x coordinade of spider eye
        y_correction -- y coordinade of spider eye
        """
        self.rect = pygame.Rect(
            self.origin_position[0] + x_correction,
            self.origin_position[1] + y_correction,
            RAY_WIDTH,
            RAY_HEIGHT,
        )
        self.current_image += self.gradent_animate

        if self.current_image >= len(self.images) - 1:
            self.current_image = len(self.images) - 1

        self.image = self.images[int(self.current_image)]
