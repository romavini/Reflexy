import math
import pygame
from reflexy.helpers.general import draw_box, get_surface
from reflexy.constants import (
    RAY_WIDTH,
    RAY_HEIGHT,
    RAY_ORIGIN_X,
    RAY_ANIMATION_TIME,
)
from typing import Sequence


class Sword(pygame.sprite.Sprite):
    def __init__(
        self,
        screen,
        correct_spider_eye,
        aim_angle,
        eye_position,
        id,
        show_vision: bool = True,
    ):
        """"""
        pass

    def next_sprite(self, screen, x_correction, y_correction):
        """"""
        pass

    def hit_line(self):
        """"""
        pass

    def correct_ray_to_eye(self):
        """Adjust the laser into the spider."""
        pass
