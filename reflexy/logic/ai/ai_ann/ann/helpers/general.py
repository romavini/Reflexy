import os
import json
import numpy as np


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
