import os

import numpy as np
from reflexy.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from typing import Tuple
import pygame
import math


def intersect_hit_box(segment_a, hit_box) -> bool:
    for [
        box_start_side_point,
        box_end_side_point,
    ] in hit_box:
        dx0 = segment_a[1][0] - segment_a[0][0]
        dx1 = box_end_side_point[0] - box_start_side_point[0]
        dy0 = segment_a[1][1] - segment_a[0][1]
        dy1 = box_end_side_point[1] - box_start_side_point[1]
        p0 = dy1 * (box_end_side_point[0] - segment_a[0][0]) - dx1 * (
            box_end_side_point[1] - segment_a[0][1]
        )
        p1 = dy1 * (box_end_side_point[0] - segment_a[1][0]) - dx1 * (
            box_end_side_point[1] - segment_a[1][1]
        )
        p2 = dy0 * (segment_a[1][0] - box_start_side_point[0]) - dx0 * (
            segment_a[1][1] - box_start_side_point[1]
        )
        p3 = dy0 * (segment_a[1][0] - box_end_side_point[0]) - dx0 * (
            segment_a[1][1] - box_end_side_point[1]
        )
        if (p0 * p1 <= 0) & (p2 * p3 <= 0):
            return True

    return False


def get_hit_box(individual, angle: float = 0):
    hit_box = []

    # Top line
    start_pos = individual.rect[:2]
    end_pos = [individual.rect[0] + individual.rect[2], individual.rect[1]]
    hit_box.append([start_pos, end_pos])

    # Left line
    start_pos = individual.rect[:2]
    end_pos = [individual.rect[0], individual.rect[1] + individual.rect[3]]
    hit_box.append([start_pos, end_pos])

    # Down line
    start_pos = [
        individual.rect[0] + individual.rect[2],
        individual.rect[1] + individual.rect[3],
    ]
    end_pos = [individual.rect[0], individual.rect[1] + individual.rect[3]]
    hit_box.append([start_pos, end_pos])

    # Right line
    start_pos = [
        individual.rect[0] + individual.rect[2],
        individual.rect[1] + individual.rect[3],
    ]
    end_pos = [individual.rect[0] + individual.rect[2], individual.rect[1]]
    hit_box.append([start_pos, end_pos])

    return hit_box


def draw_box(
    screen: pygame.Surface,
    self_sprite,
    color=pygame.Color("green"),
    width=2,
):
    # if len(self_sprite.hit_box) == 2:
    #     pygame.draw.line(
    #         screen,
    #         color=color,
    #         start_pos=self_sprite.hit_box[0],
    #         end_pos=self_sprite.hit_box[1],
    #         width=2,
    #     )
    # else:
    for [box_start_side_point, box_end_side_point] in self_sprite.hit_box:
        pygame.draw.line(
            screen,
            color=color,
            start_pos=box_start_side_point,
            end_pos=box_end_side_point,
            width=width,
        )


