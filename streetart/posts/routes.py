
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from streetart import db
from streetart import GoogleMaps
from streetart.models import Post
from streetart.posts.forms import PostForm
from streetart.posts.forms import SearchTag
from streetart.posts.utils import save_art
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    searchform=SearchTag()
    form = PostForm()
    if form.validate_on_submit():
        art_file = save_art(form.art.data)
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user, tag=searchform.tag.data,
                    category=form.category.data,art=art_file,location=form.location.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    if searchform.is_submitted():
        result=request.form
        page = request.args.get('page', 1, type=int)
        tag = searchform.tag.data
        search = "%{}%".format(tag)
        array = Post.query.filter(Post.tag.like(search))
        posts = array\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
        return render_template('tag_posts.html', posts=posts , tag=searchform.tag.data,searchform=searchform)
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post' , searchform=searchform)


@posts.route("/post/<int:post_id>")
def post(post_id):
    searchform=SearchTag()
    post = Post.query.get_or_404(post_id)
    if searchform.is_submitted():
        result=request.form
        page = request.args.get('page', 1, type=int)
        tag = searchform.tag.data
        search = "%{}%".format(tag)
        array = Post.query.filter(Post.tag.like(search))
        posts = array\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
        return render_template('tag_posts.html', posts=posts , tag=searchform.tag.data,searchform=searchform)
    return render_template('post.html', title=post.title, post=post,searchform=searchform)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    searchform=SearchTag()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.tag = form.tag.data
        post.category = form.category.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.tag.data = post.tag
    if searchform.is_submitted():
        result=request.form
        page = request.args.get('page', 1, type=int)
        tag = searchform.tag.data
        search = "%{}%".format(tag)
        array = Post.query.filter(Post.tag.like(search))
        posts = array\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
        return render_template('tag_posts.html', posts=posts , tag=searchform.tag.data,searchform=searchform)
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post',searchform=searchform)


@posts.route("/post/<int:post_id>/delete" ,methods=['GET','POST'])
@login_required
def delete_post(post_id):
    searchform=SearchTag()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    if searchform.is_submitted():
        result=request.form
        page = request.args.get('page', 1, type=int)
        tag = searchform.tag.data
        search = "%{}%".format(tag)
        array = Post.query.filter(Post.tag.like(search))
        posts = array\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
        return render_template('tag_posts.html', posts=posts , tag=searchform.tag.data,searchform=searchform)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home',searchform=searchform))

@posts.route("/category/<string:category>",methods=['GET','POST'])
def category_posts(category):
  searchform=SearchTag()
  if searchform.is_submitted():
        result=request.form
        page = request.args.get('page', 1, type=int)
        tag = searchform.tag.data
        search = "%{}%".format(tag)
        array = Post.query.filter(Post.tag.like(search))
        posts = array\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
        return render_template('tag_posts.html', posts=posts , tag=searchform.tag.data,searchform=searchform)
  page = request.args.get('page', 1, type=int)
  posts = Post.query.filter_by(category=category)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
  return render_template('category_posts.html', posts=posts , category=category,searchform=searchform)

@posts.route('/search', methods=['POST', 'GET'])
def search():
  searchform=SearchTag()

  if searchform.is_submitted():
        result=request.form
        page = request.args.get('page', 1, type=int)
        tag = searchform.tag.data
        search = "%{}%".format(tag)
        array = Post.query.filter(Post.tag.like(search))
        posts = array\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
        return render_template('tag_posts.html', posts=posts , tag=searchform.tag.data,searchform=searchform)
  tag = searchform.tag.data
  page = request.args.get('page', 1, type=int)
  posts = Post.query.filter_by(tag=searchform.tag.data)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
  return render_template('tag_posts.html', posts=posts , tag=searchform.tag.data)


@posts.route("/map",methods=['GET','POST'])
def map_posts():
  searchform=SearchTag()
  if searchform.is_submitted():
        result=request.form
        page = request.args.get('page', 1, type=int)
        tag = searchform.tag.data
        search = "%{}%".format(tag)
        array = Post.query.filter(Post.tag.like(search))
        posts = array\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
        return render_template('tag_posts.html', posts=posts , tag=searchform.tag.data,searchform=searchform)
  page = request.args.get('page', 1, type=int)
  posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
  marked_posts=Post.query.order_by(Post.date_posted.desc())
  marker=[]
  for i in marked_posts:
      location=i.location.split(",")
      markerdict={
      'icon':'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
      'lat':float(location[0]),
      'lng':float(location[1]),
      'infobox': "<img src='/static/art/"+i.art+"' />"
     
      }
      marker.append(markerdict)
  print(marker)
  sndmap =     Map(
        identifier="grafittimap",
        lat=30.2543,
        lng=-97.7670,
        markers=marker
    )
  return render_template('map_posts.html', posts=posts ,sndmap=sndmap, searchform=searchform)