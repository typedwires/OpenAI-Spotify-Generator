import spotipy
from dotenv import dotenv_values
import openai
import json
import argparse

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

parser = argparse.ArgumentParser(description="Command line song utility")
parser.add_argument("-p", type=str, default="Fun songs", help="The promp to describe the playlist.")
parser.add_argument("-n", type=int, default=8, help="The number of songs to add to the playlist.")

args = parser.parse_args()


def get_playlist(prompt, count=8):
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
    
    playlist = json.loads(response["choices"][0]["message"]["content"])
    return playlist

playlist = get_playlist(args.p, args.n)
#print(playlist)


sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        client_id = config["SPOTIFY_CLIENT_ID"],
        client_secret = config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://localhost:9999",
        scope="playlist-modify-private"
    )
)


current_user = sp.current_user()
track_ids = []
assert current_user is not None

for item in playlist:
    artist, song = item["artist"], item["song"]
    query = f"{song} {artist}"
    search_results = sp.search(q=query, type="track", limit=10)
    track_ids.append(search_results["tracks"]["items"][0]["id"])


created_playlist = sp.user_playlist_create(
    current_user["id"],
    public=False,
    name=args.p
)

sp.user_playlist_add_tracks(current_user["id"], created_playlist["id"], track_ids) 

