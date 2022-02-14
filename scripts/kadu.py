import json

import numpy as np
import pandas as pd


def load_spell_data():
    with open("spell_data.js") as dataFile:
        data = dataFile.read()
        obj = data[data.find("{") : data.rfind("}") + 1]
        jsonObj = json.loads(obj)
    return jsonObj


def select_wizard_spells(d):
    wizard_spells = {}
    for spell_name, data in d.items():
        if "Wizard" in data["class"]:
            wizard_spells[spell_name] = {k: v for k, v in data.items() if k != "class"}
    return wizard_spells


def assign_weights(row, weights):
    return weights.get(row["level"], 0)


def roll(size):
    return np.random.randint(1, size + 1)


wizard_spells = select_wizard_spells(load_spell_data())
df = (
    pd.DataFrame.from_records(list(wizard_spells.values()))
    .set_index("name")
    .drop(
        columns=[
            "page",
            "srd_name",
            "ritual",
            "casting_time",
            "duration",
            "components",
            "range",
            "concentration",
        ]
    )
)

weights = {
    "1st": 0.5,
    "2nd": 0.3,
    "3rd": 0.2,
}
df["weight"] = df.apply(lambda row: assign_weights(row, weights), axis=1)

schools = pd.unique(df["school"])
school = np.random.choice(schools)
print(school)
school_multiplier = 5
df["weight"][df["school"] == school] *= school_multiplier
df["weight"] /= df["weight"].sum()

nspells = roll(6) + roll(6) + roll(6)
spells_selected = np.random.choice(
    df.index, size=nspells, p=df["weight"], replace=False
)
df = df.loc[spells_selected, :].sort_values("level")
print(df.head(18))

costs = {
    "1st": 25,
    "2nd": 75,
    "3rd": 150,
}
cost = 0
for _, row in df.iterrows():
    cost += costs[row["level"]]
print(f"Cost: {cost}")

with open("spellbook.txt", "w+") as fh:
    fh.write(f"School: {school}, Cost: {cost}\n\n")
    for name, row in df.iterrows():
        spell_level = row["level"]
        spell_school = row["school"]
        fh.write(f"{name} ({spell_level}, {spell_school})\n")
