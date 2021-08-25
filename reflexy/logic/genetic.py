import json
from json import JSONEncoder
import numpy as np
from numpy import random
from reflexy.constants import (
    LAYERS,
    PLAYER_OUTPUTS,
    PLAYER_VISION_CHANNELS,
    SPIDER_OUTPUTS,
    SPIDER_VISION_CHANNELS,
    START_HP,
)
from reflexy.runner import Runner


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class GeneticAlgorithm:
    def __init__(self, elem="both", max_geration=100, population=30, std=1e-1):
        self.std = std
        self.time_per_simulatiron = 30
        self.local_dir = "reflexy/logic/"

        if elem == "both":
            self.player_score = None
            self.enemy_score = None
        elif elem == "player":
            self.player_score = None
        elif elem == "enemy":
            self.enemy_score = None

        if population < 4:
            self.population = 4
        else:
            self.population = population

        self.create_poulation()
        for generation in range(max_geration):
            self.run_simulation(generation)

            if generation != 0:
                print(
                    f"G: {generation+1}, player_max_score: "
                    + f"{self.player_score[generation].max()}, "
                    + f"enemy_max_score: {self.enemy_score[generation].max()}"
                )
            else:
                print(
                    f"G: {generation+1}, player_max_score: "
                    + f"{self.player_score.max()}, "
                    + f"enemy_max_score: {self.enemy_score.max()}"
                )

            self.last_generation = generation
            self.last_player_weights = self.W_player
            self.last_player_bias = self.b_player
            self.last_enemy_weights = self.W_enemy
            self.last_enemy_bias = self.b_enemy
            p_weights, e_weights = self.selection(generation)
            p_weights, e_weights = self.crossover(p_weights, e_weights)

            self.W_player, self.W_enemy = self.mutation(
                p_weights,
                e_weights,
                1e-6,
            )

        self.save_last_generation(max_geration)

    def save_last_generation(self, g):
        if g == 0:
            print("No generation to be saved.")
            return None

        print("Saving")
        self.last_generation
        self.last_player_weights
        self.last_enemy_weights

        saving_params = {}

        best_player_score = self.player_score[self.last_generation].max()
        best_enemy_score = self.enemy_score[self.last_generation].max()

        saving_params["generation"] = self.last_generation + 1
        saving_params["best_player_score"] = best_player_score
        saving_params["best_enemy_score"] = best_enemy_score
        saving_params["last_player_weights"] = self.last_player_weights
        saving_params["last_player_bias"] = self.last_player_bias
        saving_params["last_enemy_weights"] = self.last_enemy_weights
        saving_params["last_enemy_bias"] = self.last_enemy_bias

        with open(
            f"{self.local_dir}params/G{self.last_generation+1}_"
            f"playerScore{str(best_player_score).replace('.',',')}_"
            f"enemyScore{str(best_enemy_score).replace('.',',')}.json",
            "w",
        ) as f:
            json.dump(
                saving_params,
                f,
                cls=NumpyArrayEncoder,
            )

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

        self.W_enemy = np.array(self.W_enemy, dtype=object)
        self.b_enemy = np.array(self.b_enemy, dtype=object)
        self.W_player = np.array(self.W_player, dtype=object)
        self.b_player = np.array(self.b_player, dtype=object)

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

            [time, player_score, player_hp, exit] = runner.run(
                self.time_per_simulatiron,
                generation=generation,
                pop=pop,
                max_pop=self.population,
            )

            if exit:
                self.save_last_generation(generation)
                runner.exit_game()

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

    def selection(self, generation):
        if len(np.shape(self.player_score)) == 1:
            p_idx_sorted = np.argsort(self.player_score)
            e_idx_sorted = np.argsort(self.enemy_score)

            p_weights = [self.W_player[idx] for idx in p_idx_sorted][
                : self.population // 2
            ]

            e_weights = [self.W_enemy[idx] for idx in e_idx_sorted][
                : self.population // 2
            ]
        else:
            p_idx_sorted = np.argsort(self.player_score[generation, :])
            e_idx_sorted = np.argsort(self.enemy_score[generation, :])

            p_weights = [self.W_player[idx] for idx in p_idx_sorted][
                : self.population // 2
            ]

            e_weights = [self.W_enemy[idx] for idx in e_idx_sorted][
                : self.population // 2
            ]

        return (
            np.array(p_weights, dtype=object),
            np.array(e_weights, dtype=object),
        )

    def crossover(self, p_weights, e_weights):
        local_p_weights = None
        local_e_weights = None

        for idx, weights in enumerate([p_weights, e_weights]):
            new_weights = None

            for i in range(self.population - np.shape(weights)[0]):
                i_other = i

                while i_other == i:
                    i_other = random.randint(0, self.population - np.shape(weights)[0])

                new_weight_list = []

                for layer in range(np.shape(weights[0])[0]):

                    cross_over = ["lines", "columns"][random.randint(0, 1)]

                    if cross_over == "lines":
                        cross_point = random.randint(1, np.shape(weights[i][layer])[0])

                        local_new_weight = np.vstack(
                            (
                                weights[i][layer][:cross_point],
                                weights[i_other][layer][cross_point:],
                            )
                        )
                    elif cross_over == "columns":
                        cross_point = random.randint(
                            1, np.shape(weights[i][layer])[1] - 1
                        )

                        local_new_weight = np.hstack(
                            (
                                weights[i][layer][:][:cross_point],
                                weights[i_other][layer][:][cross_point:],
                            )
                        )

                    new_weight_list.append(local_new_weight)

                if new_weights is None:
                    new_weights = np.array(new_weight_list, dtype=object)
                else:
                    new_weights = np.vstack(
                        (new_weights, np.array(new_weight_list, dtype=object))
                    )

            weights = np.vstack((weights, new_weights))

            if idx == 0:
                local_p_weights = weights
            elif idx == 1:
                local_e_weights = weights

        p_weights = local_p_weights
        e_weights = local_e_weights

        return p_weights, e_weights

    def mutation(self, p_weights, e_weights, mutation_ratio):
        local_p_weights = None
        local_e_weights = None

        for idx, weights in enumerate([p_weights, e_weights]):
            weight_mutation = None

            for i in range(np.shape(weights)[0]):
                mutation = []

                for layer in range(np.shape(weights)[1]):
                    shape = np.shape(weights[i][layer])
                    mutation.append(
                        np.random.randn(shape[0], shape[1]) * mutation_ratio
                    )

                if weight_mutation is None:
                    weight_mutation = np.array(mutation, dtype=object)
                else:
                    weight_mutation = np.vstack((weight_mutation, mutation))

            if idx == 0:
                local_p_weights = weight_mutation
            elif idx == 1:
                local_e_weights = weight_mutation

        p_weights = p_weights + local_p_weights
        e_weights = e_weights + local_e_weights

        return p_weights, e_weights


if __name__ == "__main__":
    ga = GeneticAlgorithm()
