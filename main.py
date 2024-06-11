""" This is the Python script for the main core app functionality """

import string
import random
import subprocess
import configparser
from flask import Flask, render_template, redirect, request
import mysql.connector


app = Flask(__name__)

# Read the configuration file
config = configparser.ConfigParser()
config.read("./configs/variables.config")

db_config = {
    "host": config.get("database", "host"),
    "user": config.get("database", "user"),
    "password": config.get("database", "password"),
    "port": config.get("database", "port"),
    "database": config.get("database", "database"),
    "table": config.get("database", "table")
}

app_config = {
    "app_host": config.get("application", "app_host"),
    "app_port": config.get("application", "app_port"),
    "homepage": config.get("application", "homepage"),
    "randomly_generated_url_length": config.get("application", "randomly_generateD_url_length"),
    "debug": config.get("application", "debug")
}


def generate_short_url(length):
    """ Generates 5 random characters """
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


@app.route("/", methods=["GET", "POST"])
def index():
    """ GET and POST functionality for the index page """
    if request.method == "POST":
        user_long_url = request.form["long_url"]
        simplified_short_url = generate_short_url(length=int(app_config["randomly_generated_url_length"]))

        # there shouldn't be a pre-existing duplicate of the randomly generated short url
        db_cursor.execute(f"SELECT * FROM {db_config['table']} WHERE short_url = '{simplified_short_url}'")
        result = db_cursor.fetchone()
        while result:  # if randomized shortened URLs collide, run function again
            simplified_short_url = generate_short_url(length=int(app_config["randomly_generated_url_length"]))

            db_cursor.execute(f"SELECT * FROM {db_config['table']} WHERE short_url = '{simplified_short_url}'")
            result = db_cursor.fetchone()

        db_cursor.execute(f"INSERT INTO {db_config['table']} (original_url, short_url) VALUES ('{user_long_url}','{simplified_short_url}')")
        db_conn.commit()
        return render_template(f"{app_config['homepage']}", short_url=simplified_short_url)
    return render_template(f"{app_config['homepage']}")


@app.route("/<simplified_short_url>")
def redirect_url(simplified_short_url):
    """ This function performs the routing logic based on what is stored in MySQL """

    db_cursor.execute(f"SELECT original_url FROM {db_config['table']} WHERE short_url = '{simplified_short_url}'")
    result = db_cursor.fetchone()
    if result:
        return redirect(result[0])
    return "URL does not exist on our server.", 404


subprocess.call(["python", "./database/create_tables_mysql.py"])

db_conn =  mysql.connector.connect(host=db_config["host"], user=db_config["user"], password=db_config["password"], port=db_config["port"], database=db_config["database"])
db_cursor = db_conn.cursor()

# host="0.0.0.0" is necessary because the app is dockerized and 127.0.0.1 is a loopback address
app.run(host=app_config["app_host"], port=app_config["app_port"], debug=app_config["debug"])

db_conn.close()
