import os
import pygame
import math


def get_image_path(filename: str, folder: str = "../images") -> str:
    """Return the path of a image.

    Keyword arguments:
    filename -- name of image
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), folder, filename))


def create_pygame_font(
    name: str = "Comic Sans", size: int = 18, bold: bool = False
) -> pygame.font.Font:
    """Return a font.

    Keyword arguments:
    size -- size of the image (defalt 18)
    name -- name of the font (defalt "Comic Sans")
    bold -- bold of the font (defalt False)
    """
    return pygame.font.SysFont(name, size, bold)


def calc_acceleration(func, time, tracker, acceleration) -> float:
    """Calculate the acceleration.

    Keyword arguments:
    func -- acceleration function (defalt "lin")
    time -- duration of the acceleration
    tracker -- current time
    acceleration -- current acceleration
    """
    if not isinstance(func, str):
        raise TypeError(
            "Acceleration funtion must be a string. Options: 'log', 'lin' and 'exp'."
        )

    if not (
        (isinstance(time, float) or isinstance(time, int))
        and (isinstance(tracker, float) or isinstance(tracker, int))
        and (isinstance(acceleration, float) or isinstance(acceleration, int))
    ):
        raise TypeError("Acceleration time must be a number.")

    if func not in ["log", "lin", "exp"]:
        raise ValueError("Acceleration funtions: 'log', 'lin' and 'exp'.")

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
