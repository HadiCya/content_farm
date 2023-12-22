from pprint import PrettyPrinter
from dotenv import load_dotenv
import os
from apiclient.discovery import build
from pytube import YouTube


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


def download_audio(url):
    try:
        SAVE_PATH = "snippets"
        yt = YouTube(url)
        print('Title:', yt.title)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            print('\nDownloading audio of:', yt.title,
                  'into location:', SAVE_PATH)
            audio_stream.download(SAVE_PATH)
            print('Download completed!')
        else:
            print("No audio streams available for this video")

    except Exception as e:
        print("Error:", e)
