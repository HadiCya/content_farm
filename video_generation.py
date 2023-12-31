# Standard library imports
from os import listdir
from os.path import isfile, join
import random
import textwrap
from datetime import datetime

# Third-party imports
from moviepy.editor import *
from tiktok_voice import tts

# Local application/library specific imports
import config
from spotify_utils import *
from utils import *
from video_utils import *
from youtube_utils import *

DURATION = config.DURATION
REVEAL_DURATION = config.REVEAL_DURATION
FPS = config.FPS
SIZE = config.SIZE
IMAGE_SIZE = config.IMAGE_SIZE
FONT_SIZE = config.FONT_SIZE
INTRO_DURATION = config.INTRO_DURATION
CHARACTER_WRAP = config.CHARACTER_WRAP
FONT_PATH = config.FONT_PATH
ASSET_FILE_PATH = config.ASSET_FILE_PATH
MIN_AVG_VOLUME = config.MIN_AVG_VOLUME
SONG_COUNT = config.SONG_COUNT


def create_intro(artist_image_url, artist_name, artist_id, background_clip_file_path):
    image_file_path = f"{ASSET_FILE_PATH}assets/images/{artist_id}.jpeg"

    background_clip = create_background_clip(background_clip_file_path)

    intro_text = TextClip("Guess the Song", font=FONT_PATH, fontsize=int(FONT_SIZE), color='white').set_duration(
        INTRO_DURATION).set_fps(FPS).set_position(("center", SIZE[1]//4))
    download_image(artist_image_url, image_file_path, IMAGE_SIZE)
    artist_image_clip = ImageClip(image_file_path).set_duration(
        INTRO_DURATION).set_fps(FPS).resize(width=600).set_position("center")
    artist_name_clip = TextClip(textwrap.fill(artist_name, CHARACTER_WRAP), font=FONT_PATH, fontsize=int(FONT_SIZE), color='white').set_duration(
        INTRO_DURATION).set_fps(FPS).set_position(("center", (SIZE[1]//4)*3))

    intro_clip = CompositeVideoClip(
        [background_clip, artist_image_clip, intro_text, artist_name_clip], size=SIZE).set_duration(INTRO_DURATION)

    text_to_speech_file_path = f"{ASSET_FILE_PATH}assets/snippets/{artist_id}.mp3"

    if os.path.isfile(text_to_speech_file_path):
        print("Text to Speech already downloaded!")
        text_to_speech = AudioFileClip(text_to_speech_file_path)
        intro_clip.audio = CompositeAudioClip([text_to_speech])
        return intro_clip

    try:
        tts(config.SESSION_ID,
            req_text=f"Guess the {artist_name} song", filename=text_to_speech_file_path)
        text_to_speech = AudioFileClip(text_to_speech_file_path)
        intro_clip.audio = CompositeAudioClip([text_to_speech])
    except:
        print("Error Getting Text To Speech Audio")

    return intro_clip

def create_billboard_intro (video_id, background_clip_file_path):

    background_clip = create_background_clip(background_clip_file_path)

    intro_text = TextClip("Rank the Song", font=FONT_PATH, fontsize=int(FONT_SIZE), color='white').set_duration(
        INTRO_DURATION).set_fps(FPS).set_position(("center", SIZE[1]//4))

    intro_clip = CompositeVideoClip(
        [background_clip, intro_text], size=SIZE).set_duration(INTRO_DURATION)

    text_to_speech_file_path = f"{ASSET_FILE_PATH}assets/snippets/{video_id}.mp3"

    if os.path.isfile(text_to_speech_file_path):
        print("Text to Speech already downloaded!")
        text_to_speech = AudioFileClip(text_to_speech_file_path)
        intro_clip.audio = CompositeAudioClip([text_to_speech])
        return intro_clip

    try:
        tts(config.SESSION_ID,
            req_text=f"Rank the song", filename=text_to_speech_file_path)
        text_to_speech = AudioFileClip(text_to_speech_file_path)
        intro_clip.audio = CompositeAudioClip([text_to_speech])
    except:
        print("Error Getting Text To Speech Audio")

    return intro_clip


def create_artist_video(artist_name, token):
    result = search_for_artist(token, artist_name)
    print(f'Artist: {artist_name}')
    artist_id = result["id"]
    print(f"Artist ID: {artist_id}")
    artist_image_url = result["images"][0]["url"]
    songs = get_songs_by_artist(token, artist_id)
    random.shuffle(songs)
    songs = songs[:SONG_COUNT]

    # Download artist video
    max_music_videos = min(SONG_COUNT, int(
        result['popularity'])*SONG_COUNT // 100)

    download_video(f'{artist_name} Music Video', artist_id, max_music_videos)
    artist_music_videos = [f for f in listdir(
        f"{ASSET_FILE_PATH}assets/videos") if isfile(join(f"{ASSET_FILE_PATH}assets/videos", f))]
    artist_music_videos = [
        f for f in artist_music_videos if f.startswith(artist_id + "-")]

    last_music_video = random.choice(artist_music_videos)
    intro_clip = create_intro(
        artist_image_url, artist_name, artist_id, f"{ASSET_FILE_PATH}assets/videos/{last_music_video}")

    # Begin Creating Clips
    clips = []

    for i, song in enumerate(songs):
        song_name = remove_parentheses(song['name'])
        song_id = song['id']
        song_image_url = song['album']['images'][0]['url']
        image_file_path = f"{ASSET_FILE_PATH}assets/images/{song_id}.jpeg"

        # VISUAL COMPONENTS

        # Create Background Clip
        newly_selected_music_video = random.choice(artist_music_videos)
        while (last_music_video == newly_selected_music_video and len(artist_music_videos) > 1):
            newly_selected_music_video = random.choice(artist_music_videos)

        last_music_video = newly_selected_music_video

        background_clip = create_background_clip(
            f"{ASSET_FILE_PATH}assets/videos/{last_music_video}")

        # Create Album Cover Image Clip
        download_image(song_image_url, image_file_path, IMAGE_SIZE)
        album_cover_clip = ImageClip(image_file_path).set_duration(
            REVEAL_DURATION).set_fps(FPS).set_position("center")

        # Create Title Text Clip
        title_clip = TextClip(
            f'{textwrap.fill(song_name, CHARACTER_WRAP)}', font=FONT_PATH, fontsize=FONT_SIZE, color='white', stroke_width=2, stroke_color='black') \
            .set_duration(REVEAL_DURATION).set_fps(FPS).set_position(("center", (SIZE[1]//4)*3))

        # Create Song Count Text Clip
        sound_count_clip = TextClip(
            f'Song {i+1}/{len(songs)}', font=FONT_PATH, fontsize=FONT_SIZE, color='white', stroke_width=2, stroke_color='black') \
            .set_duration(DURATION).set_fps(FPS).set_position(("center", (SIZE[1]//7)))

        # Create Countdown
        countdown_clips = [create_countdown_clip(
            number) for number in range(1, DURATION - REVEAL_DURATION)]

        # AUDIO COMPONENTS
        composite_audio = []
        song_clip_snippet = create_song_snippet_clip(
            song_name, song_id, artist_name)
        composite_audio.append(song_clip_snippet)

        # Create Sound Effects
        checkmark_sound = AudioFileClip(
            f"template/checkmark.mp3").set_start(DURATION-REVEAL_DURATION)
        composite_audio.append(checkmark_sound)

        clock_sound = AudioFileClip(
            f"template/clock.mp3").set_start(1).set_duration(DURATION-REVEAL_DURATION-1)
        composite_audio.append(clock_sound)

        swipe_sound = AudioFileClip(
            f"template/swipe.mp3").set_start(DURATION-0.5)
        composite_audio.append(swipe_sound)

        # ASSEMBLING EVERYTHING AND STORING INTO FINAL ARRAY

        # Assembling the clips
        song_clip = CompositeVideoClip(
            [background_clip,
             *countdown_clips,
             album_cover_clip.set_start(
                 DURATION-REVEAL_DURATION),
             sound_count_clip,
             title_clip.set_start(
                 DURATION-REVEAL_DURATION)],
            SIZE).set_duration(DURATION)

        song_clip.audio = CompositeAudioClip(composite_audio)
        clips.append(song_clip)

    release = []
    release.append(process_clips(clips, intro_clip, artist_name))
    return release

def create_billboard_video(songs):

    # Download the five videos
    for song in enumerate(songs[:5]):
        download_video(f'{song} Music Video', song, 1)

   # Retrieve downloaded videos
    billboard_music_videos = [f for f in listdir(f"{config.ASSET_FILE_PATH}assets/videos")
                          if isfile(join(f"{config.ASSET_FILE_PATH}assets/videos", f))]
    
    last_music_video = random.choice(billboard_music_videos)
    intro_clip = create_billboard_intro(str(songs[0]), f"{ASSET_FILE_PATH}assets/videos/{last_music_video}")
    
    # Begin Creating Clips
    clips = []
    
    for song in enumerate(songs):
        newly_selected_music_video = random.choice(billboard_music_videos)

        last_music_video = newly_selected_music_video
        
        composite_audio = []
        song_clip_snippet = create_song_snippet_clip(
            str(song[1]), str(song[1]))
        composite_audio.append(song_clip_snippet)

        background_clip = create_background_clip(
            f"{ASSET_FILE_PATH}assets/videos/{last_music_video}")
        
        title_clip = TextClip(
            f'{textwrap.fill(str(song[1]), CHARACTER_WRAP)}', font=FONT_PATH, fontsize=FONT_SIZE, color='white', stroke_width=2, stroke_color='black') \
            .set_duration(REVEAL_DURATION).set_fps(FPS).set_position(("center", SIZE[1]//4))
            
        # Creating the list clip
        number_list = "\n".join([f"{i}." for i in range(1, 6)])
        list_clip = TextClip(
            f'{textwrap.fill(number_list, CHARACTER_WRAP)}',
            font=FONT_PATH,
            fontsize=FONT_SIZE,
            color='white',
            stroke_width=2,
            stroke_color='black'
        ).set_duration(REVEAL_DURATION).set_fps(FPS).set_position(("left", SIZE[1] - 100))
        
        # Assembling the clips
        song_clip = CompositeVideoClip(
            [background_clip,title_clip,list_clip],
            SIZE).set_duration(DURATION)

        song_clip.audio = CompositeAudioClip(composite_audio)
        clips.append(song_clip)
    
    #adds intro and writes to final_videos dir   
    process_clips(clips, intro_clip)