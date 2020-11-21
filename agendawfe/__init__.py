import os
from pathlib import Path
from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    # ensure the instance folder exists
    p = Path(app.instance_path)
    p.mkdir(exist_ok=True)
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
        except OSError as e:
            with open(Path(p, 'config.py'), 'w') as f:
                f.write('SECRET_KEY = ' + app.config['SECRET_KEY'] + '\n' + 'DATABASE = ' + app.config['DATABASE'])


    else:
        # load the test config if passed in
        app.config.update(test_config)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from agendawfe import db

    db.init_app(app)

    # apply the blueprints to the app
    from agendawfe import auth, agenda

    app.register_blueprint(auth.bp)
    app.register_blueprint(agenda.bp)

    # agenda will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
