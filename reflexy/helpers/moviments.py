from typing import List

from reflexy.helpers.math_helpers import angle2_pi_minus_pi
from reflexy.logic.ai.ai_ann.ann.spider_logic import Brain


def autonomous_spider_vision(brain: Brain, spider_vision: List[int]) -> List[float]:
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
