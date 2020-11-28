import flask
import sqlite3
app = flask.Flask(__name__)
with app.app_context():
    app.config.from_mapping(DATABASE='minimal.sqlite', SECRET_KEY='1234')
conn = sqlite3.connect(app.config['DATABASE'])
conn.execute('create table if not exists tab1(col1)')

@app.route('/')
def index():
    conn = sqlite3.connect(app.config['DATABASE'])
    table_data = conn.execute('select * from tab1').fetchall()
    return f'<!doctype html><meta charset=utf-8><title>Minimal sqlite3 app</title>{table_data}'

@app.route('/create', methods=('GET', 'POST'))
def post():
    if flask.request.method == 'POST':
        conn = sqlite3.connect(app.config['DATABASE'])
        with conn:
            conn.execute('insert into tab1 select ?',
                         (flask.request.form['input'],))
        return flask.redirect(flask.url_for('index'))
    return '<!doctype html><meta charset=utf-8><title>Minimal create</title><form method="post"><input name="input" id="input"><input type="submit" value="Save"></form>'

