
![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)


# Betterfy - A more detailed Spotify Experience

Description comming soon....


## Roadmap

- *Completely* random shuffle
- *Completely* random song choice
- Controlling Spotify through the WEB API
- Option to build a Spotify Connect device in a browser or on a wifi enabled machine (tries to emulate the Spotify CarThing)
- Using Audioanalysis to display detailed song details (BPM, Key, Instrumentalisation etc.)
- Using Audioanalysis to build a metronome for the current song
- Using Audioanalysis to sync [WLED lights](https://github.com/Aircoookie/WLED) to the currently playing song (Idea and logic courtesy of [T-vK](https://github.com/T-vK/Beats4Wled))
- Maybe migrate from python to a faster language in the future if I encounter any problems with performance


## Usage/Examples
Really barebones use of the app to first log in to the Spotify API on behalf of a user with the default Oauth Protocol and default Scopes. Then the app continously prints out the current position in the currently playing song of the User.

```python
import Spotify

# setup Spotify instance 
Credentials = '{ "client_id":"YOUR_APP_ID", "state":"GENERATED_SAFETY_STRING"}'
Spotify = Spotify(oauth=Default, cred=Credentials, scopes=Default)

while True:
    print("Song position: " + Spotify.playback.position, end="\r")

```

## Documentation

For further documentation and information checkout the docs:
[Wiki]() (coming soon....)


## Contributing

Contributions are always welcome, as I'm just a guy with lots of ideas and some coding knowledge and my code can be done way better `99.9%` of the time!



## Support

For support, email me ([@simply Gamic](https://github.com/simply-Gamic)) or open an issue.


## License

[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) [![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)



## Acknowledgements
coming soon...
