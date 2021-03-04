import os
import pygame
import math


def get_image_path(filename):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "images", filename)
    )


def create_pygame_font(size=18, name="Comic Sans", bold=False):
    return pygame.font.SysFont(name, size, bold)


def calc_acceleration(func, time, tracker, acceleration):
    if func == "log":
        if not (time - tracker):
            return 0

        log = math.log10(1 / acceleration * (time - tracker))

        if log < 0:
            return 0

        return (log + 2) / 2

    if func == "lin":
        return 1 / acceleration * (time - tracker)

    if func == "exp":
        return 2 ** (1 / acceleration * (time - tracker)) - 1
