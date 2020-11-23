# Agenda web front end

## Installation
### Clone repository
    git clone https://github.com/shanemcandrewai/agendawfe.git
### Change directory to repository root
#### Create a virtual enviroment
##### Linux
    python3.x -m venv venv
##### Windows
    py -3 -m venv venv
#### Activate the virtual environment
##### Linux
    . ./venv/bin/activate
##### Windows
    venv\Scripts\activate
#### From with the virtual environment
##### Install Flask
    pip install Flask
##### Run the application
###### Linux
    export FLASK_APP=agendawfe.py
    export FLASK_ENV=development
    flask run
###### Windows
    set FLASK_APP=agendawfe.py
    set FLASK_ENV=development
    flask run
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
#### Enable HTTPS
1. Force HTTS: Enabled
2. Reload web app
### Browse the application
    http://127.0.0.1:5000/
