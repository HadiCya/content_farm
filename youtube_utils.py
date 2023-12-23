from dotenv import load_dotenv
import os
from apiclient.discovery import build
from pytube import YouTube
from pathlib import Path


# TODO: Optimize video searching to work in batches, both 1 and 50 results cost 100 tokens (Low Priority)
def search_video(title, maxResults=1):
    load_dotenv(override=True)
    api_key = os.getenv("YOUTUBE_KEY")

    youtube = build('youtube', 'v3',
                    developerKey=api_key)

    request = youtube.search().list(q=title,
                                    part='snippet', type='video', maxResults=maxResults, videoDuration='medium')
    res = request.execute()
    urls = []
    for video in res['items']:
        urls.append(
            f"https://www.youtube.com/watch?v={video['id']['videoId']}")
    return urls


def download_audio(title, id):
    print(f'Attempting Download of {title}')
    FILE_NAME = f'{id}.mp3'

    SAVE_PATH = "assets/snippets"

    if os.path.isfile(f"{SAVE_PATH}/{FILE_NAME}"):
        print("Audio already downloaded!")
        return

    try:
        yt = YouTube(search_video(title)[0])
        print('Title:', yt.title)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            print(f'\nDownloading audio of: {yt.title}')
            audio_stream.download(SAVE_PATH, filename=FILE_NAME)
            print('Download completed!')
        else:
            print("No audio streams available for this video")
    except Exception as e:
        print("Error:", e)


def download_video(title, id, maxVideos):
    print(
        f'Attempting Download of {maxVideos} {title}{"s" if maxVideos > 1 else ""}')

    SAVE_PATH = "assets/videos"

    if os.path.isfile(f"{SAVE_PATH}/{id}-{maxVideos-1}.mp4"):
        print("Videos already downloaded!")
        return

    try:
        urls = search_video(title, maxVideos)
        for i, url in enumerate(urls):
            yt = YouTube(url)
            print('Title:', yt.title)

            if yt.age_restricted:
                print(f'Skipping age-restricted video: {yt.title}')
                continue

            video_stream = yt.streams.get_highest_resolution()

            if video_stream and not os.path.isfile(f"{SAVE_PATH}/{id}-{i}.mp4"):
                print(f'\nDownloading video of: {yt.title}')
                video_stream.download(SAVE_PATH, filename=f'{id}-{i}.mp4')
                print('Download completed!')
            else:
                print(
                    "No video streams available for this video / Video is already downloaded")
    except Exception as e:
        print("Error:", e)
