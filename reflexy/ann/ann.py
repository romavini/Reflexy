import pygame
import math
import numpy as np
from reflexy.constants import (
    SPIDER_VISION,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)


class Ann():
    def __init__(self):
        pass

    def activate_function(self, output_weight_layer_1):
        output_layer_1 = []
        for val in output_weight_layer_1:
            output_layer_1.append(1/(1 + np.exp(-val)))

        return output_layer_1

    def neural(self, ang, a, b, dist):
        input_layer = np.array([ang, a[0], a[1], b[0], b[1], dist])
        weight_layer_1 = np.zeros((6, 6))

        # output_layer_1 = self.activate_function(np.matmul(weight_layer_1, input_layer.T))
    
    def angle_between(self, p1, p2):
        d1 = p2[0] - p1[0]
        d2 = p2[1] - p1[1]
        if d1 == 0:
            if d2 == 0:
                deg = 0
            else:
                deg = 0 if p1[1] > p2[1] else 180
        elif d2 == 0:
            deg = 90 if p1[0] < p2[0] else 270
        else:
            deg = math.atan(d2 / d1) / math.pi * 180
            lowering = p1[1] < p2[1]
            if (lowering and deg < 0) or (not lowering and deg > 0):
                deg += 270
            else:
                deg += 90
        return deg

    def update(self, player, enemy):
        a = np.array(player)
        b = np.array(enemy)
    
        dist = np.linalg.norm(a - b) # Range of distance
        ang = self.angle_between(a, b) # Angle to aim

        x = a[0] + math.cos(math.radians(ang + 90)) * SPIDER_VISION
        y = a[1] + math.sin(math.radians(ang + 90)) * SPIDER_VISION

        # self.neural(ang, a, b, dist)

        return 0, ang, x, y
