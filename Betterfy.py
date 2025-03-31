"""A collection of functions aimed to interact with the Spotify API."""
import requests
from authflow import auth
from literals import _limit, _state, _type, _kind, _typeu, _kindt, _groups, _time, _kindto
from img_encoder import encode


def authenticate():
    r"""Initializes the authentication flow and requests the user to authorize your app.

        :returns: A valid user token for the Spotify API.
        """
    return auth()


def create_header(token: str):
    r"""Creates a header to send with the Spotify API calls.

        :param token: The token of the user required to access the Spotify API.
        :return: The header.
        """
    header = {"Authorization": "Bearer " + f"{token}"}
    return header


#get
def get_profile(token: str, id: str = None):
    r"""Gets the profile of a user.

        :param token: The token of the user required to access the Spotify API.
        :param id: ID of the user you want the profile of. If none is given, gets the current users profile.
        :return: JSON response.
        """
    if id is None:
        profile = requests.get('https://api.spotify.com/v1/me', headers=create_header(token), stream=True).json()
        return profile
    else:
        profiles = requests.get(f'https://api.spotify.com/v1/users/{id}', headers=create_header(token), stream=True).json()
        return profiles


def check_following(token: str, ids: list, type: _typeu): #ids = max 50
    r"""Checks if the user is following a User/Artist.

        :param token: The token of the user required to access the Spotify API.
        :param ids: List of User/Artist IDs. A max of 50 can be provided
        :param type: The type of ID to check.
        :return: JSON response.
        """
    if len(ids) > 50:
        print("Error: Can only check 50 artists/users at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        check = requests.get(f'https://api.spotify.com/v1/me/following/contains?type={type}&ids={uri}', headers=create_header(token), stream=True)
        return check


def check_following_playlist(token: str, id: str):
    r"""Checks if user is following the playlist.

        :param token: The token of the user required to access the Spotify API.
        :param id: The ID of the playlist to check.
        :return: JSON response.
        """
    check = requests.get(f'https://api.spotify.com/v1/playlists/{id}/followers/contains', headers=create_header(token), stream=True)
    return check


def check_saved_album(token: str, ids: list): #ids = max 20
    r"""Checks if the user saved an Album.

        :param token: The token of the user required to access the Spotify API.
        :param ids: List of Album IDs. A max of 20 can be provided
        :return: JSON response.
        """
    if len(ids) > 20:
        print("Error: Can only check 20 albums at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        check = requests.get(f'https://api.spotify.com/v1/me/albums/contains?ids={uri}', headers=create_header(token), stream=True)
        return check


def get_new_release(token: str, limit: _limit = 20, offset = 0): #limit = min1/max50
    r"""Gets the new releases for a user.

        :param token: The token of the user required to access the Spotify API.
        :param limit: Number of releases to show.
        :param offset: Where to begin in the list of new releases.
        :return: JSON response.
        """
    releases = requests.get(f'https://api.spotify.com/v1/browse/new-releases?limit={limit}&offset={offset}', headers=create_header(token), stream=True)
    return releases


def get_top(token: str, kind: _kindto, time: _time = "medium_term", limit: _limit = 20, offset=0): #kind = artists/tracks | limit = min1/max50
    top = requests.get(f'https://api.spotify.com/v1/me/top/{kind}?time_range={time}&limit={limit}&offset={offset}', headers=create_header(token), stream=True).json()
    return top


def current_trackname(token: str):
    r"""Gets the currently playing track name.

        :param token: The token of the user required to access the Spotify API.
        :return: String with name.
        """
    track = requests.get('https://api.spotify.com/v1/me/player', headers=create_header(token), stream=True).json()
    track_name = track['item']['name']
    return track_name


def current_track(token: str):
    r"""Gets the currently playing track as JSON.

        :param token: The token of the user required to access the Spotify API.
        :return: JSON response.
        """
    track = requests.get('https://api.spotify.com/v1/me/player', headers=create_header(token), stream=True).json()
    return track


def current_trackId(token: str):
    r"""Gets the trackID of the currently playing track.

        :param token: The token of the user required to access the Spotify API.
        :return: String with ID.
        """
    track = requests.get('https://api.spotify.com/v1/me/player', headers=create_header(token), stream=True).json()
    track_id = track['item']['id']
    return track_id


def get_track(token: str, id: str):
    r"""Gets a specific track as JSON.

        :param token: The token of the user required to access the Spotify API.
        :param id: TrackID of the specified track.
        :return: JSON response.
        """
    track = requests.get(f'https://api.spotify.com/v1/tracks/{id}', headers=create_header(token), stream=True).json()
    return track


def get_progress(token: str):
    r"""Gets the progress of the currently playing track represented as 0 to 1.

        :param token: The token of the user required to access the Spotify API.
        :return: int (0 is the start of the track and 1 is the end).
        """
    track = current_track(token)
    return int(track["progress_ms"]) / int(track["item"]["duration_ms"])


#def get_audio_feautures(token, id): #currently not available because spotify is a greedy company and terminated access to these endpoints
    #feautures = requests.get(f'https://api.spotify.com/v1/audio-features/{id}', headers=create_header(token), stream=True).json()
    #return feautures


#def get_key(token, id): #currently not available because spotify is a greedy company and terminated access to these endpoints
    #return get_audio_feautures(token, id)["key"]


def get_top_tracks(token: str, id: str, limit: _limit = 20):
    tracks = requests.get(f'https://api.spotify.com/v1/artists/{id}/top-tracks', headers=create_header(token), stream=True).json()
    track_list = []
    for _ in range(limit):
        track_list.append(
            f"{tracks["items"][_]["track"]["name"]} | {tracks["items"][_]["track"]["artists"][0]["name"]}")
    return track_list


def get_album(token: str, id: str):
    r"""Gets the specified Album as JSON.

        :param token: The token of the user required to access the Spotify API.
        :param id: The ID of the album.
        :return: JSON response.
        """
    album = requests.get(f'https://api.spotify.com/v1/albums/{id}', headers=create_header(token), stream=True).json()
    return album


def get_artist(token: str, id: str):
    r"""Gets the artist specified as JSON.

        :param token: The token of the user required to access the Spotify API.
        :param ids: The ID of the artist.
        :return: JSON response.
        """
    artist = requests.get(f'https://api.spotify.com/v1/artists/{id}', headers=create_header(token), stream=True).json()
    return artist


def get_category(token: str, id: str, locale: str): #locale = ISO 639-1 language code and an ISO 3166-1 alpha-2 country code
    category = requests.get(f'https://api.spotify.com/v1/browse/categories/{id}?locale={locale}', headers=create_header(token), stream=True).json()
    return category


def get_tracks(token: str, ids: list):
    r"""Gets tracks as JSON.

        :param token: The token of the user required to access the Spotify API.
        :param ids: List of track IDs. A max of 50 can be provided.
        :return: JSON response.
        """
    if len(ids) > 50:
        print("Error: Can only get 50 tracks at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        tracks = requests.get(f'https://api.spotify.com/v1/tracks?ids={uri}', headers=create_header(token), stream=True).json()
        return tracks


def get_albums(token: str, ids: list):
    r"""Gets albums as JSON.

        :param token: The token of the user required to access the Spotify API.
        :param ids: List of album IDs. A max of 20 can be provided
        :return: JSON response.
        """
    if len(ids) > 20:
        print("Error: Can only get 20 albums at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        albums = requests.get(f'https://api.spotify.com/v1/albums?ids={uri}', headers=create_header(token), stream=True).json()
        return albums


def get_artists(token: str, ids: list):
    r"""Gets artists as JSON.

        :param token: The token of the user required to access the Spotify API.
        :param ids: List of artist IDs. A max of 50 can be provided
        :return: JSON response.
        """
    if len(ids) > 50:
        print("Error: Can only get 50 artists at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        artists = requests.get(f'https://api.spotify.com/v1/artists?ids={uri}', headers=create_header(token), stream=True).json()
        return artists


def check_saved_tracks(token: str, ids: list):
    r"""Checks if tracks are saved.

        :param token: The token of the user required to access the Spotify API.
        :param ids: List of track IDs. A max of 50 can be provided
        :return: JSON response.
        """
    if len(ids) > 50:
        print("Error: Can only check 50 tracks at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        check = requests.get(f'https://api.spotify.com/v1/me/tracks/contains?ids={uri}', headers=create_header(token), stream=True).json()
        return check


def get_saved_tracks(token: str, limit: _limit = 20, offset=0):
    r"""Gets the last saved tracks as JSON.

        :param token: The token of the user required to access the Spotify API.
        :param limit: How many tracks to get. min of 1 and max of 50.
        :param offset: Where in the list of tracks to begin.
        :return: JSON response.
        """
    tracks = requests.get(f'https://api.spotify.com/v1/me/tracks?offset={offset}&limit={limit}', headers=create_header(token), stream=True).json()
    track_list = []
    for _ in range(limit):
        track_list.append(f"{tracks["items"][_]["track"]["name"]} | {tracks["items"][_]["track"]["artists"][0]["name"]}")
    return track_list


def get_saved_albums(token: str, limit: _limit = 20, offset=0):
    r"""Gets the last saved albums as JSON.

        :param token: The token of the user required to access the Spotify API.
        :param limit: How many albums to get. min of 1 and max of 50.
        :param offset: Where in the list of albums to begin.
        :return: JSON response.
        """
    albums = requests.get(f'https://api.spotify.com/v1/me/albums?limit={limit}&offset={offset}', headers=create_header(token), stream=True).json()
    return albums


def get_album_tracks(token: str, id: str, limit: _limit = 20, offset=0):
    r"""Gets the tracks of an album as JSON.

        :param token: The token of the user required to access the Spotify API.
        :param limit: How many tracks to get. min of 1 and max of 50.
        :param offset: Where in the list of tracks to begin.
        :return: JSON response.
        """
    tracks = requests.get(f'https://api.spotify.com/v1/albums/{id}/tracks?limit={limit}&offset={offset}', headers=create_header(token), stream=True).json()
    return tracks


def get_artist_albums(token: str, id: str, groups: _groups, limit: _limit = 20, offset=0): #limit = min1/max50
    albums = requests.get(f'https://api.spotify.com/v1/artists/{id}/albums?include_groups={groups}&limit={limit}&offset={offset}', headers=create_header(token), stream=True).json()
    return albums


def get_browse_categories(token: str, locale: str, limit: _limit = 20, offset=0): #limit = min1/max50 | locale = ISO 639-1 language code and an ISO 3166-1 alpha-2 country code
    if 0 < limit <= 50:
        categories = requests.get(f'https://api.spotify.com/v1/browse/categories?locale={locale}&limit={limit}&offset={offset}', headers=create_header(token), stream=True).json()
        return categories
    else:
        print("Can only get 50 categories at a time")


def search(token: str, track: str, artist: str, type: _type = "track", limit: _limit = 20): #limit = min1/max50/default20 | offset = default0 | type = album/artist/playlist/track/show/episode/audiobook
    if limit > 50 or limit <= 0:
        return "Can only show 50 songs at once"
    else:
        q = f"query=track:{track}" + f"%252520artist:{artist}"
        result = requests.get(f'https://api.spotify.com/v1/search?q={q}&type={type}&limit={limit}',
                              headers=create_header(token), stream=True).json()
        tracks = []
        for _ in range(len(result["tracks"]["items"])):
            tracks.append(
                f"{result["tracks"]["items"][_]["name"]} | {result["tracks"]["items"][_]["artists"][0]["name"]}")
        return tracks


def get_playlists(token: str, limit: _limit = 20, offset=0):
    r"""Gets the last saved playlists with name and creator.

        :param token: The token of the user required to access the Spotify API.
        :param limit: How many playlists to get. min of 1 and max of 50.
        :param offset: Where in the list of playlists to begin.
        :return: List with the names and creators of the playlists.
        """
    if limit > 50 or limit <= 0:
        return "Can only show 50 playlists at once"
    else:
        result = requests.get(f'https://api.spotify.com/v1/me/playlists?limit={limit}&offset={offset}',
                              headers=create_header(token), stream=True).json()
        playlists = []
        for _ in range(int(result["total"])):
            playlists.append(f"{result["items"][_]["name"]} | {result["items"][_]["owner"]["display_name"]}")
        return playlists


def get_user_playlists(token: str, id: str, limit: _limit = 20, offset=0):
    r"""Gets the playlists of a user with name and creator.

        :param token: The token of the user required to access the Spotify API.
        :param limit: How many playlists to get. min of 1 and max of 50.
        :param offset: Where in the list of playlists to begin.
        :param id: The user ID.
        :return: List with the names and creators of the playlists.
        """
    if limit > 50 or limit <= 0:
        return "Can only show 50 playlists at once"
    else:
        result = requests.get(f'https://api.spotify.com/v1/users/{id}/playlists?limit={limit}&offset={offset}',headers=create_header(token), stream=True).json()
        playlists = []
        for _ in range(int(result["total"])):
            playlists.append(f"{result["items"][_]["name"]} | {result["items"][_]["owner"]["display_name"]}")
        return playlists


#set
def set_volume(token: str, vol: int):
    r"""Sets the volume of the player.

            :param token: The token of the user required to access the Spotify API.
            :param vol: The volume from 0 to 100.
            """
    return requests.put(f'https://api.spotify.com/v1/me/player/volume?volume_percent={int(vol)}', headers=create_header(token), stream=True)


def set_shuffle(token: str, state: bool):
    r"""Enables/Disables shuffle mode.

            :param token: The token of the user required to access the Spotify API.
            :param state: False/True.
            """
    return requests.put(f'https://api.spotify.com/v1/me/player/shuffle?state={str(state)}', headers=create_header(token), stream=True)


def set_repeat(token: str, state: _state):
    r"""Sets the repeat mode.

            :param token: The token of the user required to access the Spotify API.
            :param state: The repeat mode that's wanted.
            """
    return requests.put(f'https://api.spotify.com/v1/me/player/repeat?state={state}', headers=create_header(token), stream=True)


def pause(token: str):
    r"""Pauses the player..

            :param token: The token of the user required to access the Spotify API.
            """
    return requests.put('https://api.spotify.com/v1/me/player/pause', headers=create_header(token), stream=True)


def play(token: str):
    r"""Sets the player status to play..

            :param token: The token of the user required to access the Spotify API.
            """
    return requests.put('https://api.spotify.com/v1/me/player/play', headers=create_header(token), stream=True)


def next(token: str):
    r"""Plays the next song.

            :param token: The token of the user required to access the Spotify API.
            """
    requests.post('https://api.spotify.com/v1/me/player/next', headers=create_header(token), stream=True)
    return


def previous(token: str):
    r"""Plays the previous song.

            :param token: The token of the user required to access the Spotify API.
            """
    requests.post('https://api.spotify.com/v1/me/player/previous', headers=create_header(token), stream=True)
    return


def queue_track(token: str, uri: str):
    r"""Adds a track to the queue.

            :param token: The token of the user required to access the Spotify API.
            :param uri: The uri of a track.
            """
    requests.post(f'https://api.spotify.com/v1/me/player/queue?uri=spotify:track:{uri}', headers=create_header(token), stream=True)
    return


def save_track(token: str, ids: list, kind: _kindt):
    r"""Saves/Unsaves tracks from the users liked songs.

        :param token: The token of the user required to access the Spotify API.
        :param ids: The track IDs. Max of 50
        :param kind: Specifies if you want to delete or add a track.
        """
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


def follow_playlist(token: str, id: str, kind: _kind, public: bool = False):
    if kind == "follow":
        requests.put(f'https://api.spotify.com/v1/playlists/{id}/followers', headers=create_header(token), stream=True)
        return
    if kind == "unfollow":
        requests.delete(f'https://api.spotify.com/v1/playlists/{id}/followers', headers=create_header(token), stream=True)
        return


def follow(token: str, ids: list, kind: _kind, type: _typeu): #ids = max 50
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


def save_album(token: str, ids: list, kind: _kind): #ids = max 20
    if len(ids) > 20:
        print("Error: Can only save 20 albums at a time")
        return
    else:
        uri = str(ids).removeprefix("(").removesuffix(")")
        if kind == "follow":
            requests.put(f'https://api.spotify.com/v1/me/albums?ids={uri}', headers=create_header(token), stream=True)
            return
        if kind == "unfollow":
            requests.delete(f'https://api.spotify.com/v1/me/albums?ids={uri}', headers=create_header(token), stream=True)
            return


def create_playlist(token: str, id: str, data: dict):
    r"""Creates a playlist.

            :param token: The token of the user required to access the Spotify API.
            :param id: The playlist ID.
            :param data: The deailts of the playlist in JSON form (name, description etc.)
            :returns: The ID of the newly created playlist.
            """
    r = requests.post(f'https://api.spotify.com/v1/users/{id}/playlists', json=data, headers=create_header(token), stream=True)
    return r.json()["id"]


def change_playlist(token: str, id: str, data: dict):
    r"""Changes the details of a playlist.

            :param token: The token of the user required to access the Spotify API.
            :param id: The playlist ID.
            :param data: The changes to the playlist in JSON form.
            """
    requests.put(f'https://api.spotify.com/v1/playlists/{id}', json=data, headers=create_header(token),stream=True)


def add_song_playlist(token: str, id: str, urilist: list, pos: str = 0):
    r"""Adds songs to a playlist.

            :param token: The token of the user required to access the Spotify API.
            :param id: The playlist ID.
            :param urilist: A list containing track IDs. Max of 100 IDs
            :param pos: Which position in the playlist the songs should be added. If None then they get added at the top.
            """
    uris = f"spotify:track:{urilist[0]}"
    if 0 < len(urilist) < 100:
        for _ in range(len(urilist)-1):
            uris += f",spotify:track:{urilist[_+1]}"
        requests.post(f'https://api.spotify.com/v1/playlists/{id}/tracks?position={pos}&uris={uris}', headers=create_header(token), stream=True)
    else:
        return print("Can only add 100 songs at a time")


def remove_song_playlist(token: str, id: str, urilist: list):
    r"""Removes songs from a playlist.

            :param token: The token of the user required to access the Spotify API.
            :param id: The playlist ID.
            :param urilist: A list containing track IDs. Max of 100 IDs
            """
    data = {"tracks": []}
    if 0 < len(urilist) < 100:
        for _ in range(len(urilist)):
            data["tracks"].append({"uri": f"spotify:track:{urilist[_]}"})
        requests.delete(f'https://api.spotify.com/v1/playlists/{id}/tracks', json=data, headers=create_header(token), stream=True)
    else:
        return print("Can only add 100 songs at a time")


def get_playlist(token: str, id: str):
    r"""Gets an playlist as JSON.

            :param token: The token of the user required to access the Spotify API.
            :param id: The playlist ID.
            :return: JSON response.
            """
    return requests.get(f'https://api.spotify.com/v1/playlists/{id}', headers=create_header(token), stream=True).json()


def reorder_playlist(token: str, id: str, range_start: int, insert_before: int, range_length: int = 1):
    data = {"range_start": range_start-1, "insert_before": insert_before, "range_length": range_length}
    requests.put(f'https://api.spotify.com/v1/playlists/{id}/tracks', json=data, headers=create_header(token), stream=True)


def get_playlist_tracks(token: str, id: str, limit: _limit = 20, offset=0): #limit = min1/max50
    if 0 < limit <= 50:
        tracks = requests.get(f'https://api.spotify.com/v1/playlists/{id}/tracks?limit={limit}&offset={offset}', headers=create_header(token), stream=True).json()
        return tracks
    else:
        print("Can only get 50 tracks at a time")


def get_playlist_cover(token: str, id: str):
    r"""Gets the cover of a playlist.

            :param token: The token of the user required to access the Spotify API.
            :param id: The playlist ID.
            :return: JSON response.
            """
    return requests.get(f'https://api.spotify.com/v1/playlists/{id}/images', headers=create_header(token), stream=True).json()


def add_playlist_cover(token: str, id: str, img_path: str):
    r"""Adds a cover to a playlist.

            :param token: The token of the user required to access the Spotify API.
            :param id: The playlist ID.
            :param img_path: The path to the image which should be used as the cover.
            :return: JSON response.
            """
    header = create_header(token)
    header.update({"Content-Type": "image/jpeg; charset=utf-8"})
    return requests.put(f'https://api.spotify.com/v1/playlists/{id}/images', data=encode(img_path), headers=header, stream=True)
