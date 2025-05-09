import pandas as pd
import json
import numpy as np

def getMicro(xs_json, energy):
    with open(xs_json, 'r') as file:
        data = json.load(file)

    points = data["datasets"][0]["pts"]
    df = pd.DataFrame(points)

    df_energy = df["E"]
    df_energy = df_energy / 1e6
    df_xs = df["Sig"]

    e_diff = np.abs(df_energy - energy)
    e_minloc = e_diff.idxmin()

    xs_corr = df_xs.iloc[e_minloc]

    return xs_corr