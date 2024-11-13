import os
from dotenv import load_dotenv

# VIDEO GENERATION

# IMAGE_SIZE = (928, 928)
# FONT_SIZE = 90
# CHARACTER_WRAP = 20
# MIN_AVG_VOLUME = -11
# SONG_COUNT = 5

# DRIVER

# BILLBOARD_CHARTS = ('greatest-r-b-hip-hop-artists', None), \
#     ('greatest-alternative-artists', None), ('artist-100', None), \
#     ('top-rap-artists', 2021), ('top-rap-artists', None), \
#     ('top-r-and-b-hip-hop-artists',
#      2021), ('top-r-and-b-hip-hop-artists', None)

# CONFIG
FPS = 24
SIZE = (1080, 1920)
MAX_ATTEMPTS = 3
STATIC_PATH = "template"
ASSET_FILE_PATH = ""

# ENV FILES
load_dotenv(override=True)
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_KEY = os.getenv("YOUTUBE_KEY")
SESSION_ID = os.getenv("SESSION_ID")
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")
TIKTOK_PASSWORD = os.getenv("TIKTOK_PASSWORD")
MAKERSUITE_KEY = os.getenv("MAKERSUITE_KEY")
ELEVENLABS_KEY = os.getenv("ELEVENLABS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")