import numpy as np
from reflexy.constants import (
    LAYERS,
    PLAYER_OUTPUTS,
    PLAYER_VISION_CHANNELS,
    SPIDER_OUTPUTS,
    SPIDER_VISION_CHANNELS,
    START_HP,
)
from reflexy.runner import Runner


class GeneticAlgorithm:
    def __init__(self, max_geration=100, population=10, std=1e-1):
        self.max_geration = max_geration
        self.population = population
        self.std = std
        self.time_per_simulatiron = 10
        self.player_score = None
        self.enemy_score = None

        self.create_poulation()
        for g in range(max_geration):
            self.run_simulation(g)
            if g != 0:
                print(
                    f"G: {g+1}, player_max_score: {self.player_score[g].max()},"
                    + f" enemy_max_score: {self.enemy_score[g].max()}"
                )
            else:
                print(
                    f"G: {g+1}, player_max_score: {max(self.player_score)},"
                    + f" enemy_max_score: {max(self.enemy_score)}"
                )
            self.selection()
            self.crossover()
            self.mutation()

    def create_poulation(self):
        self.params = {}
        self.W_player = []
        self.W_enemy = []
        self.b_player = []
        self.b_enemy = []

        for pop in range(self.population):

            local_W, local_b = self.create_weights(
                pop, PLAYER_VISION_CHANNELS, LAYERS, PLAYER_OUTPUTS
            )
            self.W_player.append(local_W)
            self.b_player.append(local_b)

            local_W, local_b = self.create_weights(
                pop, SPIDER_VISION_CHANNELS, LAYERS, SPIDER_OUTPUTS
            )
            self.W_enemy.append(local_W)
            self.b_enemy.append(local_b)

    def create_weights(self, pop, vision, ocult_layers, outputs):
        layers = [vision]
        layers.extend(ocult_layers)
        layers.extend([outputs])
        self.layers = layers
        local_W = []
        local_b = []

        for i in range(1, len(self.layers)):
            self.params[f"pop_{pop + 1}_W{i}"] = self.std * np.random.randn(
                self.layers[i - 1], self.layers[i]
            )
            local_W.append(self.params[f"pop_{pop + 1}_W{i}"])
            self.params[f"pop_{pop + 1}_b{i}"] = np.ones(self.layers[i])
            local_b.append(self.params[f"pop_{pop + 1}_b{i}"])

        return local_W, local_b

    def get_player_score(self, time, player_score, player_hp):
        return round(time + player_score * 10 + player_hp * 10, 2)

    def get_enemy_score(self, time, player_score, player_lost_hp):
        return round(
            time - self.time_per_simulatiron + player_score * 10 + player_lost_hp,
            2,
        )

    def run_simulation(self, generation):
        local_player_score = np.zeros(self.population)
        local_enemy_score = np.zeros(self.population)

        for pop in range(self.population):
            runner = Runner(
                autonomous=True,
                show_vision=True,
                allow_restart=False,
                W_player_matrix=self.W_player[pop],
                b_player_matrix=self.b_player[pop],
                W_enemy_matrix=self.W_enemy[pop],
                b_enemy_matrix=self.b_enemy[pop],
            )
            [time, player_score, player_hp] = runner.run(self.time_per_simulatiron)
            local_player_score[pop] = self.get_player_score(
                time, player_score, player_hp
            )
            local_enemy_score[pop] = self.get_enemy_score(
                time, player_score, START_HP - player_hp
            )

        if self.player_score is None:
            self.player_score = local_player_score
            self.enemy_score = local_enemy_score
        else:
            self.player_score = np.vstack((self.player_score, local_player_score))
            self.enemy_score = np.vstack((self.enemy_score, local_enemy_score))

    def selection(self):
        pass

    def crossover(self):
        pass

    def mutation(self):
        pass


if __name__ == "__main__":
    ga = GeneticAlgorithm()
