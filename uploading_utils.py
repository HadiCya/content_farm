from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend
from selenium.webdriver.chrome.options import Options


from utils import *


def upload_to_tiktok(videos):
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--profile-directory=Default')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    auth = AuthBackend(username=config.TIKTOK_USERNAME,
                       password=config.TIKTOK_PASSWORD, cookies=config.COOKIES_FILE_PATH)
    failed = upload_videos(videos=videos, auth=auth,
                           headless=True, options=options)

    return failed == []
