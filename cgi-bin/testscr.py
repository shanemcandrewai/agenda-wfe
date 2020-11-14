import cgitb
import cgi
cgitb.enable()
form = cgi.FieldStorage()
print("Content-Type: text/html")
print()
print(form.getfirst("test-input"))
