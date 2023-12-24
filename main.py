from spotify_utils import *
from uploading_utils import *
from video_utils import *

create_asset_directories()
create_artist_video(sys.argv[1], get_token())
upload_to_tiktok()
