import os
import Betterfy
import time
from datetime import datetime

token = Betterfy.authenticate()
time.sleep(5)
os.system('CLS||clear')

while True:
    resp_json = Betterfy.current_track(token)
    track_name = resp_json['item']['name']
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

