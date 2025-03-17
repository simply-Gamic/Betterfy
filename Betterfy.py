import requests
from authflow import auth


def authenticate():
    return auth()


def create_header(token):
    header = {"Authorization": "Bearer " + f"{token}"}
    return header


#get
def get_profile(token, id): #if no id is given get current users profile
    if id is None:
        profile = requests.get('https://api.spotify.com/v1/me', headers=create_header(token), stream=True).json()
        return profile
    else:
        profiles = requests.get(f'https://api.spotify.com/v1/users/{id}', headers=create_header(token), stream=True).json()
        return profiles


def check_following(token, ids, type): #ids = max 50 | type = artist/user
    if len(ids) > 50:
        print("Error: Can only check 50 artists/users at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        check = requests.get(f'https://api.spotify.com/v1/me/following/contains?type={type}&ids={uri}', headers=create_header(token), stream=True)
        return check


def check_following_playlist(token, id):
    check = requests.get(f'https://api.spotify.com/v1/playlists/{id}/followers/contains', headers=create_header(token), stream=True)
    return check


def get_top(token, kind, time, limit, offset): #kind = artists/tracks | limit = min1/max50/default 20 | offset = default 0 | time = long/medium/short_term
    top = requests.get(f'https://api.spotify.com/v1/me/top/{kind}', headers=create_header(token), stream=True).json()
    return top


def current_trackname(token):
    track = requests.get('https://api.spotify.com/v1/me/player', headers=create_header(token), stream=True).json()
    track_name = track['item']['name']
    return track_name


def current_track(token):
    track = requests.get('https://api.spotify.com/v1/me/player', headers=create_header(token), stream=True).json()
    return track


def get_track(token, id):
    track = requests.get(f'https://api.spotify.com/v1/tracks/{id}', headers=create_header(token), stream=True).json()
    return track


def get_tracks(token, ids): #max 50 ids
    if len(ids) > 50:
        print("Error: Can only get 50 tracks at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        tracks = requests.get(f'https://api.spotify.com/v1/tracks?ids={uri}', headers=create_header(token), stream=True).json()
        return tracks


def check_saved_tracks(token, ids): #max 50ids
    if len(ids) > 50:
        print("Error: Can only check 50 tracks at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        check = requests.get(f'https://api.spotify.com/v1/me/tracks/contains?ids={uri}', headers=create_header(token), stream=True).json()
        return check


def get_saved_tracks(token, limit, offset): #limit = min1/max50/default20 | offset = default0
    tracks = requests.get(f'https://api.spotify.com/v1/me/tracks?offset={offset}&limit={limit}', headers=create_header(token), stream=True).json()
    return tracks


#set
def set_volume(token, vol): #percentage
    requests.put(f'https://api.spotify.com/v1/me/player/volume?volume_percent={vol}', headers=create_header(token), stream=True)
    return


def set_shuffle(token, state): #true or false
    requests.put(f'https://api.spotify.com/v1/me/player/shuffle?state={state}', headers=create_header(token), stream=True)
    return


def set_repeat(token, state): #context, track, off
    requests.put(f'https://api.spotify.com/v1/me/player/repeat?state={state}', headers=create_header(token), stream=True)
    return


def pause(token):
    requests.put('https://api.spotify.com/v1/me/player/pause', headers=create_header(token), stream=True)
    return


def next(token):
    requests.put('https://api.spotify.com/v1/me/player/next', headers=create_header(token), stream=True)
    return


def previous(token):
    requests.put('https://api.spotify.com/v1/me/player/previous', headers=create_header(token), stream=True)
    return


def queue_track(token, uri):
    requests.put(f'https://api.spotify.com/v1/me/player/queue?uri=spotify%3Atrack%3A{uri}', headers=create_header(token), stream=True)
    return


def save_track(token, ids, kind): #max 50ids; kind = delete or save
    if len(ids) > 50:
        print("Error: Can only save/delete 50 tracks at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        if kind == "save":
            requests.put(f'https://api.spotify.com/v1/me/tracks?ids={uri}', headers=create_header(token), stream=True)
        if kind == "delete":
            requests.delete(f'https://api.spotify.com/v1/me/tracks?ids={uri}', headers=create_header(token), stream=True)
        return


def follow_playlist(token, id, public, kind): #public = True/False | kind = follow/unfollow
    if kind == "follow":
        requests.put(f'https://api.spotify.com/v1/playlists/{id}/followers', headers=create_header(token), stream=True)
        return
    if kind == "unfollow":
        requests.delete(f'https://api.spotify.com/v1/playlists/{id}/followers', headers=create_header(token), stream=True)
        return


def follow(token, ids, kind, type): #ids = max 50 | kind = follow/unfollow | type = artist/user
    if len(ids) > 50:
        print("Error: Can only follow 50 artists/users at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        if kind == "follow":
            requests.put(f'https://api.spotify.com/v1/me/following?type={type}&ids={uri}', headers=create_header(token), stream=True)
            return
        if kind == "unfollow":
            requests.delete(f'https://api.spotify.com/v1/me/following?type={type}&ids={uri}', headers=create_header(token), stream=True)
            return


