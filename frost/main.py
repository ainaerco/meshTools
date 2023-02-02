import os
import json
from model import Ability, Action, Monster, MonsterStat


LANG = "en"
data_root = "gloomhavensecretariat/data/fh"
with open(os.path.join(data_root, "label.json"),
        "r", encoding="utf-8") as f:
    label_data = json.load(f)
    label_data = label_data[LANG]


def read_actions():
    with open(os.path.join(data_root, "monster", "abael-herder.json"),
            "r", encoding="utf-8") as f:
        data = json.load(f)
        data["name"] = label_data["monster"].get(data["name"]) or data["name"]
        print(Monster(**data))
        for stat in data["stats"]:
            actions = []
            for action in stat.get("actions", []):
                actions.append(Action(**action))
            stat["actions"] = actions
            print(MonsterStat(**stat))


with open(os.path.join(data_root, "deck", "abael-herder.json"),
        "r", encoding="utf-8") as f:
    data = json.load(f)
    data["name"] = label_data["monster"].get(data["name"]) or data["name"]
    print(Monster(**data))
    for ability in data["abilities"]:
        actions = []
        for action in ability.get("actions", []):
            sub_actions = []
            actions.append(Action(**action))
        ability["actions"] = actions
        print(Ability(**ability))
