from billboard_utils import *
from image_utils import *
from llm_utils import *
from spotify_utils import *
from video_generation import *
from video_utils import *
import config

MAX_ATTEMPTS = config.MAX_ATTEMPTS


def main():
    create_asset_directories()
    messages = generate_imessage_style_conversation(
        create_conversation_json(), 'imessage_style_conversation.png')
    create_fake_conversation_video(messages, 'imessage_style_conversation.png')
    # for i in range(1):
    #     print(
    #         f"Attempting to create video. Attempt: {i+1} of {MAX_ATTEMPTS}.")
    #     try:
    #         video = create_artist_video(get_random_artist(), get_token())
    #         if video:
    #             print(f"Video created successfully! View at: {video}")
    #             break
    #         print(f"Attempt {i+1} of {MAX_ATTEMPTS} failed.")
    #     except Exception as e:
    #         print(f"Attempt {i+1} of {MAX_ATTEMPTS} failed with error: {e}")


if __name__ == "__main__":
    main()
