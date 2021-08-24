import math


def segments_intersect(segment_self, segment_target):
    """Return the point of irtercet of two segments.

    Keyword arguments:
    two sets of segments
    """

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
            return x, y
        else:
            return False

    L1 = line(segment_self)
    L2 = line(segment_target)

    R = intersection(L1, L2)

    if not R:
        return segment_self[0]

    return R


def angle2_pi_minus_pi(angle):
    angle_deg = math.degrees(angle)

    if angle_deg < 360:
        if angle_deg > 180:
            angle_deg = angle_deg - 360
    else:
        while (angle_deg + 360) // 360 >= 1 and angle_deg > 180:
            if angle_deg > 180:
                angle_deg = angle_deg - 360

    return math.radians(angle_deg)


def get_relative_distance_point(start_point, final_point, defaul_value):
    """Return a float value to distance."""
    s_x, s_y = start_point
    e_x, e_y = final_point

    h_dist = round(s_x - e_x)
    v_dist = round(s_y - e_y)
    value = math.sqrt(h_dist ** 2 + v_dist ** 2) / defaul_value
    value = 0 if value < 0 else 1 if value > 1 else round(value, 3)

    return value


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
