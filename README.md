<b>GPT-3.5-turbo AI Spotify Playlist Generator</b>

<img src="https://github.com/typedwires/OpenAI-Spotify-Generator/blob/main/playlist.png" width="800">

Project based on Colt Steele's Mastering OpenAI Python APIs: Unleash ChatGPT and GPT4.

<b> How to generate the playlist </b>

Once the project is set up (see instructions below) in the command line, nagivate to the project and run

```shell
python app.py -p "90s and early 2000s rock love songs" -n 10
```

Where ```-p``` represents the prompt or playlist title, and ``-n`` denotes the number of songs to generate.

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

<b>Spotipy</b>

We use the Spotify Python library for the Spotify Web API. For detailed usage instructions and information, refer to the Spotipy official documentation, available at: https://spotipy.readthedocs.io/en/2.22.1/

<b>Python-dotenv</b>

We use the python-dotenv package to handle the API keys read as key-value pairs in our .env file. For further understanding and instructions on using python-dotenv, please refer to the official documentation available at the following link: https://pypi.org/project/python-dotenv/

In the code you will use dictionaries to manage our keys in the lines below:

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

<b>Example output based our messages prompt</b>

Based on the code below:

```python

    example_json = """[
    {"song": "Around the World", "artist":"Daft Punk"},
    {"song": "I Feel Love", "artist": "Donna Summer"},
    {"song": "Blue Monday", "artist": "New Order"},
    {"song": "Windowlicker", "artist": "Aphex Twin"},
    {"song": "Pump Up the Jam", "artist": "Technotronic"},
    {"song": "Born Slippy", "artist": "Underworld"},
    {"song": "Insomnia", "artist": "Faithless"},
    {"song": "The Man with the Red Face", "artist": "Laurent Garnier"},
    ]"""

    messages = [
        {"role": "system", "content": """You are a helpful playlist generating assistant.
        You should generate a list of songs and their artist according to the text prompt.
        You should return a JSON array, where each element follows this format: {"song": <song_title>, "artist": <artist_ name>}
        Do not include any other text. Do not include comments like 'Here is a playlist of breakup songs:
    '. Or 'Enjoy listening to these breakup songs!'. Do not give extra text. """
        },
        {"role": "user", "content": f"Generate a playlist of {count} songs based on the following prompt: {prompt}"},
        {"role": "assistant", "content": example_json}
    ]

    response = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo",
        max_tokens=400)
```

OpenAI's api will return the output in the following JSON format (in code this the resulr of printing our ```response``` variable).

```json
{
  "id": "chatcmpl-7YFMhW937uZ5xNTAnlTperMxnH8uk",
  "object": "chat.completion",
  "created": 1688396571,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "[\n    {\"song\": \"I Will Always Love You\", \"artist\": \"Whitney Houston\"}\n]"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 277,
    "completion_tokens": 22,
    "total_tokens": 299
  }
}
```
More to come.
