import json
import os


def load():
    if (not os.path.exists('/tmp/strava-cli-activities') or
            len(os.listdir('/tmp/strava-cli-activities')) == 0):
        raise FileNotFoundError('activities directory empty or does not exist.')
    files = os.listdir('/tmp/strava-cli-activities')
    data = []
    for file in files:
        file = os.path.join('/tmp/strava-cli-activities', file)
        with open(file, 'r') as f:
            activities = json.load(f)
        data.extend(activities)
    return data
