
from flask import render_template, request, Blueprint, jsonify, send_from_directory
from streetart.models import Post,Subscription, User
from streetart.posts.forms import SearchTag
from flask_login import current_user
from streetart.posts.utils import save_art,save_art_android
from streetart.users.utils import send_reset_email
from streetart import db, bcrypt
import base64 
import io
from PIL import Image
api = Blueprint('api', __name__)


@api.route("/api/login",methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        data = request.get_json()
        post_email = data['email']
        post_pswd = data['password']

        user = User.query.filter_by(email=post_email).first()

        if user and bcrypt.check_password_hash(user.password, post_pswd):
            return jsonify(status="You are logged in!")
        else:
            return jsonify(status="Wrong password!")
    else:
        return jsonify(status="Not a POST request!")


@api.route("/api/register",methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        data = request.get_json()
        post_username = data['username']
        post_email = data['useremail']
        post_pswd = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        user = User(username=post_username, email=post_email, password=post_pswd)

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'status': 'Registered!'})
        except:
            return jsonify({'status': 'Registration failed'})
    else:
        return jsonify({'status': 'Not a POST request!'})


@api.route("/api/forgottenPswd",methods=['GET', 'POST'])
def forgotten_pswd():

    if request.method=='POST':

        data = request.get_json()

        user = User.query.filter_by(email=data['email']).first()

        if len(user) == 0:
            return jsonify(status="User not found!")
        else:
            send_reset_email(user)
            return jsonify(status="Reset email sent!")
    else:
        return jsonify(status="Not a POST request!")


@api.route("/api/viewCategories/<selected_category>",methods=['GET','POST'])
def view_categories(selected_category):

    if selected_category == "Poster":
        cat = " Poster (paste-up)"
    elif selected_category == "Sticker":
        cat = " Sticker (slap)"
    else:
        cat = selected_category

    if cat!= "All":
        wanted_posts = Post.query.filter_by(category=cat)\
        .order_by(Post.date_posted.desc())
    else:
        wanted_posts = Post.query.order_by(Post.date_posted.desc())

    json_posts = {"posts": [x.serialize_to_json for x in wanted_posts]}
    return jsonify(json_posts)

@api.route("/api/newPost", methods=['POST'])
def upload_new_post():
    data = request.get_json()
    post_description = data['content']
    coords = data['location']
    post_title = data['title']
    post_category = data['category']
    useremail = data['user']
    user =  User.query.filter_by(email=useremail).first()
    tags = data['tags']
    bytearrayimage = base64.b64decode(data['image'])
    image= Image.open(io.BytesIO(bytearrayimage))
    image_filename = save_art_android(image) ####need to verify with jose that save art would work!

    post = Post(title=post_title, content=post_description,
                author=user, tag=tags,
                category=post_category, art=image_filename,location=coords)
    try:

        db.session.add(post)
        db.session.commit()
        return jsonify({'success': True})

    except:
        return jsonify({'success': False})

## /api/post/new
