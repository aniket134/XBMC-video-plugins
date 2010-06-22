
import os, sys
import su

import cgi, cgitb
cgitb.enable()

name = os.getenv("REMOTE_USER")

print 'Content-Type: text/html'
print

print '<P> Hello!,', name

if name != 'admin':
    print '<P>Administrator only..'
    sys.exit(1)

print '<P><a href="/cgi-bin/StartAllServices.py">Start all services</a>'

print '<P><a href="/cgi-bin/StopAllServices.py">Stop all services</a>'

print '<P><a href="/cgi-bin/ProcessIncomingDiscs.py">Process a stack of incoming discs</a>'

print '<P><a href="/cgi-bin/ManageUserAccounts.py">Manage User Accounts</a>'

print '<P><a href="/cgi-bin/EditConfig.py">Edit the configuration file Resources.txt</a>'
