import os.path
from os.path import expanduser


USER_CONFIG_DIR = expanduser(os.path.join('~', '.config'))
ROOT_DIR = expanduser(os.path.join('~', '.config', 'strava-cli'))
ACTIVITIES_DIR = expanduser(os.path.join('~', '.config', 'strava-cli', 'strava-cli-activities'))
CONFIG_PATH = expanduser(os.path.join('~', '.config', 'strava-cli', 'config.json'))
ACCESS_TOKEN = expanduser(os.path.join('~', '.config', 'strava-cli', 'access_token.pickle'))
