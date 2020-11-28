import flask
import sqlite3
app = flask.Flask(__name__)
with app.app_context():
    app.config.from_mapping(DATABASE='minimal.sqlite', SECRET_KEY='1234')
conn = sqlite3.connect(app.config['DATABASE'])
conn.execute('create table if not exists tab1(col1)')
with conn:
    conn.execute('insert into tab1 select "testdata"')
@app.route('/')
def index():
    table_data = conn.execute('select * from tab1').fetchall()
    return f'<!doctype html><meta charset=utf-8><title>Minimal sqlite3 app</title>{table_data}'

