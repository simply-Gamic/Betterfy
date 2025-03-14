import requests
from authflow import auth


def authenticate():
    return auth()


def create_header(token):
    header = {"Authorization": "Bearer " + f"{token}"}
    return header


def current_trackname(token):
    track = requests.get('https://api.spotify.com/v1/me/player', headers=create_header(token), stream=True).json()
    track_name = track['item']['name']
    return track_name


def current_track(token):
    track = requests.get('https://api.spotify.com/v1/me/player', headers=create_header(token), stream=True).json()
    return track
