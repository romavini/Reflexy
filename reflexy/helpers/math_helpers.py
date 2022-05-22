import math
from typing import List, Optional


def distance(a: List[float], b: List[float]) -> float:
    return round(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2), 2)


def segments_intersect(segment_self, segment_target):
    """Return the point of intercept of two segments.

    Keyword arguments:
    two sets of segments
    """

    def is_between(a: List[float], c: List[float], b: List[float]) -> bool:
        return math.isclose(
            distance(a, c) + distance(c, b), distance(a, b), abs_tol=0.05
        )

    def line(segment):
        p1, p2 = segment
        A = p1[1] - p2[1]
        B = p2[0] - p1[0]
        C = p1[0] * p2[1] - p2[0] * p1[1]

        return A, B, -C

    def intersection(L1, L2):
        D = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]

        if D != 0:
            x = int(Dx / D)
            y = int(Dy / D)

            if is_between(segment_target[0], [x, y], segment_target[1]):
                return x, y
            else:
                return False
        else:
            return False

    L1 = line(segment_self)
    L2 = line(segment_target)

    R = intersection(L1, L2)

    return R


def angle2_pi_minus_pi(angle: float) -> Optional[float]:
    angle_deg = math.degrees(angle)

    if angle_deg < 360:
        if angle_deg > 180:
            angle_deg = angle_deg - 360
    else:
        while (angle_deg + 360) // 360 >= 1 and angle_deg > 180:
            if angle_deg > 180:
                angle_deg = angle_deg - 360

    return math.radians(angle_deg)


def get_relative_distance_point(start_point, final_point, default_value):
    """Return a float value to distance."""
    # s_x, s_y = start_point
    # e_x, e_y = final_point

    # h_dist = round(s_x - e_x)
    # v_dist = round(s_y - e_y)
    value = 1 - (distance(start_point, final_point) / default_value)
    value = 0 if value < 0 else 1 if value > 1 else round(value, 3)

    return value


def aim(
    center_coord_1, center_coord_2, h_increment: int = 0, v_increment: int = 0
) -> float:
    """Aim system.

    Keyword arguments:
    center_coord_1 -- sequence of player's center coordinates
    center_coord_2 -- sequence of enemy's center coordinates
    h_increment -- horizontal increment (default 0)
    v_increment -- vertical increment (default 0)
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

    x_aim = int(center_coord_2[0] + h_increment - center_coord_1[0])
    y_aim = int(center_coord_2[1] + v_increment - center_coord_1[1])

    return math.atan2(y_aim, -x_aim)


def calc_acceleration(func_acc: str, time: float, acceleration: float) -> float:
    """Calculate the acceleration.

    Keyword arguments:
    func_acc -- acceleration function (default "lin")
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
        and (isinstance(acceleration, float) or isinstance(acceleration, int))
    ):
        raise TypeError(
            f"Acceleration values must be numbers. Got time: {type(time)}"
            + f" and acceleration: {type(acceleration)}."
        )

    if func_acc not in ["log", "lin", "exp"]:
        raise ValueError(
            "Acceleration functions: 'log', 'lin' and 'exp'. Got" + f" '{func_acc}'."
        )

    elif func_acc == "log":
        if not (time):
            return 0

        log = math.log10(1 / acceleration * (time))
        if log < 0:
            return 0

        return (log + 2) / 2

    elif func_acc == "lin":
        return 1 / acceleration * (time)

    elif func_acc == "exp":
        return 2 ** (1 / acceleration * (time)) - 1

    else:
        return 0
