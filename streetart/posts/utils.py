import os
import secrets
from PIL import Image
from flask import url_for, current_app


def save_art(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/art', picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn

def save_art_android(form_picture):
    random_hex = secrets.token_hex(8)
    f_ext = ".jpeg"
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/art', picture_fn)
    i = form_picture
    i.save(picture_path)

    return picture_fn