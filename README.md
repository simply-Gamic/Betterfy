
![logo](https://github.com/simply-Gamic/Betterfy/assets/80588359/c80edbcc-624e-4c97-b78b-47e0e73f9edb)


# Betterfy - A more detailed Spotify Experience

Are you annoyed from hitting shuffle in your favourite playlist and getting the same 10 songs over and over again? Are you the friend that's always the DJ at partys and you'd like to see what BPM the next song has to keep the dance floor going? Are you a music nerd and want to know what key a song is in without having to google? Do you love pretty lights and want perfectly beat synced leds to your currently playing spotify song?

If you answered yes to any of these questions `Betterfy` might be for you. Born from the ideas of a music lover, who's annoyed by some of Spotify's features, this library aims to bring everything you (or rather me) ever wanted to the Spotify experience. 

I have quiet a lot of ideas for this whole thing and I'm just at the beginning, so for now I'm focusing on the basics. Once I have a working basis I'll expand the project. 


## Really early UI Layout and function (v0.1)
Here's the app in action (well at least a really early barebones version of it) to give a slight idea of how it will work and look like.
![gif](https://github.com/simply-Gamic/Betterfy/assets/80588359/9b364bfd-4ae4-474d-8d58-71ce633d41bb)

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
Really barebones use of the library to do some simple calls to the API.

```python
import Betterfy

# Get API token 
token = Betterfy.authenticate()

# print out name of currently playing song
print(f"Song name: {Betterfy.current_trackname(token)}")
```
Output:
```
Song name: songtitle
```
<br/>
<br/>

```python
# print out last 5 saved songs of the user, skipping the newest 10 --> so song number 10 to 15 from the users saved songs
limit = 5
offset = 10
tracks = Betterfy.get_saved_tracks(token, limit=limit, offset=offset)

for _ in range(limit):
    print(f"{_+1+offset}. {tracks[_]}")
```

Output:
```
11. songtitle | artist
12. songtitle | artist
13. songtitle | artist
14. songtitle | artist
15. songtitle | artist
```
<br/>
<br/>

```python
# skip to the next song
Betterfy.next(token)
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
