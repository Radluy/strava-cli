import requests
import json
import pickle
import time
import os


with open('config.json', 'r') as f:
    config = json.load(f)
STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET = config['client_id'], config['client_secret']


def get_access_token():
    if not os.path.exists('access_token.pickle'):
        refresh_response = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                                         data={'client_id': STRAVA_CLIENT_ID,
                                               'client_secret': STRAVA_CLIENT_SECRET,
                                               'grant_type': 'authorization_code',
                                               'code': config['code']})
        access_token = refresh_response.json()
        with open('access_token.pickle', 'wb') as f:
            pickle.dump(access_token, f)
    else:
        with open('access_token.pickle', 'rb') as f:
            access_token = pickle.load(f)

        if time.time() > access_token['expires_at']:
            refresh_response = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                                             data={'client_id': STRAVA_CLIENT_ID,
                                                   'client_secret': STRAVA_CLIENT_SECRET,
                                                   'grant_type': 'refresh_token',
                                                   'refresh_token': access_token['refresh_token']})
            access_token = refresh_response.json()
            with open('access_token.pickle', 'wb') as f:
                pickle.dump(access_token, f)

    return access_token


def download():
    access_token = get_access_token()

    if os.path.exists('/tmp/strava-cli-activities'):
        for filename in os.listdir('/tmp/strava-cli-activities'):
            file_path = os.path.join('/tmp/strava-cli-activities', filename)
            os.remove(file_path)
    else:
        os.mkdir('/tmp/strava-cli-activities')

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
        with open(f"/tmp/strava-cli-activities/activities_{index}.json", 'w') as f:
            json.dump(response.json(), f)

    print("Download successful")


if __name__ == '__main__':
    download()
