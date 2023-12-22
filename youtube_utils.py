from dotenv import load_dotenv
import os
from apiclient.discovery import build
from pytube import YouTube
from pathlib import Path


def search_video(title):
    load_dotenv()
    api_key = os.getenv("YOUTUBE_KEY")

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(q=title,
                                    part='snippet', type='video', maxResults=1)
    res = request.execute()
    video = res['items'][0]
    video_id = video['id']['videoId']
    url = f"https://www.youtube.com/watch?v={video_id}"
    return url


def download_audio(title, id):
    print(f'Attempting Download of {title}')
    FILE_NAME = f'{id}.mp3'

    SAVE_PATH = "assets/snippets"

    if os.path.isfile(f"{SAVE_PATH}/{FILE_NAME}"):
        print("File already downloaded!")
        return

    try:
        yt = YouTube(search_video(title))
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
