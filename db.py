""" Database access """
import sqlite3
from pathlib import Path
import flask

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in flask.g:
        flask.g.db = sqlite3.connect(
            Path(flask.current_app.instance_path,
                 flask.current_app.config['DATABASE']),
                 detect_types=sqlite3.PARSE_DECLTYPES)
        cur = flask.g.db.cursor()
        cur.execute('select count(*) from sqlite_master')
        if cur.fetchone() == (0,):
            with flask.current_app.open_resource("schema.sql") as schema_fo:
                flask.g.db.executescript(schema_fo.read().decode("utf8"))
        flask.g.db.row_factory = sqlite3.Row
    return flask.g.db

def close_db(exception=None):
    """If this request connected to the database, close the
    connection.
    """
    if exception is not None:
        print(exception)
    request_db = flask.g.pop("db", None)
    if request_db is not None:
        request_db.close()

def init_db():
    """Clear existing data and create new tables."""
    request_db = get_db()
    with flask.current_app.open_resource("schema.sql") as schema_fo:
        request_db.executescript(schema_fo.read().decode("utf8"))
