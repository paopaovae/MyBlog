import functools

from flask import Blueprint
from flask import flash
import datetime
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        )

@bp.route("/register", methods=("GET", "POST"))
def register():

    if request.method == "POST":
        user_name = request.form["username"]
        user_pass = request.form["password"]
        user_email = request.form["email"]
        user_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_level = 1

        db = get_db()
        error = None

        if user_name is None:
            error = "Username is required."
        elif user_pass is None:
            error = "Username is reuqired."
        elif user_email is None:
            error = "User email is required."
        elif(
            db.execute("SELECT user_name FROM users WHERE user_name = ?", (user_name, )).fetchone()
            is not None
        ):
            error = "User {0} is already registered.".format(user_name)

        if error is None:
            db.execute("INSERT INTO users (user_name, user_pass, user_email, user_date, user_level) VALUES (?,?,?,?,?)",
            (user_name, generate_password_hash(user_pass), user_email, user_date, user_level))
            db.commit()
            return redirect(url_for("auth.login"))
        else:
            flash(error)

    else:
        return render_template("auth/register.html")

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        user_name = request.form["username"]
        user_pass = request.form["password"]
        db = get_db()
        error = None

        user = db.execute("SELECT * FROM users WHERE user_name = ?", (user_name,)).fetchone()

        if user_name is None:
            error = "Incorrect user name."
        elif not check_password_hash(user["user_pass"], user_pass):
            error = "Incorrect user password."

        if error is None:
            session.clear()
            session["user_id"] = user["user_id"]
            return redirect(url_for("blog.index"))
        else:
            flash(error)
    else:
        return render_template("auth/login.html")

@bp.route("./logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
