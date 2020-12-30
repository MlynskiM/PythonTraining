from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import requests as rq
from pprint import pprint


API_KEY = "b54863ede45b7b172246aead78a8af71"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

#CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top-10-movies.db"
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)    
db.create_all()


class MovieForm(FlaskForm):
    rating = StringField('Your rating out of 10 e.g. 7.8', validators=[DataRequired()])
    review = StringField("Your review", validators=[DataRequired()])
    sumbit = SubmitField('Submit')
    
class AddMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    sumbit = SubmitField('Submit')

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()





@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()


    if form.validate_on_submit():
        movie_title = form.title.data
        response = rq.get(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=en-US&query={movie_title}&page=1&include_adult=false")
        data = response.json()["results"]
        return render_template("select.html", movies=data)


    return render_template("add.html", form=form)



@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        #The language parameter is optional, if you were making the website for a different audience 
        #e.g. Hindi speakers then you might choose "hi-IN"
        response = rq.get(movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            #The data in release_date includes month and day, we will want to get rid of.
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("edit", id=new_movie.id))



@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = MovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)



@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    # DELETE A RECORD BY ID
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



@app.route("/")
def home():
    #This line creates a list of all the movies sorted by rating
    all_movies = Movie.query.order_by(Movie.rating).all()
    
    #This line loops through all the movies
    for i in range(len(all_movies)):
        #This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


if __name__ == '__main__':
    app.run(debug=True)
