import string
import random
from flask import Flask, render_template, redirect, request
import subprocess
import mysql.connector
#db = mysql.connector.connect(host="mydb", user="root", password="root", port=3306)


app = Flask(__name__)
shortened_urls = {}


def generate_short_url(length=5):
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_long_url = request.form["long_url"]
        simplified_short_url = generate_short_url(length=5)

        while simplified_short_url in shortened_urls:  # if randomized shortened URLs collide, run function again
            simplified_short_url = generate_short_url(length=5)
        shortened_urls[simplified_short_url] = user_long_url
        return render_template("index.html", short_url=simplified_short_url)
    
    elif request.method == "GET":
        return render_template("index.html")


@app.route("/<simplified_short_url>")
def redirect_url(simplified_short_url):
    user_long_url = shortened_urls.get(simplified_short_url)
    if user_long_url:
        return redirect(user_long_url)
    else:
        return "URL does not exist on our server.", 404


if __name__ == "__main__":
    subprocess.call(["python", "./database/create_tables_mysql.py"])
    # host="0.0.0.0" is necessary because the app is dockerized and 127.0.0.1 is a loopback address
    app.run(host="0.0.0.0", port=9091, debug=True)