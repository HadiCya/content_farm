from dotenv import load_dotenv
from billboard_utils import get_random_artist
from spotify_utils import *
from uploading_utils import *
from video_utils import *
import config

MAX_ATTEMPTS = config.MAX_ATTEMPTS

create_asset_directories()
videos = create_artist_video(get_random_artist(), get_token())
for i in range(MAX_ATTEMPTS):
    print(f"Attempting to upload videos. Attempt: {i+1} of {MAX_ATTEMPTS}.")
    success = upload_to_tiktok(videos)
    if success:
        print("Video(s) uploaded successfully!")
        break
    print(f"Attempt {i+1} of {MAX_ATTEMPTS} failed.")
