<b> <h1> GPT-3.5-turbo AI Spotify Playlist Generator </h1> </b>

<img src="https://github.com/typedwires/OpenAI-Spotify-Generator/blob/main/playlist.png" width="800">

Project based on Colt Steele's Mastering OpenAI Python APIs: Unleash ChatGPT and GPT4.

<b> Example of how to generate a Spotify playlist </b>

Once the project is set up (see instructions below) in the command line, nagivate to the project and run

```shell
python app.py -p "90s and early 2000s rock love songs" -n 10
```

Where ```-p``` represents the prompt and playlist title, and ``-n`` denotes the number of songs to generate.

<b>Creating your Spotify Web API to obtain Spotify Client ID and Client Secret keys</b>

Follow the instructions here: https://developer.spotify.com/documentation/web-api

Also, inside your Spotify WEB API set your ```Website``` and ``Redirect URIs`` both to```http://localhost:9999```

<b>Finding your OpenAI secret keys</b>

Read the instructions here: https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key

<b>Create an .env text file to add your API keys</b>

Add your:

SPOTIFY CLIENT ID <br>
SPOTIFY CLIENT SECRET <br>
OPENAI API KEY <br>

in the following format in your .env file:

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

OpenAI's api will return the output in the following JSON format (in code this the result of printing our ```response``` variable).

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
````

Based on the above format we write

```python
playlist = json.loads(response["choices"][0]["message"]["content"])
```
and `print(playlist)` outputs: 

```
[{'song': "I Will Always Love You", 'artist': 'Whitney Houston'}]
```
The output above is then used within the Spotipy api to search for the artist/song as seen in the code below:

```python
for item in playlist:
    artist, song = item["artist"], item["song"]
    query = f"{song} {artist}"
    search_results = sp.search(q=query, type="track", limit=10)
    track_ids.append(search_results["tracks"]["items"][0]["id"])
```
`print(search_results)` will output data like:

```python
[{'song': "I Don't Want to Miss a Thing", 'artist': 'Aerosmith'}]

{'tracks': {'href': 'https://api.spotify.com/v1/search?query=I+Don%27t+Want+to+Miss+a+Thing+Aerosmith&type=track&offset=0&limit=10', 'items':

[{'album': {'album_type': 'compilation', 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/0LyfQWJT6nXafLPZqxe9Of'},

'href': 'https://api.spotify.com/v1/artists/0LyfQWJT6nXafLPZqxe9Of', 'id': '0LyfQWJT6nXafLPZqxe9Of', 'name': 'Various Artists', 'type': 'artist',

'uri': 'spotify:artist:0LyfQWJT6nXafLPZqxe9Of'}], 'available_markets': ['AD', 'AE', 'AG', 'AL', 'AM', 'AO', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB',

'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BN', 'BO', 'BR', 'BS', 'BT', 'BW', 'BY', 'BZ', 'CA', 'CD', 'CG', 'CH', 'CI', 'CL', 'CM', 'CO', 'CR',

'CV', 'CW', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'ET', 'FI', 'FJ', 'FM', 'FR', 'GA', 'GB', 'GD', 'GE', 'GH',

'GM', 'GN', 'GQ', 'GR', 'GT', 'GW', 'GY', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG',

'KH', 'KI', 'KM', 'KN', 'KR', 'KW', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MG', 'MH',

'MK', 'ML', 'MN', 'MO', 'MR', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NE', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE',

'PG', 'PH', 'PK', 'PL', 'PS', 'PT', 'PW', 'PY', 'QA', 'RO', 'RS', 'RW', 'SA', 'SB', 'SC', 'SE', 'SG', 'SI', 'SK', 'SL', 'SM', 'SN', 'SR', 'ST',

'SV', 'SZ', 'TD', 'TG', 'TH', 'TJ', 'TL', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VC', 'VE', 'VN', 'VU', 'WS',

'XK', 'ZA', 'ZM', 'ZW'], 'external_urls': {'spotify': 'https://open.spotify.com/album/4f7HKjBnjpMsDBDTHYV890'}, 'href': 'https://api.spotify.com

/v1/albums/4f7HKjBnjpMsDBDTHYV890', 'id': '4f7HKjBnjpMsDBDTHYV890', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image

/ab67616d0000b273da8d92affd796f7e20af7375', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image

/ab67616d00001e02da8d92affd796f7e20af7375', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d00004851da8d92affd796f7e20af7375',

'width': 64}], 'name': 'Armageddon - The Album', 'release_date': '1998-06-23', 'release_date_precision': 'day', 'total_tracks': 14, 'type':

'album', 'uri': 'spotify:album:4f7HKjBnjpMsDBDTHYV890'}, 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist

/7Ey4PD4MYsKc5I2dolUwbH'}, 'href': 'https://api.spotify.com/v1/artists/7Ey4PD4MYsKc5I2dolUwbH', 'id': '7Ey4PD4MYsKc5I2dolUwbH', 'name': 'Aerosmith',

'type': 'artist', 'uri': 'spotify:artist:7Ey4PD4MYsKc5I2dolUwbH'}], 'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL',

'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY',

'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI',

'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ',

'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT',

'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE',

'PW', 'PG', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD',

'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD',

'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'], 'disc_number': 1, 'duration_ms': 298760, 'explicit': False, 'external_ids': {'isrc': 'USSM19801545'},

'external_urls': {'spotify': 'https://open.spotify.com/track/225xvV8r1yKMHErSWivnow'}, 'href': 'https://api.spotify.com/v1/tracks
/225xvV8r1yKMHErSWivnow', 'id': '225xvV8r1yKMHErSWivnow',..
```
and `search_results["tracks"]["items"][0]["id"]` will output (from the above example):

`225xvV8r1yKMHErSWivnow`

More to come.
