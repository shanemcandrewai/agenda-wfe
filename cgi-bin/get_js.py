#! /usr/bin/env python
import cgitb
import cgi
cgitb.enable()
form = cgi.FieldStorage()
print('Content-Type: text/html')
print()
print("document.getElementById('output').innerHTML = 'output text'")
