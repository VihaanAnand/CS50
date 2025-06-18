# Import necessary libraries
import base64
from cs50 import SQL
import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
import json
import math
import random as rando
import urllib.request, urllib.parse, urllib.error

# Startup Flask application
app = Flask(__name__)

# Configuration of Flask application
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
                if session.get("user_id") is None:
                        return redirect("/login")
                return f(*args, **kwargs)
        return decorated_function

# Configuration of database
database = SQL("sqlite:///lightningmaths.db")

# Error screen
def error(message, retry):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"), ("%", "~p"), ("#", "~h"), ("/", "~s"), ('"', "''")]:
                message = message.replace(old, new)
        return render_template("error.html", top="Error 400", bottom=message, retry=retry)

# Random number generator
def random(n, min, max):
        answer = []
        for i in range(n):
                answer.append(rando.randint(min, max))
        return answer

# Homepage route
@app.route("/")
def home():
        return render_template("home.html")

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
        # User submitted a form
        if request.method == "POST":
                # Get form data
                username = request.form.get("username")
                password = request.form.get("password")
                repeat = request.form.get("repeat")

                # Get list of users
                usernames = []
                for uname in database.execute("SELECT username FROM users"):
                        usernames.append(uname["username"])

                # Ensure data is valid
                if not username:
                        return error("No username given", "/signup")
                elif username in usernames:
                        return error("Username already taken", "/signup")
                elif not password:
                        return error("No password given", "/signup")
                elif not repeat:
                        return error("Need to repeat password to verify", "/signup")
                elif password != repeat:
                        return error("Password doesn't match repeat", "/signup")
                storpwd = base64.b64encode(password.encode("ascii")).decode("ascii")

                # Add user to database
                database.execute("INSERT INTO users (username, password) VALUES(?, ?)", username, storpwd)

                # Send to login page
                return redirect("/login")
        else:
                return render_template("signup.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
        # Forget any user
        session.clear()

        # User submitted a form
        if request.method == "POST":
                # Get form data
                username = request.form.get("username")
                password = request.form.get("password")

                # Ensure data is valid
                if not username:
                        return error("No username given", "/login")
                elif not password:
                        return error("No password given", "/login")

                # Lookup user
                users = database.execute("SELECT password, id FROM users WHERE username = ?", username)
                if len(users) != 1:
                        return error("Username doesn't exist", "/login")
                corpwd = base64.b64decode(users[0]["password"].encode("ascii")).decode("ascii")
                if corpwd != password:
                        return error("Incorrect password", "/login")

                # Remember who is logged in
                session["user_id"] = users[0]["id"]

                # Send to home page
                return redirect("/")
        else:
                return render_template("login.html")

# Logout route
@app.route("/logout")
def logout():
        # Forget any user
        session.clear()

        # Send to login page
        return redirect("/")

# Start practise route
@app.route("/practise", methods=["GET", "POST"])
@login_required
def practise():
        # Types of questions
        q_types = ["addition", "subtraction", "multiplication", "division", "exponentiation"]

        # User submitted a form
        if request.method == "POST":
                # Get form data
                questions = request.form.get("questions")
                q_type = request.form.get("q_type")

                # Ensure data is valid
                if not questions:
                        return error("No question amount given", "/practise")
                elif not q_type:
                        return error("No type of question given", "/practise")
                elif q_type not in q_types:
                        return error("Invalid question type", "/practise")

                # Add session to database
                rn = datetime.datetime.now()
                database.execute("INSERT INTO practise_rounds (user_id, questions, q_type, start_time) VALUES(?, ?, ?, ?)", session["user_id"], questions, q_type, rn)

                # Send to round
                id = database.execute("SELECT id FROM practise_rounds WHERE user_id = ? AND questions = ? AND q_type = ? AND start_time = ?", session["user_id"], questions, q_type, rn)[0]["id"]
                return redirect(f"/practise/round?id={id}")
        else:
                return render_template("practise.html")

# Practise round route
@app.route("/practise/round", methods=["GET", "POST"])
@login_required
def practise_round():
        if request.method == "GET":
                # Get the round id
                r_id = request.args.get("id")

                # See if round is done
                q_num = database.execute("SELECT COUNT(id) FROM questions WHERE round_id = ? AND user_ans IS NOT NULL", r_id)[0]["COUNT(id)"]
                questions = database.execute("SELECT questions FROM practise_rounds WHERE id = ?", r_id)[0]["questions"]
                if q_num >= questions:
                        return redirect(f"/practise/finish?id={r_id}")

                # Generate question
                q_type = database.execute("SELECT q_type FROM practise_rounds WHERE id = ?", r_id)[0]["q_type"]
                if q_type == "addition" or q_type == "subtraction":
                        data = random(2, 1, 128)
                elif q_type == "multiplication":
                        data = random(2, 1, 32)
                elif q_type == "division":
                        data = random(1, 2, 16)
                        data += random(1, 16, 256)
                elif q_type == "exponentiation":
                        data = random(1, 1, 16)
                        data += random(1, 2, 3)

                # Add question to database
                database.execute("INSERT INTO questions (round_id, operand_1, operand_2) VALUES(?, ?, ?)", r_id, data[0], data[1])
                id = database.execute("SELECT id FROM questions WHERE round_id = ? AND operand_1 = ? AND operand_2 = ? ORDER BY id DESC LIMIT 1", r_id, data[0], data[1])[0]["id"]

                # Print question
                operand_1 = data[0]
                operand_2 = data[1]
                latex = ""
                if q_type == "addition":
                        latex = f"$${operand_1}+{operand_2}$$"
                elif q_type == "subtraction":
                        latex = f"$${operand_1}-{operand_2}$$"
                elif q_type == "multiplication":
                        latex = "$$" + str(operand_1) + " \\" + "times" + " " + str(operand_2) + "$$"
                elif q_type == "division":
                        latex = "$$" + str(operand_1) + " \\" + "div" + " " + str(operand_2) + "$$"
                elif q_type == "exponentiation":
                        latex = f"$${operand_1}^{operand_2}$$"
                return render_template("question.html", latex=latex, type=q_type, round=r_id, id=id)
        else:
                # Get form data
                r_id = request.form.get("round")
                q_id = request.form.get("id")
                q_type = database.execute("SELECT q_type FROM practise_rounds WHERE id = ?", q_id)
                answer = request.form.get("answer")

                # Add answer to database
                database.execute("UPDATE questions SET user_ans = ? WHERE id = ?", answer, q_id)

                # Send user to next question
                return redirect(f"/practise/round?id={r_id}")

# Practise round summary route
@app.route("/practise/finish")
@login_required
def practise_finish():
        # Get the round id
        id = request.args.get("id")

        # Add end time to database
        rn = datetime.datetime.now()
        database.execute("UPDATE practise_rounds SET end_time = ? WHERE id = ?", rn, id)

        # Calculate score
        questions_num = database.execute("SELECT questions FROM practise_rounds WHERE id = ?", id)[0]["questions"]
        q_type = database.execute("SELECT q_type FROM practise_rounds WHERE id = ?", id)[0]["q_type"]
        questions = database.execute("SELECT * FROM questions WHERE round_id = ?", id)
        score = 0
        for question in questions:
                if q_type == "addition":
                        if int(question["user_ans"]) == int(question["operand_1"]) + int(question["operand_2"]):
                                score += 1
                elif q_type == "subtraction":
                        if int(question["user_ans"]) == int(question["operand_1"]) - int(question["operand_2"]):
                                score += 1
                elif q_type == "multiplication":
                        if int(question["user_ans"]) == int(question["operand_1"]) * int(question["operand_2"]):
                                score += 1
                elif q_type == "division":
                        if int(question["user_ans"]) == int(question["operand_1"]) / int(question["operand_2"]):
                                score += 1
                elif q_type == "exponentiation":
                        if int(question["user_ans"]) == int(question["operand_1"]) ** int(question["operand_2"]):
                                score += 1
        percent = math.ceil(score / questions_num * 100)

        # Calculate time
        end = database.execute("SELECT end_time FROM practise_rounds WHERE id = ?", id)[0]["end_time"]
        start = database.execute("SELECT start_time FROM practise_rounds WHERE id = ?", id)[0]["start_time"]
        end = datetime.datetime.fromisoformat(end)
        start = datetime.datetime.fromisoformat(start)
        time = str(end - start)
        min = time[2:4]
        sec = time[5:10]

        # Calculate per second score
        seconds = int(min) * 60 + int(sec)
        persec = round(seconds / questions_num, 2)

        # Print question
        return render_template("summary.html", correct=score, questions=questions_num, score=percent, minutes=min, seconds=sec, per=persec, id=id)

# Practise round practise route
@app.route("/practise/practise", methods=["GET", "POST"])
@login_required
def practise_practise():
        if request.method == "GET":
                # Get the round id
                r_id = request.args.get("id")
                q_needed = json.loads(request.args.get("q_needed"))
                prev_a = request.args.get("prev_a")
                justin = request.args.get("justin")

                # See if practise is done
                if len(q_needed) == 0 and justin == "False":
                        return redirect("/")

                # Lookup questions
                if justin == "True":
                        q_needed = []
                        q_type = database.execute("SELECT q_type FROM practise_rounds WHERE id = ?", r_id)[0]["q_type"]
                        questions = database.execute("SELECT * FROM questions WHERE round_id = ?", r_id)
                        for question in questions:
                                if q_type == "addition":
                                        if int(question["user_ans"]) != int(question["operand_1"]) + int(question["operand_2"]):
                                                q_needed.append(question["id"])
                                elif q_type == "subtraction":
                                        if int(question["user_ans"]) != int(question["operand_1"]) - int(question["operand_2"]):
                                                q_needed.append(question["id"])
                                elif q_type == "multiplication":
                                        if int(question["user_ans"]) != int(question["operand_1"]) * int(question["operand_2"]):
                                                q_needed.append(question["id"])
                                elif q_type == "division":
                                        if int(question["user_ans"]) != int(question["operand_1"]) / int(question["operand_2"]):
                                                q_needed.append(question["id"])
                                elif q_type == "exponentiation":
                                        if int(question["user_ans"]) != int(question["operand_1"]) ** int(question["operand_2"]):
                                                q_needed.append(question["id"])

                # Lookup question
                q_id = q_needed[0]
                operand_1 = database.execute("SELECT operand_1 FROM questions WHERE id = ?", q_id)[0]["operand_1"]
                operand_2 = database.execute("SELECT operand_2 FROM questions WHERE id = ?", q_id)[0]["operand_2"]

                # Print question
                latex = ""
                q_type = database.execute("SELECT q_type FROM practise_rounds WHERE id = ?", r_id)[0]["q_type"]
                if q_type == "addition":
                        latex = f"$${operand_1}+{operand_2}$$"
                elif q_type == "subtraction":
                        latex = f"$${operand_1}-{operand_2}$$"
                elif q_type == "multiplication":
                        latex = "$$" + str(operand_1) + " \\" + "times" + " " + str(operand_2) + "$$"
                elif q_type == "division":
                        latex = "$$" + str(operand_1) + " \\" + "div" + " " + str(operand_2) + "$$"
                elif q_type == "exponentiation":
                        latex = f"$${operand_1}^{operand_2}$$"
                return render_template("wrong.html", prevresult=prev_a, latex=latex, type=q_type, round=r_id, id=q_id, q_needed=q_needed)
        else:
                # Get form data
                r_id = request.form.get("round")
                q_id = request.form.get("id")
                q_type = database.execute("SELECT q_type FROM practise_rounds WHERE id = ?", r_id)[0]["q_type"]
                q_needed = json.loads(request.form.get("q_needed"))
                u_answer = request.form.get("answer")

                # Calculate answer
                questions = database.execute("SELECT * FROM questions WHERE id = ?", q_id)
                if q_type == "addition":
                        answer = int(questions[0]["operand_1"]) + int(questions[0]["operand_2"])
                elif q_type == "subtraction":
                        answer = int(questions[0]["operand_1"]) - int(questions[0]["operand_2"])
                elif q_type == "multiplication":
                        answer = int(questions[0]["operand_1"]) * int(questions[0]["operand_2"])
                elif q_type == "division":
                        answer = int(questions[0]["operand_1"]) / int(questions[0]["operand_2"])
                elif q_type == "exponentiation":
                        answer = int(questions[0]["operand_1"]) ** int(questions[0]["operand_2"])

                if int(u_answer) == int(answer):
                        ansstr = "Your answer was correct!"
                else:
                        ansstr = f"The correct answer was $${answer}$$."

                # Process q_needed
                del q_needed[0]

                # Send user to next question
                return redirect(f"/practise/practise?id={r_id}&q_needed={q_needed}&prev_a={ansstr}&justin=False")

# Statistics route
@app.route("/stats")
def stats():
        # User is logged in
        try:
                print(session["user_id"])
        except:
                # Calculate average accuracy worldwide
                questions_num = database.execute("SELECT SUM(questions) FROM practise_rounds")[0]["SUM(questions)"]
                score = 0
                questions = database.execute("SELECT * FROM questions")
                for question in questions:
                        q_type = database.execute("SELECT q_type FROM practise_rounds WHERE id = ?", question["round_id"])[0]["q_type"]
                        if q_type == "addition":
                                if int(question["user_ans"]) == int(question["operand_1"]) + int(question["operand_2"]):
                                        score += 1
                        elif q_type == "subtraction":
                                if int(question["user_ans"]) == int(question["operand_1"]) - int(question["operand_2"]):
                                        score += 1
                        elif q_type == "multiplication":
                                if int(question["user_ans"]) == int(question["operand_1"]) * int(question["operand_2"]):
                                        score += 1
                        elif q_type == "division":
                                if int(question["user_ans"]) == int(question["operand_1"]) / int(question["operand_2"]):
                                        score += 1
                        elif q_type == "exponentiation":
                                if int(question["user_ans"]) == int(question["operand_1"]) ** int(question["operand_2"]):
                                        score += 1
                percent = math.ceil(score / questions_num * 100)

                # Calculate average time worldwide
                persec = []
                for rnd in database.execute("SELECT * FROM practise_rounds"):
                        questions_num = rnd["questions"]
                        end = rnd["end_time"]
                        start = rnd["start_time"]
                        end = datetime.datetime.fromisoformat(end)
                        start = datetime.datetime.fromisoformat(start)
                        time = str(end - start)
                        min = time[2:4]
                        sec = time[5:10]
                        seconds = int(min) * 60 + int(sec)
                        persec.append(round(seconds / questions_num, 2))
                persec = round(sum(persec) / len(persec), 2)

                return render_template("statt.html", avg_acc_glob=percent, avg_time_glob=persec)
        else:
                # Calculate average accuracy
                rounds = database.execute("SELECT id FROM practise_rounds WHERE user_id = ?", session["user_id"])
                questions_num = database.execute("SELECT SUM(questions) FROM practise_rounds WHERE user_id = ?", session["user_id"])[0]["SUM(questions)"]
                score = 0
                for rnd in rounds:
                        id = rnd["id"]
                        questions = database.execute("SELECT * FROM questions WHERE round_id = ?", id)
                        for question in questions:
                                q_type = database.execute("SELECT q_type FROM practise_rounds WHERE id = ?", question["round_id"])[0]["q_type"]
                                if q_type == "addition":
                                        if int(question["user_ans"]) == int(question["operand_1"]) + int(question["operand_2"]):
                                                score += 1
                                elif q_type == "subtraction":
                                        if int(question["user_ans"]) == int(question["operand_1"]) - int(question["operand_2"]):
                                                score += 1
                                elif q_type == "multiplication":
                                        if int(question["user_ans"]) == int(question["operand_1"]) * int(question["operand_2"]):
                                                score += 1
                                elif q_type == "division":
                                        if int(question["user_ans"]) == int(question["operand_1"]) / int(question["operand_2"]):
                                                score += 1
                                elif q_type == "exponentiation":
                                        if int(question["user_ans"]) == int(question["operand_1"]) ** int(question["operand_2"]):
                                                score += 1
                percent2 = round(score / questions_num * 100, 2)

                # Calculate average time
                persec = []
                for rnd in database.execute("SELECT * FROM practise_rounds WHERE user_id = ?", session["user_id"]):
                        questions_num = rnd["questions"]
                        end = rnd["end_time"]
                        start = rnd["start_time"]
                        end = datetime.datetime.fromisoformat(end)
                        start = datetime.datetime.fromisoformat(start)
                        time = str(end - start)
                        min = time[2:4]
                        sec = time[5:10]
                        seconds = int(min) * 60 + int(sec)
                        persec.append(round(seconds / questions_num, 2))
                persec2 = round(sum(persec) / len(persec), 2)

                # Calculate average accuracy worldwide
                questions_num = database.execute("SELECT SUM(questions) FROM practise_rounds")[0]["SUM(questions)"]
                score = 0
                questions = database.execute("SELECT * FROM questions")
                for question in questions:
                        q_type = database.execute("SELECT q_type FROM practise_rounds WHERE id = ?", question["round_id"])[0]["q_type"]
                        if q_type == "addition":
                                if int(question["user_ans"]) == int(question["operand_1"]) + int(question["operand_2"]):
                                        score += 1
                        elif q_type == "subtraction":
                                if int(question["user_ans"]) == int(question["operand_1"]) - int(question["operand_2"]):
                                        score += 1
                        elif q_type == "multiplication":
                                if int(question["user_ans"]) == int(question["operand_1"]) * int(question["operand_2"]):
                                        score += 1
                        elif q_type == "division":
                                if int(question["user_ans"]) == int(question["operand_1"]) / int(question["operand_2"]):
                                        score += 1
                        elif q_type == "exponentiation":
                                if int(question["user_ans"]) == int(question["operand_1"]) ** int(question["operand_2"]):
                                        score += 1
                percent = round(score / questions_num * 100, 2)

                # Calculate average time worldwide
                persec = []
                for rnd in database.execute("SELECT * FROM practise_rounds"):
                        questions_num = rnd["questions"]
                        end = rnd["end_time"]
                        start = rnd["start_time"]
                        end = datetime.datetime.fromisoformat(end)
                        start = datetime.datetime.fromisoformat(start)
                        time = str(end - start)
                        min = time[2:4]
                        sec = time[5:10]
                        seconds = int(min) * 60 + int(sec)
                        persec.append(round(seconds / questions_num, 2))
                persec = round(sum(persec) / len(persec), 2)

                return render_template("stats.html", avg_acc=percent2, avg_time=persec2, avg_acc_glob=percent, avg_time_glob=persec)
