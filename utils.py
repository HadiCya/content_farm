import json
import os
import re
import urllib.request
from PIL import Image
import config


def remove_parentheses(text):
    return re.sub(r'\s*[\[\(][^\]\)]*[\]\)]', '', text)


def remove_punc_n_spaces(text):
    return re.sub('[^A-Za-z0-9]+', '', text)


def download_image(url, image_file_path, size):
    urllib.request.urlretrieve(url, image_file_path)
    with Image.open(image_file_path) as img:
        resized_img = img.resize(
            size, Image.Resampling.LANCZOS)
        resized_img = resized_img.convert('RGB')
        resized_img.save(image_file_path)


def read_json(file_name):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except:
        print("No Data Found")
        return []


def create_asset_directories():
    directories = ['assets/images', 'assets/snippets',
                   'assets/videos', 'final_videos']

    for dir in directories:
        os.makedirs(f"{config.ASSET_FILE_PATH}{dir}", exist_ok=True)
