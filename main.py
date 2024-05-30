import string
import random
from flask import Flask, render_template, redirect, request
import subprocess
import mysql.connector


app = Flask(__name__)


def generate_short_url(length=5):
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_long_url = request.form["long_url"]
        simplified_short_url = generate_short_url(length=5)

        # there shouldn't be a pre-existing duplicate of the randomly generated short url
        db_cursor.execute(f"SELECT * FROM url_mapping WHERE short_url = '{simplified_short_url}'")
        result = db_cursor.fetchone()
        while result:  # if randomized shortened URLs collide, run function again
            simplified_short_url = generate_short_url(length=5)

            db_cursor.execute(f"SELECT * FROM url_mapping WHERE short_url = '{simplified_short_url}'")
            result = db_cursor.fetchone()

        db_cursor.execute(f"INSERT INTO url_mapping (original_url, short_url) VALUES ('{user_long_url}','{simplified_short_url}')")
        db_conn.commit()
        return render_template("index.html", short_url=simplified_short_url)
    
    elif request.method == "GET":
        return render_template("index.html")


@app.route("/<simplified_short_url>")
def redirect_url(simplified_short_url):

    db_cursor.execute(f"SELECT original_url FROM url_mapping WHERE short_url = '{simplified_short_url}'")
    result = db_cursor.fetchone()
    if result:
        return redirect(result[0])
    else:
        return "URL does not exist on our server.", 404


if __name__ == "__main__":
    subprocess.call(["python", "./database/create_tables_mysql.py"])

    db_conn =  mysql.connector.connect(host="mydb", user="root", password="root", port=3306, database="url_shortener")
    db_cursor = db_conn.cursor()

    # host="0.0.0.0" is necessary because the app is dockerized and 127.0.0.1 is a loopback address
    app.run(host="0.0.0.0", port=9091, debug=True)

    db_conn.close()