from typing import Sequence

import pygame  # type: ignore
from reflexy.constants import RAY_ANIMATION_TIME, RAY_HEIGHT, RAY_ORIGIN_X, RAY_WIDTH
from reflexy.helpers.general_helpers import draw_box, get_surface


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
