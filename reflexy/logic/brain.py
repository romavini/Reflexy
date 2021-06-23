import math
import numpy as np


class PlayerBrain:
    def __init__(self, layers=[36, 100, 5], std=1e-4):
        self.params = {}
        for i in range(1, len(layers)):
            self.params[f"W{i}"] = std * np.random.randn(layers[i - 1], layers[i])
            self.params[f"b{i}"] = np.zeros(layers[i])

    def analyze(self, vec_vision):

        return [
            move_left,
            move_right,
            move_up,
            move_down,
            to_attack,
        ]


class SpiderBrain:
    def __init__(self, layers=[72, 100, 5], std=1e-4):
        self.params = {}
        for i in range(1, len(layers)):
            self.params[f"W{i}"] = std * np.random.randn(layers[i - 1], layers[i])
            self.params[f"b{i}"] = np.zeros(layers[i])

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
