import cgi
import cgitb
import os
cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print "<TITLE>CGI script output</TITLE>"
print "<H1>Test</H1>"
print "Hello, world!"
print "<BR>"

form = cgi.FieldStorage()

print form

print "<BR>"

cgi.print_form(form)

print "<BR>"

v1 = form.getlist('foo')
print repr(v1)

print "<BR>"
cgi.print_environ()

print "<BR>"
cgi.print_environ_usage()

print os.getenv("REMOTE_USER")
