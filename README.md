
![logo](https://github.com/simply-Gamic/Betterfy/assets/80588359/c80edbcc-624e-4c97-b78b-47e0e73f9edb)


# Betterfy - A more detailed Spotify Experience

Are you annoyed from hitting shuffle in your favourite playlist and getting the same 10 songs over and over again? Are you the friend that's always the DJ at partys and you'd like to see what BPM the next song has to keep the dance floor going? Are you a music nerd and want to know what key a song is in without having to google? Do you love pretty lights and want perfectly beat synced leds to your currently playing spotify song?

If you answered yes to any of these questions `Betterfy` might be for you. Born from the ideas of a music lover, who's annoyed by some of Spotify's features, this library aims to bring everything you (or rather me) ever wanted to the Spotify experience. 

I have quiet a lot of ideas for this whole thing and I'm just at the beginning, so for now I'm focusing on the basics. Once I have a working basis I'll expand the project. 


## To Do
- Finish the authentication flow to be fully automatic
- Migrate the basic UI I created (which can control Spotify through the WEB API) from html to a basic Tkinter UI
- Integrate [T-vK's](https://github.com/T-vK/Beats4Wled) awesome work and get led lights via [WLED](https://github.com/Aircoookie/WLED) synced up to Spotify



### Roadmap
Some of the bigger ideas I have for this project:

- *Completely* random shuffle option
- *Completely* random song choice option
- Controlling Spotify playlists through the WEB API and making it easier to create them
- Option to build a Spotify Connect device in a browser or on a wifi enabled machine (tries to emulate the Spotify CarThing) --> basically: build your own Spotify UI layout
- Using Audioanalysis to display detailed song details (BPM, Key, Instrumentalisation etc.) in a easy to read format
- Using Audioanalysis to build a metronome for the current song (and also sync that up to leds to for example have a visual metronome on a rgb midi piano)
- Maybe migrate from python to a faster language in the future if I encounter any problems with performance
- Integrate DMX control into Spotify to be able to link moving heads and the like to a Spotify instance
- many, many more things that float around in my head

Track what I'm currently working on [here](https://github.com/users/simply-Gamic/projects/1/views/1)

## Example
Really barebones use of the library to first log in to the Spotify API on behalf of a user with the default Oauth flow and default scopes. Then it continously prints out the current song position of the currently playing song.

```python
import Spotify

# setup Spotify instance 
Credentials = '{ "client_id":"YOUR_APP_ID", "state":"GENERATED_SAFETY_STRING"}'
Spotify = Spotify(Oauth=Default, cred=Credentials, scopes=Default)

# print out song position
while True:
    print("Song position: " + Spotify.playback.position, end="\r")

```

## Documentation

For further documentation and information checkout the docs:
[Wiki]() (coming as soon as I have a working barebones version....)


## Contributing

Contributions are always welcome, as I'm just a guy with lots of ideas and some (little) coding knowledge and my code can be done way better `99.9%` of the time!



## Support

For support, email me ([@simply Gamic](https://github.com/simply-Gamic)) or open an issue.


## License

[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) [![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)



## Acknowledgements
coming soon...
