import math
from typing import Sequence

import pygame  # type: ignore
from reflexy.constants import RAY_ANIMATION_TIME, RAY_HEIGHT, RAY_ORIGIN_X, RAY_WIDTH
from reflexy.helpers.general_helpers import draw_box, get_surface


class Ray(pygame.sprite.Sprite):
    def __init__(
        self,
        screen,
        correct_spider_eye,
        aim_angle,
        eye_position,
        id,
        show_vision: bool = True,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.show_vision = show_vision
        self.current_angle = aim_angle
        self.correct_spider_eye = correct_spider_eye
        self.eye_position = eye_position
        self.id = id

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
        self.gradient_animate = len(self.images) / (RAY_ANIMATION_TIME * 20)
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.correct_ray_to_eye()
        self.origin_position: Sequence[int] = (self.rect[0], self.rect[1])

        self.hit_box = [self.hit_line()]
        if self.show_vision:
            draw_box(screen, self)

    def next_sprite(self, screen, x_correction, y_correction):
        self.rect = pygame.Rect(
            self.origin_position[0] + x_correction,
            self.origin_position[1] + y_correction,
            RAY_WIDTH,
            RAY_HEIGHT,
        )
        self.hit_box = [self.hit_line()]

        if self.show_vision:
            draw_box(screen, self)

        self.current_image += self.gradient_animate

        if self.current_image >= len(self.images) - 1:
            self.current_image = len(self.images) - 1

        self.image = self.images[int(self.current_image)]

    def hit_line(self):
        point_start = [
            self.correct_spider_eye[0] + self.eye_position[0],
            self.correct_spider_eye[1] + self.eye_position[1],
        ]

        point_end = [
            int(
                point_start[0] + math.cos(math.radians(self.current_angle)) * RAY_WIDTH
            ),
            int(
                point_start[1] - math.sin(math.radians(self.current_angle)) * RAY_WIDTH
            ),
        ]

        return (point_start, point_end)

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
