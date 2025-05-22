from typing import Literal

_limit = Literal[range(1,20)]
_kind = Literal["follow", "unfollow"]
_type = Literal["track", "album", "artist", "playlist", "show", "episode", "audiobook"]
_typeu = Literal["artist", "user"]
_kindt = Literal["delete", "save"]
_groups = Literal["album", "single", "appears_on", "compilation"]
_state = Literal["context", "track", "off"]
_time = Literal["long_term", "medium_term", "short_term"]
_kindto = Literal["artists", "tracks"]
_kindp = Literal["tracks", "context"]
