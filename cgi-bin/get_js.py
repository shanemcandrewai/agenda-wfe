#! /usr/bin/env python
import cgitb
import cgi
cgitb.enable()
form = cgi.FieldStorage()
test_input = form.getfirst('inp')
print('Content-Type: text/html')
print()
print('document.getElementById("output").innerHTML = ' + "'hard-coded'")
