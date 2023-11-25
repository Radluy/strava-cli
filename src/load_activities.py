import json
import os


def load():
    if not os.path.exists('activities') or len(os.listdir('activities')) == 0:
        raise FileNotFoundError('activities directory empty or does not exist.')
    files = os.listdir('activities')
    data = []
    for file in files:
        file = os.path.join('activities', file)
        with open(file, 'r') as f:
            activities = json.load(f)
        data.extend(activities)
    return data
