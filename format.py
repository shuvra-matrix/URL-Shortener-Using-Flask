from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms import ValidationError
from wtforms.validators import DataRequired, url


class Urls(FlaskForm):
    name = StringField("Your URL : ",validators=[DataRequired(), url()],render_kw={"placeholder": "Shorten your link"})
    submit = SubmitField("Submit")