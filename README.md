<b>GPT-3.5-turbo AI Spotify Playlist Generator</b>

Project based on Colt Steele's Mastering OpenAI Python APIs: Unleash ChatGPT and GPT4.

<b>Creating your Spotify Web API to obtain Spotify Client ID and Client Secret keys</b>

Follow the instructions here: https://developer.spotify.com/documentation/web-api

Inside your Spotify WEB API set your ```Website``` and ``Redirect URIs`` both to```http://localhost:9999```

<b>Finding your OpenAI secret keys</b>

Read the instructions here: https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key

<b>Create an .env text file to add your API keys</b>

Add your:

SPOTIFY_CLIENT_ID <br>
SPOTIFY_CLIENT_SECRET <br>
OPEN_API_KEY <br>

in the following format:

```
SPOTIFY_CLIENT_ID = <key>
SPOTIFY_CLIENT_SECRET = <key>
OPENAI_API_KEY = <key> 
```

Please make sure to replace ```<key>``` with your actual keys.

In the code you will use dictionaries to insert the code in the lines below:

```python
sp = spotipy.Spotify( 
    auth_manager=spotipy.SpotifyOAuth( 
        client_id = config["SPOTIFY_CLIENT_ID"], 
        client_secret = config["SPOTIFY_CLIENT_SECRET"], 
        redirect_uri="http://localhost:9999", 
        scope="playlist-modify-private" 
    ) 
)
```
More to come.
