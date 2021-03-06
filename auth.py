""" authentication """
import functools
import flask
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from werkzeug import exceptions
import db

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if flask.g.user is None:
            return flask.redirect(flask.url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@login_required
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        db_connection = db.get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        else:
            curr = db_connection.cursor()
            curr.execute("SELECT id FROM user WHERE username = ?", (username,))
            if curr.fetchone() is not None:
                error = f"User {username} is already registered."

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            curr.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                      (username, generate_password_hash(password)))
            db_connection.commit()
            flask.flash('User ' + username + ' successfully created.')
            return flask.redirect(flask.url_for("auth.login"))

        flask.flash(error)

    return flask.render_template("auth/register.html")

def login_google():
    """ Google sign-in for websites """
    try:
        username = flask.request.form["email"]
    except exceptions.BadRequest as e:
        pass


def login():
    """Log in a registered user by adding the user id to the session."""
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        db_connection = db.get_db()
        error = None
        user = db_connection.execute(
                "SELECT * FROM user WHERE username = ?", (username,)
                ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            flask.session.clear()
            flask.session["user_id"] = user["id"]
            return flask.redirect(flask.url_for("index"))

        flask.flash(error)

    return flask.render_template("auth/login.html")

def logout():
    """Clear the current session, including the stored user id."""
    flask.session.clear()
    return flask.redirect(flask.url_for("auth.login"))
