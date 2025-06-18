import csv, datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    transacted_r = db.execute(
        "SELECT DISTINCT(symbol) FROM transactions WHERE user = ?", session["user_id"]
    )
    # convmult = lookup(
    #     f"USD{db.execute('SELECT currency FROM users WHERE id = ?', session['user_id'])[0]['currency']}=X".upper()
    # )["price"]
    owned = {}
    for symbol in transacted_r:
        stock = symbol["symbol"]
        shares = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE user = ? AND symbol = ?",
            session["user_id"],
            stock,
        )[0]["SUM(shares)"]
        owned[stock] = [
            shares,
            lookup(stock.upper())["price"],  # * convmult
            shares * lookup(stock.upper())["price"],  # * convmult
        ]
    total = 0
    for stock in list(owned.keys()):
        if owned[stock][0] <= 0 or stock == "CASH":
            del owned[stock]
        else:
            total += owned[stock][2]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0][
        "cash"
    ]  # * convmult
    total += cash
    return render_template("index.html", owned=owned, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("u suck")
        elif not request.form.get("shares"):
            return apology("u suck")
        try:
            if int(request.form.get("shares")) <= 0:
                return apology("u suck")
        except ValueError:
            return apology("u suck")
        results = lookup(request.form.get("symbol").upper())
        if results == None:
            return apology("u suck")
        price = results["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0][
            "cash"
        ]
        if price > cash:
            return apology("u suck")
        db.execute(
            "INSERT INTO transactions (user, symbol, shares, price, time) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            request.form.get("symbol").upper(),
            request.form.get("shares"),
            price,
            str(datetime.datetime.now())[:-7],
        )
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash - price * int(request.form.get("shares")),
            session["user_id"],
        )
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # convmult = lookup(
    #     f"USD{db.execute('SELECT currency FROM users WHERE id = ?', session['user_id'])[0]['currency']}=X".upper()
    # )["price"]
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user = ?", session["user_id"]
    )
    for transaction in transactions:
        transaction["price"] = float(transaction["price"])  # * convmult
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT hash, id FROM users WHERE username = ?",
            request.form.get("username"),
        )
        print(rows)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("u suck")
        results = lookup(request.form.get("symbol").upper())
        if results == None:
            return apology("u suck")
        # convmult = lookup(
        #     f"USD{db.execute('SELECT currency FROM users WHERE id = ?', session['user_id'])[0]['currency']}=X".upper()
        # )["price"]
        price = results["price"]  # * convmult
        return render_template("quoted.html", symbol=results["symbol"], price=price)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        usernames_r = db.execute("SELECT username FROM users")
        usernames = []
        for username in usernames_r:
            uname = username["username"]
            usernames.append(uname)
        if not request.form.get("username"):
            return apology("u suck")
        elif request.form.get("username") in usernames:
            return apology("u suck")
        elif not request.form.get("password"):
            return apology("u suck")
        elif not request.form.get("confirmation"):
            return apology("u suck")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("u suck")
        password_hash = generate_password_hash(request.form.get("password"))
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)",
            request.form.get("username"),
            password_hash,
        )
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    transacted_r = db.execute(
        "SELECT DISTINCT(symbol) FROM transactions WHERE user = ?",
        session["user_id"],
    )
    owned = {}
    for symbol in transacted_r:
        stock = symbol["symbol"].upper()
        shares = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE user = ? AND symbol = ?",
            session["user_id"],
            stock,
        )[0]["SUM(shares)"]
        owned[stock] = shares
    for stock in list(owned.keys()):
        if owned[stock] <= 0 or stock == "CASH":
            del owned[stock]

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("u suck")
        elif request.form.get("symbol").upper() not in owned:
            return apology("u suck")
        elif not request.form.get("shares"):
            return apology("u suck")
        elif int(request.form.get("shares")) <= 0:
            return apology("u suck")
        elif (
            int(request.form.get("shares")) > owned[request.form.get("symbol").upper()]
        ):
            return apology("u suck")
        results = lookup(request.form.get("symbol").upper())
        if results == None:
            return apology("u suck")
        price = results["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0][
            "cash"
        ]
        db.execute(
            "INSERT INTO transactions (user, symbol, shares, price, time) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            request.form.get("symbol").upper(),
            int(request.form.get("shares")) * -1,
            price,
            str(datetime.datetime.now())[:-7],
        )
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash + price * int(request.form.get("shares")),
            session["user_id"],
        )
        return redirect("/")
    else:
        return render_template("sell.html", owned=owned)


@app.route("/atm", methods=["GET", "POST"])
@login_required
def atm():
    """Deposit and withdraw cash."""
    if request.method == "POST":
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0][
            "cash"
        ]
        if not request.form.get("action"):
            return apology("u suck")
        elif (
            request.form.get("action") != "deposit"
            and request.form.get("action") != "withdraw"
        ):
            return apology("u suck")
        elif not request.form.get("amount"):
            return apology("u suck")
        elif (
            request.form.get("action") == "withdraw"
            and int(request.form.get("amount")) > cash
        ):
            return apology("u suck")
        action = request.form.get("action")
        if action == "deposit":
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                cash + int(request.form.get("amount")),
                session["user_id"],
            )
            db.execute(
                "INSERT INTO transactions (user, symbol, shares, price, time) VALUES (?, ?, ?, ?, ?)",
                session["user_id"],
                "CASH",
                request.form.get("amount"),
                request.form.get("amount"),
                str(datetime.datetime.now())[:-7],
            )
        else:
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                cash - int(request.form.get("amount")),
                session["user_id"],
            )
            db.execute(
                "INSERT INTO transactions (user, symbol, shares, price, time) VALUES (?, ?, ?, ?, ?)",
                session["user_id"],
                "CASH",
                request.form.get("amount") * -1,
                request.form.get("amount") * -1,
                str(datetime.datetime.now())[:-7],
            )
        return redirect("/")
    else:
        return render_template("atm.html")


# @app.route("/acct/settings", methods=["GET", "POST"])
# @login_required
# def settings():
#     """Change currencies."""
#     if request.method == "POST":
#         db.execute(
#             "UPDATE users SET currency = ? WHERE id = ?",
#             request.form.get("currency"),
#             session["user_id"],
#         )
#         return redirect("/")
#     else:
#         currencies = {}
#         with open("currencies.csv", "r") as file:
#             reader = csv.DictReader(file)
#             next(reader)
#             for row in reader:
#                 if (
#                     db.execute(
#                         "SELECT currency FROM users WHERE id = ?", session["user_id"]
#                     )[0]["currency"]
#                     == row["currency"]
#                 ):
#                     currencies[row["currency"]] = {
#                         "fullform": row["fullform"],
#                         "seld": "selected",
#                     }
#                 else:
#                     currencies[row["currency"]] = {
#                         "fullform": row["fullform"],
#                         "seld": "",
#                     }
#         return render_template("settings.html", currencies=currencies)
