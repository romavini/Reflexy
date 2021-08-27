import os
import json
from reflexy.menus.elements import createButton
from reflexy.constants import (
    SCORE_FONT,
    SCORE_FONT_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_WIDTH_AI,
)
from reflexy.helpers.general import create_text
import numpy as np
import pygame


def read_weights(read, local_dir="../"):
    if read is None:
        read = "player"

    files = os.listdir(os.path.join(local_dir, "params/"))

    with open(f"{os.path.join(local_dir, 'params', files[0])}", "r") as f:
        obj = f.read()

    dict_weights = json.loads(obj)

    if read == "player":
        W = np.array(dict_weights["last_player_weights"], dtype=object)
        b = np.array(dict_weights["last_player_bias"], dtype=object)
    # elif read == "enemy":
    #     W = np.array(dict_weights["last_enemy_weights"], dtype=object)
    #     b = np.array(dict_weights["last_enemy_bias"], dtype=object)

    return W, b


def update_generation(runner, generation, pop, max_pop, best_score, keyboard):
    """"""
    pygame.draw.rect(
        runner.screen,
        (125, 125, 125),
        (SCREEN_WIDTH, 0, SCREEN_WIDTH_AI, SCREEN_HEIGHT),
    )
    create_text(
        runner.screen,
        "Geneation = " + str(generation + 1),
        (SCREEN_WIDTH + SCREEN_WIDTH_AI // 2, SCREEN_HEIGHT // 8 * 2),
        size=SCORE_FONT_SIZE,
        font_name=SCORE_FONT,
    )
    create_text(
        runner.screen,
        "Score = " + str(round(runner.time_display + runner.player.score * 10, 2)),
        (SCREEN_WIDTH + SCREEN_WIDTH_AI // 2, SCREEN_HEIGHT // 8 * 3),
        size=SCORE_FONT_SIZE,
        font_name=SCORE_FONT,
    )

    create_text(
        runner.screen,
        f"Pop = {str(pop + 1)} of {max_pop}",
        (SCREEN_WIDTH + SCREEN_WIDTH_AI // 2, SCREEN_HEIGHT // 8 * 4),
        size=SCORE_FONT_SIZE,
        font_name=SCORE_FONT,
    )

    create_text(
        runner.screen,
        f"Best score = {best_score}",
        (SCREEN_WIDTH + SCREEN_WIDTH_AI // 2, SCREEN_HEIGHT // 8 * 5),
        size=SCORE_FONT_SIZE,
        font_name=SCORE_FONT,
    )

    for key, key_bool in zip(
        keyboard,
        [
            runner.player.move_up,
            runner.player.move_down,
            runner.player.move_right,
            runner.player.move_left,
            runner.player.to_attack,
        ],
    ):
        if key_bool:
            pygame.draw.rect(
                runner.screen,
                key.color_dark,
                [
                    key.button_pos[0],
                    key.button_pos[1],
                    key.button_width_n_height[0],
                    key.button_width_n_height[1],
                ],
            )
        else:
            pygame.draw.rect(
                runner.screen,
                key.color_light,
                [
                    key.button_pos[0],
                    key.button_pos[1],
                    key.button_width_n_height[0],
                    key.button_width_n_height[1],
                ],
            )
