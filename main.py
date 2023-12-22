import billboard
import json

from utils import *
from spotify_utils import *
from youtube_utils import *

token = get_token()

chart = billboard.ChartData('artist-100')

top_artist = chart[62].artist

result = search_for_artist(token, top_artist)
print(result["name"])
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

for i, song in enumerate(songs):
    print(f"{i+1}. {remove_parentheses(song['name'])}")
    download_audio(search_video(f"{song['name']} by {result['name']} Audio"))
