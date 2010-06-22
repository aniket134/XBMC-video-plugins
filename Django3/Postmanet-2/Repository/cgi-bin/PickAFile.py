#!C:\Program Files\Python-2.4\python.exe -u

import os
import cgi
import cgitb
cgitb.enable()

name = os.getenv("REMOTE_USER")

pdrroot = os.getenv("PDRROOT") or "C:\\sobti\\Postmanet-1\\PDRROOT"

if pdrroot[-1] != '\\':
    pdrroot = pdrroot + "\\"

print 'Content-Type: text/html'
print

print 'Hola'

form = cgi.FieldStorage()

print '<p>'
print 'Shell Environment in HTML'
cgi.print_environ()

print '<p>'
print 'Useful Variables in HTML'
cgi.print_environ_usage()

print '<p>'
print 'Form in HTML'
cgi.print_form(form)
