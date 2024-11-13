import os
from apiclient.discovery import build
from pytubefix import YouTube
from pathlib import Path
import config


def search_video(title, maxResults=3):
    print(f"Searching For {title}")
    youtube = build('youtube', 'v3',
                    developerKey=config.YOUTUBE_KEY)
    request = youtube.search().list(q=title,
                                    part='snippet', type='video', maxResults=50)
    res = request.execute()
    youtubes = []
    for video in res['items']:
        yt = YouTube(
            f"https://www.youtube.com/watch?v={video['id']['videoId']}")
        print(f"https://www.youtube.com/watch?v={video['id']['videoId']}")
        if not yt.age_restricted:
            youtubes.append(yt)
        if len(youtubes) == maxResults:
            break
    print(youtubes)
    return youtubes


def download_audio(title, id):
    print(f'Attempting Video Search: {title}')
    FILE_NAME = f'{id}.mp3'

    SAVE_PATH = f"{config.ASSET_FILE_PATH}assets/snippets"

    if os.path.isfile(f"{SAVE_PATH}/{FILE_NAME}"):
        print("Audio already downloaded!")
        return

    youtubes = search_video(title)
    for yt in youtubes:
        try:
            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream:
                print(f'\nDownloading audio of: {yt.title}')
                audio_stream.download(SAVE_PATH, filename=FILE_NAME)
                print('Download completed!')
                return
        except Exception as e:
            print("Error:", e)
    print("Error: No audio streams found!")


def download_video(title, id, maxVideos):
    print(
        f'Attempting Download of {maxVideos} {title}{"s" if maxVideos > 1 else ""}')

    SAVE_PATH = f"{config.ASSET_FILE_PATH}assets/videos"

    if os.path.isfile(f"{SAVE_PATH}/{id}-{maxVideos-1}.mp4"):
        print("Videos already downloaded!")
        return

    youtubes = search_video(title, maxVideos*3)
    print("yay")
    for i in range(maxVideos):
        yt = youtubes[i]
        try:
            video_stream = yt.streams.get_highest_resolution()
            if os.path.isfile(f"{SAVE_PATH}/{id}-{i}.mp4"):
                print(f"Video {i} already downloaded!")
            elif video_stream:
                print(f'\nDownloading video of: {yt.title}')
                video_stream.download(SAVE_PATH, filename=f'{id}-{i}.mp4')
                print('Download completed!')
            else:
                i -= 1
        except Exception as e:
            i -= 1
            print("Error:", e)
