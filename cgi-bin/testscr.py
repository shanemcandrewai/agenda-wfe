#! /usr/bin/env python
import cgitb
import cgi
cgitb.enable()
form = cgi.FieldStorage()
print('Content-Type: text/html')
print()
print('<h1>CGI input test</h1>')
print("<label for='test-id'>Enter some text:</label>")
print("<input type='text' id='test-id' name='test-input' value='test-val' />")
print("<script>")
print("document.getElementById('test-id').addEventListener('keydown', event => {")
print("console.log(event.key)}")
#print("fetch(('cgi-bin/testscr.py'))")
#print(".then(response => response.text())")
#print(".then(data => document.body.innerHTML = data); });")
print("</script>")
#print(form.getfirst('test-inputx'))
#print('test output')
