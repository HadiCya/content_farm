import os
from dotenv import load_dotenv

# VIDEO GENERATION
DURATION = 7
REVEAL_DURATION = 3
FPS = 24
SIZE = (1080, 1920)
IMAGE_SIZE = (928, 928)
FONT_SIZE = 90
INTRO_DURATION = 2
CHARACTER_WRAP = 20
MIN_AVG_VOLUME = -11

# DRIVER
MAX_ATTEMPTS = 3
BILLBOARD_CHARTS = ('greatest-r-b-hip-hop-artists', None), \
    ('greatest-alternative-artists', None), ('artist-100', None), \
    ('top-rap-artists', 2021), ('top-rap-artists', None), \
    ('top-r-and-b-hip-hop-artists',
     2021), ('top-r-and-b-hip-hop-artists', None)

# PATHS
FONT_PATH = "template/Roboto-Regular.ttf"
COOKIES_FILE_PATH = "cookies.txt"
ASSET_FILE_PATH = "../contentassets/"

# ENV FILES
load_dotenv(override=True)
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_KEY = os.getenv("YOUTUBE_KEY")
SESSION_ID = os.getenv("SESSION_ID")
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")
TIKTOK_PASSWORD = os.getenv("TIKTOK_PASSWORD")
