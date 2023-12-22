import billboard
from spotify_utils import *
from video_utils import *

chart = billboard.ChartData('artist-100')
artist_name = chart[1].artist
create_artist_video("Taylor Swift", get_token())
