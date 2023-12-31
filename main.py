import random
from billboard_utils import *
from spotify_utils import *
from uploading_utils import *
from video_generation import *
from video_utils import *
import config

MAX_ATTEMPTS = config.MAX_ATTEMPTS

def get_5_songs():
    songs = []
    selected_indices = set()
    try:
        chart = billboard.ChartData('hot-100')
        for i in range(5):
            while True:
                random_number = random.randint(0, 99)
                if random_number not in selected_indices:
                    selected_indices.add(random_number)
                    songs.append(chart[random_number].title)
                    break
    except Exception as e:
        print(f"An error occurred: {e}")
    return songs

def main():
    create_asset_directories()
    create_billboard_video(get_5_songs())
    # for i in range(MAX_ATTEMPTS):
    #     print(
    #         f"Attempting to create video. Attempt: {i+1} of {MAX_ATTEMPTS}.")
    #     try:
    #         videos = create_artist_video(get_random_artist(), get_token())
    #         if videos:
    #             print("Video created successfully!")
    #             break
    #         print(f"Attempt {i+1} of {MAX_ATTEMPTS} failed.")
    #     except Exception as e:
    #         print(f"Attempt {i+1} of {MAX_ATTEMPTS} failed with error: {e}")
    # if videos:
    #     for i in range(MAX_ATTEMPTS):
    #         print(
    #             f"Attempting to upload video. Attempt: {i+1} of {MAX_ATTEMPTS}.")
    #         try:
    #             success = upload_to_tiktok(videos)
    #             if success:
    #                 print("Video uploaded successfully!")
    #                 break
    #             print(f"Attempt {i+1} of {MAX_ATTEMPTS} failed.")
    #         except Exception as e:
    #             print(
    #                 f"Attempt {i+1} of {MAX_ATTEMPTS} failed with error: {e}")


if __name__ == "__main__":
    main()
