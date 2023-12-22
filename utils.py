import re
import urllib.request


def remove_parentheses(text):
    return re.sub(r'\s*\([^)]*\)', '', text)


def download_image(url, image_file_path):
    urllib.request.urlretrieve(url, image_file_path)
