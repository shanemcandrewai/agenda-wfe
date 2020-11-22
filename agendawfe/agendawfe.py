""" Agenda web front end """
import os
from pathlib import Path
import flask

app = flask.Flask(__name__, instance_relative_config=True)
# ensure the instance folder exists
Path(app.instance_path).mkdir(exist_ok=True)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY=str(os.urandom(16)),
    # store the database in the instance folder
    DATABASE=os.path.join(app.instance_path, "agendawfe.sqlite"),
)

# load the instance config, if it exists
breakpoint()
try:
    app.config.from_pyfile("config.py")
except OSError:
    with open(Path(app.instance_path, 'config.py'), 'w') as config_fo:
        config_fo.write('SECRET_KEY = ' + app.config['SECRET_KEY'] + '\n' +
                "DATABASE = '" + app.config['DATABASE'] + "'\n")

@app.route("/hello")
def hello():
    return "Hello, World!"

app.teardown_appcontext(close_db)

# agenda will be the main index
app.add_url_rule("/", endpoint="index")
