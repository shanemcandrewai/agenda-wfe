import flask
import sqlite3
import functools
app = flask.Flask(__name__)
with app.app_context():
    app.config.from_mapping(DATABASE='minimal.sqlite', SECRET_KEY='1234')
#    app.add_url_rule('/favicon.ico',
#                     flask.redirect(flask.url_for('static', filename='favicon.ico')))
with sqlite3.connect(app.config['DATABASE']) as conn:
    with open('minimal.sql') as sql_fo:
        sql = sql_fo.read()
    conn.executescript(sql)


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        conn = sqlite3.connect(app.config['DATABASE'])
        flask.g.user = conn.execute('select * from user where id = ?',
                                    (flask.session.get('user_id'),)).fetchone()
        if flask.g.user is None:
            return flask.redirect(flask.url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
@login_required
def index():
    conn = sqlite3.connect(app.config['DATABASE'])
    flask.g.user = conn.execute('select * from user where id = ?',
                                (flask.session.get('user_id'),)).fetchone()
    flask.g.table_data = conn.execute('select * from tab1').fetchall()
    return flask.render_template('minimal/base.html')

@app.route('/insert', methods=('GET', 'POST'))
@login_required
def insert():
    if flask.request.method == 'POST':
        conn = sqlite3.connect(app.config['DATABASE'])
        with conn:
            conn.execute('insert into tab1 select ?',
                         (flask.request.form['input'],))
        return flask.redirect(flask.url_for('index'))
    return '<!doctype html><meta charset=utf-8><title>Minimal create</title><form method="post"><input name="input" id="input"><input type="submit" value="Save"></form>'

@app.route('/login')
def login():
    if flask.request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(app.config['DATABASE'])
        error = None
        user = db.execute( 'SELECT * FROM user WHERE username = ?',
                           (username,)).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(flask.url_for('index'))
        flash(error)
    return flask.render_template('minimal/base.html')

@app.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))
