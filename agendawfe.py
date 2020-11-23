""" Agenda web front end """
import functools
import os
from pathlib import Path
from flask import Flask
from flask import g
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
import db
import auth

app = Flask(__name__, instance_relative_config=True)

# load the instance config, if it exists
try:
    app.config.from_pyfile("config.py")
except OSError:
    # ensure the instance folder exists
    Path(app.instance_path).mkdir(exist_ok=True)
    app.config.from_mapping(
        SECRET_KEY=str(os.urandom(16)),
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "agendawfe.sqlite"),
    )
    # create a config file
    with open(Path(app.instance_path, 'config.py'), 'w') as config_fo:
        config_fo.write('SECRET_KEY = ' + app.config['SECRET_KEY'] + '\n' +
                "DATABASE = '" + app.config['DATABASE'] + "'\n")

app.teardown_appcontext(db.close_db)

@app.route("/hello")
def hello():
    return "Hello, World!"

app.add_url_rule('/login', 'auth.login', auth.login, methods=("GET", "POST"))
app.add_url_rule('/register', 'auth.register', auth.register, methods=("GET", "POST"))
app.add_url_rule('/logout', 'auth.logout', auth.logout)

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@app.before_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            db.get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )

@app.route("/")
@login_required
def index():
    """Show all the posts, most recent first."""
    db_connection = db.get_db()
    sql = ("SELECT p.id, title, body, created, author_id, username" +
          " FROM post p JOIN user u ON p.author_id = u.id" +
          " where u.id = "  + str(g.user['id']) +
          " ORDER BY created DESC")
    posts = db_connection.execute(sql).fetchall()
    return render_template("agenda/index.html", posts=posts)


def get_post(agenda_item_id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        db.get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (agenda_item_id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@app.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db_connection = db.get_db()
            db_connection.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db_connection.commit()
            return redirect(url_for("index"))

    return render_template("agenda/create.html")


@app.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db_connection = db.get_db()
            db_connection.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db_connection.commit()
            return redirect(url_for("agenda.index"))

    return render_template("agenda/update.html", post=post)


@app.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db_connection = db.get_db()
    db_connection.execute("DELETE FROM post WHERE id = ?", (id,))
    db_connection.commit()
    return redirect(url_for("index"))
