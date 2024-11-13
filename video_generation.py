from datetime import datetime
from os import listdir
from os.path import isfile, join
import textwrap
import random

import numpy as np

from tiktok_voice import tts

from utils import *
from spotify_utils import *
from video_utils import *
from youtube_utils import *
from moviepy.editor import *
import config

from PIL import Image

from elevenlabs import play, save
from elevenlabs.client import ElevenLabs

def create_fake_conversation_video(messages, image_file_path):
    FPS = 24
    SIZE = (1080, 1920)
    client = ElevenLabs(
        api_key=config.ELEVENLABS_KEY,
    )

    TTS_DURATION_SUM = 0

    imessage_image = Image.open(image_file_path)
    screenshots = []
    messages = [message for message in messages if message.get("text", None)]

    for i in range(0, len(messages), 3):
        y_start = messages[i]["bubble_y"]-50
        y_end = messages[i]["bubble_bottom_y"]+50
        for j in range(3):
            try:
                for x in range(j+1):
                    sub_message = messages[i+x]
                    y_end = sub_message['bubble_bottom_y']+50

                audio = client.generate(
                    text=messages[i+j]["text"],
                    voice="Alice" if messages[i +
                                               j]["gender"] == "female" else "Brian",
                    model="eleven_monolingual_v1"
                )
                save(audio, "temp_text.mp3")

                tts_audio_clip = AudioFileClip(
                    f"temp_text.mp3").set_start(TTS_DURATION_SUM)
                TTS_DURATION = tts_audio_clip.duration + 0.1

                imessage_image_array = np.array(
                    imessage_image.crop((0, y_start, 800, y_end)))
                sub_message_clip = ImageClip(
                    imessage_image_array).set_position("center").set_start(TTS_DURATION_SUM).set_fps(FPS).set_duration(TTS_DURATION)  # duration=tts duration

                TTS_DURATION_SUM += TTS_DURATION

                sub_message_clip.audio = tts_audio_clip

                screenshots.append(sub_message_clip)
            except Exception as e:
                print(f"Failed with error: {e}")

    download_video("Minecraft Parkour Gameplay", "minecraft-parkour", 1)
    background_clip = create_background_clip(
        f"{ASSET_FILE_PATH}assets/videos/minecraft-parkour-0.mp4", TTS_DURATION_SUM)

    final_clip = [CompositeVideoClip([background_clip, *screenshots], SIZE)]

    process_clips(final_clip, "fake_convo")


def create_artist_video(artist_name, token, SONG_COUNT=5, IMAGE_SIZE=(928, 928), DURATION=6, REVEAL_DURATION=1, FONT_NAME="TikTok.tff", FONT_SIZE=96):
    result = search_for_artist(token, artist_name)
    print(f'Artist: {artist_name}')
    artist_id = result["id"]
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
    intro_clip = create_intro("Guess the song", artist_id,
                              f"{ASSET_FILE_PATH}assets/videos/{last_music_video}", config.STATIC_PATH + FONT_NAME, FONT_SIZE, 2, IMAGE_SIZE, artist_image_url, artist_name)
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
            f"{ASSET_FILE_PATH}assets/videos/{last_music_video}", DURATION)

        download_image(song_image_url, image_file_path, IMAGE_SIZE)
        album_cover_clip, title_clip = create_image_n_text_clips(
            REVEAL_DURATION, IMAGE_SIZE[0], IMAGE_SIZE[1], image_file_path, song_name, 20, config.STATIC_PATH + FONT_NAME, FONT_SIZE)

        # Create Song Count Text Clip
        sound_count_clip = TextClip(
            f'Song {i+1}/{len(songs)}', font=config.STATIC_PATH + FONT_NAME, fontsize=FONT_SIZE, color='white', stroke_width=2, stroke_color='black') \
            .set_duration(DURATION).set_fps(FPS).set_position(("center", (SIZE[1]//7)))

        # Create Countdown
        countdown_clips = [create_countdown_clip(
            number, config.STATIC_PATH + FONT_NAME, FONT_SIZE, DURATION, REVEAL_DURATION) for number in range(1, DURATION - REVEAL_DURATION)]

        # AUDIO COMPONENTS
        composite_audio = []
        # Create Song Snippet Clip
        download_audio(f"{song_name} by {artist_name} Official Audio", song_id)

        song_clip_snippet = create_optimal_sound_clip(song_id, DURATION, -11)
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

    # Add intro clip at the beginning
    clips.insert(0, intro_clip)

    # Apply transformation to each clip and create a composite video clip
    slided_clips = [CompositeVideoClip([clip.fx(transfx.slide_out, 0.4, 'right')])
                    for clip in clips]

    release.append(process_clips(slided_clips, remove_punc_n_spaces(
        artist_name)))
    return release


# def create_billboard_video(songs):
#     video_id = "asmr"

#     # Download the five videos
#     download_video(
#         f'breaking glass oddly satisfying video cutting soap ice breaking shaving', video_id, 5)

#    # Retrieve downloaded videos
#     all_videos = [f for f in listdir(f"{config.ASSET_FILE_PATH}assets/videos")
#                   if isfile(join(f"{config.ASSET_FILE_PATH}assets/videos", f))]
#     background_videos = [
#         f for f in all_videos if f.startswith(video_id + "-")]
#     print(background_videos)

#     last_background_video = random.choice(background_videos)
#     intro_clip = create_intro(
#         "Rank the Songs", "rank-the-songs", f"{ASSET_FILE_PATH}assets/videos/{last_background_video}")

#     # Begin Creating Clips
#     clips = []

#     for i, song in enumerate(songs):
#         song_id = str(hash(remove_punc_n_spaces(song)))
#         newly_selected_background_video = random.choice(background_videos)

#         last_background_video = newly_selected_background_video

#         composite_audio = []
#         download_audio(f"{song} Official Audio", song_id)
#         song_clip_snippet = create_optimal_sound_clip(song_id)
#         composite_audio.append(song_clip_snippet)

#         background_clip = create_background_clip(
#             f"{ASSET_FILE_PATH}assets/videos/{last_background_video}")

#         title_clip = TextClip(
#             f'{textwrap.fill(song, CHARACTER_WRAP)}', font=FONT_PATH, fontsize=FONT_SIZE, color='white', stroke_width=2, stroke_color='black') \
#             .set_duration(DURATION).set_fps(FPS).set_position(("center", SIZE[1]//4))

#         # Creating the list clip
#         number_list = "\n".join([f"{i}." for i in range(1, 6)])
#         list_clip = TextClip(
#             f'{textwrap.fill(number_list, CHARACTER_WRAP)}',
#             font=FONT_PATH,
#             fontsize=FONT_SIZE,
#             color='white',
#             stroke_width=2,
#             stroke_color='black'
#         ).set_duration(REVEAL_DURATION).set_fps(FPS).set_position(("left", SIZE[1] - 100))

#         # Assembling the clips
#         song_clip = CompositeVideoClip(
#             [background_clip, title_clip, list_clip],
#             SIZE).set_duration(DURATION)

#         song_clip.audio = CompositeAudioClip(composite_audio)
#         clips.append(song_clip)

#     # adds intro and writes to final_videos dir
#     now = datetime.now()

#     release = []
#     clips.insert(0, intro_clip)
#     release.append(process_clips(clips, remove_punc_n_spaces(now.strftime("%m/%d/%Y, %H:%M:%S")),
#                                  "What were your top fives??"))
#     return release
