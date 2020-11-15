#! /usr/bin/env python
import cgitb
import cgi
import sqlite3
cgitb.enable()
form = cgi.FieldStorage()
test_input = form.getfirst('inp')
conn = sqlite3.connect('sqlwfe.db')
c = conn.cursor()
c.execute("select out from autocom where inp='" + test_input + "'")
print('Content-Type: text/html')
print()
#print('document.getElementById("output").innerHTML = ' + "'hard-coded'")
print('document.getElementById("output").innerHTML = ' + "'" + c.fetchone()[0] + "'")
conn.close()
