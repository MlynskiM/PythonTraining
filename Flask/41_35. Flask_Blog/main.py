from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import requests as rq
from datetime import datetime
import smtplib



API_ENDPOINT = "https://api.npoint.io/43644ec4f0013682fc0d"
MY_EMAIL = "Email"
PASSWORD = "PASSWORD"
EMAIL_RECIEVER_ADRESS = ""
YEAR = datetime.now().strftime("%Y")



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Posts.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        """Formating data from table to JSON data format."""

        dictionary = {}
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


##WTForm
class CreatePostForm(FlaskForm):


    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")




def post_base():
    """Returning posts from database as JSON format."""
    blog_posts = db.session.query(BlogPost).all()
    posts = [blog_post.to_dict() for blog_post in blog_posts]
    return posts



@app.route('/')
def get_all_posts():
    """Main page. Showing all available posts from DB."""
    posts = post_base()
    return render_template('index.html', posts = posts , year = YEAR)

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
        return render_template('contact.html', title = "Successfully sent your message" , year = YEAR)
    else:
        return render_template('contact.html', title = "Contact Me" , year = YEAR)

@app.route('/about')
def about_me():
    """Rendering About Section"""
    
    return render_template('about.html', posts = post_base()  , year = YEAR)



#----------------------------- RESTful Routing-------------------------------------#

def make_post():

    """Method taking data from quick form and commit it to database as new Blog Post """

    data = request.form
    new_post = BlogPost(
        title=data["title"],
        subtitle=data["subtitle"],
        date=datetime.now().strftime("%B-%d-%Y"),
        body=data["body"],
        author=data["author"],
        img_url=data["img_url"]
    )
    db.session.add(new_post)
    db.session.commit()
        



@app.route("/post/<int:index>")
def show_post(index):
    """Rendering post site. Taking id = index parametr and searching 
       for matching post."""

    posts = post_base()
    requested_post = db.session.query(BlogPost).get(index)

    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post

    return render_template("post.html", post=requested_post, year = YEAR)




@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    """Taking data from form and sending it to DB."""

    form = CreatePostForm()
    
    if request.method == "POST":
        make_post()
        return redirect(url_for("get_all_posts"))
    
    return render_template("make-post.html", form=form, title="New Post", year = YEAR)




@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    """Method take post by id then filling form with matching post data."""

    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data    
        db.session.commit()
        return redirect(url_for("show_post", index=post.id))
    return render_template("make-post.html", form=edit_form, title="Edit Post", year = YEAR)



@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    """Delete post by id."""

    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect(url_for('get_all_posts'))



if __name__ == '__main__':
    app.run(debug=True)