from billboard_utils import get_random_artist
from spotify_utils import *
from uploading_utils import *
from video_utils import *

MAX_ATTEMPTS = 3
BILLBOARD_CHARTS = ('greatest-r-b-hip-hop-artists', None), \
    ('greatest-alternative-artists', None), ('artist-100', None), \
    ('top-rap-artists', 2021), ('top-rap-artists', None), \
    ('top-r-and-b-hip-hop-artists',
     2021), ('top-r-and-b-hip-hop-artists', None)

create_asset_directories()
create_artist_video(get_random_artist(BILLBOARD_CHARTS), get_token())
for i in range(MAX_ATTEMPTS):
    print(f"Attempting to upload videos. Attempt: {i+1} of {MAX_ATTEMPTS}.")
    success = upload_to_tiktok()
    if success:
        print("Videos uploaded successfully!")
        break
    print(f"Attempt {i+1} of {MAX_ATTEMPTS} failed.")
