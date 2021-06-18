import math


class PlayerBrain:
    def __init__(self):
        pass

    def analyze(self, blinking_damage, hp, ang, h_dist, v_dist):

        return [
            move_left,
            move_right,
            move_up,
            move_down,
            to_attack,
        ]


class SpiderBrain:
    def __init__(self):
        pass

    def shot(self, enemy_angle, cooldown_ray, self_pos, enemy_pos):
        dist = math.dist(self_pos, enemy_pos)
        return enemy_angle

    def move(self, enemy_angle, cooldown_ray):
        return enemy_angle


class SpiderAi:
    def __init__(self):
        pass

    def fit(self):
        pass

    def update(self):
        pass


class PlayerAi:
    def __init__(self):
        pass

    def fit(self):
        pass

    def update(self):
        pass
