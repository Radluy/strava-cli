import json
import os

from src import ACTIVITIES_DIR


def load():
    if (not os.path.exists(ACTIVITIES_DIR) or
            len(os.listdir(ACTIVITIES_DIR)) == 0):
        raise FileNotFoundError('activities directory empty or does not exist.')
    files = os.listdir(ACTIVITIES_DIR)
    data = []
    for file in files:
        file = os.path.join(ACTIVITIES_DIR, file)
        with open(file, 'r') as f:
            activities = json.load(f)
        data.extend(activities)
    return data
