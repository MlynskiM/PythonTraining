from flask import Flask, render_template, request
import requests as rq
import datetime as dt
import smtplib

app = Flask(__name__)

API_ENDPOINT = "https://api.npoint.io/43644ec4f0013682fc0d"

posts = rq.get(API_ENDPOINT).json()

year = dt.datetime.now().strftime("%Y")


my_email = "Email"
password = "PASSWORD"



@app.route('/')
def home():
    return render_template('index.html', posts = posts , year = year)

@app.route('/contact', methods=["POST", "GET"])
def contact_us():
    if request.method == 'POST':
        data = request.form
        

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user = my_email, password=password)
            connection.sendmail(
                from_addr = my_email,
                to_addrs= "RECIEVER ADRESS",
                msg = f"Subject:Contact Form from {data['name']}\n\nPhone Number : {data['phonenumber']}\nEmail: {data['email']}\n\n{data['message']}"
            )
        return render_template('contact.html', title = "Successfully sent your message" , year = year)
    else:
        return render_template('contact.html', title = "Contact Me" , year = year)

@app.route('/about')
def about_me():
    return render_template('about.html', posts = posts  , year = year)

@app.route('/post/<int:index>')
def get_post(index):
    get_post= posts[index-1]
    return render_template("post.html", title = get_post["title"], body = get_post["body"], subtitle = get_post["subtitle"], year = year, image = get_post["image_url"])


if __name__ == '__main__':
    app.run(debug=True)