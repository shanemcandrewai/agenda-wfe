# Agenda web front end

## Installation
### Clone repository
    git clone https://github.com/shanemcandrewai/agendawfe-repo.git
### Change directory to repository root
#### Create a virtual enviroment
    python3.x -m venv venv
#### Activate the virtual environment
#### From with the virtual environment
##### Install Flask
    pip install Flask
##### Run the application
    export FLASK_APP=agendawfe
    export FLASK_ENV=development
    flask run
##### Initialise the DB
    flask init-db
### Pythonanywhere.com
    https://www.pythonanywhere.com/user/shanem/webapps/#tab_id_shanem_pythonanywhere_com
#### Source code
    /home/shanem/agendawfe-repo/agendawfe
#### Working directory
    /home/shanem/agendawfe-repo
#### WSGI configuration file
##### /var/www/shanem_pythonanywhere_com_wsgi.py
    import sys

    path = '/home/shanem/agendawfe-repo'
    if path not in sys.path:
	sys.path.append(path)

    import agendawfe
    application = agendawfe.create_app()
### Browse the application
    http://127.0.0.1:5000/
