"""Handles the technical functions behind BetterfyFunc's UI"""
#  Copyright (c) 2025.

import json
import random
import time
from BetterfyFunc import BetterfyFunc
from App import enums


def check_resource():
    r"""Checks wheter or not the needed resources file is available

            :returns: Bool
            """
    try:
        with open('../Resource.json', 'r') as f:
            return True
    except FileNotFoundError:
        return False


def create_resource(id: str, scope: list):
    r"""Creates a resource file
        :param id The ID of the Spotify APP
        :param scope List with all the scopes needed for the app
    """
    scopes = ""
    for item in scope:
        scopes += f"{item} "
    with open('../Resource.json', 'w') as f:
        data = {
            "BetterfyFunc": {
                "creds": {
                    "id": id,
                    "scopes": scopes,
                    "redirect": "http://127.0.0.1:8000/callback/",
                    "authUrl": "https://accounts.spotify.com/authorize",
                    "tokenUrl": "https://accounts.spotify.com/api/token",
                    "grant": "authorization_code",
                    "refreshGrant": "refresh_token",
                    "headers": {
                        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
                    }
                }
            }
            }
        f.write(json.dumps(data))


def song(value):
    token = enums.token
    if value == ">":
        BetterfyFunc.next(token)
    if value == "||":
        BetterfyFunc.pause(token)
    if value == "|>":
        BetterfyFunc.play(token)
    if value == "<":
        BetterfyFunc.previous(token)
    else:
        pass


def update_token():
    r"""Periodically refreshes the user token"""
    while True:
        enums.token = BetterfyFunc.authenticate()
        time.sleep(3500)
        print(f"Token Updated. New one: {enums.token}")


def volume(value):
    r"""Adjust the volume for the spotify player
        :param value The value to set the volume to from 0-100
    """
    token = enums.token
    BetterfyFunc.set_volume(token, value)


def random_shuffle_queue():
    r"""Shuffles the current queue of the user randomly. User queue can be a max of 20 songs"""
    token = enums.token
    queue = BetterfyFunc.get_queue(token)
    uris = []
    for uri in queue:
        uris.append(uri["uri"])
    random.shuffle(uris)
    BetterfyFunc.play(token, uris, "tracks")
