import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)",
            name,
            month,
            day,
        )

        return redirect("/")

    else:
        birthdays = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", birthdays=birthdays)


@app.route("/edit", methods=["POST"])
def edit():
    id = request.form.get("id")
    name = db.execute("SELECT name FROM birthdays WHERE id = ?", id)[0]["name"]
    month = db.execute("SELECT month FROM birthdays WHERE id = ?", id)[0]["month"]
    day = db.execute("SELECT day FROM birthdays WHERE id = ?", id)[0]["day"]
    return render_template("edit.html", name=name, month=month, day=day, id=id)


@app.route("/home", methods=["POST"])
def home():
    id = request.form.get("id")
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")
    db.execute(
        "UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?",
        name,
        month,
        day,
        id,
    )
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")
