import os
from typing import Tuple
import pygame
import math


def get_minor_distance(player_rect, enemy_group):
    p_x, p_y = player_rect

    minor_dist = 100_000_000
    for enemy in enemy_group:
        e_x, e_y = enemy.rect[0:2]
        h_dist = p_x - e_x
        v_dist = p_y - e_y
        if minor_dist > math.sqrt(h_dist ^ 2 + v_dist ^ 2):
            h_minor_dist = h_dist
            v_minor_dist = v_dist
            e_minor_x = e_x
            e_minor_y = e_y

    ang = aim(player_rect, [e_minor_x, e_minor_y])

    return ang, h_minor_dist, v_minor_dist


def aim(center_coord_1, center_coord_2, h_incre=0, v_incre=0):
    """Aim system.

    Keyword arguments:
    center_coord_1 -- sequence of player's center coordinates
    center_coord_2 -- sequence of enemy's center coordinates
    h_incre -- horizontal increment (default 0)
    v_incre -- vertical increment (default 0)
    """
    if center_coord_1 is None or center_coord_2 is None:
        raise TypeError("Missing argument.")
    elif not (
        isinstance(center_coord_1, list) or isinstance(center_coord_1, tuple)
    ):
        raise TypeError(
            f"center_coord_1 must be list or tuple. Got {type(center_coord_1)}."
        )
    elif not (
        isinstance(center_coord_2, list) or isinstance(center_coord_2, tuple)
    ):
        raise TypeError(
            f"center_coord_2 must be list or tuple. Got {type(center_coord_2)}."
        )

    x_aim = int(center_coord_2[0] + h_incre - center_coord_1[0])
    y_aim = int(center_coord_2[1] + v_incre - center_coord_1[1])

    return math.atan2(y_aim, -x_aim)


def get_surface(filename: str, angle: float = 0, scale: float = 1):
    """get surface given image name.

    Keyword arguments:
    filename -- image name
    angle -- angle to rotate, in degrees (default 0)
    scale -- factor to zoom (default 1)
    """
    if not filename:
        raise TypeError("Missing filename argument.")

    elif not isinstance(filename, str):
        raise TypeError(f"Image name must be a string. Got {type(filename)}.")

    elif not (isinstance(angle, float) or isinstance(angle, int)):
        raise TypeError(
            f"Angle must be an float or integer. Got {type(angle)}."
        )

    elif not (isinstance(scale, float) or isinstance(scale, int)):
        raise TypeError(
            f"Scale must be an float or integer. Got {type(scale)}."
        )

    return pygame.transform.rotozoom(
        pygame.image.load(get_image_path(filename)).convert_alpha(),
        angle,
        scale,
    )


def get_image_path(filename: str, folder: str = "../images") -> str:
    """Return the path of a image.

    Keyword arguments:
    filename -- name of image
    """
    if not filename:
        raise TypeError("Missing filename argument.")

    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), folder, filename)
    )


def create_pygame_font(
    name: str = "Comic Sans", size: int = 18, bold: bool = False
) -> pygame.font.Font:
    """Return a font.

    Keyword arguments:
    size -- size of the image (defalt 18)
    name -- name of the font (defalt "Comic Sans")
    bold -- bold of the font (defalt False)
    """
    if not isinstance(name, str):
        raise TypeError(f"Font name must be a string. Got {type(name)}.")
    if not isinstance(size, int):
        raise TypeError(f"Font size must be an integer. Got {type(size)}.")
    return pygame.font.SysFont(name, size, bold)


def create_text(
    runner,
    text: str,
    pos_center: Tuple[int, int],
):
    """Create a surface text in the window.

    Keyword arguments:
    runner -- Runner class
    text -- text to be printed
    pos_center -- tuple with the center position
    """
    if text is None:
        raise TypeError("Missing text argument.")
    elif not isinstance(text, str):
        raise TypeError(f"text must be a string. Got {type(text)}.")

    text_render = runner.text.render(text, True, (255, 255, 255))
    textRect = text_render.get_rect()
    textRect.center = pos_center

    runner.screen.blit(text_render, textRect)


def calc_acceleration(
    func_acc: str, time: float, tracker: float, acceleration: float
) -> float:
    """Calculate the acceleration.

    Keyword arguments:
    func_acc -- acceleration function (defalt "lin")
    time -- duration of the acceleration
    tracker -- current time
    acceleration -- current acceleration
    """
    if not isinstance(func_acc, str):
        raise TypeError(
            f"Acceleration function must be a string. Options: 'log', 'lin' and 'exp'. Got {type(func_acc)}."
        )

    if not (
        (isinstance(time, float) or isinstance(time, int))
        and (isinstance(tracker, float) or isinstance(tracker, int))
        and (isinstance(acceleration, float) or isinstance(acceleration, int))
    ):
        raise TypeError(
            f"Acceleration values must be numbers. Got time:{type(time)}, tracker:{type(tracker)} and acceleration:{type(acceleration)}."
        )

    if func_acc not in ["log", "lin", "exp"]:
        raise ValueError(
            f"Acceleration functions: 'log', 'lin' and 'exp'. Got '{func_acc}'."
        )

    elif func_acc == "log":
        if not (time - tracker):
            return 0

        log = math.log10(1 / acceleration * (time - tracker))
        if log < 0:
            return 0

        return (log + 2) / 2

    elif func_acc == "lin":
        return 1 / acceleration * (time - tracker)

    elif func_acc == "exp":
        return 2 ** (1 / acceleration * (time - tracker)) - 1

    else:
        return 0
