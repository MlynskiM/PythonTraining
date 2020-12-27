from flask import Flask, render_template
from post import Post
import requests
import datetime as dt

URL = "https://api.npoint.io/5abcca6f4e39b4955965"
posts = requests.get(URL).json()
all_posts = []

for post in posts:
    post_object = Post(post["id"], post["title"], post["subtitle"], post["body"])
    all_posts.append(post_object)

year = dt.datetime.now().strftime("%Y")
app = Flask(__name__)




@app.route('/')
def home():
    return render_template("index.html", all_posts = all_posts, year = year)


@app.route('/post/<int:index>')
def get_post(index):
    get_post_object = all_posts[index-1]
    return render_template("post.html", title = get_post_object.title, body = get_post_object.body, subtitle = get_post_object.subtitle, year = year)



if __name__ == "__main__":
    app.run(debug=True)
