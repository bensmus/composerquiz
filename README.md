# About

Command-line music quiz! Listen to a song segment, then guess the composer.

# Setup 

- Requires your computer to have Python and git.
- Requires your system to have VLC installed (to play the song segment).
- Requires internet connection to access Open Opus API and the Spotify API. 

1. Clone the repo. 
2. Follow the steps in https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app to obtain a client_id and client_secret. Then make an .env file (in current directory) that contains them:
```
(.env file)
client_id=<YOUR CLIENT ID>
client_secret=<YOUR CLIENT SECRET>
```

3. Install the requirements `pip install -r requirements.txt`.

# Usage

Run `python composerquiz.py`. You should see a prompt to hit enter to start song segment playback. Then you select the composer with arrow keys and enter.

```
Hit 'Enter' to start audio
[?] Select the composer: 
   Villa-Lobos
 > Webern
   Shostakovich
   Berg

Wrong! String Quartet no. 8 in C minor, op. 110 by Shostakovich
```
