import os
import pygame


def get_image_path(filename):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "images", filename)
    )


def create_pygame_font(size=18, name="Comic Sans", bold=False):
    return pygame.font.SysFont(name, size, bold)
