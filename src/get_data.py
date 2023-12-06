import requests
import json
import pickle
import time
import os

from src import CONFIG_PATH, ACCESS_TOKEN, ACTIVITIES_DIR


def get_access_token():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    client_id, client_secret = config['client_id'], config['client_secret']

    if not os.path.exists(ACCESS_TOKEN):
        refresh_response = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                                         data={'client_id': client_id,
                                               'client_secret': client_secret,
                                               'grant_type': 'authorization_code',
                                               'code': config['code']})
        access_token = refresh_response.json()
        with open(ACCESS_TOKEN, 'wb') as f:
            pickle.dump(access_token, f)
    else:
        with open(ACCESS_TOKEN, 'rb') as f:
            access_token = pickle.load(f)

        if time.time() > access_token['expires_at']:
            refresh_response = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                                             data={'client_id': client_id,
                                                   'client_secret': client_secret,
                                                   'grant_type': 'refresh_token',
                                                   'refresh_token': access_token['refresh_token']})
            access_token = refresh_response.json()
            with open(ACCESS_TOKEN, 'wb') as f:
                pickle.dump(access_token, f)

    return access_token


def download():
    access_token = get_access_token()
    if os.path.exists(ACTIVITIES_DIR):
        for filename in os.listdir(ACTIVITIES_DIR):
            file_path = os.path.join(ACTIVITIES_DIR, filename)
            os.remove(file_path)

    index = 0
    finished = False
    while not finished:
        index += 1
        response = requests.get(url='https://www.strava.com/api/v3/athlete/activities',
                                headers={'Authorization': f"Bearer {access_token['access_token']}"},
                                params={'page': index, 'per_page': 100})
        if response.text == '[]' or index == 10:
            finished = True
            continue
        with open(os.path.join(ACTIVITIES_DIR, f"activities_{index}.json"), 'w') as f:
            json.dump(response.json(), f)

    print("Download successful")


if __name__ == '__main__':
    download()
