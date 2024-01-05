import math
import random
from pydub import AudioSegment

from utils import *
from spotify_utils import *
from youtube_utils import *
from moviepy.editor import *
import config

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


def create_countdown_clip(number):
    return TextClip(str(number), font=FONT_PATH, fontsize=FONT_SIZE*3, color='white', stroke_color='black').set_duration(1).set_fps(FPS).set_position('center').set_start(DURATION - REVEAL_DURATION - number)


def process_clips(clips, id, description):
    # Concatenate and write the final video file
    final_clip = concatenate_videoclips(clips)
    output_file_name = f"{ASSET_FILE_PATH}final_videos/{id}.mp4"
    final_clip.write_videofile(
        output_file_name, audio=True, audio_codec="aac", fps=FPS)
    return {
        'video': output_file_name,
        'description': description
    }


def create_optimal_sound_clip(id):
    MAX_TRIES = 20  # Define a maximum limit for tries

    # Load audio file
    song_clip_file_path = f"{ASSET_FILE_PATH}assets/snippets/{id}.mp3"
    audio_clip = AudioFileClip(song_clip_file_path)
    song_total_duration = int(audio_clip.duration)

    # Convert to AudioSegment for volume checking
    audio_segment_file = AudioSegment.from_file(song_clip_file_path)

    tries = 0
    max_volume = -math.inf
    best_audio_clip = None

    print("Finding optimal audio snippet.")
    while True:
        random_num = random.randint(1, song_total_duration - DURATION - 10)

        # Take a slice of the segment
        slice_start_ms = random_num*1000  # convert to ms
        slice_end_ms = (random_num + DURATION)*1000  # convert to ms
        audio_segment_slice = audio_segment_file[slice_start_ms:slice_end_ms]

        # Check average volume
        if audio_segment_slice.dBFS >= MIN_AVG_VOLUME:
            # If volume is fine, create final audio clip and exit loop
            final_audio_clip = audio_clip.subclip(
                random_num, random_num + DURATION).set_duration(DURATION)
            break
        else:
            # If this segment is louder than all previous ones, store it
            if audio_segment_slice.dBFS > max_volume:
                max_volume = audio_segment_slice.dBFS
                best_audio_clip = audio_clip.subclip(
                    random_num, random_num + DURATION).set_duration(DURATION)

            tries += 1
            if tries == MAX_TRIES:
                print(
                    f"Maximum tries reached. Using segment with loudest volume: {max_volume} dBFS.")
                final_audio_clip = best_audio_clip.volumex(
                    max_volume/MIN_AVG_VOLUME)
                break
    return final_audio_clip


def create_background_clip(file_path):
    background_clip = VideoFileClip(file_path, audio=False)
    max_start_time = max(10, background_clip.duration - DURATION - 10)
    random_start_time = random.randint(10, int(max_start_time))
    background_clip = background_clip.subclip(
        random_start_time, random_start_time + DURATION).set_duration(DURATION)
    background_clip = background_clip.set_position(
        "center").resize(SIZE[1] / background_clip.size[1])
    return background_clip
