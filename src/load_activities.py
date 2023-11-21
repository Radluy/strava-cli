import json
import os


def load():
    files = os.listdir('activities')
    data = []
    for file in files:
        file = os.path.join('activities', file)
        with open(file, 'r') as f:
            activities = json.load(f)
        data.extend(activities)
    return data
