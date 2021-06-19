from flask import Flask,redirect,render_template,url_for
from format import Urls
from flask_sqlalchemy import SQLAlchemy
import os
import random
import string

app = Flask(__name__)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = "fkfhsvoygu654674auhrq5@#6274gq575798759864352"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(BASE_DIR,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
@app.before_first_request
def create_tables():
    db.create_all()

class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer,primary_key=True)
    long_url = db.Column(db.Text)
    short_url = db.Column(db.Text)

    def __init__(self,long,short):
        self.long_url=long
        self.short_url=short


def shorts_url():
    short_late = string.ascii_uppercase+string.ascii_uppercase+string.digits
    while True:
        random_latter = random.choices(short_late, k=3)
        random_latter = "".join(random_latter)
        short_url = Url.query.filter_by(short_url=random_latter).first()
        if not short_url:
            return random_latter




@app.route("/",methods=["GET","POST"])
def index():

    form = Urls()
    if form.validate_on_submit():
        user_url = form.name.data
        url_present = Url.query.filter_by(long_url=user_url).first()
        if url_present:
            return redirect(url_for("short_url",urls=url_present.short_url))
        else:
            short = shorts_url()
            all_url = Url(long=user_url,short=short)
            db.session.add(all_url)
            db.session.commit()
            return redirect(url_for("short_url",urls=short))
    else:
        return render_template("index.html",form=form)


@app.route('/short/<urls>')
def short_url(urls):
    return render_template('url.html',urls=urls)

@app.route('/<short>')
def goto(short):
    long_urls = Url.query.filter_by(short_url=short).first()
    if long_urls:
        return redirect(long_urls.long_url)
    else:
        return redirect(url_for('invalid'))


@app.route('/invalid')
def invalid():
    return render_template("invalid.html")

if __name__ == '__main__':
    app.run(debug=True)