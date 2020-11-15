# CGI page test
Send every input keystroke to server-side script and return autocompletion
## Prepare database
    sqlite3 -init sqlwfe.sql sqlwfe.db
## Start local web server in Python 3 virtual environment
    python -m http.server --cgi
## Load web page in browser
    http://localhost:8000