def vision(
    screen: pygame.Surface,
    self_sprite,
    other_sprite,
    vision_length: int,
    self_allies=None,
    other_has_group: bool = False,
    color=pygame.Color("gray"),
    width=1,
    draw=True,
):
    if draw:
        draw_box(
            screen,
            self_sprite,
        )

    vec_wall_vision = []
    vec_enemy_vision = []
    vec_laser_vision = []

    if not (self_allies is None):
        vec_ally_vision = []

    for ang in range(0, 360, 10):
        local_color = color
        local_width = width
        v_disloc = math.sin(math.radians(ang))
        h_disloc = math.cos(math.radians(ang))

        start_pos = (
            self_sprite.center[0] - v_disloc * vision_length,
            self_sprite.center[1] + h_disloc * vision_length,
        )
        end_pos = (self_sprite.center[0], self_sprite.center[1])

        # Wall detection
        if (
            start_pos[0] <= 0
            or start_pos[0] >= SCREEN_WIDTH
            or start_pos[1] <= 0
            or start_pos[1] >= SCREEN_HEIGHT
        ):
            local_color = pygame.Color("black")
            local_width = 2
            vec_wall_vision.append(1)
        else:
            vec_wall_vision.append(0)

        # Allies detection
        if not (self_allies is None):
            ally_detected = False
            for ally in self_allies:
                if ally.center != self_sprite.center:
                    has_intersect = intersect_hit_box(
                        segment_a=(start_pos, end_pos),
                        hit_box=ally.hit_box,
                    )

                    if has_intersect and (ally.center != self_sprite.center):
                        ally_detected = True
                        break

            if ally_detected:
                local_color = pygame.Color("green")
                local_width = 2
                vec_ally_vision.append(1)
            else:
                vec_ally_vision.append(0)

        # Enemy detection
        if other_has_group:
            enemy_detect = False

            for enemy in other_sprite:
                has_intersect = intersect_hit_box(
                    segment_a=(start_pos, end_pos),
                    hit_box=enemy.hit_box,
                )

                if has_intersect:
                    enemy_detect = True
                    break

            if enemy_detect:
                local_color = pygame.Color("red")
                local_width = 2
                vec_enemy_vision.append(1)
            else:
                vec_enemy_vision.append(0)

        else:
            has_intersect = intersect_hit_box(
                segment_a=(start_pos, end_pos),
                hit_box=other_sprite.hit_box,
            )

            if has_intersect:
                local_color = pygame.Color("red")
                local_width = 2
                vec_enemy_vision.append(1)
            else:
                vec_enemy_vision.append(0)

        # Laser detection
        if other_has_group:
            laser_detect = False

            for enemy in other_sprite:
                has_intersect = False
                if not (enemy.ray is None):
                    has_intersect = intersect_hit_box(
                        segment_a=(start_pos, end_pos),
                        hit_box=enemy.ray.hit_box,
                    )

                if has_intersect:
                    laser_detect = True
                    break

            if laser_detect:
                local_color = pygame.Color("blue")
                local_width = 2
                vec_laser_vision.append(1)
            else:
                vec_laser_vision.append(0)

        elif not (self_allies is None):
            ally_laser_detected = False
            for ally in self_allies:
                if ally.center != self_sprite.center and not (ally.ray is None):
                    has_intersect = intersect_hit_box(
                        segment_a=(start_pos, end_pos),
                        hit_box=ally.ray.hit_box,
                    )

                    if has_intersect and (ally.center != self_sprite.center):
                        ally_laser_detected = True
                        break

            if ally_laser_detected:
                local_color = pygame.Color("blue")
                local_width = 2
                vec_laser_vision.append(1)
            else:
                vec_laser_vision.append(0)

        else:
            laser_detect = False

            try:
                has_intersect = False

                if not (other_sprite.ray is None):
                    has_intersect = intersect_hit_box(
                        segment_a=(start_pos, end_pos),
                        hit_box=other_sprite.ray.hit_box,
                    )

            except AttributeError:
                pass

            if has_intersect:
                local_color = pygame.Color("blue")
                local_width = 2
                vec_laser_vision.append(1)
            else:
                vec_laser_vision.append(0)

        if draw:
            pygame.draw.line(
                screen,
                color=local_color,
                start_pos=start_pos,
                end_pos=end_pos,
                width=local_width,
            )

    vec_vision = vec_enemy_vision
    vec_vision.extend(vec_laser_vision)
    vec_vision.extend(vec_wall_vision)

    if not (self_allies is None):
        vec_vision.extend(vec_ally_vision)

    vec_vision = np.array(vec_vision)

    return vec_vision


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
    elif not (isinstance(center_coord_1, list) or isinstance(center_coord_1, tuple)):
        raise TypeError(
            "center_coord_1 must be list or tuple." + f" Got {type(center_coord_1)}."
        )
    elif not (isinstance(center_coord_2, list) or isinstance(center_coord_2, tuple)):
        raise TypeError(
            "center_coord_2 must be list or tuple." + f" Got {type(center_coord_2)}."
        )

    x_aim = int(center_coord_2[0] + h_incre - center_coord_1[0])
    y_aim = int(center_coord_2[1] + v_incre - center_coord_1[1])

    return math.atan2(y_aim, -x_aim)


def get_surface(
    filename: str,
    angle: float = 0,
    scale: float = 1,
) -> pygame.surface.Surface:
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
        raise TypeError(f"Angle must be an float or integer. Got {type(angle)}.")

    elif not (isinstance(scale, float) or isinstance(scale, int)):
        raise TypeError(f"Scale must be an float or integer. Got {type(scale)}.")

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
            "Acceleration function must be a string. Options: 'log', 'lin'"
            + f" and 'exp'. Got {type(func_acc)}."
        )

    if not (
        (isinstance(time, float) or isinstance(time, int))
        and (isinstance(tracker, float) or isinstance(tracker, int))
        and (isinstance(acceleration, float) or isinstance(acceleration, int))
    ):
        raise TypeError(
            f"Acceleration values must be numbers. Got time: {type(time)},"
            + f" tracker:{type(tracker)} and acceleration: "
            + f"{type(acceleration)}."
        )

    if func_acc not in ["log", "lin", "exp"]:
        raise ValueError(
            "Acceleration functions: 'log', 'lin' and 'exp'. Got" + f" '{func_acc}'."
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
