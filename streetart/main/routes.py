
from flask import render_template, request, Blueprint
from streetart.models import Post,Subscription
from streetart.posts.forms import SearchTag
from flask_login import current_user
main = Blueprint('main', __name__)


@main.route("/",methods=['GET','POST'])
@main.route("/home",methods=['GET','POST'])
def home():
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
    try:
        link = Subscription.query.filter_by(user=current_user.username).join(Post,Post.category==Subscription.category)
        posts = Post.query.order_by(Post.date_posted.desc()).filter_by(category=link).paginate(page=page, per_page=5)
    except:
        
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    return render_template('home.html', posts=posts, searchform= searchform)