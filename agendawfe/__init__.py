''' Initialize application factory package '''
import os
from pathlib import Path
from flask import Flask
from agendawfe import db
from agendawfe import auth, agenda

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    # ensure the instance folder exists
    Path(app.instance_path).mkdir(exist_ok=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY=str(os.urandom(16)),
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "agendawfe.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        try:
            app.config.from_pyfile("config.py")
        except OSError:
            with open(Path(app.instance_path, 'config.py'), 'w') as config_fo:
                config_fo.write('SECRET_KEY = ' + app.config['SECRET_KEY'] + '\n' +
                        "DATABASE = '" + app.config['DATABASE'] + "'\n")
    else:
        # load the test config if passed in
        app.config.update(test_config)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    db.init_app(app)
    # apply the blueprints to the app
    app.register_blueprint(auth.bp)
    app.register_blueprint(agenda.bp)

    # agenda will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
