
import os, sys
import su, RunPYProcessDetached as Run, KillXMLRPCServer as Kill

import cgi, cgitb
cgitb.enable()

name = os.getenv("REMOTE_USER")

print 'Content-Type: text/html'
print

print '<P> Hello!,', name

if name != 'admin':
    print '<P>Administrator only..'
    sys.exit(1)

form = cgi.FieldStorage()

username = form.getfirst('username', '')
address = form.getfirst('address', '')
passwd = form.getfirst('passwd', '')
retypepasswd = form.getfirst('retypepasswd', '')

if not username:
    print '<P><FONT COLOR=red>Must enter username</FONT>'
    sys.exit(1)

if passwd or retypepasswd:
    if passwd != retypepasswd:
        print '<P><FONT COLOR=red>Password and re-typed password do not match.</FONT>'
        sys.exit(1)
##    print '<P>Password found'

# read/write passwd file if passwd being changed
if passwd:
    try:
        pwdfile = os.path.join(RepositoryRoot, 'Passwords')
##        lines = []
##        for line in open(pwdfile).readlines():
##            name, rest = line.split(':', 1)
##            if name != username:
##                lines.append(line)
##
##        os.rename(pwdfile, pwdfile + '.OLD')
##        f = open(pwdfile, 'w')
##        for line in lines:
##            f.write(line)
##        f.close()

        try:
            resources = su.parseKeyValueFile(os.path.join(RepositoryRoot, 'Resources.txt'))
        except:
            print '<P>Could not read resources file correctly'
            sys.exit(1)

        apachepath = resources['apachepath']
        htpasswdpath = os.path.join(apachepath, 'bin', 'htpasswd.exe')

##        command = '"%s" -b "%s" "%s" "%s"' % (apachepath, pwdfile, username, passwd)
##        print 'Executing command: %s' % command
##    # replace \ by \\
##        command.replace('\\', '\\\\')
##        os.system(command)

##        print '<P>spawning'
        os.spawnl(os.P_WAIT, htpasswdpath, 'htpasswd.exe', '-b', pwdfile, username, passwd)
        print '<P><FONT COLOR=green>Password updated successfully.</FONT>'
    except:
        print '<P>Password could not be updated correctly.'
        print '<BR>Look at files "%s" and "%s".' % (pwdfile, pwdfile + '.OLD')
        sys.exit(1)

# read/write Endpoints file
endpointfile = os.path.join(RepositoryRoot, 'Endpoints.pk')
epupdated = False
try:
    ep = su.pickload(endpointfile)
except:
    ep = {}
    epupdated = True

if address:
    ep[username] = address.replace('\r', '')
    epupdated = True
    print '<P><FONT COLOR=red>Updating address.</FONT>'
else:
    if ep.has_key(username):
        address = ep[username]

if epupdated:
    try:
##        print '<P>Before dumping'
        if os.path.exists(endpointfile + '.OLD'):
            os.remove(endpointfile + '.OLD')
            os.rename(endpointfile, endpointfile + '.OLD')
##        print '<P>Dumping'
        su.pickdump(ep, endpointfile)
##        print '<P>Dumped'
    except:
        print '<P>Could not update endpoint information. Look into files "%s" and "%s".' % (endpointfile, endpointfile + '.OLD')
        sys.exit(1)

print '\n<FORM action="/cgi-bin/UpdateUserInfo.py" method="post" enctype="multipart/form-data">\n\n'

print '<P><B>Username</B><BR> <INPUT type=text name=username value=%s size=30>' % username

print '<P><B>Address</B>'
if address:
    print '(%s)' % address
print '<BR><TEXTAREA name=address rows=5 cols=60></TEXTAREA>'

print '<P><B>New Password</B><BR> <INPUT type=password name=passwd size=30>'

print '<P><B>Re-type New Password</B><BR> <INPUT type=password name=retypepasswd size=30>'

print '\n<p>\n<INPUT type="submit" value="Update User Information"> <INPUT type="reset" value="Clear All">\n'

print '\n</FORM>\n'
