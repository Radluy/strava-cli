import os.path
from enum import Enum
from os.path import expanduser


USER_CONFIG_DIR = expanduser(os.path.join('~', '.config'))
ROOT_DIR = expanduser(os.path.join('~', '.config', 'strava-cli'))
ACTIVITIES_DIR = expanduser(os.path.join('~', '.config', 'strava-cli', 'strava-cli-activities'))
CONFIG_PATH = expanduser(os.path.join('~', '.config', 'strava-cli', 'config.json'))
ACCESS_TOKEN = expanduser(os.path.join('~', '.config', 'strava-cli', 'access_token.pickle'))


class ActivityType(Enum):
    run = 'Run'
    ride = 'Ride'
    hike = 'Hike'
    workout = 'Workout'
    rock_climbing = 'RockClimbing'
    nordic_ski = 'NordicSki'
    alpine_ski = 'AlpineSki'
    weight_training = 'WeightTraining'

    def __str__(self):
        return self.value


class Attribute(Enum):
    distance = 'distance'
    elevation_gain = 'total_elevation_gain'
    average_heartrate = 'average_heartrate'
    moving_time = 'moving_time'
    average_speed = 'average_speed'
    average_pace = 'average_pace'
    date = 'start_date_local'

    def __str__(self):
        return self.value
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Units(Enum):
    distance = 'km'
    elevation_gain = 'm'
    average_heartrate = 'bpm'
    moving_time = 'hh:mm:ss'
    average_speed = 'km/h'
    average_pace = 'min/km'
    date = 'YYYY-mm-dd'

    def __str__(self):
        return self.value
