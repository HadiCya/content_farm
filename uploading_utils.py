import os
from dotenv import load_dotenv
from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend
from selenium.webdriver.chrome.options import Options

from youtube_uploader_selenium import YouTubeUploader


from utils import *

OUTPUT_FILE_JSON = 'release.json'


def upload_to_tiktok():
    videos = read_json(OUTPUT_FILE_JSON)

    load_dotenv(override=True)
    tiktok_username = os.getenv("TIKTOK_USERNAME")
    tiktok_password = os.getenv("TIKTOK_PASSWORD")
    print(tiktok_username, tiktok_password)

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    auth = AuthBackend(username=tiktok_username,
                       password=tiktok_password, cookies='cookies.txt')
    print(upload_videos(videos=videos, auth=auth, headless=True, options=options))


def upload_to_youtube():
    video_path = '123/rockets.flv'
    metadata_path = '123/rockets_metadata.json'

    uploader = YouTubeUploader(video_path, metadata_path)
    was_video_uploaded, video_id = uploader.upload()
    print("Video Uploaded!" if was_video_uploaded else "Video Failed to Upload.")
