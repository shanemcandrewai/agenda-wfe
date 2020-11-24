# Agenda web front end

## Installation
### Clone repository
    git clone https://github.com/shanemcandrewai/agenda-wfe.git
### Change directory to repository root
#### Create a virtual enviroment
##### Linux
    python3.x -m venv venv
##### Windows
    py -3 -m venv venv
#### Ensure pip, setuptools, and wheel are up to date
    python -m pip install --upgrade pip setuptools wheel
#### Activate the virtual environment
##### Linux
    . venv/bin/activate
##### Windows
    venv\Scripts\activate
#### From with the virtual environment
##### Install Flask
    pip install Flask
##### Run the application
###### Linux
    export FLASK_APP=agenda_wfe.py
    export FLASK_ENV=development
    flask run
###### Windows
    set FLASK_APP=agenda_wfe.py
    set FLASK_ENV=development
    flask run
### Pythonanywhere.com
    https://www.pythonanywhere.com/user/shanem/webapps/#tab_id_shanem_pythonanywhere_com
#### Source code
    /home/shanem/agenda-wfe
#### Working directory
    /home/shanem/agenda-wfe
#### WSGI configuration file
##### /var/www/shanem_pythonanywhere_com_wsgi.py
    import sys

    path = '/home/shanem/agenda-awfe'
    if path not in sys.path:
	sys.path.append(path)

    from agenda_wfe import app as application
#### Enable HTTPS
1. Force HTTS: Enabled
2. Reload web app
### Browse the application
    http://127.0.0.1:5000/
