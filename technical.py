import json
import time
import Betterfy
import enums


def check_resource():
    try:
        with open('Resource.json', 'r') as f:
            return True
    except FileNotFoundError:
        return False


def create_resource(id: str, scope: list):
    scopes = ""
    for item in scope:
        scopes += f"{item} "
    with open('Resource.json', 'w') as f:
        data = {
            "Betterfy": {
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
        Betterfy.next(token)
    if value == "||":
        Betterfy.pause(token)
    if value == "|>":
        Betterfy.play(token)
    if value == "<":
        Betterfy.previous(token)
    else:
        pass


def update_token():
    while True:
        enums.token = Betterfy.authenticate()
        time.sleep(3500)
        print(f"Token Updated. New one: {enums.token}")


def volume(value):
    token = enums.token
    Betterfy.set_volume(token, value)
