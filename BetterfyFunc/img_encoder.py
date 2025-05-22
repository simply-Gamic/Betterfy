#  Copyright (c) 2025.

from base64 import b64encode
from os import path as p


def encode(path: str):
    r"""Encodes a given image file into raw bytes that can be used by the Spotify API.

            :param path: The path to the img.
            :return: The image as bytes in string form.
            """
    if 0 < p.getsize(path) < 256000:
        with open(path, 'rb') as img:
            bytes = b64encode(img.read())
            return bytes.decode()
    else:
        print("File size too big. Maximum 256KB allowed")

