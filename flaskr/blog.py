from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import request
from flask import url_for

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    db=get_db()
    post_topics = db.execute(
        "SELECT t.topic_id, topic_subject, topic_date, topic_by, topic_cat, topic_name, u.user_name"
        " FROM topics t JOIN users u ON t.topic_id = u.user_id"
        " ORDER BY t.topic_date DESC"
    ).fetchall()
    return render_template("blog/index.html", post=post_topics)