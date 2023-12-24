import os
from dotenv import load_dotenv
from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

from utils import *

OUTPUT_FILE_JSON = 'release.json'


def upload_to_tiktok():
    videos = read_json(OUTPUT_FILE_JSON)

    load_dotenv(override=True)
    tiktok_username = os.getenv("TIKTOK_USERNAME")
    tiktok_password = os.getenv("TIKTOK_PASSWORD")
    print(tiktok_username, tiktok_password)

    auth = AuthBackend(username=tiktok_username,
                       password=tiktok_password, cookies='cookies.txt')
    upload_videos(videos=videos, auth=auth, headless=True)


def upload_to_youtube():
    pass
