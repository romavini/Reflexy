from ann.helpers.general import read_weights
from typing import List
import numpy as np


class annBrain:
    def __init__(self, W=None, b=None, layers=None, read=None):
        """

        read -- 'enemy' or 'player' (default None)
        """
        self.params = {}
        self.layers = layers
        self.std = 1e-1

        if not (read is None):
            self.W, self.b = read_weights(read)

        if W is None or b is None:
            self.create_weights()
        else:
            self.W = W
            self.b = b

    def create_weights(self):
        self.W = []
        self.b = []

        for i in range(1, len(self.layers)):
            self.params[f"W{i}"] = self.std * np.random.randn(
                self.layers[i - 1], self.layers[i]
            )
            self.W.append(self.params[f"W{i}"])

            self.params[f"b{i}"] = np.ones(self.layers[i])
            self.b.append(self.params[f"b{i}"])

    @staticmethod
    def func_relu(list_in: List[float]) -> List[float]:
        return np.array([0 if e < 0 else e for e in list_in])

    @staticmethod
    def action_ativation(out_layer: List[float]) -> List[bool]:
        return [False if e < 0.5 else True for e in out_layer]

    def analyze(self, vec_vision):
        len(f"{vec_vision = }")
        out_layer = vec_vision.dot(self.W[0]) + self.b[0]
        out_layer = self.func_relu(out_layer)  # ReLU
        self.params["out_layer_1"] = out_layer

        for i in range(1, len(self.layers) - 1):
            local_out_layer = out_layer.dot(self.W[i]) + self.b[i]
            out_layer = self.func_relu(local_out_layer)  # ReLU
            self.params[f"out_layer_{i+1}"] = out_layer

        out_layer = self.action_ativation(out_layer)

        return out_layer

    def score(self):
        pass
