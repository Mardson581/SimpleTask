from http.client import responses
from sqlite3 import OperationalError

from flask import make_response, request, render_template, redirect

from app.auth import signup_user, authenticate_user, login_user, is_authenticated, logoff_user
from app.entity import User
from app import app
import uuid


@app.route('/')
def index_page():
    data = uuid.uuid4()
    response = make_response(f"<h1>Some random data here: {data}</h1>")
    return response


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if is_authenticated(request.cookies["session_id"]):
        return make_response(redirect("/home"))
    if request.method == "GET":
        return render_template("login.html")

    try:
        user = User(
            username=request.values["username"],
            password=request.values["password"]
        )

        if login_user(user):
            session_id = login_user(user)
            response = make_response(redirect("/home"))
            response.set_cookie("session_id", session_id, httponly=True, samesite="Strict")

            return response
    except ValueError as e:
        return render_template("login.html", warning=e.__str__())
    except OperationalError as e:
        return render_template("login.html", warning="An internal error was occurred. Try again later")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if is_authenticated(request.cookies["session_id"]):
        return make_response(redirect("/home"))
    if request.method == "GET":
        return render_template("signup.html")

    try:
        user = User(
            username=request.values["username"],
            password=request.values["password"],
            email=request.values["email"]
        )

        if signup_user(user):
            session_id = authenticate_user(user)
            response = make_response(redirect("/home"))
            response.set_cookie("session_id", session_id, httponly=True, samesite="Strict")

            return response
    except ValueError as e:
        return render_template("signup.html", warning=e.__str__())
    except OperationalError as e:
        return render_template("signup.html", warning="An internal error was occurred. Try again later")

@app.route("/logout")
def logout():
    session_id = request.cookies["session_id"]
    if session_id:
        logoff_user(session_id)
    response = make_response(redirect("/"))
    response.set_cookie("session_id", "", httponly=True, samesite="Strict")
    return response

@app.route("/home")
def home_page():
    if not is_authenticated(request.cookies["session_id"]):
        return make_response(redirect("/login"))
    return render_template("home.html", session_id=request.cookies['session_id'])
