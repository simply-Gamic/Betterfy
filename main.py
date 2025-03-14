import os
import requests
import time
from datetime import datetime
from authflow import auth

token = auth()
header = {"Authorization": "Bearer " + f"{token}"}
time.sleep(5)
os.system('CLS||clear')

while True:
    r2 = requests.get('https://api.spotify.com/v1/me/player', headers=header, stream=True)
    resp_json = r2.json()
    track_name = r2.json()['item']['name']
    track_id = resp_json['item']['id']
    timestamp = resp_json['timestamp']
    duration = resp_json['item']['duration_ms']
    progress = resp_json['progress_ms']
    playing = resp_json['is_playing']
    artists = resp_json['item']['artists']
    artist_name = ', '.join([artist['name'] for artist in artists])
    current = str(datetime.fromtimestamp(progress // 1000)).removeprefix('1970-01-01 01:')
    percent = round(number=progress / duration * 100, ndigits=1)
    if playing == False:
        print('Pause                                                                                                              ', end='\r')
    else:
        print("Spielt gerade: " + f"{track_name}" + ' - ' + f"{artist_name}" + '  |  Zeit: ' + f"{str(percent)}" + "% | " + f"{current}", end='\r')
        time.sleep(0.02)

