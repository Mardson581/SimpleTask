import uuid
from sqlite3 import OperationalError

from flask import make_response, request, render_template, redirect
from werkzeug.exceptions import BadRequestKeyError

from app import app
from app import tasks
from app.auth import signup_user, authenticate_user, login_user, is_authenticated, logoff_user
from app.entity import User, TaskStatus
from app.tasks import list_tasks, update_task_status, get_user_session, delete_task_by_id


@app.route('/')
def index_page():
    data = uuid.uuid4()
    response = make_response(f"<h1>Some random data here: {data}</h1>")
    return response


@app.route("/login", methods=["GET", "POST"])
def login_page():
    try:
        session_id = request.cookies["session_id"]
    except BadRequestKeyError:
        response = make_response(redirect("/login"))
        response.set_cookie("session_id", "", httponly=True, samesite="Strict")
        return response

    if is_authenticated(session_id):
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
    try:
        session_id = request.cookies["session_id"]
    except BadRequestKeyError:
        response = make_response(redirect("/login"))
        response.set_cookie("session_id", "", httponly=True, samesite="Strict")
        return response

    if is_authenticated(session_id):
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
    try:
        session_id = request.cookies["session_id"]
    except BadRequestKeyError:
        response = make_response(redirect("/login"))
        response.set_cookie("session_id", "", httponly=True, samesite="Strict")
        return response

    if session_id:
        logoff_user(session_id)
    response = make_response(redirect("/"))
    response.set_cookie("session_id", "", httponly=True, samesite="Strict")
    return response


@app.route("/home")
def home_page(warning: str = None):
    try:
        session_id = request.cookies["session_id"]
    except BadRequestKeyError:
        response = make_response(redirect("/login"))
        response.set_cookie("session_id", "", httponly=True, samesite="Strict")
        return response

    if not is_authenticated(session_id):
        return make_response(redirect("/login"))
    try:
        tasks = list_tasks(request.cookies["session_id"])

        if len(tasks) > 0:
            current_task = None if tasks[0].status != TaskStatus.IN_PROGRESS else tasks.pop(0)
        else:
            current_task = None
    except ValueError as e:
        return make_response(redirect("/login"))
    return render_template("home.html", session_id=request.cookies['session_id'], tasks=tasks,
                           current_task=current_task, warning=warning)


@app.route("/add-task", methods=["POST"])
def add_task_page():
    try:
        session_id = request.cookies["session_id"]
    except BadRequestKeyError:
        response = make_response(redirect("/login"))
        response.set_cookie("session_id", "", httponly=True, samesite="Strict")
        return response

    if not is_authenticated(session_id):
        return make_response(redirect("/login"))

    try:
        task_name = request.values["task_name"]
        task_description = request.values["task_description"]
        task_status = request.values["task_status"]
        tasks.add_task(session_id, task_name, task_description, task_status)
    except ValueError as e:
        return render_template("home.html", warning=request.values)
    except OperationalError as e:
        return render_template("signup.html", warning="An internal error was occurred. Try again later")
    except BadRequestKeyError:
        render_template("home.html", warning="An error was occurred while creating task. Try again later.")

    return make_response(redirect("/home"))


@app.route("/mark-done/<int:task_id>", methods=["POST"])
def mark_done(task_id: int):
    try:
        session_id = request.cookies["session_id"]
    except BadRequestKeyError:
        response = make_response(redirect("/login"))
        response.set_cookie("session_id", "", httponly=True, samesite="Strict")
        return response

    if not is_authenticated(session_id):
        return make_response(redirect("/login"))

    user = get_user_session(session_id)
    if not user:
        return make_response(redirect("/login"))

    if update_task_status(task_id, TaskStatus.DONE, user.id):
        return make_response(redirect("/home"))
    else:
        return home_page(warning="An error was occurred while trying to update the task!"), 401


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id: int):
    try:
        session_id = request.cookies["session_id"]
    except BadRequestKeyError:
        response = make_response(redirect("/login"))
        response.set_cookie("session_id", "", httponly=True, samesite="Strict")
        return response

    if not is_authenticated(session_id):
        return make_response(redirect("/login"))

    user = get_user_session(session_id)
    if not user:
        return make_response(redirect("/login"))

    if delete_task_by_id(task_id, user.id):
        return make_response(redirect("/home"))
    else:
        return home_page(warning="An error was occurred while trying to delete the task!"), 401


@app.route("/update", methods=["POST"])
def update_task():
    try:
        session_id = request.cookies["session_id"]
    except BadRequestKeyError:
        response = make_response(redirect("/login"))
        response.set_cookie("session_id", "", httponly=True, samesite="Strict")
        return response

    if not is_authenticated(session_id):
        return make_response(redirect("/login"))

    user = get_user_session(session_id)
    if not user:
        return make_response(redirect("/login"))

    try:
        task_name = request.values["update_task_name"]
        task_description = request.values["update_task_description"]
        task_status = request.values["task_status"]
        task_id = request.values["update_task_id"]

        status = TaskStatus(task_status)
        tasks.update_task_status(task_id=int(task_id), task_status=status, user_id=user.id)
    except ValueError as e:
        return render_template("home.html", warning=request.values)
    except OperationalError as e:
        return render_template("signup.html", warning="An internal error was occurred. Try again later")
    except BadRequestKeyError:
        render_template("home.html", warning="An error was occurred while creating task. Try again later.")

    return make_response(redirect("/home"))


@app.errorhandler(code_or_exception=404)
def error_page(exception):
    return render_template("error.html", message="The page you were looking for was not found!",
                           title="Page Not Found"), 404


@app.errorhandler(code_or_exception=500)
def error_page(exception):
    return render_template("error.html", message="An internal error was occurred. Try again later",
                           title="The server is sleeping..."), 500


@app.errorhandler(code_or_exception=405)
def error_page(exception):
    return render_template("error.html", message="You are not supposed to be here >:-(",
                           title="Someone is trying to hack us!"), 405
