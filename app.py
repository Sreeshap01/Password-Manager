import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.fernet import Fernet

from helpers import apology, login_required, lookup, usd, contains_letter, contains_digit, enough_characters

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///passmanager.db")


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
    """Show sites registered"""
    rows = db.execute(
        "select id,siteurl, nickname from sitedetails where userid = ?", session["user_id"]
    )

    return render_template(
        "index.html", rows=rows
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password contains atleast a  letter
        elif (not contains_letter(request.form.get("password"))):
            return apology("Password criteria has not been met", 400)

        # Ensure password contains atleast a digit
        elif (not contains_digit(request.form.get("password"))):
            return apology("Password criteria has not been met", 400)

        # Ensure password length is atleast 8 characters
        elif (not enough_characters(request.form.get("password"))):
            return apology("Password criteria has not been met", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure confirmation was same as password
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("confirmation and password do not match", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username is not taken
        if len(rows) != 0:
            return apology("username already exists!", 400)

        # create new user in the database
        rows = db.execute(
            "INSERT INTO users (username,hash) VALUES(?,?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )
        # Remember which user has logged in
        session["user_id"] = rows

        # Redirect user to home page
        flash("Registered!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change password"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure old password was submitted
        if not request.form.get("oldpassword"):
            return apology("must provide old password", 400)

        # Ensure old password was correct
        # Get the password in the database
        rows = db.execute(
            "SELECT hash FROM users WHERE id = ?",
            session["user_id"],
        )
        if not check_password_hash(rows[0]["hash"], request.form.get("oldpassword")):
            return apology("old password is incorrect", 400)

        # Ensure new password was submitted
        elif not request.form.get("password"):
            return apology("must provide new password", 400)

        # Ensure password contains atleast a  letter
        elif (not contains_letter(request.form.get("password"))):
            return apology("Password criteria has not been met", 400)

        # Ensure password contains atleast a digit
        elif (not contains_digit(request.form.get("password"))):
            return apology("Password criteria has not been met", 400)

        # Ensure password length is atleast 8 characters
        elif (not enough_characters(request.form.get("password"))):
            return apology("Password criteria has not been met", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure confirmation was same as password
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("confirmation and password do not match", 400)

        # update the password in the database
        rows = db.execute(
            "UPDATE USERS SET hash = ? where id = ?",
            generate_password_hash(request.form.get("password")),
            session["user_id"]
        )

        # Redirect user to home page
        flash("Password Updated!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepassword.html")


@app.route("/addpassword", methods=["GET", "POST"])
@login_required
def addpassword():
    """Add login details of the site"""
    if request.method == "POST":
        # Ensure Site URL is not empty
        if not request.form.get("siteurl"):
            return apology("Missing Site URL", 400)

         # Ensure User Name is not empty
        if not request.form.get("username"):
            return apology("Missing User Name", 400)

        # Ensure Password is not empty
        if not request.form.get("sitepassword"):
            return apology("Missing password", 400)

        # Ensure confirmation is not empty
        if not request.form.get("confirmation"):
            return apology("Missing confirmation", 400)

        # Ensure confirmation is same as password
        if not request.form.get("confirmation") == request.form.get("sitepassword"):
            return apology("confirmation and password do not match", 400)

        # Query database for site url
        rows = db.execute(
            "SELECT siteurl FROM sitedetails WHERE userid = ?",
            session["user_id"]
        )
        # For each record in database, get a list of values of siteurl
        siteurls_list = []
        for row in rows:
            for value in row.values():
                siteurls_list.append(value)

        # Ensure site url  is not already saved
        if request.form.get("siteurl") in siteurls_list:
            return apology("Site URL already exists!", 400)

        # Generate a key and instantiate a Fernet instance
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        keytext = key.decode()

        # Encrypt a password
        encrypted_password = cipher_suite.encrypt(request.form.get("sitepassword").encode())
        encrypted_passtext = encrypted_password.decode()

        # Save
        rows = db.execute(
            "INSERT INTO sitedetails (siteurl, nickname, username, password, key, userid) VALUES(?,?,?,?,?,?)",
            request.form.get("siteurl"),
            request.form.get("nickname"),
            request.form.get("username"),
            encrypted_passtext,
            keytext,
            session["user_id"],
        )

        # Redirect user to home page
        flash("Login details Added!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("addpassword.html")


@app.route("/detail/<id>", methods=["GET"])
@login_required
def detail(id):
    """display the login details of the item selected from the table"""

    # Use the id to fetch the record from the database
    rows = db.execute(
        "select siteurl, nickname,username from \
        sitedetails where id = ?", id
    )
    # Pass the record data to the template
    return render_template("detail.html", rows=rows, id=id)

    # Redirect user to index page
    return redirect("/")


@app.route("/modify/<id>", methods=["GET", "POST"])
@login_required
def modify(id):
    """Modify login details of the site"""
    if request.method == "POST":
        # Ensure Site URL is not empty
        if not request.form.get("siteurl"):
            return apology("Missing Site URL", 400)

        # Ensure User Name is not empty
        if not request.form.get("username"):
            return apology("Missing User Name", 400)

         # Ensure Password is not empty
        if not request.form.get("sitepassword"):
            return apology("Missing password", 400)

        # Ensure confirmation is not empty
        if not request.form.get("confirmation"):
            return apology("Missing confirmation", 400)

        # Ensure confirmation is same as password
        if not request.form.get("confirmation") == request.form.get("sitepassword"):
            return apology("confirmation and password do not match", 400)

        # Query database for site url
        rows = db.execute(
            "SELECT siteurl FROM sitedetails WHERE userid = ? and id <> ?",
            session["user_id"], id
        )
        # For each record in database, get a list of values of siteurl
        siteurls_list = []
        for row in rows:
            for value in row.values():
                siteurls_list.append(value)
        print(siteurls_list)

        # Ensure site url  is not already saved
        if request.form.get("siteurl") in siteurls_list:
            return apology("Site URL already exists!", 400)

        # Encrypt the modified password
        # Get the key for the item from the db
        rows = db.execute(
            "select key from \
        sitedetails where id = ?", id
        )

        key = (rows[0]['key'].encode())
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(request.form.get("sitepassword").encode())
        encrypted_passtext = encrypted_password.decode()

        # Update the record in the database
        rows = db.execute(
            "UPDATE SITEDETAILS SET siteurl = ?,nickname = ?,username = ?,password = ? where id = ?",
            request.form.get("siteurl"), request.form.get("nickname"), request.form.get("username"),
            encrypted_passtext, id
        )

        flash("Login details updated!")
        # Redirect user to the detail page
        return redirect("/detail/" + id)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Query database
        rows = db.execute(
            "select siteurl, nickname,username,id,password,key from \
            sitedetails where id = ?", id
        )

        # decrypt password
        key = (rows[0]['key'].encode())
        cipher_suite = Fernet(key)

        decrypted_password = cipher_suite.decrypt(rows[0]['password'])
        return render_template("modify.html", rows=rows, password=decrypted_password.decode())


@app.route("/delete/<id>", methods=["DELETE"])
@login_required
def delete(id):
    """display a warning """
    print(id)
    if request.method == "DELETE":
        # Delete the record from the db
        rows = db.execute(
            "delete from \
        sitedetails where id = ?", id
        )
    print("deleted")
    flash("Login details deleted!")
    # Return a JSON response with a success
    return jsonify({'result': 'success'})
