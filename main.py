from billboard_utils import *
from image_utils import *
from llm_utils import *
from spotify_utils import *
from uploading_utils import *
from video_generation import *
from video_utils import *
import config

MAX_ATTEMPTS = config.MAX_ATTEMPTS


def main():
    create_asset_directories()
    generate_imessage_style_conversation(
        create_conversation_json(), 'imessage_style_conversation.png')
    # for i in range(MAX_ATTEMPTS):
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
