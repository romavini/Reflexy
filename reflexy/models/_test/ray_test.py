import pytest
import pygame
from reflexy.models.ray import Ray


def test_init():
    with pytest.raises(TypeError):
        ray = Ray()


def test_next_sprite():
    ray = Ray(
        screen=pygame.display.set_mode((1, 1)),
        correct_spider_eye=[0, 0],
        aim_angle=0,
        eye_position=[0, 0],
    )
    with pytest.raises(TypeError):
        ray.next_sprite()
