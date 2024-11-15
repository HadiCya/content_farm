import math
import random
import textwrap
from pydub import AudioSegment

from tiktok_voice import tts
from utils import *
from spotify_utils import *
from youtube_utils import *
from moviepy.editor import *
import config

FPS = config.FPS
SIZE = config.SIZE
STATIC_PATH = config.STATIC_PATH
ASSET_FILE_PATH = config.ASSET_FILE_PATH

def create_countdown_clip(number, FONT_NAME, FONT_SIZE, DURATION, REVEAL_DURATION):
    return TextClip(str(number), font=config.STATIC_PATH + FONT_NAME, fontsize=FONT_SIZE*3, color='white', stroke_color='black').set_duration(1).set_fps(FPS).set_position('center').set_start(DURATION - REVEAL_DURATION - number)


def process_clips(clips, id):
    # Concatenate and write the final video file
    final_clip = concatenate_videoclips(clips)
    output_file_name = f"{ASSET_FILE_PATH}final_videos/{id}.mp4"
    final_clip.write_videofile(
        output_file_name, audio=True, audio_codec="aac", fps=FPS)
    return output_file_name


def create_optimal_sound_clip(id, DURATION, MIN_AVG_VOLUME):
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


def create_background_clip(file_path, BACKGROUND_DURATION):
    background_clip = VideoFileClip(file_path, audio=False)
    max_start_time = max(10, background_clip.duration -
                         BACKGROUND_DURATION - 10)
    random_start_time = random.randint(10, int(max_start_time))
    background_clip = background_clip.subclip(
        random_start_time, random_start_time + BACKGROUND_DURATION).set_duration(BACKGROUND_DURATION)
    background_clip = background_clip.set_position(
        "center").resize(SIZE[1] / background_clip.size[1])
    return background_clip


def create_image_n_text_clips(duration, width, height, image_file_path, text, CHARACTER_WRAP, FONT_NAME, FONT_SIZE):
    image_clip = ImageClip(image_file_path).set_duration(
        duration).set_fps(FPS).resize(width=width, height=height).set_position("center")
    name_clip = TextClip(textwrap.fill(text, CHARACTER_WRAP), font=config.STATIC_PATH + FONT_NAME, fontsize=int(FONT_SIZE), color='white').set_duration(
        duration).set_fps(FPS).set_position(("center", (SIZE[1]//4)*3))

    return [image_clip, name_clip]


def create_tts_clip(text_to_speech_file_path, text):
    if os.path.isfile(text_to_speech_file_path):
        print("Text to Speech already downloaded!")
        text_to_speech = AudioFileClip(text_to_speech_file_path)
        return text_to_speech
    try:
        tts(config.SESSION_ID,
            req_text=text, filename=text_to_speech_file_path)
        text_to_speech = AudioFileClip(text_to_speech_file_path)
    except:
        print("Error Getting Text To Speech Audio")
    return text_to_speech


def create_intro(title, id, background_clip_file_path, FONT_NAME, FONT_SIZE, INTRO_DURATION, IMAGE_SIZE, image_url=None, subtitle=None):
    clips = []

    background_clip = create_background_clip(background_clip_file_path, INTRO_DURATION)
    clips.append(background_clip)

    intro_text = TextClip(title, font=config.STATIC_PATH + FONT_NAME, fontsize=int(FONT_SIZE), color='white').set_duration(
        INTRO_DURATION).set_fps(FPS).set_position(("center", SIZE[1]//4))
    clips.append(intro_text)

    if image_url and subtitle:
        image_file_path = f"{ASSET_FILE_PATH}assets/images/{id}.jpeg"
        download_image(image_url, image_file_path, IMAGE_SIZE)

        image_n_title = create_image_n_text_clips(
            INTRO_DURATION, 600, 600, image_file_path, subtitle, 20, FONT_NAME, FONT_SIZE)
        clips.extend(image_n_title)

    intro_clip = CompositeVideoClip(
        clips, size=SIZE).set_duration(INTRO_DURATION)

    text_to_speech_file_path = f"{ASSET_FILE_PATH}assets/snippets/{id}.mp3"
    text_to_speech = create_tts_clip(
        text_to_speech_file_path, f"{title}")
    intro_clip.audio = CompositeAudioClip([text_to_speech])

    return intro_clip
