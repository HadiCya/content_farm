import billboard
import random

from utils import *
from spotify_utils import *
from youtube_utils import *
from moviepy.editor import *


DURATION = 7
REVEAL_DURATION = 3
FPS = 24
SIZE = (1080, 1920)
IMAGE_SIZE = (640, 640)
FONT_SIZE = 72


chart = billboard.ChartData('artist-100')

artist_name = chart[0].artist

token = get_token()
result = search_for_artist(token, artist_name)
print(f'Artist: {artist_name}')
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)


clips = []
for i, song in enumerate(songs):
    song_name = remove_parentheses(song['name'])
    song_id = song['id']
    song_image_url = song['album']['images'][0]['url']
    image_file_path = f"assets/images/{song_id}.jpeg"

    # Create Blank Clip
    blank_clip = ColorClip(SIZE, (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255)), duration=DURATION)

    # Create Song Snippet Clip
    download_audio(f"{song_name} by {artist_name} Audio", song_id)
    random_num = random.randint(20, 40-DURATION)
    audio_clip = AudioFileClip(
        f'assets/snippets/{song_id}.mp3').subclip(random_num, random_num+DURATION).set_duration(DURATION)
    audio_clip = CompositeAudioClip([audio_clip])

    # Create Album Cover Image Clip
    # TODO: Create download images function
    download_image(song_image_url, image_file_path)
    album_cover_clip = ImageClip(image_file_path).set_duration(
        REVEAL_DURATION).set_fps(FPS).set_position("center")

    # Create Title and Song Artist Text Clip
    title_clip = TextClip(
        f'{song_name}', fontsize=FONT_SIZE, color='white').set_duration(REVEAL_DURATION).set_fps(FPS).set_position("center")

    # Assembling the clips
    song_clip = CompositeVideoClip(
        [blank_clip, album_cover_clip.set_start(DURATION-REVEAL_DURATION), title_clip.set_start(DURATION-REVEAL_DURATION)], SIZE).set_duration(DURATION)
    song_clip.audio = audio_clip
    clips.append(song_clip)

final_clip = concatenate_videoclips(clips)
final_clip.write_videofile(f"final_videos/{artist_name}.mp4", fps=FPS)
