import math


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