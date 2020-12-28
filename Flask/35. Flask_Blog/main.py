from flask import Flask, render_template
import requests
import datetime as dt

app = Flask(__name__)

API_ENDPOINT = "https://api.npoint.io/43644ec4f0013682fc0d"

posts = requests.get(API_ENDPOINT).json()

year = dt.datetime.now().strftime("%Y")

@app.route('/')
def home():
    return render_template('index.html', posts = posts , year = year)

@app.route('/contact')
def contact_us():
    return render_template('contact.html', posts = posts , year = year)

@app.route('/about')
def about_me():
    return render_template('about.html', posts = posts  , year = year)

@app.route('/post/<int:index>')
def get_post(index):
    get_post= posts[index-1]
    return render_template("post.html", title = get_post["title"], body = get_post["body"], subtitle = get_post["subtitle"], year = year, image = get_post["image_url"])


if __name__ == '__main__':
    app.run(debug=True)