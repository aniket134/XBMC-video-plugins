
import sys, os

#######
##a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
##a = _winreg.OpenKey(a, 'Postmanet')
##a = _winreg.OpenKey(a, 'Repository')
##reppath = _winreg.EnumValue(a, 0)[1]
###print 'reppath =', reppath
##
##sys.path.append(reppath + 'Common')
##sys.path.append(reppath + 'bin')
##
##import su
#######

import pickle, cgi, cgitb, xmlrpclib
cgitb.enable()

import objectstore

name = os.getenv("REMOTE_USER")

print 'Content-Type: text/html'
print

print '<H1> Dude, this is NULL CGI.</H1> change your form target once you have other things done.'
