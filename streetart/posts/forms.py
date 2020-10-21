
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField , SelectField
from wtforms.validators import DataRequired 
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tag = StringField('Tags', validators=[DataRequired()])
    category = SelectField(choices=[('Tag', 'Tag'), ('Throw-up', 'Throw-up'), ('Blockbuster', 'Blockbuster'),
    ('Wildstyle', 'Wildstyle'), ('Heaven', 'Heaven'), ('Stencil', 'Stencil'), (' Poster (paste-up)', ' Poster (paste-up)'),(' Sticker (slap)', 'Sticker (slap)')])
    art =  FileField('Art', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    location = StringField('Location')
    submit = SubmitField('Post')

class SearchTag(FlaskForm):
     tag = StringField( validators=[DataRequired()])
     submit = SubmitField('Search')