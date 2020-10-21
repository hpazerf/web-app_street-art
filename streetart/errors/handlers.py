from flask import Blueprint, render_template
from streetart.posts.forms import SearchTag
errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    searchform=SearchTag()
    return render_template('errors/404.html',searchform=searchform), 404


@errors.app_errorhandler(403)
def error_403(error):
    searchform=SearchTag()
    return render_template('errors/403.html',searchform=searchform), 403


@errors.app_errorhandler(500)
def error_500(error):
    searchform=SearchTag()
    return render_template('errors/500.html',searchform=searchform), 500