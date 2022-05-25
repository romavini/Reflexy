import json
from json import JSONEncoder

import numpy as np  # type: ignore
from numpy import random  # type: ignore
from reflexy.constants import LAYERS, PLAYER_OUTPUTS, PLAYER_VISION_CHANNELS
from reflexy.helpers.general_helpers import exit_game
from reflexy.runner import Runner


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class GeneticAlgorithm:
    def __init__(self, screen, max_generation=100, population=50, std=1e-1):
        self.std = std
        self.screen = screen

        self.time_per_simulation = 30
        self.local_dir = "../../../params"
        self.player_hp = 1
        self.gen = 0
        self.player_score = None
        self.population = population
        self.max_generation = max_generation

    def run(self):
        if self.population < 4:
            self.population = 4

        self.create_population()
        best_scores = []
        for generation in range(self.max_generation):
            self.gen = generation
            self.run_simulation()

            if generation != 0:
                player_max_score = self.player_score[generation].max()
                mean_score = round(self.player_score[generation].mean(), 1)
            else:
                player_max_score = self.player_score.max()
                mean_score = round(self.player_score.mean(), 1)

            best_scores.append([player_max_score, mean_score])
            print(f"G: {generation+1}, player_max_score: " + f"{player_max_score}")

            self.last_generation = generation
            self.last_player_weights = self.W_player
            self.last_player_bias = self.b_player
            p_weights = self.selection()
            p_weights = self.crossover(p_weights)

            self.W_player = self.mutation(
                p_weights,
                1e-6,
            )
            print(f"{best_scores = }")

        self.save_last_generation(self.max_generation)

    def update_details(self):
        """"""
        pass

    def save_last_generation(self, g):
        if g == 0:
            print("No generation to be saved.")
            return None

        print("Saving")
        self.last_generation
        self.last_player_weights
        best_player_score = self.player_score[self.last_generation].max()

        saving_params = {}

        saving_params["generation"] = self.last_generation + 1
        saving_params["best_player_score"] = best_player_score
        saving_params["last_player_weights"] = self.last_player_weights
        saving_params["last_player_bias"] = self.last_player_bias

        with open(
            f"{self.local_dir}G{self.last_generation+1}_"
            f"playerScore{str(best_player_score).replace('.',',')}.json",
            "w",
        ) as f:
            json.dump(
                saving_params,
                f,
                cls=NumpyArrayEncoder,
            )

    def create_population(self):
        self.params = {}
        self.W_player = []
        self.b_player = []

        for pop in range(self.population):
            local_W, local_b = self.create_weights(
                pop, PLAYER_VISION_CHANNELS, LAYERS, PLAYER_OUTPUTS
            )
            self.W_player.append(local_W)
            self.b_player.append(local_b)

        self.W_player = np.array(self.W_player, dtype=object)
        self.b_player = np.array(self.b_player, dtype=object)

    def create_weights(self, pop, vision, occult_layers, outputs):
        layers = [vision]
        layers.extend(occult_layers)
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

    def run_simulation(self):
        local_player_score = np.zeros(self.population)

        for pop in range(self.population):
            runner = Runner(
                self.screen,
                autonomous=True,
                training=True,
                show_vision=True,
                allow_restart=False,
                W_player_matrix=self.W_player[pop],
                b_player_matrix=self.b_player[pop],
            )

            [time, player_score, player_hp, exit] = runner.run(
                self.time_per_simulation,
                generation=self.gen,
                pop=pop,
                max_pop=self.population,
                best_score=local_player_score.max(),
            )

            if exit:
                self.save_last_generation(self.gen)
                exit_game()

            local_player_score[pop] = self.get_player_score(
                time, player_score, player_hp
            )

        if self.player_score is None:
            self.player_score = local_player_score
        else:
            self.player_score = np.vstack((self.player_score, local_player_score))

    def selection(self):
        if len(np.shape(self.player_score)) == 1:
            p_idx_sorted = np.argsort(self.player_score)

            p_weights = [self.W_player[idx] for idx in p_idx_sorted][
                : self.population // 2
            ]
        else:
            p_idx_sorted = np.argsort(self.player_score[self.gen, :])

            p_weights = [self.W_player[idx] for idx in p_idx_sorted][
                : self.population // 2
            ]

        return np.array(p_weights, dtype=object)

    def crossover(self, p_weights):
        new_weights = None

        for i in range(self.population - np.shape(p_weights)[0]):
            i_other = i

            while i_other == i:
                i_other = random.randint(0, self.population - np.shape(p_weights)[0])

            new_weight_list = []

            layer_to_cross = random.randint(0, np.shape(p_weights)[1] - 1)
            for layer in range(np.shape(p_weights)[1]):
                if layer == layer_to_cross:
                    cross_over = ["lines", "columns"][random.randint(0, 1)]

                    if cross_over == "lines":
                        cross_point = random.randint(
                            1, np.shape(p_weights[i][layer])[0] - 1
                        )

                        local_new_weight = np.vstack(
                            (
                                p_weights[i][layer][:cross_point],
                                p_weights[i_other][layer][cross_point:],
                            )
                        )
                    elif cross_over == "columns":
                        cross_point = random.randint(
                            1, np.shape(p_weights[i][layer])[1] - 1
                        )

                        local_new_weight = np.hstack(
                            (
                                p_weights[i][layer][:][:cross_point],
                                p_weights[i_other][layer][:][cross_point:],
                            )
                        )
                else:
                    local_new_weight = p_weights[i][layer]

                new_weight_list.append(local_new_weight)

            if new_weights is None:
                new_weights = np.array(new_weight_list, dtype=object)
            else:
                new_weights = np.vstack(
                    [new_weights, np.array(new_weight_list, dtype=object)]
                )

        p_weights = np.vstack((p_weights, new_weights))

        return p_weights

    def mutation(self, p_weights, mutation_ratio):
        weight_mutation = None

        for i in range(np.shape(p_weights)[0]):
            mutation = []

            for layer in range(np.shape(p_weights)[1]):
                shape = np.shape(p_weights[i][layer])
                mutation.append(np.random.randn(shape[0], shape[1]) * mutation_ratio)

            if weight_mutation is None:
                weight_mutation = np.array(mutation, dtype=object)
            else:
                weight_mutation = np.vstack((weight_mutation, mutation))

        p_weights = p_weights + weight_mutation

        return p_weights
