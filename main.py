from os import listdir
from os.path import isfile, join
import textwrap
import billboard
import random
from tiktok_voice import tts

from utils import *
from spotify_utils import *
from youtube_utils import *
from moviepy.editor import *


DURATION = 9
REVEAL_DURATION = 3
FPS = 24
SIZE = (1080, 1920)
IMAGE_SIZE = (928, 928)
FONT_SIZE = 72
INTRO_DURATION = 2
CHARACTER_WRAP = 24

chart = billboard.ChartData('artist-100')
artist_name = chart[1].artist


def create_countdown_clip(number):
    return TextClip(str(number), fontsize=FONT_SIZE*4, color='white').set_duration(1).set_fps(FPS).set_position('center').set_start(number)


def create_intro(artist_image_url, artist_name, artist_id, last_music_video):
    image_file_path = f"assets/images/{artist_id}.jpeg"

    background_clip = VideoFileClip(
        f'assets/videos/{last_music_video}', audio=False)
    max_start_time = max(0, background_clip.duration - DURATION - 10)
    random_start_time = random.randint(0, int(max_start_time))
    background_clip = background_clip.subclip(
        random_start_time, random_start_time + DURATION).set_duration(DURATION)
    background_clip = background_clip.set_position(
        "center").resize(SIZE[1] / background_clip.size[1])

    intro_text = TextClip("Guess the Song", fontsize=int(FONT_SIZE*1.5), color='white').set_duration(
        INTRO_DURATION).set_fps(FPS).set_position(("center", SIZE[1]//4))
    download_image(artist_image_url, image_file_path, IMAGE_SIZE)
    artist_image_clip = ImageClip(image_file_path).set_duration(
        INTRO_DURATION).set_fps(FPS).resize(width=600)
    artist_image_clip = artist_image_clip.set_position("center")
    artist_name_clip = TextClip(artist_name, fontsize=int(FONT_SIZE*1.5), color='white').set_duration(
        INTRO_DURATION).set_fps(FPS).set_position(("center", (SIZE[1]//4)*3))

    intro_clip = CompositeVideoClip(
        [background_clip, artist_image_clip, intro_text, artist_name_clip], size=SIZE).set_duration(INTRO_DURATION)

    text_to_speech_file_path = f"assets/snippets/{artist_id}.mp3"

    load_dotenv()
    session_id = os.getenv("SESSION_ID")

    try:
        tts(session_id,
            req_text=f"Guess the {artist_name} song", filename=text_to_speech_file_path)
        text_to_speech = AudioFileClip(text_to_speech_file_path)
        intro_clip.audio = CompositeAudioClip([text_to_speech])
    except:
        print("Error Getting Text To Speech Audio")

    return intro_clip


def create_artist_video(artist_name, token, split=True):
    result = search_for_artist(token, artist_name)
    print(f'Artist: {artist_name}')
    artist_id = result["id"]
    artist_image_url = result["images"][0]["url"]
    songs = get_songs_by_artist(token, artist_id)
    random.shuffle(songs)

    # Download artist video
    download_video(f'{artist_name} Music Video', artist_id,
                   int(result['popularity']) // 18)
    artist_music_videos = [f for f in listdir(
        f'assets/videos') if isfile(join(f'assets/videos', f))]
    artist_music_videos = [
        f for f in artist_music_videos if f.startswith(artist_id + "-")]

    last_music_video = random.choice(artist_music_videos)
    intro_clip = create_intro(
        artist_image_url, artist_name, artist_id, last_music_video)

    # Begin Creating Clips
    clips = []

    for song in songs:
        song_name = remove_parentheses(song['name'])
        song_id = song['id']
        song_image_url = song['album']['images'][0]['url']
        image_file_path = f"assets/images/{song_id}.jpeg"

        # VISUAL COMPONENTS

        # Create Background Clip
        newly_selected_music_video = random.choice(artist_music_videos)
        while (last_music_video == newly_selected_music_video and len(artist_music_videos) > 1):
            newly_selected_music_video = random.choice(artist_music_videos)

        last_music_video = newly_selected_music_video

        background_clip = VideoFileClip(
            f'assets/videos/{last_music_video}', audio=False)
        max_start_time = max(0, background_clip.duration - DURATION - 10)
        random_start_time = random.randint(0, int(max_start_time))
        background_clip = background_clip.subclip(
            random_start_time, random_start_time + DURATION).set_duration(DURATION)
        background_clip = background_clip.set_position(
            "center").resize(SIZE[1] / background_clip.size[1])

        # Create Album Cover Image Clip
        download_image(song_image_url, image_file_path, IMAGE_SIZE)
        album_cover_clip = ImageClip(image_file_path).set_duration(
            REVEAL_DURATION).set_fps(FPS).set_position("center")

        # Create Title and Song Artist Text Clip
        title_clip = TextClip(
            f'{textwrap.fill(song_name, CHARACTER_WRAP)}', fontsize=FONT_SIZE, color='white') \
            .set_duration(REVEAL_DURATION).set_fps(FPS).set_position(("center", (SIZE[1]//4)*3))
        title_background_clip = ColorClip(
            ((FONT_SIZE - 10)*len(remove_punc_n_spaces(song_name)), FONT_SIZE*(1+(len(song_name)//CHARACTER_WRAP))), (0, 0, 0), duration=DURATION) \
            .set_position(("center", (SIZE[1]//4)*3))

        # Create Countdown
        countdown_clips = [create_countdown_clip(
            number) for number in range(1, DURATION - REVEAL_DURATION)]

        # AUDIO COMPONENTS

        # Create Song Snippet Clip
        download_audio(f"{song_name} by {artist_name} Audio", song_id)
        random_num = random.randint(20, 50-DURATION)
        audio_clip = AudioFileClip(
            f'assets/snippets/{song_id}.mp3').subclip(random_num, random_num+DURATION).set_duration(DURATION)

        # Create Sound Effects
        checkmark_sound = AudioFileClip('assets/template/checkmark.mp3')
        clock_sound = AudioFileClip('assets/template/clock.mp3')

        # ASSEMBLING EVERYTHING AND STORING INTO FINAL ARRAY

        # Assembling the clips
        song_clip = CompositeVideoClip(
            [background_clip,
             *countdown_clips,
             album_cover_clip.set_start(
                 DURATION-REVEAL_DURATION),
             title_background_clip.set_start(
                 DURATION-REVEAL_DURATION),
             title_clip.set_start(
                 DURATION-REVEAL_DURATION)],
            SIZE).set_duration(DURATION)

        song_clip.audio = CompositeAudioClip(
            [audio_clip, clock_sound.set_start(1).set_duration(DURATION-REVEAL_DURATION-1), checkmark_sound.set_start(DURATION-REVEAL_DURATION)])
        clips.append(song_clip)

    if split:
        clips_1 = clips[:len(clips)//2]
        clips_1.insert(0, intro_clip)
        slided_clips_1 = [CompositeVideoClip(
            [clip.fx(transfx.slide_out, 0.4, 'right')]) for clip in clips_1]
        final_clip_1 = concatenate_videoclips(slided_clips_1)
        final_clip_1.write_videofile(
            f"final_videos/{artist_name}-1.mp4",
            audio=True,
            audio_codec="aac",
            threads=8,
            fps=FPS)

        clips_2 = clips[len(clips)//2:]
        clips_2.insert(0, intro_clip)
        slided_clips_2 = [CompositeVideoClip(
            [clip.fx(transfx.slide_out, 0.4, 'right')]) for clip in clips_2]
        final_clip_2 = concatenate_videoclips(slided_clips_2)
        final_clip_2.write_videofile(
            f"final_videos/{artist_name}-2.mp4",
            audio=True,
            audio_codec="aac",
            threads=8,
            fps=FPS)
    else:
        clips.insert(0, intro_clip)
        slided_clips = [CompositeVideoClip(
            [clip.fx(transfx.slide_out, 0.4, 'right')]) for clip in clips]
        final_clip = concatenate_videoclips(slided_clips)
        final_clip.write_videofile(
            f"final_videos/{artist_name}.mp4",
            audio=True,
            audio_codec="aac",
            threads=8,
            fps=FPS)


create_artist_video("Taylor Swift", get_token())
