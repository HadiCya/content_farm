import re
import urllib.request
from PIL import Image


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
