from reflexy.constants import LAYERS, PLAYER_VISION_CHANNELS
from reflexy.runner import Runner


class GeneticAlgorithm:
    def __init__(self, max_geration=100, population=10, std=1e-1):
        layers = [PLAYER_VISION_CHANNELS]
        layers.extend(LAYERS)
        layers.extend([PLAYER_VISION_OUTPUTS])
        for pop in range(population):
            self.layers = layers
            self.params = {}
            self.W = []
            self.b = []

            for i in range(1, len(self.layers)):
                self.params[f"pop_{pop + 1}_W{i}"] = std * np.random.randn(
                    self.layers[i - 1], self.layers[i]
                )
                self.W.append(self.params[f"pop_{pop + 1}_W{i}"])

                self.params[f"pop_{pop + 1}_b{i}"] = np.ones(self.layers[i])
                self.b.append(self.params[f"pop_{pop + 1}_b{i}"])

    def start_population(self):
        pass

    def run_simulation(self):
        runner = Runner(autonomous=True, show_vision=True)
        runner.run()
