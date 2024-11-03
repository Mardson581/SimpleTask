from app import app
from flask import make_response, request, render_template, redirect
import uuid
from app.entity import User

#Teste
user_db = dict()

@app.route('/')
def index_page():
    data = uuid.uuid4()
    response = make_response(f"<h1>Some random data here: {data}</h1>")
    response.set_cookie("session_id", data.__str__(), samesite="Strict")
    return response

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    name = request.values.get("username")
    email = request.values.get("email")
    password = request.values.get("password")

    try:
        user = User(username=name, email=email, password=password)
        session_id = uuid.uuid4()
        user_db[str(session_id)] = user
        response = make_response(redirect("home"))
        response.set_cookie("user", user.__repr__(), samesite="Strict")
        response.set_cookie("session_id", str(session_id), samesite="Strict", httponly=True)
        return response
    except Exception:
        return render_template("login.html", warning="User or password is incorrect!")

@app.route("/home")
def home_page():
    user = user_db[request.cookies.get("session_id")]
    return render_template("home.html", user=user)