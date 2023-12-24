import json
import os
import re
import urllib.request
from PIL import Image

OUTPUT_FILE_JSON = 'release.json'
CONFIG_FILE_JSON = 'config.json'


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


def add_to_json(output_file_name, artist_name):
    videos = []  # read_json(OUTPUT_FILE_JSON)

    videos.append({
        'video': output_file_name,
        'description': f"How many did you get?? #{artist_name.replace(' ', '').lower()} #guessthesong #songquiz #quiz"
    })

    with open(OUTPUT_FILE_JSON, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=4)


def read_json(file_name):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except:
        print("No Data Found")
        return []


def create_asset_directories():
    config_data = read_json(CONFIG_FILE_JSON)
    directories = ['assets/images', 'assets/snippets',
                   'assets/videos', 'final_videos']

    for dir in directories:
        os.makedirs(f"{config_data['asset_file_path']}{dir}", exist_ok=True)
