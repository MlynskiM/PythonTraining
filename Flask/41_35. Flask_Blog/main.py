#----------------------------- Imported Modules -------------------------------------#

from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import requests as rq
from datetime import datetime
import smtplib
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import *
from flask_gravatar import Gravatar

#----------------------------- Constants -------------------------------------#

API_ENDPOINT = "https://api.npoint.io/43644ec4f0013682fc0d"
MY_EMAIL = "Email"
PASSWORD = "PASSWORD"
EMAIL_RECIEVER_ADRESS = ""
YEAR = datetime.now().strftime("%Y")

#----------------------------- App config.-------------------------------------#

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=40, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)


#----------------------------- DB Connection -------------------------------------#


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Posts.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#----------------------------- Login manager init -------------------------------------#
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#----------------------------- Database Tables -------------------------------------#



class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")

    def to_dict(self):
        """Formating data from table to JSON data format."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    comment_author = relationship("User", back_populates="comments")
    text = db.Column(db.Text, nullable=False)
db.create_all()

#----------------------------- Decorators -------------------------------------#


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


#----------------------------- Fundamental Functionality -------------------------------------#
def post_base():
    """Returning posts from database as JSON format."""
    blog_posts = db.session.query(BlogPost).all()
    posts = [blog_post.to_dict() for blog_post in blog_posts]
    return posts



@app.route('/')
def get_all_posts():
    """Main page. Showing all available posts from DB."""
    posts = BlogPost.query.all()
    return render_template('index.html', posts = posts , year = YEAR, current_user=current_user)



@app.route('/contact', methods=["POST", "GET"])
def contact_us():
    """Sending Email"""


    if request.method == 'POST':
        data = request.form
        

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user = MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr = MY_EMAIL,
                to_addrs= EMAIL_RECIEVER_ADRESS,
                msg = f"Subject:Contact Form from {data['name']}\n\nPhone Number : {data['phonenumber']}\nEmail: {data['email']}\n\n{data['message']}"
            )
        return render_template('contact.html', title = "Successfully sent your message" , year = YEAR, current_user=current_user)
    else:
        return render_template('contact.html', title = "Contact Me" , year = YEAR, current_user=current_user)




@app.route('/about')
def about_me():
    """Rendering About Section"""
    return render_template('about.html', posts = post_base()  , year = YEAR, current_user=current_user)


#----------------------------- User Functionality-------------------------------------#

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


#----------------------------- RESTful Routing-------------------------------------#




@app.route("/post/<int:post_id>", methods= ["POST", "GET"])
def show_post(post_id):
    """Rendering post site. Taking id = index parametr and searching 
       for matching post."""
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()

    return render_template("post.html", post=requested_post, year = YEAR, form=form, current_user=current_user)




@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def new_post():
    """Taking data from form and sending it to DB."""

    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=datetime.now().strftime("%B-%d-%Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    
    return render_template("make-post.html", form=form, title="New Post", year = YEAR, current_user=current_user)




@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    """Method take post by id then filling form with matching post data."""

    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author.name,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data    
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, title="Edit Post", year = YEAR, current_user=current_user)



@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    """Delete post by id."""

    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect(url_for('get_all_posts'))



if __name__ == '__main__':
    app.run(debug=True)