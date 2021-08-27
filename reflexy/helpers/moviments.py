from reflexy.helpers.math import angle2_pi_minus_pi


def autonomous_spider_vision(brain, spider_vision):
    """"""
    [
        move_left,
        move_right,
        move_up,
        move_down,
        to_fire,
        to_angle,
    ] = brain.analyze(spider_vision)

    to_angle = angle2_pi_minus_pi(to_angle)

    moviments = [
        move_left,
        move_right,
        move_up,
        move_down,
        to_fire,
        to_angle,
    ]
    return moviments
